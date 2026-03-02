from fastapi import FastAPI
from app.database import engine, Base
from app import models  # ← ADD THIS LINE
from app.routers import scan
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI(title="CYThreatLens API")

Base.metadata.create_all(bind=engine)

app.include_router(scan.router)

@app.get("/")
def root():
    return {"message": "CYThreatLens backend running"}