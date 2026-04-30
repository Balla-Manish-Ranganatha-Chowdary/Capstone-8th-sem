from pydantic import BaseModel
from typing import Optional, List

class ChangeMetrics(BaseModel):
    changed_area_percent: float
    vegetation_change_percent: float
    water_body_change_percent: float
    bare_soil_exposure_percent: float
    change_magnitude_mean: float
    change_magnitude_max: float
    dominant_change_type: str
    risk_level: str

class AnalysisResponse(BaseModel):
    status: str
    analysis_id: str
    region_name: str
    t1_date: str
    t2_date: str
    change_metrics: ChangeMetrics
    disaster_risk_assessment: str
    processing_time_seconds: float

class HistoryItemResponse(BaseModel):
    analysis_id: str
    region_name: str
    t1_date: str
    t2_date: str
    dominant_change_type: str
    risk_level: str
    changed_area_percent: float
    created_at: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    device: str
    gemini_configured: bool

class ErrorResponse(BaseModel):
    status: str
    message: str

class ChatRequest(BaseModel):
    query: str
    state: str
    start_year: int
    end_year: int

class ChatResponse(BaseModel):
    response: str

