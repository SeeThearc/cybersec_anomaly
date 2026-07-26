"""FastAPI route definitions."""

import time
import subprocess
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import schemas, crud, models
from app.database import get_db
from app.ml.data_generator import run_generation
from app.services.copilot import CopilotService

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent

# --- ML Control Routes ---

@router.post("/generate-data")
def generate_data(db: Session = Depends(get_db)):
    """Generate synthetic users, events, and attacks."""
    try:
        run_generation(db)
        return {"status": "success", "message": "Synthetic data generated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train")
def train_models():
    """Trigger the ML training pipeline."""
    try:
        # Run train.py as a subprocess to keep memory clean and non-blocking
        script_path = BASE_DIR / "train.py"
        subprocess.Popen(["python", str(script_path)])
        return {"status": "Training Started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
def predict_event(request_data: schemas.PredictionRequest, request: Request, db: Session = Depends(get_db)):
    """Predict attack probability and risk for a single event."""
    start_time = time.time()
    
    predictor = request.app.state.predictor
    if not predictor:
        raise HTTPException(status_code=503, detail="Prediction Pipeline is not loaded yet.")
        
    event = request_data.event
    user_id = event.get("user_id")
    
    # Get user history from DB (last 9 events)
    history = []
    if user_id:
        db_events = crud.get_events_by_user(db, user_id)
        # Sort by timestamp and get last 9
        db_events = sorted(db_events, key=lambda x: x.timestamp)[-9:]
        history = [{"action": e.action, "timestamp": e.timestamp} for e in db_events]
        
    try:
        result = predictor.predict_event(event, history)
        
        # Log execution time
        exec_time = time.time() - start_time
        result["execution_time_ms"] = round(exec_time * 1000, 2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Data Retrieval Routes ---

@router.get("/events", response_model=list[schemas.EventRead])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_events(db, skip=skip, limit=limit)

@router.get("/alerts", response_model=list[schemas.AlertRead])
def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_alerts(db, skip=skip, limit=limit)

@router.get("/statistics", response_model=schemas.StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total_users = db.query(func.count(models.User.id)).scalar()
    total_events = db.query(func.count(models.Event.id)).scalar()
    critical_alerts = db.query(func.count(models.Alert.id)).filter(models.Alert.risk_score >= 80).scalar()
    
    # Mocking aggregated analytics for speed
    avg_risk = db.query(func.avg(models.Alert.risk_score)).scalar() or 0.0
    
    return {
        "total_users": total_users or 0,
        "total_events": total_events or 0,
        "attack_counts": {"BruteForce": 12, "CredentialStuffing": 8, "LateralMovement": 4},
        "average_risk": round(avg_risk, 2),
        "high_risk_users": 5,
        "critical_alerts": critical_alerts or 0
    }

@router.get("/analytics", response_model=schemas.AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    # Returns aggregation data for the frontend charts
    return {
        "attack_distribution": [
            {"name": "BruteForce", "value": 40},
            {"name": "CredentialStuffing", "value": 25},
            {"name": "LateralMovement", "value": 15},
            {"name": "InsiderDrift", "value": 20},
        ],
        "department_distribution": [
            {"name": "Engineering", "value": 120},
            {"name": "Finance", "value": 30},
            {"name": "HR", "value": 15},
            {"name": "Sales", "value": 45},
        ],
        "risk_trend": [
            {"time": "08:00", "risk": 20},
            {"time": "09:00", "risk": 45},
            {"time": "10:00", "risk": 85},
            {"time": "11:00", "risk": 30},
        ],
        "monthly_events": [
            {"name": "Jan", "events": 1200},
            {"name": "Feb", "events": 2100},
            {"name": "Mar", "events": 800},
        ],
        "top_resources": [
            {"name": "Payroll DB", "hits": 450},
            {"name": "GitHub Repo", "hits": 320},
            {"name": "Admin Console", "hits": 150},
        ],
        "top_attack_types": [
            {"name": "BruteForce", "count": 142},
            {"name": "CredentialStuffing", "count": 89},
        ]
    }

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_with_relations(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- AI Copilot Route ---

@router.post("/copilot")
def ask_copilot(request: schemas.CopilotRequest, db: Session = Depends(get_db)):
    """Interact with the AI Security Copilot."""
    # Build context for the mock LLM
    context = {}
    
    response = CopilotService.generate_response(request.question, context)
    
    return {"answer": response}
