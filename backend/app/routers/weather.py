"""
Weather monitoring endpoints for real-time weather data
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from app.database import get_db
from app.services.weather_monitor import WeatherMonitor
from app.services.weather_worker import get_weather_worker
from app import crud

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/organization/{organization_id}")
async def get_organization_weather(
    organization_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get real-time weather data for all suppliers of an organization
    
    Args:
        organization_id: Organization ID
        db: Database session
        
    Returns:
        Weather summary with all supplier conditions and alerts
    """
    # Verify organization exists
    organization = crud.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get all suppliers for this organization
    suppliers = crud.get_suppliers_by_organization(db, organization_id)
    
    if not suppliers:
        return {
            "organization_id": organization_id,
            "organization_name": organization.name,
            "timestamp": datetime.utcnow().isoformat(),
            "total_suppliers": 0,
            "monitored_suppliers": 0,
            "total_alerts": 0,
            "critical_alerts": [],
            "high_alerts": [],
            "moderate_alerts": [],
            "weather_data": []
        }
    
    # Get weather data
    weather_monitor = WeatherMonitor()
    summary = weather_monitor.get_weather_summary(suppliers)
    
    return {
        "organization_id": organization_id,
        "organization_name": organization.name,
        **summary
    }


@router.get("/supplier/{supplier_id}")
async def get_supplier_weather(
    supplier_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get real-time weather data for a specific supplier
    
    Args:
        supplier_id: Supplier ID
        db: Database session
        
    Returns:
        Weather data for the supplier
    """
    # Get supplier
    supplier = crud.get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    if not supplier.latitude or not supplier.longitude:
        raise HTTPException(
            status_code=400, 
            detail="Supplier location coordinates not available"
        )
    
    # Get weather data
    weather_monitor = WeatherMonitor()
    weather_data = weather_monitor.get_weather_for_supplier(supplier)
    
    if not weather_data:
        raise HTTPException(
            status_code=503, 
            detail="Failed to fetch weather data"
        )
    
    return weather_data


@router.post("/organization/{organization_id}/analyze-alerts")
async def analyze_weather_alerts(
    organization_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze current weather alerts and create events for severe conditions
    
    Args:
        organization_id: Organization ID
        db: Database session
        
    Returns:
        Summary of created events
    """
    from app.models import Event
    from app.agents.orchestrator import AgentOrchestrator
    
    # Verify organization exists
    organization = crud.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get suppliers
    suppliers = crud.get_suppliers_by_organization(db, organization_id)
    if not suppliers:
        return {
            "message": "No suppliers found for organization",
            "events_created": 0
        }
    
    # Get weather data
    weather_monitor = WeatherMonitor()
    weather_data = weather_monitor.get_weather_for_suppliers(suppliers)
    
    created_events = []
    
    # Create events for suppliers with alerts
    for weather in weather_data:
        alerts = weather.get("alerts", [])
        
        # Only create events for high severity alerts (severity >= 3)
        high_severity_alerts = [a for a in alerts if a.get("severity", 0) >= 3]
        
        if high_severity_alerts:
            # Get supplier
            supplier = next((s for s in suppliers if s.id == weather["supplier_id"]), None)
            if not supplier:
                continue
            
            # Use the highest severity alert
            primary_alert = max(high_severity_alerts, key=lambda x: x.get("severity", 0))
            
            # Generate event description
            event_description = weather_monitor.generate_weather_event_description(
                primary_alert, 
                supplier
            )
            
            # Create event
            event = Event(
                organization_id=organization_id,
                event_type="weather_disruption",
                severity=primary_alert["severity"],
                description=event_description,
                location=weather["location"],
                event_data={
                    "weather_conditions": {
                        "temperature": weather["temperature"],
                        "precipitation": weather["precipitation"],
                        "wind_speed": weather["wind_speed"],
                        "wind_gusts": weather["wind_gusts"],
                        "weather_code": weather["weather_code"]
                    },
                    "alerts": alerts,
                    "primary_alert": primary_alert,
                    "affected_supplier": {
                        "id": supplier.id,
                        "name": supplier.name,
                        "location": weather["location"]
                    }
                },
                processing_status="pending"
            )
            
            db.add(event)
            db.commit()
            db.refresh(event)
            
            created_events.append({
                "event_id": event.id,
                "supplier": supplier.name,
                "alert_type": primary_alert["type"],
                "severity": primary_alert["severity"]
            })
            
            # Trigger agent analysis in background
            orchestrator = AgentOrchestrator(db)
            try:
                await orchestrator.process_event_async(event.id)
            except Exception as e:
                print(f"Error processing event {event.id}: {str(e)}")
    
    return {
        "message": f"Created {len(created_events)} weather-related events",
        "events_created": len(created_events),
        "events": created_events,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/alerts/{organization_id}/active")
async def get_active_weather_alerts(
    organization_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get all active weather alerts for an organization (no event creation)
    
    Args:
        organization_id: Organization ID
        db: Database session
        
    Returns:
        Active weather alerts
    """
    # Verify organization exists
    organization = crud.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get suppliers
    suppliers = crud.get_suppliers_by_organization(db, organization_id)
    
    # Get weather summary
    weather_monitor = WeatherMonitor()
    summary = weather_monitor.get_weather_summary(suppliers)
    
    return {
        "organization_id": organization_id,
        "organization_name": organization.name,
        "timestamp": summary["timestamp"],
        "total_alerts": summary["total_alerts"],
        "critical_alerts": summary["critical_alerts"],
        "high_alerts": summary["high_alerts"],
        "moderate_alerts": summary["moderate_alerts"]
    }


@router.get("/worker/status")
async def get_worker_status() -> Dict[str, Any]:
    """
    Get weather monitoring worker status
    
    Returns:
        Worker status information
    """
    worker = get_weather_worker()
    return {
        "running": worker.running,
        "poll_interval": worker.poll_interval,
        "monitored_organizations": len(worker.processed_alerts),
        "status": "active" if worker.running else "stopped"
    }


@router.post("/worker/start")
async def start_worker() -> Dict[str, Any]:
    """
    Start the weather monitoring worker
    
    Returns:
        Success message
    """
    from app.services.weather_worker import start_weather_worker
    import asyncio
    
    worker = get_weather_worker()
    if worker.running:
        return {
            "message": "Weather worker is already running",
            "status": "running"
        }
    
    asyncio.create_task(start_weather_worker())
    
    return {
        "message": "Weather monitoring worker started",
        "status": "started",
        "poll_interval": worker.poll_interval
    }


@router.post("/worker/stop")
async def stop_worker() -> Dict[str, Any]:
    """
    Stop the weather monitoring worker
    
    Returns:
        Success message
    """
    from app.services.weather_worker import stop_weather_worker
    
    stop_weather_worker()
    
    return {
        "message": "Weather monitoring worker stopped",
        "status": "stopped"
    }
