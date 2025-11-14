"""
Monitoring and Logging Module
Provides structured logging and metrics collection for the Supply Chain Risk Monitor
"""
import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from functools import wraps
from collections import defaultdict
import asyncio

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class MonitoringService:
    """Centralized monitoring and metrics collection"""
    
    def __init__(self):
        self.api_calls = defaultdict(int)
        self.api_errors = defaultdict(int)
        self.api_response_times = defaultdict(list)
        self.system_events = []
        self.start_time = datetime.now()
        
    def record_api_call(self, endpoint: str, method: str, status_code: int, response_time: float):
        """Record API call metrics"""
        key = f"{method} {endpoint}"
        self.api_calls[key] += 1
        self.api_response_times[key].append(response_time)
        
        if status_code >= 400:
            self.api_errors[key] += 1
            
        # Log the call
        logger.info(f"API Call: {method} {endpoint} - Status: {status_code} - Time: {response_time:.3f}s")
        
    def record_event(self, event_type: str, message: str, level: str = "INFO", metadata: Optional[Dict] = None):
        """Record system events"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "message": message,
            "level": level,
            "metadata": metadata or {}
        }
        self.system_events.append(event)
        
        # Keep only last 100 events
        if len(self.system_events) > 100:
            self.system_events = self.system_events[-100:]
            
        # Log based on level
        log_func = getattr(logger, level.lower(), logger.info)
        log_func(f"{event_type}: {message}")
        
    def get_metrics(self) -> Dict:
        """Get current metrics snapshot"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Calculate average response times
        avg_response_times = {}
        for endpoint, times in self.api_response_times.items():
            if times:
                avg_response_times[endpoint] = sum(times) / len(times)
        
        return {
            "uptime_seconds": uptime,
            "total_api_calls": sum(self.api_calls.values()),
            "total_errors": sum(self.api_errors.values()),
            "api_calls_by_endpoint": dict(self.api_calls),
            "api_errors_by_endpoint": dict(self.api_errors),
            "avg_response_times": avg_response_times,
            "recent_events": self.system_events[-10:],  # Last 10 events
            "timestamp": datetime.now().isoformat()
        }
    
    def get_health_status(self) -> Dict:
        """Get system health status"""
        total_calls = sum(self.api_calls.values())
        total_errors = sum(self.api_errors.values())
        error_rate = (total_errors / total_calls * 100) if total_calls > 0 else 0
        
        # Determine health status
        if error_rate > 10:
            status = "UNHEALTHY"
            color = "red"
        elif error_rate > 5:
            status = "DEGRADED"
            color = "yellow"
        else:
            status = "HEALTHY"
            color = "green"
            
        return {
            "status": status,
            "color": color,
            "error_rate": round(error_rate, 2),
            "total_calls": total_calls,
            "total_errors": total_errors,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }


# Global monitoring instance
_monitoring_service = MonitoringService()


def get_monitoring_service() -> MonitoringService:
    """Get the global monitoring service instance"""
    return _monitoring_service


def monitor_api_call(endpoint_name: str = None):
    """Decorator to monitor API endpoint calls"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200
            endpoint = endpoint_name or func.__name__
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = 500
                logger.error(f"Error in {endpoint}: {str(e)}", exc_info=True)
                raise
            finally:
                response_time = time.time() - start_time
                _monitoring_service.record_api_call(endpoint, "API", status_code, response_time)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200
            endpoint = endpoint_name or func.__name__
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = 500
                logger.error(f"Error in {endpoint}: {str(e)}", exc_info=True)
                raise
            finally:
                response_time = time.time() - start_time
                _monitoring_service.record_api_call(endpoint, "API", status_code, response_time)
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Example usage functions
def log_info(message: str, **kwargs):
    """Log info level message"""
    _monitoring_service.record_event("INFO", message, "INFO", kwargs)


def log_warning(message: str, **kwargs):
    """Log warning level message"""
    _monitoring_service.record_event("WARNING", message, "WARNING", kwargs)


def log_error(message: str, **kwargs):
    """Log error level message"""
    _monitoring_service.record_event("ERROR", message, "ERROR", kwargs)


def log_api_call(service: str, endpoint: str, status: str, **kwargs):
    """Log external API calls"""
    _monitoring_service.record_event(
        "API_CALL",
        f"{service} - {endpoint}",
        "INFO",
        {"service": service, "endpoint": endpoint, "status": status, **kwargs}
    )
