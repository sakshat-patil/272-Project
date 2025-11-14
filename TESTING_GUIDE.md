# 🧪 Complete Testing Guide - Tier 1 Enhanced APIs

## Quick Start Testing (Right Now)

### Option 1: Test Script (Fastest - 30 seconds)
```bash
cd backend
source venv/bin/activate
python test_enhanced_apis.py
```

**What it tests:**
- ✅ All 4 API categories (Financial, Shipping, Geopolitical, Social)
- ✅ Real API calls to Exchange Rates, Google Trends, OpenSanctions
- ✅ Mock data validation for Shipping
- ✅ Error handling

**Expected output:**
```
🧪 Testing Tier 1 Enhanced APIs
💹 Testing Financial Data Service...
   CNY: 7.1300
   EUR: 0.8660
🚢 Testing Shipping Data Service...
   ⚓ Port: Los Angeles - Congestion Level: 8/10
⚠️  Testing Geopolitical Risk Service...
   Ukraine: Conflict Level: 9/10 - CRITICAL
📱 Testing Social Media Monitor...
   TSMC: Trending True - Change: 128.44%
✅ All Tier 1 API tests complete!
```

---

## Option 2: API Endpoint Testing (Backend + HTTP Requests)

### Step 1: Start Backend
```bash
cd backend
source venv/bin/activate
python run.py
```

**Wait for:**
```
🚀 Starting Supply Chain Risk Monitor API...
✅ Database initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test via cURL (New Terminal)

**A. Test All Services At Once:**
```bash
curl http://localhost:8000/api/enhanced/test/all | jq
```

**B. Test Individual Endpoints:**

**Financial APIs:**
```bash
# Stock data (TSMC - Taiwan Semiconductor)
curl -X POST http://localhost:8000/api/enhanced/financial/stock \
  -H "Content-Type: application/json" \
  -d '{"ticker": "TSM"}' | jq

# Commodity prices
curl -X POST http://localhost:8000/api/enhanced/financial/commodities \
  -H "Content-Type: application/json" \
  -d '{"commodities": ["oil", "gold", "copper"]}' | jq

# Exchange rates
curl http://localhost:8000/api/enhanced/financial/exchange-rates | jq
```

**Shipping APIs:**
```bash
# Port status
curl -X POST http://localhost:8000/api/enhanced/shipping/port-status \
  -H "Content-Type: application/json" \
  -d '{"port_name": "Los Angeles"}' | jq

# Shipping route estimate
curl -X POST http://localhost:8000/api/enhanced/shipping/route-estimate \
  -H "Content-Type: application/json" \
  -d '{"origin": "Shanghai", "destination": "Los Angeles"}' | jq

# All major ports
curl http://localhost:8000/api/enhanced/shipping/major-ports | jq
```

**Geopolitical APIs:**
```bash
# Sanctions check
curl -X POST http://localhost:8000/api/enhanced/geopolitical/sanctions \
  -H "Content-Type: application/json" \
  -d '{"entity_name": "Test Company"}' | jq

# Conflict data
curl -X POST http://localhost:8000/api/enhanced/geopolitical/conflict \
  -H "Content-Type: application/json" \
  -d '{"country": "Taiwan"}' | jq

# High-risk countries
curl http://localhost:8000/api/enhanced/geopolitical/high-risk-countries | jq
```

**Social Media APIs:**
```bash
# Google Trends
curl "http://localhost:8000/api/enhanced/social/trends?keyword=TSMC" | jq
curl "http://localhost:8000/api/enhanced/social/trends?keyword=Tesla" | jq
```

**Comprehensive Risk:**
```bash
# Risk for specific supplier (Semiconductor Fab Taiwan)
curl -X POST http://localhost:8000/api/enhanced/risk/comprehensive \
  -H "Content-Type: application/json" \
  -d '{"supplier_id": 18}' | jq

# Dashboard for organization (PharmaCorp)
curl "http://localhost:8000/api/enhanced/risk/dashboard?organization_id=1" | jq
```

---

## Option 3: Swagger UI Testing (Visual/Interactive)

### Step 1: Start Backend
```bash
cd backend
source venv/bin/activate
python run.py
```

### Step 2: Open Swagger Docs
Open browser: **http://localhost:8000/docs**

### Step 3: Test Endpoints Interactively

1. **Expand "Enhanced Data" section**
2. **Click on any endpoint** (e.g., `POST /api/enhanced/financial/stock`)
3. **Click "Try it out"**
4. **Enter request body:**
   ```json
   {"ticker": "AAPL"}
   ```
5. **Click "Execute"**
6. **See response below**

**Advantages:**
- ✅ Visual interface
- ✅ Auto-generated request examples
- ✅ Response validation
- ✅ Easy to copy/paste results

---

## Option 4: End-to-End Full Stack Testing

### Step 1: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python run.py
# Wait for: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Wait for: Local: http://localhost:3000/
```

### Step 2: Use Frontend (When Enhanced UI is Added)

**Current State:**
- Backend APIs are ready
- Frontend needs Enhanced Data dashboard component (future)

**To test with existing UI:**
1. Go to http://localhost:3000
2. Select an organization (e.g., PharmaCorp)
3. The backend is ready to serve enhanced data via API calls

### Step 3: Create Quick Frontend Test (Optional)

Create `frontend/src/pages/EnhancedDataTestPage.jsx`:
```jsx
import { useState } from 'react';
import api from '../services/api';

export default function EnhancedDataTestPage() {
  const [result, setResult] = useState(null);
  
  const testFinancial = async () => {
    const res = await api.post('/enhanced/financial/stock', {ticker: 'AAPL'});
    setResult(res.data);
  };
  
  const testTrends = async () => {
    const res = await api.get('/enhanced/social/trends?keyword=TSMC');
    setResult(res.data);
  };
  
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Enhanced APIs Test</h1>
      <div className="space-x-4">
        <button onClick={testFinancial} className="btn">Test Financial</button>
        <button onClick={testTrends} className="btn">Test Trends</button>
      </div>
      <pre className="mt-4 bg-gray-100 p-4 rounded">
        {JSON.stringify(result, null, 2)}
      </pre>
    </div>
  );
}
```

---

## Option 5: Background Worker Testing

### Test Automatic Monitoring (Every 5 Minutes)

**Step 1: Enable Worker**

Edit `backend/app/main.py`:
```python
# Line ~17-18 - UNCOMMENT these lines:
await start_enhanced_worker(poll_interval=300)
print("💹 Enhanced data monitoring started")

# Line ~25 - UNCOMMENT this line:
stop_enhanced_worker()
```

**Step 2: Start Backend**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Step 3: Watch Logs**

You'll see automatic scans every 5 minutes:
```
💹 Enhanced data worker started - polling every 300s
🔍 Running enhanced data scan...
💹 Commodity prices stable: {...}
⚓ All major ports operating normally
🌍 Geopolitical situation stable
💱 Exchange rates (USD): {...}
✅ Enhanced data scan complete
```

**To test immediately (don't wait 5 min):**

Change `poll_interval` from 300 to 60 seconds:
```python
await start_enhanced_worker(poll_interval=60)  # Test mode: 1 minute
```

---

## 🎯 Recommended Testing Flow

### For Quick Validation (5 minutes):
1. ✅ Run `python test_enhanced_apis.py`
2. ✅ Check Swagger UI at http://localhost:8000/docs
3. ✅ Test 2-3 endpoints via cURL

### For Demo/Presentation (15 minutes):
1. ✅ Start backend
2. ✅ Open Swagger UI
3. ✅ Test financial data (stocks, commodities)
4. ✅ Test Google Trends (show TSMC trending)
5. ✅ Test port congestion
6. ✅ Test geopolitical risks
7. ✅ Show comprehensive risk endpoint

### For Full Integration (30 minutes):
1. ✅ Enable background worker
2. ✅ Start both frontend + backend
3. ✅ Monitor logs for automatic scans
4. ✅ Test API endpoints
5. ✅ Verify data updates

---

## 📊 Sample Test Scenarios

### Scenario 1: Supplier Financial Health
```bash
# Check if TSMC stock is healthy
curl -X POST http://localhost:8000/api/enhanced/financial/stock \
  -H "Content-Type: application/json" \
  -d '{"ticker": "TSM"}' | jq

# Expected:
# {
#   "ticker": "TSM",
#   "current_price": 186.5,
#   "price_change_5d": 2.3,
#   "financial_health": "STABLE - Normal trading range",
#   "alert_level": "LOW"
# }
```

### Scenario 2: Port Disruption
```bash
# Check Los Angeles port congestion
curl -X POST http://localhost:8000/api/enhanced/shipping/port-status \
  -H "Content-Type: application/json" \
  -d '{"port_name": "Los Angeles"}' | jq

# Expected:
# {
#   "port": "Los Angeles",
#   "congestion_level": 8,
#   "status": "CRITICAL - Severe delays expected",
#   "estimated_delay_days": 3
# }
```

### Scenario 3: Geopolitical Risk
```bash
# Check Taiwan stability (important for semiconductor suppliers)
curl -X POST http://localhost:8000/api/enhanced/geopolitical/conflict \
  -H "Content-Type: application/json" \
  -d '{"country": "Taiwan"}' | jq

# Expected:
# {
#   "country": "Taiwan",
#   "conflict_level": 4,
#   "status": "Heightened Tensions",
#   "risk_assessment": "MODERATE - Tensions present, monitor closely"
# }
```

### Scenario 4: Trending Topics
```bash
# Is TSMC trending? (could indicate news/issues)
curl "http://localhost:8000/api/enhanced/social/trends?keyword=TSMC" | jq

# Expected:
# {
#   "keyword": "TSMC",
#   "current_interest": 100,
#   "avg_interest": 43,
#   "trending": true,
#   "change_percent": 128.44
# }
```

### Scenario 5: Comprehensive Risk Dashboard
```bash
# Full risk assessment for PharmaCorp organization
curl "http://localhost:8000/api/enhanced/risk/dashboard?organization_id=1" | jq

# Expected:
# {
#   "organization": "PharmaCorp",
#   "supplier_count": 8,
#   "risk_summary": {
#     "financial_risks": 0,
#     "shipping_delays": 1,
#     "sanctions_alerts": 0,
#     "geopolitical_risks": 2
#   },
#   "suppliers": [...]
# }
```

---

## 🐛 Troubleshooting Tests

### Issue: "Import errors" when running test
**Solution:**
```bash
cd backend
source venv/bin/activate  # Make sure venv is activated
pip install yfinance pytrends apscheduler
python test_enhanced_apis.py
```

### Issue: "Connection refused" errors
**Solution:**
```bash
# Make sure backend is running:
cd backend
source venv/bin/activate
python run.py

# In another terminal, run tests
```

### Issue: "Too Many Requests" from Yahoo Finance
**Solution:**
- This is expected in heavy testing (rate limit)
- Exchange Rates API still works
- Wait 1 hour or use different stocks
- For demo, use mock data or Google Trends instead

### Issue: "Module not found: app.routers.enhanced_data"
**Solution:**
```bash
# Make sure enhanced_data.py exists
ls backend/app/routers/enhanced_data.py

# If missing, the file was created earlier
# Check git status to see if it's untracked
cd backend
git status
```

---

## 📈 Expected Performance

| API | Response Time | Rate Limit | Cost |
|-----|--------------|------------|------|
| Exchange Rates | 200-500ms | 1500/month | Free |
| Google Trends | 1-3s | Unlimited | Free |
| OpenSanctions | 500ms-1s | Unlimited | Free |
| Yahoo Finance | 500ms-2s | ~2000/day | Free |
| Shipping (Mock) | <50ms | Unlimited | N/A |
| Geopolitical (Mock) | <50ms | Unlimited | N/A |

---

## ✅ Test Checklist

Before your demo/presentation:

- [ ] Run `python test_enhanced_apis.py` - all pass?
- [ ] Backend starts without errors?
- [ ] Can access http://localhost:8000/docs?
- [ ] Test at least 3 endpoints via cURL
- [ ] Exchange rates endpoint working?
- [ ] Google Trends endpoint working?
- [ ] Sanctions check endpoint working?
- [ ] Mock shipping data returns correctly?
- [ ] Background worker logs appear (if enabled)?
- [ ] No error messages in console?

---

## 🎬 Demo Script (5-Minute Walkthrough)

**For Showing to Professor/TA:**

1. **Start Backend** (30 sec)
   ```bash
   cd backend && source venv/bin/activate && python run.py
   ```

2. **Open Swagger UI** (30 sec)
   - Navigate to http://localhost:8000/docs
   - Show all the new `/api/enhanced/*` endpoints

3. **Live Demo: Google Trends** (1 min)
   - Click `GET /api/enhanced/social/trends`
   - Try it out with keyword "TSMC"
   - Execute → Show trending result (128% above average!)

4. **Live Demo: Geopolitical Risk** (1 min)
   - Click `POST /api/enhanced/geopolitical/conflict`
   - Try it out with country "Ukraine"
   - Execute → Show conflict level 9/10 CRITICAL

5. **Live Demo: Port Congestion** (1 min)
   - Click `POST /api/enhanced/shipping/port-status`
   - Try it out with port "Los Angeles"
   - Execute → Show congestion level 8/10

6. **Show Test Results** (1 min)
   ```bash
   python test_enhanced_apis.py
   ```
   - Scroll through output showing all APIs tested

7. **Explain Integration** (30 sec)
   - "These 4 API categories monitor suppliers in real-time"
   - "Financial health, shipping delays, geopolitical risks, trending issues"
   - "Can run automatically every 5 minutes in background"

**Total: ~5 minutes, very impressive!**

---

## 🚀 Next Steps After Testing

Once you verify everything works:

1. **Commit Your Changes:**
   ```bash
   git add backend/
   git commit -m "Add Tier 1 Enhanced APIs: Financial, Shipping, Geopolitical, Social Media monitoring"
   git push
   ```

2. **Create Frontend UI** (Future):
   - Enhanced Data Dashboard component
   - Real-time risk charts
   - Alert notifications

3. **Enable Background Worker:**
   - Uncomment lines in `main.py`
   - Monitor logs for automatic scans

4. **Add Real APIs:**
   - Get MarineTraffic API key
   - Get ACLED API key for conflict data
   - Add to `.env` file

**You're all set for comprehensive testing! 🎉**
