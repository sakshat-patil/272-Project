"""
Monitoring API endpoints
Provides real-time monitoring and logging dashboard data
"""
from fastapi import APIRouter, Depends
from typing import Dict, List
from datetime import datetime

from app.monitoring import get_monitoring_service, MonitoringService

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/metrics")
async def get_metrics() -> Dict:
    """
    Get current system metrics
    
    Returns:
        - API call statistics
        - Error rates
        - Response times
        - Recent events
    """
    monitoring = get_monitoring_service()
    return monitoring.get_metrics()


@router.get("/health")
async def get_health() -> Dict:
    """
    Get system health status
    
    Returns:
        - Overall health status (HEALTHY/DEGRADED/UNHEALTHY)
        - Error rate
        - Uptime
    """
    monitoring = get_monitoring_service()
    return monitoring.get_health_status()


@router.get("/events")
async def get_recent_events(limit: int = 50) -> Dict:
    """
    Get recent system events/logs
    
    Args:
        limit: Number of events to return (default: 50)
    
    Returns:
        List of recent events with timestamps and metadata
    """
    monitoring = get_monitoring_service()
    events = monitoring.system_events[-limit:] if monitoring.system_events else []
    
    return {
        "total_events": len(monitoring.system_events),
        "events": events,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/api-stats")
async def get_api_stats() -> Dict:
    """
    Get detailed API endpoint statistics
    
    Returns:
        - Calls per endpoint
        - Errors per endpoint
        - Average response times
    """
    monitoring = get_monitoring_service()
    
    # Calculate stats for each endpoint
    endpoint_stats = []
    for endpoint in monitoring.api_calls.keys():
        calls = monitoring.api_calls[endpoint]
        errors = monitoring.api_errors.get(endpoint, 0)
        response_times = monitoring.api_response_times.get(endpoint, [])
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        error_rate = (errors / calls * 100) if calls > 0 else 0
        
        endpoint_stats.append({
            "endpoint": endpoint,
            "total_calls": calls,
            "errors": errors,
            "error_rate": round(error_rate, 2),
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "success_rate": round(100 - error_rate, 2)
        })
    
    # Sort by total calls descending
    endpoint_stats.sort(key=lambda x: x["total_calls"], reverse=True)
    
    return {
        "endpoints": endpoint_stats,
        "total_endpoints": len(endpoint_stats),
        "timestamp": datetime.now().isoformat()
    }


@router.get("/dashboard")
async def get_dashboard_data() -> Dict:
    """
    Get comprehensive dashboard data
    
    Returns complete monitoring dashboard data including:
    - Health status
    - API statistics
    - Recent events
    - System metrics
    """
    monitoring = get_monitoring_service()
    
    health = monitoring.get_health_status()
    metrics = monitoring.get_metrics()
    
    # Top 5 most called endpoints
    top_endpoints = sorted(
        monitoring.api_calls.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    # Top 5 slowest endpoints
    slowest_endpoints = []
    for endpoint, times in monitoring.api_response_times.items():
        if times:
            avg_time = sum(times) / len(times)
            slowest_endpoints.append((endpoint, avg_time))
    slowest_endpoints.sort(key=lambda x: x[1], reverse=True)
    slowest_endpoints = slowest_endpoints[:5]
    
    return {
        "health": health,
        "summary": {
            "total_api_calls": metrics["total_api_calls"],
            "total_errors": metrics["total_errors"],
            "uptime_seconds": metrics["uptime_seconds"],
            "error_rate": health["error_rate"]
        },
        "top_endpoints": [{"endpoint": ep, "calls": count} for ep, count in top_endpoints],
        "slowest_endpoints": [{"endpoint": ep, "avg_time_ms": round(time * 1000, 2)} for ep, time in slowest_endpoints],
        "recent_events": metrics["recent_events"],
        "timestamp": datetime.now().isoformat()
    }
