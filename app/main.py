from fastapi import FastAPI
from app.database import engine, Base
from app import models  
from app.routers import scan,news,soc,telegram,news_intel,email_analyzer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="CYThreatLens API")
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
Base.metadata.create_all(bind=engine)

app.include_router(scan.router)
app.include_router(news.router)
app.include_router(soc.router)
app.include_router(telegram.router)
app.include_router(news_intel.router)
app.include_router(email_analyzer.router)
@app.get("/")
def root():
    return {"message": "CYThreatLens backend running"}