"""
Background scheduler for live feed monitoring
Uses APScheduler to periodically check for supply chain alerts
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
from typing import List, Dict
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .live_feeds import AlertDetector

logger = logging.getLogger(__name__)


class FeedScheduler:
    """Manages scheduled tasks for live feed monitoring"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    def start(self):
        """Start the background scheduler"""
        if not self.is_running:
            # Check for alerts every 15 minutes
            self.scheduler.add_job(
                self.check_alerts,
                trigger=IntervalTrigger(minutes=15),
                id='alert_scanner',
                name='Scan for supply chain alerts',
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            logger.info("🔄 Alert scheduler started - checking every 15 minutes")
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("🛑 Alert scheduler stopped")
    
    async def check_alerts(self):
        """Scheduled job to check for new alerts"""
        logger.info(f"⏰ Running alert scan at {datetime.now()}")
        
        db = SessionLocal()
        try:
            detector = AlertDetector(db)
            alerts = await detector.scan_for_alerts()
            
            if alerts:
                logger.info(f"🚨 Found {len(alerts)} new alerts")
                # Here you could trigger notifications, webhooks, etc.
                await self.notify_alerts(alerts)
            else:
                logger.info("✅ No critical alerts detected")
                
        except Exception as e:
            logger.error(f"❌ Error during alert scan: {str(e)}")
        finally:
            db.close()
    
    async def notify_alerts(self, alerts: List[Dict]):
        """Send notifications for detected alerts"""
        # You can implement various notification channels:
        # - Email
        # - Slack/Teams webhooks
        # - SMS
        # - In-app notifications
        
        for alert in alerts:
            logger.warning(
                f"🚨 ALERT: {alert['title']} | "
                f"Severity: {alert['severity']} | "
                f"Affected suppliers: {alert['affected_count']}"
            )


# Global scheduler instance
feed_scheduler = FeedScheduler()
