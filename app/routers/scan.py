from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.services.threat_engine import analyze_ip
from app import models

router = APIRouter(prefix="/scan", tags=["Scan"])


class IPRequest(BaseModel):
    ip: str


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ip")
def scan_ip(request: IPRequest, db: Session = Depends(get_db)):

    result = analyze_ip(request.ip)

    # Create DB object
    new_scan = models.Scan(
        ip=request.ip,
        country=result["country"],
        region=result["region"],
        city=result["city"],
        isp=result["isp"],
        asn=result["asn"],
        latitude=result["latitude"],
        longitude=result["longitude"],
        abuse_score=result["abuse_score"],
        threat_score=result["threat_score"],
        risk_level=result["risk_level"])

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return result


@router.get("/history")
def get_scan_history(limit: int = 20, db: Session = Depends(get_db)):

    scans = (
        db.query(models.Scan)
        .order_by(models.Scan.created_at.desc())
        .limit(limit)
        .all()
    )

    return scans

@router.get("/map-data")
def get_map_data(limit: int = 100, db: Session = Depends(get_db)):

    scans = (
        db.query(models.Scan)
        .order_by(models.Scan.created_at.desc())
        .limit(limit)
        .all()
    )

    map_data = []

    for scan in scans:
        if scan.latitude and scan.longitude:
            map_data.append({
                "ip": scan.ip,
                "lat": scan.latitude,
                "lon": scan.longitude,
                "threat_score": scan.threat_score,
                "risk_level": scan.risk_level,
                "country": scan.country
            })

    return map_data

from sqlalchemy import func, case

@router.get("/country-stats")
def get_country_stats(db: Session = Depends(get_db)):

    stats = (
        db.query(
            models.Scan.country,
            func.count(models.Scan.id).label("total_scans"),
            func.avg(models.Scan.threat_score).label("avg_threat_score"),
            func.sum(
                case(
                    (models.Scan.risk_level == "High", 1),
                    else_=0
                )
            ).label("high_risk_count")
        )
        .group_by(models.Scan.country)
        .all()
    )

    result = []

    for row in stats:
        result.append({
            "country": row.country,
            "total_scans": row.total_scans,
            "avg_threat_score": round(row.avg_threat_score or 0, 2),
            "high_risk_count": row.high_risk_count or 0
        })

    return result
