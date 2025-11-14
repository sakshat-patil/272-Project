"""
Alert Detection Flow Diagram

STEP 1: BACKGROUND SCHEDULER (Runs every 15 minutes)
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  APScheduler (app/services/scheduler.py)                            │
│  ⏰ Triggers: AlertDetector.scan_for_alerts() every 15 minutes      │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 2: FETCH EVENTS FROM EXTERNAL APIs
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  LiveFeedService.fetch_gdelt_events()                               │
│  ├─ API: https://api.gdeltproject.org/api/v2/doc/doc                │
│  ├─ Query: "supply chain OR earthquake OR strike OR flood"          │
│  ├─ Returns: News articles with location, tone, keywords            │
│  └─ Example:                                                         │
│      {                                                               │
│        "title": "7.2 Earthquake Strikes Taiwan",                    │
│        "tone": -8.5,  ← Negative = bad news                         │
│        "location": {"country": "Taiwan", "lat": 24.8, "lon": 120.9} │
│      }                                                               │
├─────────────────────────────────────────────────────────────────────┤
│  LiveFeedService.fetch_weather_alerts()                             │
│  ├─ API: https://api.weather.gov/alerts/active?area=CA              │
│  ├─ Regions: Where your suppliers are located                       │
│  └─ Example:                                                         │
│      {                                                               │
│        "event": "Severe Thunderstorm Warning",                      │
│        "severity": "Severe",                                         │
│        "areaDesc": "Los Angeles County"                             │
│      }                                                               │
├─────────────────────────────────────────────────────────────────────┤
│  LiveFeedService.fetch_news_alerts() [Optional]                     │
│  ├─ API: https://newsapi.org/v2/everything                          │
│  ├─ Requires: NEWS_API_KEY (free tier available)                    │
│  └─ Returns: Curated news about supply chain disruptions            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 3: PARSE & CLASSIFY EVENTS
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  For each raw event:                                                │
│                                                                      │
│  A. Extract Location                                                │
│     ├─ Country (e.g., "Taiwan")                                     │
│     ├─ Region (e.g., "Hsinchu")                                     │
│     └─ Coordinates (lat: 24.8, lon: 120.9)                          │
│                                                                      │
│  B. Classify Event Type (keyword-based)                             │
│     ├─ "earthquake" → NATURAL_DISASTER                              │
│     ├─ "strike" → LABOR_DISPUTE                                     │
│     ├─ "flood" → WEATHER_EVENT                                      │
│     ├─ "fire" → INDUSTRIAL_ACCIDENT                                 │
│     └─ "port" → LOGISTICS_DISRUPTION                                │
│                                                                      │
│  C. Calculate Severity                                              │
│     ├─ tone < -5 OR "catastrophic" → CRITICAL                       │
│     ├─ tone < -2 → HIGH                                             │
│     ├─ tone < 0 → MEDIUM                                            │
│     └─ else → LOW                                                   │
│                                                                      │
│  Result: Standardized Event Object                                  │
│  {                                                                   │
│    "source": "GDELT",                                               │
│    "title": "7.2 Earthquake Strikes Taiwan",                        │
│    "event_type": "NATURAL_DISASTER",                                │
│    "severity": "CRITICAL",                                          │
│    "location": {"country": "Taiwan", "lat": 24.8, "lon": 120.9}    │
│  }                                                                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 4: MATCH EVENTS TO SUPPLIERS
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  LiveFeedService.match_events_to_suppliers()                        │
│                                                                      │
│  For each event + each supplier in database:                        │
│                                                                      │
│  A. Country Match                                                   │
│     if event.location.country == supplier.country:                  │
│         supplier is AFFECTED ✓                                      │
│                                                                      │
│  B. Distance Match (using Haversine formula)                        │
│     distance = calculate_distance(                                  │
│         event.lat, event.lon,                                       │
│         supplier.latitude, supplier.longitude                       │
│     )                                                                │
│                                                                      │
│     Impact Radius by Event Type:                                    │
│     ├─ NATURAL_DISASTER: 500 km                                     │
│     ├─ WEATHER_EVENT: 300 km                                        │
│     ├─ LABOR_DISPUTE: 50 km                                         │
│     ├─ INDUSTRIAL_ACCIDENT: 100 km                                  │
│     └─ LOGISTICS_DISRUPTION: 200 km                                 │
│                                                                      │
│     if distance <= impact_radius:                                   │
│         supplier is AFFECTED ✓                                      │
│                                                                      │
│  Example Result:                                                    │
│  {                                                                   │
│    "event": "7.2 Earthquake Taiwan",                                │
│    "affected_suppliers": [                                          │
│      {                                                               │
│        "supplier_id": 18,                                           │
│        "name": "Semiconductor Fab Taiwan",                          │
│        "distance_km": 12,  ← Very close!                            │
│        "criticality": "CRITICAL"  ← This matters!                   │
│      },                                                              │
│      {                                                               │
│        "supplier_id": 20,                                           │
│        "name": "PCB Manufacturing Taiwan",                          │
│        "distance_km": 45,                                           │
│        "criticality": "HIGH"                                        │
│      }                                                               │
│    ],                                                                │
│    "affected_count": 2                                              │
│  }                                                                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 5: FILTER EVENTS → ALERTS
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  AlertDetector._should_trigger_alert()                              │
│                                                                      │
│  Trigger alert if ANY of these conditions:                          │
│                                                                      │
│  ☑️ Condition 1: High Severity                                      │
│     if event.severity in ["HIGH", "CRITICAL"]:                      │
│         return True                                                 │
│                                                                      │
│  ☑️ Condition 2: Affects Critical Suppliers                         │
│     critical_suppliers = [                                          │
│         s for s in affected_suppliers                               │
│         if s.criticality == "CRITICAL"                              │
│     ]                                                                │
│     if len(critical_suppliers) > 0:                                 │
│         return True                                                 │
│                                                                      │
│  ☑️ Condition 3: Affects Many Suppliers                             │
│     if affected_count >= 3:                                         │
│         return True                                                 │
│                                                                      │
│  Example:                                                           │
│  Input: 50 events detected                                          │
│  After filtering: 3 critical alerts                                 │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 6: CALCULATE IMPACT SCORES
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  AlertDetector._calculate_impact_score()                            │
│                                                                      │
│  Score = 0-100 based on three factors:                              │
│                                                                      │
│  Factor 1: Severity (0-40 points)                                   │
│    CRITICAL → +40                                                   │
│    HIGH     → +30                                                   │
│    MEDIUM   → +20                                                   │
│    LOW      → +10                                                   │
│                                                                      │
│  Factor 2: Number of Suppliers (0-30 points)                        │
│    score += min(affected_count × 5, 30)                             │
│    Examples:                                                         │
│    ├─ 1 supplier  → +5 points                                       │
│    ├─ 3 suppliers → +15 points                                      │
│    └─ 6+ suppliers → +30 points (max)                               │
│                                                                      │
│  Factor 3: Supplier Criticality (0-30 points)                       │
│    critical_count = count(criticality == "CRITICAL")                │
│    score += min(critical_count × 10, 30)                            │
│    Examples:                                                         │
│    ├─ 1 critical → +10 points                                       │
│    ├─ 2 critical → +20 points                                       │
│    └─ 3+ critical → +30 points (max)                                │
│                                                                      │
│  Example Calculation:                                               │
│  Event: Taiwan Earthquake                                           │
│  ├─ Severity: CRITICAL → +40                                        │
│  ├─ Affected: 2 suppliers → +10                                     │
│  └─ Critical suppliers: 2 → +20                                     │
│  Total Impact Score: 70/100                                         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 7: GENERATE RECOMMENDED ACTIONS
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  AlertDetector._generate_recommended_actions()                      │
│                                                                      │
│  Based on event_type:                                               │
│                                                                      │
│  NATURAL_DISASTER:                                                  │
│    ✓ "Activate disaster recovery protocols"                         │
│    ✓ "Assess alternative supplier capacity"                         │
│    ✓ "Review insurance coverage"                                    │
│                                                                      │
│  LABOR_DISPUTE:                                                     │
│    ✓ "Identify backup suppliers in different regions"               │
│    ✓ "Negotiate expedited shipping if needed"                       │
│                                                                      │
│  WEATHER_EVENT:                                                     │
│    ✓ "Monitor weather forecasts for duration"                       │
│    ✓ "Adjust inventory levels as precaution"                        │
│                                                                      │
│  LOGISTICS_DISRUPTION:                                              │
│    ✓ "Explore alternative shipping routes"                          │
│    ✓ "Consider air freight for critical components"                 │
│                                                                      │
│  If severity == HIGH or CRITICAL, add:                              │
│    ✓ "Escalate to executive team immediately"                       │
│    ✓ "Initiate emergency supplier sourcing"                         │
│                                                                      │
│  Generic actions always included:                                   │
│    ✓ "Review affected supplier contracts and SLAs"                  │
│    ✓ "Contact affected suppliers for status updates"                │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 8: CREATE STRUCTURED ALERT
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  AlertDetector._create_alert()                                      │
│                                                                      │
│  Final Alert Structure:                                             │
│  {                                                                   │
│    "alert_id": "ALERT-20251109144523",                              │
│    "timestamp": "2025-11-09T14:45:23",                              │
│    "severity": "CRITICAL",                                          │
│    "event_type": "NATURAL_DISASTER",                                │
│    "title": "7.2 Magnitude Earthquake Strikes Taiwan",              │
│    "description": "Major seismic event...",                         │
│    "source": "GDELT",                                               │
│    "location": {                                                    │
│      "country": "Taiwan",                                           │
│      "region": "Hsinchu",                                           │
│      "lat": 24.8138,                                                │
│      "lon": 120.9675                                                │
│    },                                                                │
│    "impact_score": 90,                                              │
│    "affected_suppliers": [                                          │
│      {                                                               │
│        "supplier_id": 18,                                           │
│        "supplier_name": "Semiconductor Fab Taiwan",                 │
│        "distance_km": 12,                                           │
│        "criticality": "CRITICAL"                                    │
│      }                                                               │
│    ],                                                                │
│    "affected_count": 2,                                             │
│    "recommended_actions": [                                         │
│      "Contact Semiconductor Fab Taiwan immediately",                │
│      "Activate disaster recovery protocols",                        │
│      "Escalate to executive team"                                   │
│    ],                                                                │
│    "source_url": "https://www.reuters.com/taiwan-earthquake"        │
│  }                                                                   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 9: STORE IN DATABASE
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  Table: live_feeds                                                  │
│  ┌────┬──────────┬───────────┬─────────────┬──────────┬────────┐   │
│  │ id │  source  │ data_type │  timestamp  │ payload  │processed│   │
│  ├────┼──────────┼───────────┼─────────────┼──────────┼────────┤   │
│  │ 1  │  GDELT   │   ALERT   │ 2025-11-09  │  {JSON}  │   0    │   │
│  │ 2  │  NOAA    │   ALERT   │ 2025-11-09  │  {JSON}  │   0    │   │
│  └────┴──────────┴───────────┴─────────────┴──────────┴────────┘   │
│                                                                      │
│  The payload column stores the complete alert JSON                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼

STEP 10: NOTIFY STAKEHOLDERS (Future Enhancement)
═══════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────┐
│  Potential notification channels:                                   │
│                                                                      │
│  📧 Email Alerts                                                    │
│     send_email(                                                     │
│         to="supply.chain@company.com",                              │
│         subject=f"CRITICAL: {alert.title}",                         │
│         body=alert.recommended_actions                              │
│     )                                                                │
│                                                                      │
│  💬 Slack/Teams Webhooks                                            │
│     post_to_slack(                                                  │
│         channel="#supply-chain-alerts",                             │
│         message=format_alert_message(alert)                         │
│     )                                                                │
│                                                                      │
│  📱 SMS (via Twilio)                                                │
│     if alert.severity == "CRITICAL":                                │
│         send_sms(                                                   │
│             to="+1234567890",                                       │
│             message=f"URGENT: {alert.title[:100]}"                  │
│         )                                                            │
│                                                                      │
│  🌐 Webhook (to other systems)                                      │
│     requests.post(                                                  │
│         "https://your-system.com/webhook",                          │
│         json=alert                                                  │
│     )                                                                │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
API ENDPOINTS FOR FRONTEND
═══════════════════════════════════════════════════════════════════════

GET /api/alerts/recent?hours=24&severity=CRITICAL
→ Returns recent alerts for dashboard

GET /api/alerts/dashboard
→ Returns summary statistics

POST /api/alerts/scan
→ Manually trigger alert scan

GET /api/alerts/events?source=GDELT
→ Get raw events (before alert filtering)

POST /api/alerts/scheduler/start
→ Start background scanning

POST /api/alerts/scheduler/stop
→ Stop background scanning


═══════════════════════════════════════════════════════════════════════
TIMING
═══════════════════════════════════════════════════════════════════════

Background Schedule: Every 15 minutes (configurable)
API Response Time: 2-5 seconds
Database Query: <100ms
Alert Processing: 1-3 seconds per event
Total Time: ~10 seconds from event happening to alert in your system
"""
