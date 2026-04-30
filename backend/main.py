import os
import uuid
import time
import asyncio
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Setup logging before local imports
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from backend.database import engine, get_db, create_tables, AnalysisRecord
from backend.schemas import HealthResponse, AnalysisResponse, HistoryItemResponse, ChangeMetrics, ChatRequest, ChatResponse
from backend.model import load_model, get_model_status, preprocess_image, extract_features
from backend.analysis import run_change_analysis
from backend.llm import generate_risk_assessment, get_gemini_status, chat_with_analyst

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up EO Intelligence Backend...")
    create_tables()
    load_model()
    yield
    logger.info("Shutting down...")

app = FastAPI(title="EO Intelligence System", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"status": "ok", "message": "EO Intelligence Backend is successfully running! You can view the API documentation at /docs."}

@app.get("/api/health", response_model=HealthResponse)
def health_endpoint():
    model_loaded, model_name, device = get_model_status()
    genai_configured = get_gemini_status()
    return HealthResponse(
        status="ok",
        model_loaded=model_loaded,
        model_name=model_name,
        device=device,
        gemini_configured=genai_configured
    )

def run_pipeline(
    t1_bytes: bytes, t1_name: str,
    t2_bytes: bytes, t2_name: str,
    region_name: str, t1_date: str, t2_date: str
) -> dict:
    
    # Model checking code is still present but pipeline is bypassed
    model_loaded, _, _ = get_model_status()
    if not model_loaded:
        raise RuntimeError("Prithvi model is still loading or failed to load. Please try again in a moment.")
        
    logger.info("--- Starting Pipeline ---")
    logger.info("Bypassing Prithvi Model and Analysis Engine. Generating LLM response directly from state/dates...")
    
    # Mock some metrics so the DB schema doesn't crash
    mock_metrics = {
        "changed_area_percent": 0.0,
        "vegetation_change_percent": 0.0,
        "water_body_change_percent": 0.0,
        "bare_soil_exposure_percent": 0.0,
        "change_magnitude_mean": 0.0,
        "change_magnitude_max": 0.0,
        "dominant_change_type": "bypassed",
        "risk_level": "bypassed"
    }
    
    logger.info("Stage 4: Generating risk assessment via Gemini directly from state and dates...")
    assessment = generate_risk_assessment(region_name, t1_date, t2_date)
    logger.info(f"Stage 4 complete: Gemini response received, length={len(assessment)} chars")
    
    logger.info("--- Pipeline Completed Successfully ---")
    return {
        "change_metrics": mock_metrics,
        "assessment": assessment
    }

@app.post("/api/analyze")
async def analyze_endpoint(
    image_t1: UploadFile = File(...),
    image_t2: UploadFile = File(...),
    region_name: str = Form("Unknown Region"),
    t1_date: str = Form("T1"),
    t2_date: str = Form("T2"),
    db: Session = Depends(get_db)
):
    try:
        t1_bytes = await image_t1.read()
        t2_bytes = await image_t2.read()
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": f"Failed to read upload files: {str(e)}"})
        
    start_time = time.time()
    
    loop = asyncio.get_event_loop()
    try:
        pipeline_results = await loop.run_in_executor(
            None, 
            run_pipeline,
            t1_bytes, image_t1.filename,
            t2_bytes, image_t2.filename,
            region_name, t1_date, t2_date
        )
    except RuntimeError as re:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(re)})
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Pipeline failed: {str(e)}"})
        
    processing_time = time.time() - start_time
    
    analysis_id = str(uuid.uuid4())
    change_metrics = pipeline_results["change_metrics"]
    assessment = pipeline_results["assessment"]
    
    db_record = AnalysisRecord(
        id=analysis_id,
        region_name=region_name,
        t1_date=t1_date,
        t2_date=t2_date,
        changed_area_percent=change_metrics["changed_area_percent"],
        vegetation_change_percent=change_metrics["vegetation_change_percent"],
        water_body_change_percent=change_metrics["water_body_change_percent"],
        bare_soil_exposure_percent=change_metrics["bare_soil_exposure_percent"],
        change_magnitude_mean=change_metrics["change_magnitude_mean"],
        change_magnitude_max=change_metrics["change_magnitude_max"],
        dominant_change_type=change_metrics["dominant_change_type"],
        risk_level=change_metrics["risk_level"],
        gemini_response=assessment,
        processing_time_seconds=processing_time
    )
    db.add(db_record)
    db.commit()
    
    return AnalysisResponse(
        status="success",
        analysis_id=analysis_id,
        region_name=region_name,
        t1_date=t1_date,
        t2_date=t2_date,
        change_metrics=ChangeMetrics(**change_metrics),
        disaster_risk_assessment=assessment,
        processing_time_seconds=processing_time
    )

@app.get("/api/history", response_model=list[HistoryItemResponse])
def get_history(db: Session = Depends(get_db)):
    records = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).all()
    history = []
    for r in records:
        history.append(HistoryItemResponse(
            analysis_id=r.id,
            region_name=r.region_name,
            t1_date=r.t1_date,
            t2_date=r.t2_date,
            dominant_change_type=r.dominant_change_type,
            risk_level=r.risk_level,
            changed_area_percent=r.changed_area_percent,
            created_at=r.created_at.isoformat()
        ))
    return history

@app.get("/api/analysis/{analysis_id}")
def get_analysis_by_id(analysis_id: str, db: Session = Depends(get_db)):
    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    return {
        "analysis_id": record.id,
        "region_name": record.region_name,
        "t1_date": record.t1_date,
        "t2_date": record.t2_date,
        "change_metrics": {
            "changed_area_percent": record.changed_area_percent,
            "vegetation_change_percent": record.vegetation_change_percent,
            "water_body_change_percent": record.water_body_change_percent,
            "bare_soil_exposure_percent": record.bare_soil_exposure_percent,
            "change_magnitude_mean": record.change_magnitude_mean,
            "change_magnitude_max": record.change_magnitude_max,
            "dominant_change_type": record.dominant_change_type,
            "risk_level": record.risk_level
        },
        "disaster_risk_assessment": record.gemini_response,
        "processing_time_seconds": record.processing_time_seconds,
        "created_at": record.created_at.isoformat()
    }

@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest, db: Session = Depends(get_db)):
    record = db.query(AnalysisRecord).filter(AnalysisRecord.region_name == request.state).order_by(AnalysisRecord.created_at.desc()).first()
    
    metrics = None
    assessment = None
    if record:
        metrics = {
            "changed_area_percent": record.changed_area_percent,
            "vegetation_change_percent": record.vegetation_change_percent,
            "water_body_change_percent": record.water_body_change_percent,
            "bare_soil_exposure_percent": record.bare_soil_exposure_percent,
            "change_magnitude_mean": record.change_magnitude_mean,
            "change_magnitude_max": record.change_magnitude_max,
            "dominant_change_type": record.dominant_change_type,
            "risk_level": record.risk_level
        }
        assessment = record.gemini_response
        
    try:
        response_text = chat_with_analyst(
            query=request.query,
            state=request.state,
            start_year=request.start_year,
            end_year=request.end_year,
            db_record_metrics=metrics,
            db_record_assessment=assessment
        )
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Chat failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
