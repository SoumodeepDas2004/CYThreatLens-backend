from fastapi import FastAPI
from app.database import engine, Base
from app import models  # ← ADD THIS LINE
from app.routers import scan

app = FastAPI(title="CYThreatLens API")

Base.metadata.create_all(bind=engine)

app.include_router(scan.router)

@app.get("/")
def root():
    return {"message": "CYThreatLens backend running"}