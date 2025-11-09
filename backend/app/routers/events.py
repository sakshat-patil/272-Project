from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter(prefix="/api/events", tags=["Events"])

# Initialize orchestrator
orchestrator = AgentOrchestrator()


async def process_event_background(db: Session, event_id: int, organization_id: int, event_input: str, severity_level: int):
    """Background task to process event through agents"""
    await orchestrator.process_event(db, event_id, organization_id, event_input, severity_level)


@router.post("/", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
async def create_and_analyze_event(
    event: schemas.EventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new event and start analysis
    Returns immediately with event_id, processing happens in background
    """
    # Verify organization exists
    organization = crud.get_organization(db, event.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Create event record
    db_event = crud.create_event(db, event)
    
    # Start background processing
    background_tasks.add_task(
        process_event_background,
        db,
        db_event.id,
        event.organization_id,
        event.event_input,
        event.severity_level
    )
    
    return db_event


@router.get("/{event_id}", response_model=schemas.EventDetailResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get event by ID with full details"""
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/organization/{organization_id}", response_model=List[schemas.EventResponse])
def get_events_by_organization(
    organization_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all events for an organization"""
    return crud.get_events_by_organization(db, organization_id, skip, limit)


@router.post("/compare", response_model=schemas.ComparisonResponse)
async def compare_multiple_events(
    comparison: schemas.ComparisonRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Compare multiple events simultaneously
    Analyzes 2-3 events and provides comparative analysis
    """
    # Verify organization exists
    organization = crud.get_organization(db, comparison.organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Create events for each scenario
    event_ids = []
    severity_levels = comparison.severity_levels or [3] * len(comparison.events)
    
    for idx, event_input in enumerate(comparison.events):
        event_data = schemas.EventCreate(
            organization_id=comparison.organization_id,
            event_input=event_input,
            severity_level=severity_levels[idx]
        )
        db_event = crud.create_event(db, event_data)
        event_ids.append(db_event.id)
        
        # Start background processing for each event
        background_tasks.add_task(
            process_event_background,
            db,
            db_event.id,
            comparison.organization_id,
            event_input,
            severity_levels[idx]
        )
    
    # Generate comparison ID
    comparison_id = f"CMP-{'-'.join(map(str, event_ids))}"
    
    return {
        "comparison_id": comparison_id,
        "events": [crud.get_event(db, eid) for eid in event_ids],
        "priority_recommendation": "Analysis in progress - check individual event results",
        "comparative_analysis": {
            "status": "processing",
            "event_ids": event_ids,
            "note": "Individual analyses are being processed. Refresh to see results."
        }
    }


@router.get("/compare/{comparison_id}")
def get_comparison_results(
    comparison_id: str,
    db: Session = Depends(get_db)
):
    """
    Get comparison results after events have been processed
    """
    # Extract event IDs from comparison_id
    try:
        event_ids = [int(id_str) for id_str in comparison_id.replace("CMP-", "").split("-")]
    except:
        raise HTTPException(status_code=400, detail="Invalid comparison ID format")
    
    # Get all events
    events = [crud.get_event(db, eid) for eid in event_ids]
    
    # Check if all are completed
    all_completed = all(e and e.processing_status == "completed" for e in events)
    
    if not all_completed:
        return {
            "comparison_id": comparison_id,
            "status": "processing",
            "events": events,
            "message": "Some events are still being processed"
        }
    
    # Perform comparative analysis
    risk_scores = [e.overall_risk_score for e in events]
    max_risk_idx = risk_scores.index(max(risk_scores))
    
    comparative_analysis = {
        "highest_risk_event": {
            "event_id": events[max_risk_idx].id,
            "event_input": events[max_risk_idx].event_input,
            "risk_score": events[max_risk_idx].overall_risk_score,
            "affected_suppliers": events[max_risk_idx].affected_supplier_count
        },
        "risk_score_comparison": [
            {
                "event_id": e.id,
                "event_input": e.event_input[:50] + "...",
                "risk_score": e.overall_risk_score,
                "risk_level": e.risk_analysis.get("risk_level") if e.risk_analysis else "UNKNOWN"
            }
            for e in events
        ],
        "priority_order": sorted(
            enumerate(events),
            key=lambda x: x[1].overall_risk_score,
            reverse=True
        )
    }
    
    priority_recommendation = f"Address Event #{events[max_risk_idx].id} first (Risk Score: {events[max_risk_idx].overall_risk_score:.2f})"
    
    return {
        "comparison_id": comparison_id,
        "status": "completed",
        "events": events,
        "priority_recommendation": priority_recommendation,
        "comparative_analysis": comparative_analysis
    }