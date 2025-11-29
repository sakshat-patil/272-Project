from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import httpx
import math

router = APIRouter()


class SupplierLocation(BaseModel):
    name: str
    city: str
    country: str
    latitude: float
    longitude: float


class HistoricalMonitoringRequest(BaseModel):
    suppliers: List[SupplierLocation]


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Haversine distance between two points in kilometers."""
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


async def fetch_historical_weather(latitude: float, longitude: float) -> dict:
    """Fetch historical weather data from Open-Meteo API."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "auto"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Calculate summary statistics
            daily = data.get("daily", {})
            temps_max = daily.get("temperature_2m_max", [])
            temps_min = daily.get("temperature_2m_min", [])
            precip = daily.get("precipitation_sum", [])
            wind = daily.get("windspeed_10m_max", [])
            
            # Filter out None values
            temps_max = [t for t in temps_max if t is not None]
            temps_min = [t for t in temps_min if t is not None]
            precip = [p for p in precip if p is not None]
            wind = [w for w in wind if w is not None]
            
            return {
                "avg_temp_max": round(sum(temps_max) / len(temps_max), 1) if temps_max else None,
                "avg_temp_min": round(sum(temps_min) / len(temps_min), 1) if temps_min else None,
                "total_precipitation": round(sum(precip), 1) if precip else 0,
                "precipitation_days": len([p for p in precip if p > 0.1]),
                "max_wind_speed": round(max(wind), 1) if wind else None,
                "extreme_temp_high": round(max(temps_max), 1) if temps_max else None,
                "extreme_temp_low": round(min(temps_min), 1) if temps_min else None,
                "period_days": 30
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {
            "error": "Failed to fetch weather data",
            "avg_temp_max": None,
            "avg_temp_min": None,
            "total_precipitation": 0,
            "precipitation_days": 0,
            "max_wind_speed": None,
            "extreme_temp_high": None,
            "extreme_temp_low": None,
            "period_days": 30
        }


def get_nearby_sample_events(latitude: float, longitude: float, radius_km: float = 200) -> List[dict]:
    """Get sample historical events near the supplier location."""
    # Sample events database (in production, this would query the Event table)
    sample_events = [
        {
            "title": "Typhoon Mangkhut",
            "description": "Category 5 super typhoon caused widespread disruption across southern China and Hong Kong",
            "latitude": 22.3964,
            "longitude": 114.1095,
            "date": "2018-09-16",
            "severity": "High"
        },
        {
            "title": "Taiwan Earthquake",
            "description": "6.4 magnitude earthquake disrupted semiconductor manufacturing in Taiwan",
            "latitude": 24.1393,
            "longitude": 120.6861,
            "date": "2022-09-18",
            "severity": "High"
        },
        {
            "title": "Shenzhen Port Congestion",
            "description": "COVID-19 restrictions caused severe port congestion and delays",
            "latitude": 22.5431,
            "longitude": 114.0579,
            "date": "2022-03-14",
            "severity": "Medium"
        },
        {
            "title": "Singapore Haze",
            "description": "Severe air pollution from Indonesian forest fires affected operations",
            "latitude": 1.3521,
            "longitude": 103.8198,
            "date": "2019-09-10",
            "severity": "Medium"
        },
        {
            "title": "South Korea Floods",
            "description": "Heavy monsoon rains caused flooding in Seoul and surrounding areas",
            "latitude": 37.5665,
            "longitude": 126.978,
            "date": "2020-08-09",
            "severity": "Medium"
        }
    ]
    
    nearby_events = []
    for event in sample_events:
        distance = calculate_distance(latitude, longitude, event["latitude"], event["longitude"])
        if distance <= radius_km:
            nearby_events.append({
                **event,
                "distance_km": round(distance, 1)
            })
    
    return sorted(nearby_events, key=lambda x: x["distance_km"])


@router.post("/api/monitoring/historical")
async def get_historical_monitoring(request: HistoricalMonitoringRequest):
    """
    Get historical monitoring data (weather patterns and events) for supplier locations.
    """
    results = []
    
    for supplier in request.suppliers:
        # Fetch historical weather
        weather_data = await fetch_historical_weather(supplier.latitude, supplier.longitude)
        
        # Get nearby historical events
        nearby_events = get_nearby_sample_events(supplier.latitude, supplier.longitude, radius_km=200)
        
        results.append({
            "supplier": {
                "name": supplier.name,
                "city": supplier.city,
                "country": supplier.country,
                "latitude": supplier.latitude,
                "longitude": supplier.longitude
            },
            "weather_summary": weather_data,
            "nearby_events": nearby_events,
            "risk_indicators": {
                "extreme_weather_risk": "High" if weather_data.get("max_wind_speed", 0) > 60 else "Low",
                "precipitation_risk": "High" if weather_data.get("precipitation_days", 0) > 15 else "Low",
                "historical_disruptions": len(nearby_events)
            }
        })
    
    return {
        "success": True,
        "supplier_count": len(results),
        "monitoring_data": results
    }
