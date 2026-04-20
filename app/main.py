from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import auth, user, document,workflow

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Document System")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(document.router)
app.include_router(workflow.router)

@app.get("/")
async def root():
    return {
        "message": "Backend running successfully and database tables created"
    }