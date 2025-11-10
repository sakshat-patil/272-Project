"""
Background worker for continuous weather monitoring and automatic event analysis
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Set
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.weather_monitor import WeatherMonitor
from app.models import Event
from app.agents.orchestrator import AgentOrchestrator
from app import crud

logger = logging.getLogger(__name__)


class WeatherWorker:
    """Background worker that monitors weather and creates events automatically"""
    
    def __init__(self, poll_interval: int = 10):
        """
        Initialize weather worker
        
        Args:
            poll_interval: Seconds between weather checks (default: 10)
        """
        self.poll_interval = poll_interval
        self.weather_monitor = WeatherMonitor()
        self.running = False
        self.processed_alerts: Dict[int, Set[str]] = {}  # org_id -> set of alert signatures
        
    async def start(self):
        """Start the weather monitoring worker"""
        self.running = True
        logger.info(f"🌦️ Weather worker started - polling every {self.poll_interval}s")
        
        while self.running:
            try:
                await self._check_all_organizations()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Error in weather worker: {str(e)}", exc_info=True)
                await asyncio.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the weather monitoring worker"""
        self.running = False
        logger.info("🛑 Weather worker stopped")
    
    async def _check_all_organizations(self):
        """Check weather for all organizations and create events for severe conditions"""
        db = SessionLocal()
        try:
            # Get all organizations
            organizations = crud.get_organizations(db, skip=0, limit=1000)
            
            for org in organizations:
                await self._check_organization_weather(db, org.id)
                
        except Exception as e:
            logger.error(f"Error checking organizations: {str(e)}")
        finally:
            db.close()
    
    async def _check_organization_weather(self, db: Session, org_id: int):
        """
        Check weather for a specific organization and create events if needed
        
        Args:
            db: Database session
            org_id: Organization ID
        """
        try:
            # Get suppliers for this organization
            suppliers = crud.get_suppliers_by_organization(db, org_id)
            if not suppliers:
                return
            
            # Add delay between requests to respect rate limits
            # Open-Meteo allows ~10k requests/day for free tier
            # With 35 suppliers polled every 10s = ~300k requests/day - TOO MUCH!
            # Solution: Add delay between each supplier request
            weather_data = []
            for supplier in suppliers:
                data = self.weather_monitor.get_weather_for_supplier(supplier)
                if data:
                    weather_data.append(data)
                # Add 0.5s delay between requests (max 2 req/sec)
                await asyncio.sleep(0.5)
            
            # Initialize processed alerts for this org if not exists
            if org_id not in self.processed_alerts:
                self.processed_alerts[org_id] = set()
            
            # Check each supplier's weather
            for weather in weather_data:
                alerts = weather.get("alerts", [])
                
                # Only process high severity alerts (severity >= 4)
                critical_alerts = [a for a in alerts if a.get("severity", 0) >= 4]
                
                if critical_alerts:
                    # Get supplier
                    supplier = next((s for s in suppliers if s.id == weather["supplier_id"]), None)
                    if not supplier:
                        continue
                    
                    # Create unique signature for this alert to avoid duplicates
                    primary_alert = max(critical_alerts, key=lambda x: x.get("severity", 0))
                    alert_signature = f"{supplier.id}_{primary_alert['type']}_{datetime.utcnow().strftime('%Y-%m-%d-%H')}"
                    
                    # Skip if we've already processed this alert in the last hour
                    if alert_signature in self.processed_alerts[org_id]:
                        continue
                    
                    # Create event
                    event_description = self.weather_monitor.generate_weather_event_description(
                        primary_alert,
                        supplier
                    )
                    
                    event = Event(
                        organization_id=org_id,
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
                            },
                            "auto_detected": True,
                            "detection_time": datetime.utcnow().isoformat()
                        },
                        processing_status="pending"
                    )
                    
                    db.add(event)
                    db.commit()
                    db.refresh(event)
                    
                    logger.info(f"🚨 Auto-created weather event {event.id} for {supplier.name}: {primary_alert['type']}")
                    
                    # Mark as processed
                    self.processed_alerts[org_id].add(alert_signature)
                    
                    # Clean up old signatures (keep only last 100 per org)
                    if len(self.processed_alerts[org_id]) > 100:
                        # Remove oldest half
                        signatures_list = list(self.processed_alerts[org_id])
                        self.processed_alerts[org_id] = set(signatures_list[-50:])
                    
                    # Trigger agent analysis in background
                    try:
                        orchestrator = AgentOrchestrator(db)
                        await orchestrator.process_event_async(event.id)
                        logger.info(f"✅ Completed analysis for weather event {event.id}")
                    except Exception as e:
                        logger.error(f"Error processing event {event.id}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Error checking weather for org {org_id}: {str(e)}")


# Global worker instance
_weather_worker: WeatherWorker = None


def get_weather_worker() -> WeatherWorker:
    """Get or create the global weather worker instance"""
    global _weather_worker
    if _weather_worker is None:
        # Increased to 60 seconds (1 minute) to reduce API load
        # With 35 suppliers + 0.5s delay = ~17.5s per poll cycle
        # This gives plenty of time between cycles
        _weather_worker = WeatherWorker(poll_interval=60)
    return _weather_worker


async def start_weather_worker():
    """Start the weather monitoring worker"""
    worker = get_weather_worker()
    if not worker.running:
        asyncio.create_task(worker.start())


def stop_weather_worker():
    """Stop the weather monitoring worker"""
    worker = get_weather_worker()
    worker.stop()
