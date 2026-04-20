from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filepath = Column(String, nullable=False)
    status = Column(String, default="processing", nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer,ForeignKey("users.id"), nullable=True)

    extracted_data = Column(String,nullable=True)