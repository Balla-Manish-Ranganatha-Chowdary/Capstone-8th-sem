import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eo_intelligence.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    region_name = Column(String)
    t1_date = Column(String)
    t2_date = Column(String)
    changed_area_percent = Column(Float)
    vegetation_change_percent = Column(Float)
    water_body_change_percent = Column(Float)
    bare_soil_exposure_percent = Column(Float)
    change_magnitude_mean = Column(Float)
    change_magnitude_max = Column(Float)
    dominant_change_type = Column(String)
    risk_level = Column(String)
    gemini_response = Column(Text)
    processing_time_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
