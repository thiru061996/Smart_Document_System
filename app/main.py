from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import auth

# Create tables based on models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Document System")

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"Message": "Backend running with supabase URL and table has been created"}