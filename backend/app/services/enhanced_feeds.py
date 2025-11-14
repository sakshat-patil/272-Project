"""
Enhanced Live Feeds - Additional APIs beyond news/weather
"""
import httpx
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class FinancialDataService:
    """Track supplier financial health and commodity prices"""
    
    async def get_stock_data(self, ticker: str) -> Dict:
        """
        Get stock data for publicly traded supplier companies
        
        Example: ticker = "TSMC" (Taiwan Semiconductor)
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get recent price history
            hist = stock.history(period="5d")
            
            if len(hist) >= 2:
                price_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / 
                               hist['Close'].iloc[0] * 100)
            else:
                price_change = 0
            
            return {
                "ticker": ticker,
                "current_price": info.get('regularMarketPrice'),
                "price_change_5d": round(price_change, 2),
                "market_cap": info.get('marketCap'),
                "financial_health": self._assess_financial_health(price_change),
                "alert_level": "HIGH" if price_change < -15 else "MEDIUM" if price_change < -10 else "LOW",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Stock data error for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    def _assess_financial_health(self, price_change: float) -> str:
        """Assess financial health based on recent stock performance"""
        if price_change < -20:
            return "CRITICAL - Severe stock decline, potential financial distress"
        elif price_change < -15:
            return "WARNING - Significant decline, monitor closely"
        elif price_change < -10:
            return "CAUTION - Notable decline"
        elif price_change > 15:
            return "STRONG - Significant growth"
        else:
            return "STABLE - Normal trading range"
    
    async def get_commodity_prices(self, commodities: List[str]) -> Dict:
        """
        Track commodity prices (lithium, copper, oil, etc.)
        
        Note: For demo, using yfinance futures
        For production, use Trading Economics API or World Bank API
        """
        results = {}
        
        # Commodity ticker mappings
        commodity_tickers = {
            "oil": "CL=F",      # Crude Oil
            "gold": "GC=F",     # Gold
            "copper": "HG=F",   # Copper
            "lithium": "LAC",   # Lithium Americas (proxy)
        }
        
        for commodity in commodities:
            ticker = commodity_tickers.get(commodity.lower())
            if ticker:
                try:
                    data = yf.Ticker(ticker)
                    hist = data.history(period="30d")
                    
                    if len(hist) >= 2:
                        price_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / 
                                      hist['Close'].iloc[0] * 100)
                        
                        results[commodity] = {
                            "current_price": round(hist['Close'].iloc[-1], 2),
                            "change_30d": round(price_change, 2),
                            "alert": price_change > 30 or price_change < -30,
                            "trend": "UP" if price_change > 5 else "DOWN" if price_change < -5 else "STABLE"
                        }
                except Exception as e:
                    logger.error(f"Commodity price error for {commodity}: {str(e)}")
        
        return results
    
    async def get_exchange_rates(self, base_currency: str = "USD") -> Dict:
        """
        Get current exchange rates
        Uses exchangerate-api.com (free tier: 1500 requests/month)
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "base": base_currency,
                        "rates": data.get("rates", {}),
                        "timestamp": datetime.now().isoformat()
                    }
        except Exception as e:
            logger.error(f"Exchange rate error: {str(e)}")
            return {"error": str(e)}


class ShippingDataService:
    """Track shipping routes, port congestion, delivery delays"""
    
    async def check_port_status(self, port_name: str) -> Dict:
        """
        Check port congestion and delays
        
        Note: For demo, using mock data
        For production, integrate MarineTraffic API or Searoutes API
        """
        # Mock data for demonstration
        # In production, call actual API:
        # https://www.marinetraffic.com/en/ais-api-services
        
        port_data = {
            "Los Angeles": {"congestion": 8, "avg_wait_hours": 72, "vessels_waiting": 45},
            "Shanghai": {"congestion": 6, "avg_wait_hours": 48, "vessels_waiting": 30},
            "Rotterdam": {"congestion": 4, "avg_wait_hours": 24, "vessels_waiting": 15},
            "Singapore": {"congestion": 3, "avg_wait_hours": 12, "vessels_waiting": 8},
        }
        
        data = port_data.get(port_name, {"congestion": 5, "avg_wait_hours": 36, "vessels_waiting": 20})
        
        return {
            "port": port_name,
            "congestion_level": data["congestion"],  # 0-10 scale
            "avg_wait_time_hours": data["avg_wait_hours"],
            "vessels_waiting": data["vessels_waiting"],
            "status": self._assess_port_status(data["congestion"]),
            "estimated_delay_days": data["avg_wait_hours"] // 24,
            "timestamp": datetime.now().isoformat()
        }
    
    def _assess_port_status(self, congestion: int) -> str:
        """Assess port status based on congestion level"""
        if congestion >= 8:
            return "CRITICAL - Severe delays expected"
        elif congestion >= 6:
            return "HIGH - Significant delays"
        elif congestion >= 4:
            return "MODERATE - Minor delays"
        else:
            return "NORMAL - Operating smoothly"
    
    async def track_shipping_route(self, origin: str, destination: str) -> Dict:
        """
        Estimate shipping time and detect route disruptions
        
        For production: Use Searoutes API
        https://www.searoutes.com/api
        """
        # Mock estimated transit times (in days)
        routes = {
            ("Shanghai", "Los Angeles"): 14,
            ("Rotterdam", "New York"): 10,
            ("Singapore", "London"): 18,
            ("Tokyo", "San Francisco"): 12,
        }
        
        route_key = (origin, destination)
        base_time = routes.get(route_key, 15)
        
        # Add random delay factor for demo
        # In production, this would come from real-time API
        current_delay = 0  # Could be calculated from weather, port status, etc.
        
        return {
            "origin": origin,
            "destination": destination,
            "estimated_days": base_time + current_delay,
            "status": "ON_TIME" if current_delay < 2 else "DELAYED",
            "delay_days": current_delay,
            "timestamp": datetime.now().isoformat()
        }


class GeopoliticalRiskService:
    """Monitor geopolitical events, conflicts, sanctions"""
    
    async def check_sanctions(self, entity_name: str) -> Dict:
        """
        Check if entity is on sanctions lists
        
        Uses OpenSanctions API (free)
        https://www.opensanctions.org/api/
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://api.opensanctions.org/search/default",
                    params={"q": entity_name, "limit": 5}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    return {
                        "entity": entity_name,
                        "sanctioned": len(results) > 0,
                        "matches": results,
                        "risk_level": "CRITICAL" if len(results) > 0 else "CLEAR",
                        "details": results[0] if results else None,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "entity": entity_name,
                        "sanctioned": False,
                        "risk_level": "UNKNOWN",
                        "error": f"API returned status {response.status_code}",
                        "timestamp": datetime.now().isoformat()
                    }
        except Exception as e:
            logger.error(f"Sanctions check error: {str(e)}")
            return {
                "entity": entity_name,
                "sanctioned": False,
                "risk_level": "UNKNOWN",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_conflict_data(self, country: str) -> Dict:
        """
        Get conflict/political instability data
        
        Uses ACLED API (Armed Conflict Location & Event Data)
        https://acleddata.com/acleddatanew/
        
        Note: Requires free API key
        """
        # Mock data for demo
        # In production, call actual ACLED API
        
        conflict_levels = {
            "Ukraine": {"level": 9, "events_30d": 145, "status": "Active Conflict"},
            "Israel": {"level": 8, "events_30d": 89, "status": "Active Conflict"},
            "Taiwan": {"level": 4, "events_30d": 12, "status": "Heightened Tensions"},
            "China": {"level": 2, "events_30d": 5, "status": "Stable"},
            "USA": {"level": 1, "events_30d": 2, "status": "Stable"},
        }
        
        data = conflict_levels.get(country, {"level": 3, "events_30d": 8, "status": "Moderate"})
        
        return {
            "country": country,
            "conflict_level": data["level"],  # 0-10 scale
            "events_last_30_days": data["events_30d"],
            "status": data["status"],
            "risk_assessment": self._assess_geopolitical_risk(data["level"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def _assess_geopolitical_risk(self, level: int) -> str:
        """Assess geopolitical risk level"""
        if level >= 8:
            return "CRITICAL - Active conflict, immediate supply chain impact"
        elif level >= 6:
            return "HIGH - Significant political instability"
        elif level >= 4:
            return "MODERATE - Tensions present, monitor closely"
        else:
            return "LOW - Stable political environment"


class SocialMediaMonitor:
    """Monitor social media for early warning signals"""
    
    async def search_twitter(self, query: str, supplier_name: str) -> Dict:
        """
        Search Twitter for mentions of supplier issues
        
        Note: Requires Twitter API v2 credentials
        For demo, using mock data
        """
        # Mock sentiment analysis
        # In production, use Twitter API + sentiment analysis library
        
        return {
            "supplier": supplier_name,
            "query": query,
            "mentions_24h": 0,  # Would come from actual API
            "sentiment_score": 0.5,  # -1 to 1 scale
            "sentiment": "NEUTRAL",
            "trending": False,
            "sample_tweets": [],
            "alert": False,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_google_trends(self, keyword: str) -> Dict:
        """
        Check if supplier name is trending on Google
        
        Uses pytrends library (free)
        Note: Google may rate-limit requests. Using fallback mock data for demo.
        """
        try:
            # Try to use pytrends, but it may fail due to rate limiting
            from pytrends.request import TrendReq
            import pandas as pd
            
            # Run in executor to avoid blocking
            import asyncio
            from concurrent.futures import ThreadPoolExecutor
            
            def get_trends():
                try:
                    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
                    pytrends.build_payload([keyword], timeframe='now 7-d')
                    data = pytrends.interest_over_time()
                    
                    if not data.empty and keyword in data.columns:
                        recent_interest = float(data[keyword].iloc[-1])
                        avg_interest = float(data[keyword].mean())
                        is_trending = bool(recent_interest > avg_interest * 1.5)
                        
                        return {
                            "keyword": keyword,
                            "current_interest": int(recent_interest),
                            "avg_interest": int(avg_interest),
                            "trending": is_trending,
                            "change_percent": round(((recent_interest - avg_interest) / avg_interest * 100), 2),
                            "timestamp": datetime.now().isoformat(),
                            "source": "google_trends"
                        }
                    return None
                except Exception as e:
                    logger.warning(f"Google Trends API error: {str(e)}")
                    return None
            
            # Try to get real data with timeout
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                result = await asyncio.wait_for(
                    loop.run_in_executor(executor, get_trends),
                    timeout=5.0
                )
                if result:
                    return result
        
        except Exception as e:
            logger.warning(f"Google Trends error: {str(e)}, using mock data")
        
        # Fallback to mock data for demo purposes
        import random
        current_interest = random.randint(40, 100)
        avg_interest = random.randint(30, 70)
        
        return {
            "keyword": keyword,
            "current_interest": current_interest,
            "avg_interest": avg_interest,
            "trending": current_interest > avg_interest * 1.5,
            "change_percent": round(((current_interest - avg_interest) / avg_interest * 100), 2),
            "timestamp": datetime.now().isoformat(),
            "source": "mock_data",
            "note": "Using mock data - Google Trends may be rate limited"
        }


# Unified enhanced feed aggregator
class EnhancedFeedAggregator:
    """Combines all enhanced data sources"""
    
    def __init__(self):
        self.financial = FinancialDataService()
        self.shipping = ShippingDataService()
        self.geopolitical = GeopoliticalRiskService()
        self.social = SocialMediaMonitor()
    
    async def get_comprehensive_risk_data(self, supplier_data: Dict) -> Dict:
        """
        Get all available risk data for a supplier
        
        Returns comprehensive risk assessment from all sources
        """
        results = {
            "supplier": supplier_data.get("name"),
            "timestamp": datetime.now().isoformat(),
            "data_sources": {}
        }
        
        # Financial data (if supplier is public company)
        if supplier_data.get("stock_ticker"):
            results["data_sources"]["financial"] = await self.financial.get_stock_data(
                supplier_data["stock_ticker"]
            )
        
        # Shipping status (if supplier uses specific ports)
        if supplier_data.get("primary_port"):
            results["data_sources"]["shipping"] = await self.shipping.check_port_status(
                supplier_data["primary_port"]
            )
        
        # Sanctions check
        results["data_sources"]["sanctions"] = await self.geopolitical.check_sanctions(
            supplier_data.get("name")
        )
        
        # Geopolitical risk for supplier's country
        if supplier_data.get("country"):
            results["data_sources"]["geopolitical"] = await self.geopolitical.get_conflict_data(
                supplier_data["country"]
            )
        
        # Calculate aggregate risk score
        results["aggregate_risk_score"] = self._calculate_aggregate_risk(results["data_sources"])
        
        return results
    
    def _calculate_aggregate_risk(self, data_sources: Dict) -> int:
        """Calculate 0-100 risk score from all data sources"""
        risk_score = 0
        
        # Financial risk
        if "financial" in data_sources and "alert_level" in data_sources["financial"]:
            if data_sources["financial"]["alert_level"] == "HIGH":
                risk_score += 25
            elif data_sources["financial"]["alert_level"] == "MEDIUM":
                risk_score += 15
        
        # Shipping delays
        if "shipping" in data_sources:
            congestion = data_sources["shipping"].get("congestion_level", 0)
            risk_score += min(congestion * 2, 20)
        
        # Sanctions
        if "sanctions" in data_sources and data_sources["sanctions"].get("sanctioned"):
            risk_score += 40  # Critical risk
        
        # Geopolitical
        if "geopolitical" in data_sources:
            conflict_level = data_sources["geopolitical"].get("conflict_level", 0)
            risk_score += min(conflict_level * 3, 30)
        
        return min(risk_score, 100)
