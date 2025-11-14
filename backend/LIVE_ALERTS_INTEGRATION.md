# 🚨 Live Alert Detection System - Integration Guide

## Overview

This document explains how real-time APIs are integrated into the Supply Chain Risk Monitor to provide automated alert detection.

## 📊 Architecture Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL DATA SOURCES                        │
├─────────────────────────────────────────────────────────────────┤
│  GDELT API    │  NewsAPI    │  NOAA Weather  │  Supply Hub     │
│  (Events)     │  (News)     │  (Alerts)      │  (Suppliers)    │
└──────┬──────────────┬──────────────┬───────────────┬────────────┘
       │              │              │               │
       ▼              ▼              ▼               ▼
┌─────────────────────────────────────────────────────────────────┐
│              LIVE FEED SERVICE (app/services/live_feeds.py)     │
├─────────────────────────────────────────────────────────────────┤
│  • fetch_gdelt_events()                                         │
│  • fetch_news_alerts()                                          │
│  • fetch_weather_alerts()                                       │
│  • match_events_to_suppliers()  ◄─── Uses Supplier Database    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              ALERT DETECTOR (app/services/live_feeds.py)        │
├─────────────────────────────────────────────────────────────────┤
│  1. Fetch events from all sources                               │
│  2. Match events to suppliers by location                       │
│  3. Calculate impact scores                                     │
│  4. Filter critical events                                      │
│  5. Generate structured alerts                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ALERT STORAGE (Database)                     │
├─────────────────────────────────────────────────────────────────┤
│  Table: live_feeds                                              │
│  • id, source, data_type, timestamp, payload, processed         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│          BACKGROUND SCHEDULER (app/services/scheduler.py)       │
├─────────────────────────────────────────────────────────────────┤
│  • Runs every 15 minutes (configurable)                         │
│  • Calls AlertDetector.scan_for_alerts()                        │
│  • Triggers notifications for critical alerts                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              API ENDPOINTS (app/routers/alerts.py)              │
├─────────────────────────────────────────────────────────────────┤
│  GET  /api/alerts/recent          - Get recent alerts           │
│  GET  /api/alerts/dashboard        - Dashboard summary          │
│  POST /api/alerts/scan             - Manual trigger             │
│  POST /api/alerts/scheduler/start  - Start background scanner   │
│  GET  /api/alerts/test/gdelt       - Test GDELT connection      │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Alert Detection Flow

### Step 1: Data Ingestion (Every 15 minutes)

```python
# Scheduler triggers AlertDetector.scan_for_alerts()

1. Fetch GDELT Events:
   - Query: "supply chain OR earthquake OR strike OR flood"
   - Time range: Last 24 hours
   - Returns: News articles with geolocation and tone

2. Fetch News Alerts:
   - Query: Topics related to supply chain disruptions
   - Sources: Reuters, Bloomberg, CNN, etc.
   - Returns: Recent news articles

3. Fetch Weather Alerts:
   - Regions: Where suppliers are located
   - Source: NOAA (for US), others for international
   - Returns: Active weather warnings
```

### Step 2: Event Classification

```python
# Each event is classified by type and severity

Event Types:
- NATURAL_DISASTER (earthquakes, tsunamis)
- WEATHER_EVENT (floods, hurricanes, storms)
- LABOR_DISPUTE (strikes, protests)
- INDUSTRIAL_ACCIDENT (fires, explosions)
- LOGISTICS_DISRUPTION (port closures, shipping delays)

Severity Levels (based on):
- News tone (GDELT tone score)
- Keywords ("major", "severe", "catastrophic")
- Number of affected suppliers
- Criticality of suppliers

Calculation:
if tone < -5 OR "catastrophic" in title:
    severity = CRITICAL
elif tone < -2:
    severity = HIGH
else:
    severity = MEDIUM
```

### Step 3: Supplier Matching

```python
# Match events to suppliers using geographic proximity

For each event:
    1. Extract location (country, lat/lon)
    2. Query all suppliers from database
    3. For each supplier:
        a. Check if country matches
        b. Calculate distance using Haversine formula
        c. Apply event-specific impact radius:
           - Earthquake: 500km
           - Weather: 300km
           - Port strike: 50km
           - Factory fire: 100km
    4. Mark supplier as "affected" if within radius

Returns: List of affected suppliers with distances
```

### Step 4: Impact Scoring

```python
# Calculate 0-100 impact score for each event

score = 0

# Severity component (0-40 points)
if severity == CRITICAL: score += 40
if severity == HIGH: score += 30
if severity == MEDIUM: score += 20

# Supplier count (0-30 points)
score += min(affected_supplier_count * 5, 30)

# Criticality (0-30 points)
critical_supplier_count = count where criticality == "CRITICAL"
score += min(critical_supplier_count * 10, 30)

total_impact_score = min(score, 100)
```

### Step 5: Alert Filtering

```python
# Determine which events warrant alerts

Should trigger alert if:
1. Severity is HIGH or CRITICAL
   OR
2. Affects any CRITICAL suppliers
   OR
3. Affects 3+ suppliers

If alert triggered:
    - Generate recommended actions
    - Store in database
    - Notify stakeholders
```

### Step 6: Recommended Actions

```python
# Generate context-specific action items

For NATURAL_DISASTER:
- "Activate disaster recovery protocols"
- "Assess alternative supplier capacity"
- "Review insurance coverage"

For LABOR_DISPUTE:
- "Identify backup suppliers in different regions"
- "Negotiate expedited shipping if needed"

For HIGH/CRITICAL severity:
- "Escalate to executive team immediately"
- "Initiate emergency supplier sourcing"

Returns: List of 5-8 actionable recommendations
```

## 📡 API Integration Examples

### Example 1: GDELT Event Detection

**API Call:**
```bash
GET https://api.gdeltproject.org/api/v2/doc/doc?query=earthquake%20taiwan&mode=artlist&format=json&maxrecords=10&timespan=24h
```

**Response Processing:**
```python
{
  "articles": [
    {
      "title": "7.2 Magnitude Earthquake Strikes Taiwan",
      "url": "https://news.com/taiwan-quake",
      "seendate": "20251109T103000Z",
      "tone": -8.5,  # Very negative
      "locations": [{
        "country": "Taiwan",
        "name": "Hsinchu",
        "lat": 24.8138,
        "lon": 120.9675
      }]
    }
  ]
}

# Our system extracts:
event = {
    "source": "GDELT",
    "title": "7.2 Magnitude Earthquake Strikes Taiwan",
    "event_type": "NATURAL_DISASTER",  # from keywords
    "severity": "CRITICAL",  # from tone < -5
    "location": {"country": "Taiwan", "lat": 24.8138, "lon": 120.9675}
}

# Then matches to suppliers:
affected_suppliers = [
    {"id": 18, "name": "Semiconductor Fab Taiwan", "distance_km": 12, "criticality": "CRITICAL"},
    {"id": 20, "name": "PCB Manufacturing Taiwan", "distance_km": 45, "criticality": "CRITICAL"}
]

# Generates alert:
alert = {
    "alert_id": "ALERT-20251109103045",
    "severity": "CRITICAL",
    "title": "7.2 Magnitude Earthquake Strikes Taiwan",
    "impact_score": 90,  # High score due to critical suppliers
    "affected_count": 2,
    "recommended_actions": [
        "Contact Semiconductor Fab Taiwan for damage assessment",
        "Activate disaster recovery protocols",
        "Assess production timeline impact",
        "Identify backup semiconductor suppliers",
        "Escalate to executive team immediately"
    ]
}
```

### Example 2: Weather Alert Detection

**API Call:**
```bash
GET https://api.weather.gov/alerts/active?area=CA
```

**Response Processing:**
```python
{
  "features": [{
    "properties": {
      "event": "Severe Thunderstorm Warning",
      "severity": "Severe",
      "areaDesc": "Los Angeles County",
      "effective": "2025-11-09T10:00:00-08:00",
      "ends": "2025-11-09T16:00:00-08:00",
      "description": "Heavy rainfall may cause flash flooding..."
    }
  }]
}

# Our system processes:
event = {
    "source": "NOAA",
    "event_type": "WEATHER_EVENT",
    "severity": "HIGH",  # from NOAA severity mapping
    "location": {"region": "Los Angeles County", "country": "USA"}
}

# Matches suppliers in LA area:
affected_suppliers = [
    {"id": 17, "name": "Shipping Logistics USA", "city": "Los Angeles"}
]

# Alert generated with weather-specific actions
```

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install httpx apscheduler
```

### 2. Add API Keys (Optional)

Edit `backend/.env`:
```bash
# For NewsAPI (optional, free tier available)
NEWS_API_KEY=your_newsapi_key_here

# GDELT and NOAA are free, no key needed
```

### 3. Update Database Schema

```bash
# Run migrations to add live_feeds table
python seed_data.py  # This will create the new table
```

### 4. Register Alert Router

Edit `backend/app/main.py`:
```python
from app.routers import alerts

app.include_router(alerts.router)
```

### 5. Start Background Scheduler

Add to `backend/app/main.py`:
```python
from app.services.scheduler import feed_scheduler

@app.on_event("startup")
async def startup_event():
    feed_scheduler.start()
    logger.info("✅ Alert monitoring started")

@app.on_event("shutdown")
async def shutdown_event():
    feed_scheduler.stop()
    logger.info("🛑 Alert monitoring stopped")
```

## 🎮 Usage Examples

### API Testing

```bash
# Test GDELT connection
curl http://localhost:8000/api/alerts/test/gdelt

# Test weather API
curl http://localhost:8000/api/alerts/test/weather

# Manual alert scan
curl -X POST http://localhost:8000/api/alerts/scan

# Get recent alerts
curl http://localhost:8000/api/alerts/recent?hours=24&severity=CRITICAL

# Dashboard summary
curl http://localhost:8000/api/alerts/dashboard

# Start/stop scheduler
curl -X POST http://localhost:8000/api/alerts/scheduler/start
curl -X POST http://localhost:8000/api/alerts/scheduler/stop
```

### Frontend Integration

```javascript
// In your React app
const AlertDashboard = () => {
  const [alerts, setAlerts] = useState([]);
  
  useEffect(() => {
    // Fetch alerts every 5 minutes
    const fetchAlerts = async () => {
      const response = await fetch('http://localhost:8000/api/alerts/recent?hours=24');
      const data = await response.json();
      setAlerts(data.alerts);
    };
    
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div>
      {alerts.map(alert => (
        <AlertCard 
          key={alert.alert_id}
          title={alert.title}
          severity={alert.severity}
          affectedSuppliers={alert.affected_suppliers}
          actions={alert.recommended_actions}
        />
      ))}
    </div>
  );
};
```

## 📈 Benefits of This Integration

1. **Proactive Risk Detection**
   - Catches disruptions within 15 minutes of global news
   - No manual monitoring required

2. **Automated Supplier Matching**
   - Instantly knows which suppliers are affected
   - Calculates impact radius automatically

3. **Intelligent Prioritization**
   - Only alerts on high-impact events
   - Filters out noise

4. **Actionable Recommendations**
   - Context-specific action items
   - Ready-to-execute playbooks

5. **Historical Tracking**
   - All events stored in database
   - Trend analysis and reporting

## 🔮 Future Enhancements

1. **Machine Learning**
   - Train model on historical events
   - Predict likelihood of supplier impact

2. **More Data Sources**
   - MarineTraffic for shipping delays
   - ThomasNet for supplier discovery
   - Social media sentiment analysis

3. **Real-time Notifications**
   - Email/Slack/SMS alerts
   - Webhook integration
   - Mobile push notifications

4. **Supplier Communication**
   - Automated supplier check-ins
   - Impact confirmation workflow
   - Recovery timeline tracking
