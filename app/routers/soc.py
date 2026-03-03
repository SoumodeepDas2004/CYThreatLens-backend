from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.vt_engine import analyze_md5
from app import models
from pydantic import BaseModel
router = APIRouter(prefix="/soc", tags=["SOC"])

class HashRequest(BaseModel):
    hash: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/file")
def scan_file(request: HashRequest, db: Session = Depends(get_db)):

    result = analyze_md5(request.hash)

    if "error" in result:
        return result

    new_scan = models.FileScan(
        hash=result["hash"],
        malicious=result["malicious"],
        suspicious=result["suspicious"],
        harmless=result["harmless"],
        risk_level=result["risk_level"]
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return result


@router.get("/history")
def file_history(db: Session = Depends(get_db)):
    return db.query(models.FileScan).order_by(models.FileScan.created_at.desc()).limit(20).all()