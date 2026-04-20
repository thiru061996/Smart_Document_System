from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.document import Document
from app.models.user import User
from app.core.deps import get_current_user
from app.db.database import get_db

router = APIRouter(prefix="/workflow",tags=["workflow"])

#Assign Document
@router.post("/assign/{doc_id}")
async def assign_document(doc_id:int,user_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404,detail="Document not found!")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found!")
    
    doc.assigned_to = user_id
    doc.status = "assigned"

    db.commit()
    return{'message':'Document assigned successfully'}

@router.post("/approve/{doc_id}")
async def approve_document(doc_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404,detail="Document not found!")
    
    if doc.assigned_to != current_user.id:
        raise HTTPException(status_code=403,detail="Not authorized")
    
    doc.status = "approved"
    
    db.commit()
    return{'message':'Document approved'}

@router.post("/reject/{doc_id}")
async def reject_document(doc_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404,detail="Document not found!")
    
    if doc.assigned_to != current_user.id:
        raise HTTPException(status_code=403,detail="Not authorized")
    
    doc.status = "rejected"
    
    db.commit()
    return{'message':'Document rejected'}