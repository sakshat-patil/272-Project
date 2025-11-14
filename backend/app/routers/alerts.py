"""
Live Alerts API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import LiveFeed
from ..services.live_feeds import AlertDetector, LiveFeedService
from ..services.scheduler import feed_scheduler

router = APIRouter(prefix="/api/alerts", tags=["Live Alerts"])


@router.post("/scan")
async def trigger_alert_scan(db: Session = Depends(get_db)):
    """
    Manually trigger an alert scan
    
    This runs the alert detection process immediately instead of waiting for the scheduled scan
    """
    try:
        detector = AlertDetector(db)
        alerts = await detector.scan_for_alerts()
        
        return {
            "status": "success",
            "scan_time": datetime.now().isoformat(),
            "alerts_found": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert scan failed: {str(e)}")


@router.get("/recent")
async def get_recent_alerts(
    hours: int = 24,
    severity: str = None,
    db: Session = Depends(get_db)
):
    """
    Get recent alerts from the last N hours
    
    Parameters:
    - hours: Number of hours to look back (default: 24)
    - severity: Filter by severity level (CRITICAL, HIGH, MEDIUM, LOW)
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        query = db.query(LiveFeed).filter(
            LiveFeed.data_type == "ALERT",
            LiveFeed.timestamp >= cutoff_time
        )
        
        alerts = query.order_by(LiveFeed.timestamp.desc()).all()
        
        # Filter by severity if specified
        result = []
        for alert in alerts:
            alert_data = alert.payload
            if severity is None or alert_data.get("severity") == severity:
                result.append(alert_data)
        
        return {
            "status": "success",
            "time_range_hours": hours,
            "severity_filter": severity,
            "count": len(result),
            "alerts": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")


@router.get("/events")
async def get_live_events(
    source: str = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """
    Get raw live events from external feeds (before alert filtering)
    
    Parameters:
    - source: Filter by source (GDELT, NewsAPI, NOAA)
    - hours: Number of hours to look back
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        query = db.query(LiveFeed).filter(
            LiveFeed.data_type == "EVENT",
            LiveFeed.timestamp >= cutoff_time
        )
        
        if source:
            query = query.filter(LiveFeed.source == source)
        
        events = query.order_by(LiveFeed.timestamp.desc()).limit(100).all()
        
        return {
            "status": "success",
            "source_filter": source,
            "count": len(events),
            "events": [e.payload for e in events]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch events: {str(e)}")


@router.get("/dashboard")
async def get_alert_dashboard(db: Session = Depends(get_db)):
    """
    Get dashboard summary of alerts and threats
    """
    try:
        # Get alerts from last 7 days
        cutoff = datetime.now() - timedelta(days=7)
        
        recent_alerts = db.query(LiveFeed).filter(
            LiveFeed.data_type == "ALERT",
            LiveFeed.timestamp >= cutoff
        ).all()
        
        # Calculate statistics
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        event_type_counts = {}
        total_affected_suppliers = 0
        
        for alert in recent_alerts:
            alert_data = alert.payload
            severity = alert_data.get("severity", "MEDIUM")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            event_type = alert_data.get("event_type", "OTHER")
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
            
            total_affected_suppliers += alert_data.get("affected_count", 0)
        
        # Get recent critical alerts
        critical_alerts = [
            a.payload for a in recent_alerts
            if a.payload.get("severity") in ["CRITICAL", "HIGH"]
        ][:10]
        
        return {
            "status": "success",
            "period_days": 7,
            "summary": {
                "total_alerts": len(recent_alerts),
                "critical_count": severity_counts["CRITICAL"],
                "high_count": severity_counts["HIGH"],
                "total_affected_suppliers": total_affected_suppliers,
                "severity_breakdown": severity_counts,
                "event_type_breakdown": event_type_counts
            },
            "recent_critical_alerts": critical_alerts,
            "scheduler_status": "running" if feed_scheduler.is_running else "stopped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")


@router.post("/scheduler/start")
async def start_scheduler():
    """Start the background alert scanner"""
    try:
        feed_scheduler.start()
        return {
            "status": "success",
            "message": "Alert scanner started",
            "check_interval_minutes": 15
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scheduler: {str(e)}")


@router.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the background alert scanner"""
    try:
        feed_scheduler.stop()
        return {
            "status": "success",
            "message": "Alert scanner stopped"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop scheduler: {str(e)}")


@router.get("/test/gdelt")
async def test_gdelt_feed():
    """Test GDELT API connection"""
    try:
        service = LiveFeedService()
        events = await service.fetch_gdelt_events("supply chain OR earthquake")
        
        return {
            "status": "success",
            "source": "GDELT",
            "events_found": len(events),
            "sample_events": events[:5]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GDELT test failed: {str(e)}")


@router.get("/test/weather")
async def test_weather_feed():
    """Test NOAA weather API connection"""
    try:
        service = LiveFeedService()
        alerts = await service.fetch_weather_alerts(["CA", "TX", "FL"])
        
        return {
            "status": "success",
            "source": "NOAA",
            "alerts_found": len(alerts),
            "sample_alerts": alerts[:5]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather API test failed: {str(e)}")
