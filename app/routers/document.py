from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.db.database import get_db
from app.models.document import Document
from app.core.deps import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"


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
            filepath=file_location,  # ✅ matches model field name
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