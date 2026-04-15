from fastapi import FastAPI
from app.database import engine, Base
from app import models  
from app.routers import scan,news,soc,telegram,news_intel,email_analyzer
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "https://cy-threat-lens-frontend.vercel.app",
    "http://localhost:5173"
]

app = FastAPI(title="CYThreatLens API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.middleware.cors import CORSMiddleware


# https://cy-threat-lens-frontend.vercel.app/
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("DB connection failed:", e)
    
app.include_router(scan.router)
app.include_router(news.router)
app.include_router(soc.router)
app.include_router(telegram.router)
app.include_router(news_intel.router)
app.include_router(email_analyzer.router)
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"message": "CYThreatLens backend running"}