from fastapi import Depends,HTTPException
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.db.database import SessionLocal,get_db
from app.models.user import User
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401,detail="Invalid token")
        
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")

    db = next(get_db())
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user