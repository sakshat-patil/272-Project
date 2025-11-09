from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/api/predictions", tags=["Future Risk Predictions"])

orchestrator = AgentOrchestrator()


async def generate_prediction_background(db: Session, organization_id: int, prediction_period_days: int):
    """Background task to generate future risk predictions"""
    await orchestrator.predict_future_risks(db, organization_id, prediction_period_days)


@router.post("/", response_model=schemas.FutureRiskPredictionResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_future_prediction(
    prediction: schemas.FutureRiskPredictionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate future risk predictions for an organization
    """
    # Verify organization exists
    organization = crud.get_organization(db, prediction.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check if recent prediction exists
    existing = crud.get_latest_prediction(db, prediction.organization_id, prediction.prediction_period_days)
    if existing:
        # Return existing if less than 24 hours old
        from datetime import datetime, timedelta
        if datetime.utcnow() - existing.created_at < timedelta(hours=24):
            return existing
    
    # Start background processing
    background_tasks.add_task(
        generate_prediction_background,
        db,
        prediction.organization_id,
        prediction.prediction_period_days
    )
    
    # Return placeholder response
    return {
        "id": 0,
        "organization_id": prediction.organization_id,
        "prediction_period_days": prediction.prediction_period_days,
        "predicted_risk_score": 0.0,
        "risk_factors": [],
        "recommendations": [],
        "confidence_level": 0.0,
        "created_at": datetime.utcnow()
    }


@router.get("/organization/{organization_id}/latest")
def get_latest_prediction(
    organization_id: int,
    period_days: int = 90,
    db: Session = Depends(get_db)
):
    """
    Get the latest prediction for an organization
    """
    prediction = crud.get_latest_prediction(db, organization_id, period_days)
    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="No predictions found. Create one first."
        )
    return prediction