from fastapi import APIRouter, Depends, UploadFile, File, HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
import shutil
import os

from app.db.database import get_db,SessionLocal
from app.models.document import Document
from app.core.deps import get_current_user

from app.services.ocr import extract_text_from_image

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"

def process_document(doc_id: int):
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return

        try:
            text = extract_text_from_image(doc.file_path)
            doc.extracted_data = text
            doc.status = "completed"
        except Exception as e:
            doc.status = "failed"
            doc.extracted_data = str(e)

        db.commit()
    finally:
        db.close()

@router.post("/upload", summary="Upload a document")
async def upload_document(
    file: UploadFile = File(...),  # ✅ IMPORTANT
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # ✅ Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_doc = Document(
            file_path=file_location,  # ✅ matches model field name
            status="uploaded",
            uploaded_by=current_user.id
        )

        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "File uploaded successfully",
        "file_path": file_location
    }

@router.post("/uploadOCR")
async def upload_ocr_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    os.makedirs("uploads", exist_ok=True)

    if file.content_type not in {"image/png", "image/jpeg"}:
        raise HTTPException(400, "Only PNG/JPEG images allowed")

    file_location = os.path.join("uploads", file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        file_path=file_location,
        status="processing",
        uploaded_by=current_user.id
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    background_tasks.add_task(process_document, new_doc.id)

    return {
        "message": "File uploaded successfully. OCR started.",
        "document_id": new_doc.id
    }
