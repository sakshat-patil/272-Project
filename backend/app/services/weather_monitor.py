"""
Real-time weather monitoring service using WeatherAPI.com
Fetches live weather data for supplier locations and detects severe weather events
"""
import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models import Supplier


class WeatherMonitor:
    """Monitor real-time weather conditions for suppliers using WeatherAPI.com"""
    
    # WeatherAPI.com (1M calls/month free)
    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    API_KEY = os.getenv("WEATHERAPI_KEY", "")  # Get from .env
    
    # Weather alert thresholds
    THRESHOLDS = {
        "extreme_heat": 35,  # Celsius
        "extreme_cold": -10,  # Celsius
        "heavy_rain": 50,  # mm per hour
        "strong_wind": 70,  # km/h
        "severe_wind": 100,  # km/h
    }
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_weather_for_supplier(self, supplier: Supplier) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather for a single supplier location
        
        Args:
            supplier: Supplier object with latitude/longitude
            
        Returns:
            Dictionary with weather data or None if failed
        """
        if not supplier.latitude or not supplier.longitude:
            return None
        
        if not self.API_KEY:
            print("⚠️  WEATHERAPI_KEY not set - weather monitoring disabled")
            return None
        
        try:
            params = {
                "key": self.API_KEY,
                "q": f"{supplier.latitude},{supplier.longitude}",
                "aqi": "no"
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            location = data.get("location", {})
            condition = current.get("condition", {})
            
            weather_data = {
                "supplier_id": supplier.id,
                "supplier_name": supplier.name,
                "location": f"{supplier.city}, {supplier.country}",
                "latitude": supplier.latitude,
                "longitude": supplier.longitude,
                "temperature": current.get("temp_c"),
                "feels_like": current.get("feelslike_c"),
                "precipitation": current.get("precip_mm", 0),
                "humidity": current.get("humidity", 0),
                "wind_speed": current.get("wind_kph", 0),
                "wind_gusts": current.get("gust_kph", 0),
                "wind_direction": current.get("wind_dir", ""),
                "pressure": current.get("pressure_mb", 0),
                "visibility": current.get("vis_km", 0),
                "uv_index": current.get("uv", 0),
                "condition": condition.get("text", ""),
                "condition_code": condition.get("code", 0),
                "is_day": current.get("is_day", 1),
                "timestamp": current.get("last_updated"),
                "alerts": self._detect_weather_alerts(current, supplier)
            }
            
            return weather_data
            
        except Exception as e:
            print(f"Error fetching weather for {supplier.name}: {str(e)}")
            return None
    
    def get_weather_for_suppliers(self, suppliers: List[Supplier]) -> List[Dict[str, Any]]:
        """
        Fetch weather for multiple suppliers
        
        Args:
            suppliers: List of Supplier objects
            
        Returns:
            List of weather data dictionaries
        """
        weather_data = []
        
        for supplier in suppliers:
            if supplier.latitude and supplier.longitude:
                data = self.get_weather_for_supplier(supplier)
                if data:
                    weather_data.append(data)
        
        return weather_data
    
    def _detect_weather_alerts(self, weather: Dict, supplier: Supplier) -> List[Dict[str, Any]]:
        """
        Detect severe weather conditions that could affect operations
        
        Args:
            weather: Current weather data from WeatherAPI
            supplier: Supplier object
            
        Returns:
            List of alert dictionaries
        """
        alerts = []
        temp = weather.get("temp_c", 0)
        precip = weather.get("precip_mm", 0)
        wind_speed = weather.get("wind_kph", 0)
        wind_gusts = weather.get("gust_kph", 0)
        condition_code = weather.get("condition", {}).get("code", 0)
        
        # Temperature alerts
        if temp >= self.THRESHOLDS["extreme_heat"]:
            alerts.append({
                "type": "extreme_heat",
                "severity": 4 if temp >= 40 else 3,
                "message": f"Extreme heat warning: {temp}°C",
                "description": f"High temperatures affecting operations at {supplier.city}",
                "impact": "Potential equipment failure, worker safety concerns, production delays"
            })
        
        if temp <= self.THRESHOLDS["extreme_cold"]:
            alerts.append({
                "type": "extreme_cold",
                "severity": 4 if temp <= -20 else 3,
                "message": f"Extreme cold warning: {temp}°C",
                "description": f"Freezing conditions affecting operations at {supplier.city}",
                "impact": "Equipment freezing, transportation delays, production issues"
            })
        
        # Precipitation alerts
        if precip >= self.THRESHOLDS["heavy_rain"]:
            alerts.append({
                "type": "heavy_rain",
                "severity": 4 if precip >= 100 else 3,
                "message": f"Heavy rainfall: {precip}mm",
                "description": f"Severe rainfall affecting {supplier.city}",
                "impact": "Flooding risk, transportation disruption, facility damage"
            })
        
        # Wind alerts
        if wind_gusts >= self.THRESHOLDS["severe_wind"]:
            alerts.append({
                "type": "severe_wind",
                "severity": 5,
                "message": f"Severe wind gusts: {wind_gusts}km/h",
                "description": f"Dangerous wind conditions at {supplier.city}",
                "impact": "Facility damage, transportation halted, safety shutdown required"
            })
        elif wind_speed >= self.THRESHOLDS["strong_wind"]:
            alerts.append({
                "type": "strong_wind",
                "severity": 3,
                "message": f"Strong winds: {wind_speed}km/h",
                "description": f"High wind conditions at {supplier.city}",
                "impact": "Transportation delays, outdoor operations affected"
            })
        
        # WeatherAPI condition codes
        # 1000s: Thunderstorms, severe weather
        if condition_code in [1087, 1273, 1276, 1279, 1282]:  # Thunderstorms
            alerts.append({
                "type": "thunderstorm",
                "severity": 4,
                "message": "Thunderstorm detected",
                "description": f"Severe thunderstorm activity near {supplier.city}",
                "impact": "Power outages, equipment damage, operations suspended"
            })
        # Heavy snow
        elif condition_code in [1225, 1258]:  # Heavy snow
            alerts.append({
                "type": "heavy_snow",
                "severity": 4,
                "message": "Heavy snow detected",
                "description": f"Heavy snowfall affecting {supplier.city}",
                "impact": "Transportation blocked, facility access limited, production delays"
            })
        # Moderate snow
        elif condition_code in [1210, 1213, 1216, 1219, 1222, 1255]:  # Snow
            alerts.append({
                "type": "snow",
                "severity": 3,
                "message": "Snowfall detected",
                "description": f"Snow conditions at {supplier.city}",
                "impact": "Transportation delays, reduced operations"
            })
        # Blizzard
        elif condition_code == 1117:
            alerts.append({
                "type": "blizzard",
                "severity": 5,
                "message": "Blizzard warning",
                "description": f"Severe blizzard conditions at {supplier.city}",
                "impact": "All operations halted, extreme danger, facility closure"
            })
        
        return alerts
    
    def generate_weather_event_description(self, alert: Dict, supplier: Supplier) -> str:
        """
        Generate natural language event description from weather alert
        
        Args:
            alert: Alert dictionary
            supplier: Supplier object
            
        Returns:
            Human-readable event description
        """
        templates = {
            "extreme_heat": f"Extreme heat wave affecting {supplier.city}, {supplier.country} with temperatures reaching critical levels",
            "extreme_cold": f"Severe cold snap impacting operations in {supplier.city}, {supplier.country} with freezing conditions",
            "heavy_rain": f"Heavy rainfall and flooding risk at {supplier.city}, {supplier.country} affecting logistics and operations",
            "severe_wind": f"Severe wind storm hitting {supplier.city}, {supplier.country} causing operational disruptions",
            "strong_wind": f"Strong winds affecting {supplier.city}, {supplier.country} with potential transportation delays",
            "thunderstorm": f"Severe thunderstorm activity near {supplier.city}, {supplier.country} threatening power and operations",
            "heavy_snow": f"Heavy snowfall disrupting operations and transportation in {supplier.city}, {supplier.country}",
            "snow": f"Snowfall affecting logistics and operations in {supplier.city}, {supplier.country}"
        }
        
        return templates.get(alert["type"], f"Severe weather affecting {supplier.city}, {supplier.country}")
    
    def get_weather_summary(self, suppliers: List[Supplier]) -> Dict[str, Any]:
        """
        Get weather summary for all suppliers including alert counts
        
        Args:
            suppliers: List of Supplier objects
            
        Returns:
            Summary dictionary with statistics
        """
        weather_data = self.get_weather_for_suppliers(suppliers)
        
        total_suppliers = len(suppliers)
        monitored_suppliers = len(weather_data)
        total_alerts = sum(len(w.get("alerts", [])) for w in weather_data)
        
        # Group by severity
        critical_alerts = []
        high_alerts = []
        moderate_alerts = []
        
        for weather in weather_data:
            for alert in weather.get("alerts", []):
                if alert["severity"] >= 5:
                    critical_alerts.append({**alert, "supplier": weather["supplier_name"], "location": weather["location"]})
                elif alert["severity"] >= 4:
                    high_alerts.append({**alert, "supplier": weather["supplier_name"], "location": weather["location"]})
                elif alert["severity"] >= 3:
                    moderate_alerts.append({**alert, "supplier": weather["supplier_name"], "location": weather["location"]})
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_suppliers": total_suppliers,
            "monitored_suppliers": monitored_suppliers,
            "total_alerts": total_alerts,
            "critical_alerts": critical_alerts,
            "high_alerts": high_alerts,
            "moderate_alerts": moderate_alerts,
            "weather_data": weather_data
        }
    
    @staticmethod
    def interpret_weather_code(code: int) -> str:
        """
        Interpret WeatherAPI condition code
        
        Args:
            code: WeatherAPI condition code
            
        Returns:
            Human-readable description
        """
        codes = {
            1000: "Clear/Sunny",
            1003: "Partly cloudy",
            1006: "Cloudy",
            1009: "Overcast",
            1030: "Mist",
            1063: "Patchy rain possible",
            1066: "Patchy snow possible",
            1069: "Patchy sleet possible",
            1072: "Patchy freezing drizzle possible",
            1087: "Thundery outbreaks possible",
            1114: "Blowing snow",
            1117: "Blizzard",
            1135: "Fog",
            1147: "Freezing fog",
            1150: "Patchy light drizzle",
            1153: "Light drizzle",
            1168: "Freezing drizzle",
            1171: "Heavy freezing drizzle",
            1180: "Patchy light rain",
            1183: "Light rain",
            1186: "Moderate rain at times",
            1189: "Moderate rain",
            1192: "Heavy rain at times",
            1195: "Heavy rain",
            1198: "Light freezing rain",
            1201: "Moderate or heavy freezing rain",
            1204: "Light sleet",
            1207: "Moderate or heavy sleet",
            1210: "Patchy light snow",
            1213: "Light snow",
            1216: "Patchy moderate snow",
            1219: "Moderate snow",
            1222: "Patchy heavy snow",
            1225: "Heavy snow",
            1237: "Ice pellets",
            1240: "Light rain shower",
            1243: "Moderate or heavy rain shower",
            1246: "Torrential rain shower",
            1249: "Light sleet showers",
            1252: "Moderate or heavy sleet showers",
            1255: "Light snow showers",
            1258: "Moderate or heavy snow showers",
            1261: "Light showers of ice pellets",
            1264: "Moderate or heavy showers of ice pellets",
            1273: "Patchy light rain with thunder",
            1276: "Moderate or heavy rain with thunder",
            1279: "Patchy light snow with thunder",
            1282: "Moderate or heavy snow with thunder"
        }
        return codes.get(code, f"Unknown weather condition (code: {code})")
