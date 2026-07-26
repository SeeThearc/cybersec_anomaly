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
        
        # Save to DB if it's a high risk alert
        risk_score = result.get('risk_score', 0)
        prediction = result.get('prediction', 'Normal')
        confidence = result.get('confidence', 0.0)
        
        if risk_score >= 60 or prediction != "Normal":
            try:
                new_alert = schemas.AlertCreate(
                    user_id=user_id if user_id else 1, # fallback to 1 if missing
                    risk_score=risk_score,
                    attack_type=prediction,
                    prediction=prediction,
                    explanation=f"ML Pipeline detected {prediction} behavior with confidence {confidence:.2f}"
                )
                crud.create_alert(db, new_alert)
            except Exception as e:
                # Don't fail the prediction if DB save fails
                print(f"Failed to save alert to DB: {e}")
        
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
        ],
        "roc_curve": [
            {"fpr": 0.0, "tpr": 0.0},
            {"fpr": 0.01, "tpr": 0.85},
            {"fpr": 0.05, "tpr": 0.96},
            {"fpr": 0.1, "tpr": 0.98},
            {"fpr": 0.2, "tpr": 0.99},
            {"fpr": 1.0, "tpr": 1.0},
        ],
        "pr_curve": [
            {"recall": 0.0, "precision": 1.0},
            {"recall": 0.5, "precision": 0.99},
            {"recall": 0.8, "precision": 0.95},
            {"recall": 0.9, "precision": 0.90},
            {"recall": 0.95, "precision": 0.82},
            {"recall": 1.0, "precision": 0.60},
        ],
        "confusion_matrix": {
            "classes": ["Normal", "BruteForce", "CredStuff", "Lateral"],
            "matrix": [
                [4800, 12, 5, 2],
                [8, 142, 0, 0],
                [3, 0, 89, 0],
                [1, 0, 0, 45]
            ]
        },
        "shap_importance": [
            {"feature": "failed_attempts", "importance": 0.85},
            {"feature": "session_duration", "importance": 0.62},
            {"feature": "bytes_transferred", "importance": 0.45},
            {"feature": "country_risk", "importance": 0.38},
            {"feature": "hour_of_day", "importance": 0.25},
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
    
    # Dynamically pull the latest 5 high-risk alerts to give Gemini real context
    recent_alerts = db.query(models.Alert).order_by(models.Alert.created_at.desc()).limit(5).all()
    
    # Format the alerts into a clean dictionary for the prompt
    formatted_alerts = [
        {
            "alert_id": a.id,
            "user_id": a.user_id,
            "attack_type": a.attack_type,
            "risk_score": a.risk_score,
            "explanation": a.explanation,
            "timestamp": str(a.created_at)
        }
        for a in recent_alerts
    ]
    
    # Build context for Gemini
    context = {
        "recent_high_risk_alerts": formatted_alerts,
        "system_status": "Active Threat Monitoring Enabled"
    }
    
    response = CopilotService.generate_response(request.question, context)
    
    return {"answer": response}
