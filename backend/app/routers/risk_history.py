from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/api/risk-history", tags=["Risk History"])


@router.post("/", response_model=schemas.RiskHistoryResponse, status_code=201)
def create_risk_history_entry(
    risk_history: schemas.RiskHistoryCreate,
    db: Session = Depends(get_db)
):
    """Create a risk history entry"""
    # Verify organization exists
    organization = crud.get_organization(db, risk_history.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return crud.create_risk_history(db, risk_history)


@router.get("/organization/{organization_id}", response_model=List[schemas.RiskHistoryResponse])
def get_organization_risk_history(
    organization_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get risk history for an organization"""
    # Verify organization exists
    organization = crud.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return crud.get_risk_history(db, organization_id, days)