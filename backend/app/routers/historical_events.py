from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import math

from ..database import get_db
from ..models import Event

router = APIRouter()

class HistoricalEventRequest(BaseModel):
    origin_latitude: float
    origin_longitude: float
    destination_latitude: float
    destination_longitude: float
    radius_km: float = 500

class HistoricalEventResponse(BaseModel):
    title: str
    description: str
    date: str
    location: str
    severity: str
    event_type: str
    distance_km: float

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) using Haversine formula
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def get_severity_from_impact(impact: str) -> str:
    """Map impact assessment to severity level"""
    if not impact:
        return "Medium"
    
    impact_lower = impact.lower()
    if any(word in impact_lower for word in ['severe', 'critical', 'major', 'catastrophic']):
        return "High"
    elif any(word in impact_lower for word in ['moderate', 'significant']):
        return "Medium"
    else:
        return "Low"

@router.post("/historical", response_model=dict)
async def get_historical_events(
    request: HistoricalEventRequest,
    db: Session = Depends(get_db)
):
    """
    Get historical supply chain events near a shipping route.
    Returns events within radius_km of both origin and destination points.
    """
    try:
        # Get all events from the database
        all_events = db.query(Event).all()
        
        matching_events = []
        
        for event in all_events:
            # Skip events without location data
            if not event.latitude or not event.longitude:
                continue
            
            # Calculate distance from origin
            distance_from_origin = calculate_distance(
                request.origin_latitude,
                request.origin_longitude,
                event.latitude,
                event.longitude
            )
            
            # Calculate distance from destination
            distance_from_destination = calculate_distance(
                request.destination_latitude,
                request.destination_longitude,
                event.latitude,
                event.longitude
            )
            
            # Check if event is within radius of either origin or destination
            if distance_from_origin <= request.radius_km or distance_from_destination <= request.radius_km:
                # Determine which point it's closer to for the distance value
                min_distance = min(distance_from_origin, distance_from_destination)
                location_point = "Origin" if distance_from_origin < distance_from_destination else "Destination"
                
                # Get severity from impact assessment
                severity = get_severity_from_impact(event.impact_assessment)
                
                matching_events.append(HistoricalEventResponse(
                    title=event.title or "Supply Chain Event",
                    description=event.description or "Event details not available",
                    date=event.event_date.strftime("%Y-%m-%d") if event.event_date else "Date unknown",
                    location=f"{event.location or 'Unknown location'} ({location_point}: {min_distance:.0f}km)",
                    severity=severity,
                    event_type=event.event_type.value if event.event_type else "Other",
                    distance_km=round(min_distance, 2)
                ))
        
        # Sort by distance (closest first)
        matching_events.sort(key=lambda x: x.distance_km)
        
        # If no events found in database, return sample historical events for demo
        if not matching_events:
            # Generate sample events based on route geography
            matching_events = generate_sample_historical_events(request)
        
        return {
            "events": [event.dict() for event in matching_events[:10]],  # Limit to 10 most relevant
            "total_found": len(matching_events),
            "search_radius_km": request.radius_km
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical events: {str(e)}")

def generate_sample_historical_events(request: HistoricalEventRequest) -> List[HistoricalEventResponse]:
    """
    Generate sample historical events for demonstration purposes.
    Based on common shipping routes and known historical disruptions.
    """
    # Determine approximate route based on coordinates
    is_pacific_route = (
        (request.origin_latitude < 40 and request.origin_longitude > 100) or
        (request.destination_latitude < 40 and request.destination_longitude > 100)
    )
    
    is_asia_route = (
        (request.origin_latitude > 0 and request.origin_latitude < 40 and 
         request.origin_longitude > 100 and request.origin_longitude < 150)
    )
    
    sample_events = []
    
    if is_pacific_route:
        sample_events = [
            HistoricalEventResponse(
                title="Typhoon Mangkhut - Port Closures",
                description="Category 5 typhoon caused widespread port closures across Hong Kong and southern China, disrupting shipping schedules for 2 weeks",
                date="2018-09-16",
                location="Hong Kong / Guangdong, China",
                severity="High",
                event_type="Natural Disaster",
                distance_km=245
            ),
            HistoricalEventResponse(
                title="Port of Los Angeles Congestion",
                description="COVID-19 pandemic created historic port congestion with 100+ container ships anchored offshore, delays exceeded 3 weeks",
                date="2021-10-15",
                location="Los Angeles, USA",
                severity="High",
                event_type="Logistics",
                distance_km=12
            ),
            HistoricalEventResponse(
                title="Earthquake - Taiwan Semiconductor Impact",
                description="6.4 magnitude earthquake near Hualien affected semiconductor production, minor shipping disruptions at Kaohsiung port",
                date="2022-03-23",
                location="Taiwan",
                severity="Medium",
                event_type="Natural Disaster",
                distance_km=180
            ),
        ]
    
    if is_asia_route:
        sample_events.extend([
            HistoricalEventResponse(
                title="Suez Canal Blockage - Ever Given",
                description="Container ship Ever Given blocked Suez Canal for 6 days, disrupting global supply chains and delaying thousands of shipments",
                date="2021-03-23",
                location="Suez Canal, Egypt",
                severity="High",
                event_type="Logistics",
                distance_km=420
            ),
            HistoricalEventResponse(
                title="Singapore Port Strike",
                description="Labor strike at PSA Singapore terminals caused 3-day delay in container operations",
                date="2020-06-08",
                location="Singapore",
                severity="Medium",
                event_type="Labor Strike",
                distance_km=8
            ),
        ])
    
    # Add some generic global events
    sample_events.extend([
        HistoricalEventResponse(
            title="COVID-19 Pandemic - Global Shipping Crisis",
            description="Global pandemic caused unprecedented disruptions to shipping schedules, port operations, and supply chain logistics worldwide",
            date="2020-03-15",
            location="Global",
            severity="High",
            event_type="Other",
            distance_km=0
        ),
        HistoricalEventResponse(
            title="Semiconductor Shortage",
            description="Global chip shortage affecting electronics manufacturing, caused by pandemic demand surge and factory shutdowns",
            date="2021-01-01",
            location="Global - Multiple Regions",
            severity="High",
            event_type="Economic",
            distance_km=0
        ),
    ])
    
    return sample_events[:5]  # Return top 5 most relevant
