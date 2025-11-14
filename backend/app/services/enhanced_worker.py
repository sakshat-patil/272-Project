"""
Background worker for Tier 1 Enhanced API monitoring (Financial, Shipping, Geopolitical)
Runs every 5 minutes to check financial markets, port status, sanctions, and geopolitical risks
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.enhanced_feeds import (
    FinancialDataService,
    ShippingDataService,
    GeopoliticalRiskService,
    EnhancedFeedAggregator
)
from app import crud

logger = logging.getLogger(__name__)


class EnhancedDataWorker:
    """Background worker that monitors financial, shipping, and geopolitical data"""
    
    def __init__(self, poll_interval: int = 300):  # 5 minutes default
        """
        Initialize enhanced data worker
        
        Args:
            poll_interval: Seconds between checks (default: 300 = 5 minutes)
        """
        self.poll_interval = poll_interval
        self.financial_service = FinancialDataService()
        self.shipping_service = ShippingDataService()
        self.geopolitical_service = GeopoliticalRiskService()
        self.aggregator = EnhancedFeedAggregator()
        self.running = False
        
    async def start(self):
        """Start the enhanced data monitoring worker"""
        self.running = True
        logger.info(f"💹 Enhanced data worker started - polling every {self.poll_interval}s")
        
        while self.running:
            try:
                await self._check_all_data_sources()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Error in enhanced data worker: {str(e)}", exc_info=True)
                await asyncio.sleep(self.poll_interval)
    
    def stop(self):
        """Stop the enhanced data monitoring worker"""
        self.running = False
        logger.info("🛑 Enhanced data worker stopped")
    
    async def _check_all_data_sources(self):
        """Check all enhanced data sources and log significant changes"""
        logger.info("🔍 Running enhanced data scan...")
        
        try:
            # 1. Check major commodity prices
            await self._check_commodity_prices()
            
            # 2. Check major port statuses
            await self._check_port_statuses()
            
            # 3. Check high-risk countries for geopolitical changes
            await self._check_geopolitical_risks()
            
            # 4. Check exchange rates for major currencies
            await self._check_exchange_rates()
            
            logger.info("✅ Enhanced data scan complete")
            
        except Exception as e:
            logger.error(f"Error in enhanced data scan: {str(e)}")
    
    async def _check_commodity_prices(self):
        """Monitor key commodity prices for significant changes"""
        try:
            commodities = ["oil", "gold", "copper", "lithium"]
            prices = await self.financial_service.get_commodity_prices(commodities)
            
            alerts = []
            for commodity, data in prices.items():
                if data.get("alert"):  # Significant price change (>30% or <-30%)
                    alerts.append(f"{commodity.upper()}: {data.get('change_30d')}% in 30 days")
            
            if alerts:
                logger.warning(f"📊 Commodity price alerts: {', '.join(alerts)}")
            else:
                logger.debug(f"💹 Commodity prices stable: {prices}")
                
        except Exception as e:
            logger.error(f"Commodity price check failed: {str(e)}")
    
    async def _check_port_statuses(self):
        """Monitor major ports for congestion"""
        try:
            major_ports = ["Los Angeles", "Shanghai", "Rotterdam", "Singapore"]
            congested_ports = []
            
            for port in major_ports:
                status = await self.shipping_service.check_port_status(port)
                congestion_level = status.get("congestion_level", 0)
                
                if congestion_level >= 7:  # High congestion
                    congested_ports.append(f"{port} ({congestion_level}/10)")
            
            if congested_ports:
                logger.warning(f"🚢 Port congestion alerts: {', '.join(congested_ports)}")
            else:
                logger.debug(f"⚓ All major ports operating normally")
                
        except Exception as e:
            logger.error(f"Port status check failed: {str(e)}")
    
    async def _check_geopolitical_risks(self):
        """Monitor high-risk countries for conflicts"""
        try:
            high_risk_countries = ["Ukraine", "Israel", "Taiwan", "Iran"]
            critical_risks = []
            
            for country in high_risk_countries:
                conflict_data = await self.geopolitical_service.get_conflict_data(country)
                conflict_level = conflict_data.get("conflict_level", 0)
                
                if conflict_level >= 7:  # Critical risk
                    critical_risks.append(f"{country} (level {conflict_level}/10)")
            
            if critical_risks:
                logger.warning(f"⚠️  Geopolitical risk alerts: {', '.join(critical_risks)}")
            else:
                logger.debug(f"🌍 Geopolitical situation stable")
                
        except Exception as e:
            logger.error(f"Geopolitical risk check failed: {str(e)}")
    
    async def _check_exchange_rates(self):
        """Monitor exchange rates for major currencies"""
        try:
            rates = await self.financial_service.get_exchange_rates()
            
            if "error" in rates:
                logger.error(f"Exchange rate check failed: {rates['error']}")
            else:
                # Log key rates for monitoring (can expand this with change detection)
                key_rates = {k: v for k, v in rates.get("rates", {}).items() 
                            if k in ["EUR", "GBP", "JPY", "CNY", "INR"]}
                logger.debug(f"💱 Exchange rates (USD): {key_rates}")
                
        except Exception as e:
            logger.error(f"Exchange rate check failed: {str(e)}")
    
    async def check_supplier_comprehensive_risk(self, supplier_id: int) -> Dict:
        """
        On-demand comprehensive risk check for a specific supplier
        This can be called from API endpoints for real-time analysis
        
        Args:
            supplier_id: ID of supplier to analyze
            
        Returns:
            Comprehensive risk assessment
        """
        db = SessionLocal()
        try:
            supplier = crud.get_supplier(db, supplier_id)
            if not supplier:
                return {"error": "Supplier not found"}
            
            supplier_data = {
                "name": supplier.name,
                "country": supplier.country,
                "city": supplier.city,
            }
            
            # Get comprehensive risk data from all sources
            risk_data = await self.aggregator.get_comprehensive_risk_data(supplier_data)
            
            logger.info(f"🔍 Comprehensive risk check for {supplier.name}: Score {risk_data.get('aggregate_risk_score')}/100")
            
            return risk_data
            
        except Exception as e:
            logger.error(f"Supplier risk check failed: {str(e)}")
            return {"error": str(e)}
        finally:
            db.close()


# Global worker instance
_enhanced_worker = None
_worker_task = None


async def start_enhanced_worker(poll_interval: int = 300):
    """
    Start the enhanced data worker
    
    Args:
        poll_interval: Seconds between checks (default: 300 = 5 minutes)
    """
    global _enhanced_worker, _worker_task
    
    if _enhanced_worker is None:
        _enhanced_worker = EnhancedDataWorker(poll_interval=poll_interval)
        _worker_task = asyncio.create_task(_enhanced_worker.start())
        logger.info("💹 Enhanced data monitoring started")


def stop_enhanced_worker():
    """Stop the enhanced data worker"""
    global _enhanced_worker, _worker_task
    
    if _enhanced_worker:
        _enhanced_worker.stop()
        if _worker_task:
            _worker_task.cancel()
        _enhanced_worker = None
        _worker_task = None
        logger.info("🛑 Enhanced data monitoring stopped")


def get_enhanced_worker() -> EnhancedDataWorker:
    """Get the global enhanced worker instance"""
    global _enhanced_worker
    if _enhanced_worker is None:
        _enhanced_worker = EnhancedDataWorker()
    return _enhanced_worker
