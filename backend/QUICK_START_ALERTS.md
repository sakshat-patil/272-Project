# 🚀 Quick Start: Activating Live Alerts

## ✅ What I've Created

I've added a complete live alert detection system to your project:

### New Files Created:
1. **`app/services/live_feeds.py`** - Core alert detection logic
2. **`app/services/scheduler.py`** - Background task scheduler
3. **`app/routers/alerts.py`** - API endpoints for alerts
4. **`LIVE_ALERTS_INTEGRATION.md`** - Full documentation

### Modified Files:
1. **`app/models.py`** - Added `LiveFeed` database model

## 🔧 To Activate (3 Steps)

### Step 1: Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install httpx apscheduler
```

### Step 2: Update main.py

Add these imports and code to `backend/app/main.py`:

```python
# Add at top of file
from app.routers import alerts
from app.services.scheduler import feed_scheduler

# Add after other router includes
app.include_router(alerts.router)

# Add these startup/shutdown handlers
@app.on_event("startup")
async def startup_event():
    """Start background services"""
    feed_scheduler.start()
    logger.info("✅ Alert monitoring started - checking every 15 minutes")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    feed_scheduler.stop()
    logger.info("🛑 Alert monitoring stopped")
```

### Step 3: Run Migration

```bash
# This creates the live_feeds table
python seed_data.py
```

## 🧪 Test It

```bash
# Test GDELT connection (free, no API key needed)
curl http://localhost:8000/api/alerts/test/gdelt

# Test weather API (free, no API key needed)
curl http://localhost:8000/api/alerts/test/weather

# Manually trigger alert scan
curl -X POST http://localhost:8000/api/alerts/scan

# View alert dashboard
curl http://localhost:8000/api/alerts/dashboard
```

## 📊 How It Works

**Automated Flow (every 15 minutes):**
1. 🔍 Scans GDELT for global events
2. 🌦️ Checks NOAA for weather alerts
3. 📍 Matches events to your suppliers by location
4. 💯 Calculates impact scores
5. 🚨 Creates alerts for critical events
6. 💾 Stores in database

**Manual Trigger:**
- You can also trigger scans on-demand via the API
- Great for testing or immediate checks

## 🎯 What You Get

### Real-Time Detection:
- Earthquakes affecting supplier regions
- Weather events (floods, hurricanes)
- Labor strikes at ports/factories
- Industrial accidents
- Logistics disruptions

### Smart Matching:
- Automatically finds which suppliers are affected
- Uses distance calculations (Haversine formula)
- Considers event type (earthquake = 500km radius)

### Impact Scoring:
- 0-100 risk score based on:
  - Event severity
  - Number of suppliers affected
  - Criticality of affected suppliers

### Action Recommendations:
- Context-specific actions
- e.g., "Contact Semiconductor Fab Taiwan for damage assessment"
- e.g., "Activate disaster recovery protocols"

## 📱 Frontend Integration Example

```javascript
// Add to your React dashboard
const LiveAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  
  useEffect(() => {
    const fetchAlerts = async () => {
      const res = await fetch('/api/alerts/recent?hours=24');
      const data = await res.json();
      setAlerts(data.alerts);
    };
    fetchAlerts();
    setInterval(fetchAlerts, 5 * 60 * 1000); // Refresh every 5 min
  }, []);
  
  return (
    <div className="alerts-feed">
      {alerts.map(alert => (
        <div key={alert.alert_id} 
             className={`alert alert-${alert.severity.toLowerCase()}`}>
          <h3>🚨 {alert.title}</h3>
          <p>{alert.description}</p>
          <p>Affected suppliers: {alert.affected_count}</p>
          <p>Impact score: {alert.impact_score}/100</p>
        </div>
      ))}
    </div>
  );
};
```

## 🔑 Optional: Add NewsAPI

For more comprehensive news coverage:

1. Get free API key from https://newsapi.org
2. Add to `.env`: `NEWS_API_KEY=your_key_here`
3. Update `live_feeds.py` to use it

## ⚡ API Endpoints Available

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/alerts/scan` | POST | Manual scan trigger |
| `/api/alerts/recent` | GET | Get recent alerts |
| `/api/alerts/dashboard` | GET | Dashboard summary |
| `/api/alerts/events` | GET | Raw events (before filtering) |
| `/api/alerts/scheduler/start` | POST | Start background scanner |
| `/api/alerts/scheduler/stop` | POST | Stop background scanner |
| `/api/alerts/test/gdelt` | GET | Test GDELT API |
| `/api/alerts/test/weather` | GET | Test NOAA API |

## 🎓 Example Alert JSON

```json
{
  "alert_id": "ALERT-20251109144523",
  "timestamp": "2025-11-09T14:45:23",
  "severity": "CRITICAL",
  "event_type": "NATURAL_DISASTER",
  "title": "7.2 Magnitude Earthquake Strikes Taiwan",
  "impact_score": 90,
  "affected_suppliers": [
    {
      "supplier_id": 18,
      "supplier_name": "Semiconductor Fab Taiwan",
      "distance_km": 12,
      "criticality": "CRITICAL"
    }
  ],
  "affected_count": 2,
  "recommended_actions": [
    "Contact Semiconductor Fab Taiwan for damage assessment",
    "Activate disaster recovery protocols",
    "Assess production timeline impact",
    "Identify backup semiconductor suppliers",
    "Escalate to executive team immediately"
  ],
  "source_url": "https://www.reuters.com/article/taiwan-earthquake"
}
```

## 🎨 Demo Scenarios

### Scenario 1: Port Strike
```
Event: "Port of Los Angeles workers strike"
↓
Matches: Shipping Logistics USA (distance: 5km)
↓
Alert: HIGH severity, impact_score: 65
Actions: "Explore alternative shipping routes", "Consider air freight"
```

### Scenario 2: Earthquake
```
Event: "7.2 earthquake in Taiwan"
↓
Matches: Semiconductor Fab Taiwan, PCB Manufacturing Taiwan
↓
Alert: CRITICAL severity, impact_score: 90
Actions: "Activate disaster recovery", "Contact suppliers immediately"
```

### Scenario 3: Weather
```
Event: "Hurricane approaching Florida"
↓
Matches: Any suppliers in FL region
↓
Alert: HIGH severity, impact_score: 70
Actions: "Monitor weather forecasts", "Adjust inventory levels"
```

## 📈 Next Steps

After basic setup works:

1. **Add Frontend Dashboard**
   - Create AlertsFeed component
   - Add to main dashboard
   - Show real-time alerts

2. **Enable Notifications**
   - Email alerts for CRITICAL events
   - Slack/Teams webhooks
   - SMS for executives

3. **Enhance Matching**
   - More sophisticated geolocation
   - Supplier dependency chains
   - Industry-specific rules

4. **Add More Sources**
   - MarineTraffic for shipping
   - Twitter/X for real-time updates
   - Industry-specific feeds

## ❓ FAQ

**Q: Will this cost money?**
A: GDELT and NOAA are 100% free. NewsAPI has free tier (100 requests/day).

**Q: How much data will it use?**
A: ~5-10MB per scan, ~1GB/month with 15-min intervals.

**Q: Can I adjust the scan frequency?**
A: Yes, edit `scheduler.py` line 23: change `minutes=15` to desired interval.

**Q: What if I don't want certain event types?**
A: Add filters in `AlertDetector._should_trigger_alert()` method.

**Q: Can I test without waiting 15 minutes?**
A: Yes! Use `POST /api/alerts/scan` to trigger immediately.

## 🐛 Troubleshooting

**Error: "Import httpx could not be resolved"**
```bash
pip install httpx apscheduler
```

**Error: "Table live_feeds doesn't exist"**
```bash
python seed_data.py  # Recreates all tables
```

**No alerts showing up**
- Check logs for API errors
- Run test endpoints first
- Verify suppliers have lat/lon coordinates

**Scheduler not starting**
- Check for errors in logs
- Verify startup event is called
- Manually start: `POST /api/alerts/scheduler/start`
