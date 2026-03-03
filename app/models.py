from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    country = Column(String)
    region = Column(String)
    city = Column(String)
    isp = Column(String)
    asn = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    abuse_score = Column(Integer)
    threat_score = Column(Integer)
    risk_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class FileScan(Base):
    __tablename__ = "file_scans"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, index=True)
    malicious = Column(Integer)
    suspicious = Column(Integer)
    harmless = Column(Integer)
    risk_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)