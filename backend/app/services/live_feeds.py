"""
Live Feed Service - Real-time data ingestion from external APIs
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..models import LiveFeed, Supplier, Organization
from ..database import SessionLocal
import logging

logger = logging.getLogger(__name__)


class LiveFeedService:
    """Service for fetching and processing real-time supply chain risk data"""
    
    def __init__(self):
        self.gdelt_base = "https://api.gdeltproject.org/api/v2"
        self.news_api_base = "https://newsapi.org/v2"
        self.noaa_base = "https://api.weather.gov"
        self.supply_hub_base = "https://opensupplyhub.org/api"
        
    async def fetch_gdelt_events(self, query: str = "supply chain OR earthquake OR strike OR flood") -> List[Dict]:
        """
        Fetch real-time global events from GDELT
        
        Returns events that might impact supply chains
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {
                    "query": query,
                    "mode": "artlist",
                    "format": "json",
                    "maxrecords": 50,
                    "timespan": "24h"
                }
                
                response = await client.get(
                    f"{self.gdelt_base}/doc/doc",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_gdelt_events(data)
                    
        except Exception as e:
            logger.error(f"GDELT API error: {str(e)}")
            return []
    
    def _parse_gdelt_events(self, data: Dict) -> List[Dict]:
        """Parse GDELT response into standardized event format"""
        events = []
        
        if "articles" not in data:
            return events
            
        for article in data.get("articles", []):
            # Extract location and severity
            event = {
                "source": "GDELT",
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "published_at": article.get("seendate", ""),
                "tone": article.get("tone", 0),  # Negative tone = bad news
                "location": self._extract_location(article),
                "event_type": self._classify_event_type(article.get("title", "")),
                "severity": self._calculate_severity(article),
                "raw_data": article
            }
            events.append(event)
            
        return events
    
    def _extract_location(self, article: Dict) -> Optional[Dict]:
        """Extract geographic location from GDELT article"""
        # GDELT provides location data in various fields
        if "locations" in article and len(article["locations"]) > 0:
            loc = article["locations"][0]
            return {
                "country": loc.get("country", ""),
                "region": loc.get("name", ""),
                "lat": loc.get("lat", 0),
                "lon": loc.get("lon", 0)
            }
        return None
    
    def _classify_event_type(self, title: str) -> str:
        """Classify event type based on keywords"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["earthquake", "quake", "seismic"]):
            return "NATURAL_DISASTER"
        elif any(word in title_lower for word in ["strike", "protest", "walkout"]):
            return "LABOR_DISPUTE"
        elif any(word in title_lower for word in ["flood", "hurricane", "typhoon", "storm"]):
            return "WEATHER_EVENT"
        elif any(word in title_lower for word in ["fire", "explosion", "accident"]):
            return "INDUSTRIAL_ACCIDENT"
        elif any(word in title_lower for word in ["port", "shipping", "logistics"]):
            return "LOGISTICS_DISRUPTION"
        else:
            return "OTHER"
    
    def _calculate_severity(self, article: Dict) -> str:
        """Calculate severity based on tone and keywords"""
        tone = float(article.get("tone", 0))
        title = article.get("title", "").lower()
        
        # Very negative tone or critical keywords
        if tone < -5 or any(word in title for word in ["major", "severe", "catastrophic", "disaster"]):
            return "CRITICAL"
        elif tone < -2:
            return "HIGH"
        elif tone < 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def fetch_news_alerts(self, api_key: str, topics: List[str]) -> List[Dict]:
        """
        Fetch news from NewsAPI for supply chain disruptions
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                query = " OR ".join(topics)
                params = {
                    "q": query,
                    "apiKey": api_key,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 50,
                    "from": (datetime.now() - timedelta(days=1)).isoformat()
                }
                
                response = await client.get(
                    f"{self.news_api_base}/everything",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_news_articles(data)
                    
        except Exception as e:
            logger.error(f"NewsAPI error: {str(e)}")
            return []
    
    def _parse_news_articles(self, data: Dict) -> List[Dict]:
        """Parse NewsAPI response"""
        events = []
        
        for article in data.get("articles", []):
            event = {
                "source": "NewsAPI",
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", ""),
                "event_type": self._classify_event_type(article.get("title", "")),
                "severity": "MEDIUM",  # Default, can be enhanced with NLP
                "raw_data": article
            }
            events.append(event)
            
        return events
    
    async def fetch_weather_alerts(self, regions: List[str]) -> List[Dict]:
        """
        Fetch weather alerts from NOAA for specific regions
        """
        alerts = []
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                for region in regions:
                    response = await client.get(
                        f"{self.noaa_base}/alerts/active",
                        params={"area": region}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        alerts.extend(self._parse_weather_alerts(data))
                        
        except Exception as e:
            logger.error(f"NOAA API error: {str(e)}")
            
        return alerts
    
    def _parse_weather_alerts(self, data: Dict) -> List[Dict]:
        """Parse NOAA weather alerts"""
        events = []
        
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            event = {
                "source": "NOAA",
                "title": props.get("headline", ""),
                "event_type": "WEATHER_EVENT",
                "severity": self._map_noaa_severity(props.get("severity", "")),
                "location": {
                    "region": props.get("areaDesc", ""),
                    "country": "USA"
                },
                "starts_at": props.get("effective", ""),
                "ends_at": props.get("ends", ""),
                "description": props.get("description", ""),
                "raw_data": props
            }
            events.append(event)
            
        return events
    
    def _map_noaa_severity(self, noaa_severity: str) -> str:
        """Map NOAA severity to our system"""
        mapping = {
            "Extreme": "CRITICAL",
            "Severe": "HIGH",
            "Moderate": "MEDIUM",
            "Minor": "LOW"
        }
        return mapping.get(noaa_severity, "MEDIUM")
    
    async def match_events_to_suppliers(
        self, 
        events: List[Dict], 
        db: Session
    ) -> List[Dict]:
        """
        Match detected events to affected suppliers based on location
        
        Returns list of matched events with affected suppliers
        """
        matched_events = []
        
        # Get all suppliers with locations
        suppliers = db.query(Supplier).filter(
            Supplier.latitude.isnot(None),
            Supplier.longitude.isnot(None)
        ).all()
        
        for event in events:
            event_location = event.get("location")
            if not event_location:
                continue
                
            affected_suppliers = []
            
            for supplier in suppliers:
                # Check if supplier is in affected region
                if self._is_supplier_affected(supplier, event_location, event.get("event_type")):
                    affected_suppliers.append({
                        "supplier_id": supplier.id,
                        "supplier_name": supplier.name,
                        "distance_km": self._calculate_distance(
                            supplier.latitude, supplier.longitude,
                            event_location.get("lat", 0), event_location.get("lon", 0)
                        ),
                        "criticality": supplier.criticality
                    })
            
            if affected_suppliers:
                event["affected_suppliers"] = affected_suppliers
                event["affected_count"] = len(affected_suppliers)
                matched_events.append(event)
        
        return matched_events
    
    def _is_supplier_affected(
        self, 
        supplier: Supplier, 
        event_location: Dict, 
        event_type: str
    ) -> bool:
        """Determine if a supplier is affected by an event"""
        
        # Country-level match
        if event_location.get("country") and supplier.country:
            if event_location["country"].upper() in supplier.country.upper():
                return True
        
        # Distance-based match (if coordinates available)
        if event_location.get("lat") and event_location.get("lon"):
            distance = self._calculate_distance(
                supplier.latitude, supplier.longitude,
                event_location["lat"], event_location["lon"]
            )
            
            # Different event types have different impact radius
            impact_radius = {
                "NATURAL_DISASTER": 500,  # 500km
                "WEATHER_EVENT": 300,
                "LABOR_DISPUTE": 50,
                "INDUSTRIAL_ACCIDENT": 100,
                "LOGISTICS_DISRUPTION": 200
            }
            
            radius = impact_radius.get(event_type, 100)
            if distance <= radius:
                return True
        
        return False
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Earth's radius in km
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c


class AlertDetector:
    """Detect and trigger alerts based on live feed events"""
    
    def __init__(self, db: Session):
        self.db = db
        self.feed_service = LiveFeedService()
    
    async def scan_for_alerts(self) -> List[Dict]:
        """
        Main alert detection flow:
        1. Fetch events from all sources
        2. Match to suppliers
        3. Calculate risk scores
        4. Generate alerts
        """
        logger.info("🔍 Starting alert scan...")
        
        all_events = []
        
        # 1. Fetch from all sources
        gdelt_events = await self.feed_service.fetch_gdelt_events()
        all_events.extend(gdelt_events)
        
        # Weather alerts for supplier countries
        supplier_countries = self._get_supplier_regions()
        weather_events = await self.feed_service.fetch_weather_alerts(supplier_countries)
        all_events.extend(weather_events)
        
        logger.info(f"📰 Found {len(all_events)} events")
        
        # 2. Match events to suppliers
        matched_events = await self.feed_service.match_events_to_suppliers(
            all_events, 
            self.db
        )
        
        logger.info(f"⚠️ {len(matched_events)} events affect suppliers")
        
        # 3. Generate alerts for critical events
        alerts = []
        for event in matched_events:
            if self._should_trigger_alert(event):
                alert = await self._create_alert(event)
                alerts.append(alert)
        
        logger.info(f"🚨 Generated {len(alerts)} alerts")
        
        return alerts
    
    def _get_supplier_regions(self) -> List[str]:
        """Get unique regions where suppliers are located"""
        suppliers = self.db.query(Supplier).all()
        
        # For NOAA, use US state codes
        # For other countries, you'd need different weather APIs
        us_states = set()
        for supplier in suppliers:
            if supplier.country == "United States":
                # Extract state from city (simplified)
                if supplier.city:
                    # Map cities to state codes (you'd expand this)
                    state_mapping = {
                        "Los Angeles": "CA",
                        "Portland": "OR",
                        "Atlanta": "GA"
                    }
                    state = state_mapping.get(supplier.city)
                    if state:
                        us_states.add(state)
        
        return list(us_states)
    
    def _should_trigger_alert(self, event: Dict) -> bool:
        """Determine if event warrants an alert"""
        
        # Alert criteria:
        # 1. Severity is HIGH or CRITICAL
        if event.get("severity") in ["HIGH", "CRITICAL"]:
            return True
        
        # 2. Affects critical suppliers
        critical_suppliers = [
            s for s in event.get("affected_suppliers", [])
            if s.get("criticality") == "CRITICAL"
        ]
        if len(critical_suppliers) > 0:
            return True
        
        # 3. Affects multiple suppliers
        if event.get("affected_count", 0) >= 3:
            return True
        
        return False
    
    async def _create_alert(self, event: Dict) -> Dict:
        """Create structured alert from event"""
        
        # Calculate impact score
        impact_score = self._calculate_impact_score(event)
        
        alert = {
            "alert_id": f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "severity": event.get("severity"),
            "event_type": event.get("event_type"),
            "title": event.get("title"),
            "description": event.get("description", ""),
            "source": event.get("source"),
            "location": event.get("location"),
            "impact_score": impact_score,
            "affected_suppliers": event.get("affected_suppliers", []),
            "affected_count": event.get("affected_count", 0),
            "recommended_actions": self._generate_recommended_actions(event),
            "source_url": event.get("url"),
            "raw_event": event
        }
        
        # Store alert in database
        self._store_alert(alert)
        
        return alert
    
    def _calculate_impact_score(self, event: Dict) -> float:
        """Calculate 0-100 impact score based on event characteristics"""
        
        score = 0.0
        
        # Severity weight (0-40 points)
        severity_scores = {
            "CRITICAL": 40,
            "HIGH": 30,
            "MEDIUM": 20,
            "LOW": 10
        }
        score += severity_scores.get(event.get("severity", "MEDIUM"), 20)
        
        # Number of affected suppliers (0-30 points)
        affected_count = event.get("affected_count", 0)
        score += min(affected_count * 5, 30)
        
        # Criticality of suppliers (0-30 points)
        critical_count = sum(
            1 for s in event.get("affected_suppliers", [])
            if s.get("criticality") == "CRITICAL"
        )
        score += min(critical_count * 10, 30)
        
        return min(score, 100)
    
    def _generate_recommended_actions(self, event: Dict) -> List[str]:
        """Generate immediate action recommendations"""
        
        actions = []
        event_type = event.get("event_type")
        severity = event.get("severity")
        
        # Generic actions
        actions.append("Review affected supplier contracts and SLAs")
        actions.append("Contact affected suppliers for status updates")
        
        # Event-specific actions
        if event_type == "NATURAL_DISASTER":
            actions.append("Activate disaster recovery protocols")
            actions.append("Assess alternative supplier capacity")
            actions.append("Review insurance coverage for affected regions")
        
        elif event_type == "LABOR_DISPUTE":
            actions.append("Identify backup suppliers in different regions")
            actions.append("Negotiate expedited shipping if needed")
        
        elif event_type == "WEATHER_EVENT":
            actions.append("Monitor weather forecasts for duration")
            actions.append("Adjust inventory levels as precaution")
        
        elif event_type == "LOGISTICS_DISRUPTION":
            actions.append("Explore alternative shipping routes")
            actions.append("Consider air freight for critical components")
        
        # Severity-based actions
        if severity in ["HIGH", "CRITICAL"]:
            actions.append("Escalate to executive team immediately")
            actions.append("Initiate emergency supplier sourcing")
        
        return actions
    
    def _store_alert(self, alert: Dict):
        """Store alert in database"""
        try:
            live_feed = LiveFeed(
                source=alert["source"],
                data_type="ALERT",
                payload=alert
            )
            self.db.add(live_feed)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to store alert: {str(e)}")
            self.db.rollback()
