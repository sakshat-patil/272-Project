# Live Monitoring Frontend - User Guide

## 🎯 Where to See the Live Monitoring Tab

### Access Path:
1. **Start both servers:**
   ```bash
   # Terminal 1 - Backend
   cd backend && python run.py
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

2. **Navigate to:**
   - Open browser: `http://localhost:3000`
   - Click on any organization card
   - Click the **"Live Monitoring"** tab (formerly "Live Weather")

### Tab Location:
The Live Monitoring tab is the **second tab** in the organization page:
- Tab 1: **Suppliers** (list of all suppliers)
- Tab 2: **Live Monitoring** ⭐ **NEW** (real-time data feeds)
- Tab 3: **Event Analysis** (AI-powered event analysis)
- Tab 4: **History** (historical risk data)

---

## 📊 What You'll See in Live Monitoring

### Four Sub-Tabs:

#### 1. **Weather Tab** 🌦️
Shows real-time weather data for all supplier locations:
- Severe weather alerts (if any)
- Temperature, wind speed, conditions for each supplier
- Location-based monitoring
- Auto-refreshes every 30 seconds

**Data Source:** WeatherAPI.com (from your roommate's integration)

---

#### 2. **Shipping Tab** 🚢
Global port status and congestion monitoring:
- **Los Angeles** - Congestion level, wait times, vessels waiting
- **Shanghai** - Port status and delays
- **Rotterdam** - European hub monitoring
- **Singapore** - Asian shipping hub

**Features:**
- Congestion levels (0-10 scale)
- Average wait times in hours
- Estimated delay in days
- Color-coded status (green/yellow/red)

**Data Source:** Mock data ready for MarineTraffic/Searoutes API integration

---

#### 3. **Markets Tab** 📈
Market trends and financial sentiment:
- **Google Trends Analysis**
  - Search interest trends for supply chain keywords
  - Current interest score (0-100)
  - Percentage change from average
  - Trending indicators

**Example Output:**
```
Keyword: "supply chain"
Current Interest: 100
Average: 43.7
Change: +128.44% ⬆️ TRENDING!
```

**Data Sources:**
- Google Trends API (pytrends) - ✅ Working
- Exchange Rates API - ✅ Working
- Yahoo Finance - ⚠️ Rate-limited (works but may need delays)

---

#### 4. **Risks Tab** ⚠️
Comprehensive risk dashboard:

**Summary Cards:**
- 🔴 Sanctions Alerts
- 🟠 Geopolitical Risks
- 🟡 Shipping Delays
- 🔵 Financial Risks

**Supplier Risk Scores:**
- Color-coded risk indicators (green/yellow/red)
- Aggregate risk scores (0-100)
- Sortable by risk level

**Data Sources:**
- OpenSanctions API - ✅ Working
- Geopolitical conflict data (ACLED placeholder)
- Combined risk calculations

---

## 🔄 Auto-Refresh Behavior

The Live Monitoring tab automatically refreshes data every **30 seconds**:
- Weather data updates
- Shipping port status updates
- Market trends updates
- Risk calculations refresh

You can also manually refresh by clicking the **"Refresh"** button in the top-right corner.

---

## 🎨 UI Features

### Color-Coded Alerts:
- 🔴 **Red/Critical** - Severe risk (score ≥ 70)
- 🟡 **Yellow/Warning** - Moderate risk (score 40-69)
- 🟢 **Green/Normal** - Low risk (score < 40)

### Icons:
- 🌦️ Weather conditions
- 🚢 Shipping status
- 📈 Market trends
- ⚠️ Risk alerts
- 🌍 Geopolitical events

### Badges:
- Risk levels (CRITICAL, HIGH, MODERATE, LOW)
- Congestion levels (0-10)
- Trending indicators

---

## 🧪 Testing the Features

### 1. **Test Weather Tab:**
- Should show weather for all supplier locations
- Look for severe weather alerts (if any)
- Verify auto-refresh after 30 seconds

### 2. **Test Shipping Tab:**
- Check Los Angeles port (usually congestion 8/10 - CRITICAL)
- Verify wait times and delays
- Look for color-coded congestion bars

### 3. **Test Markets Tab:**
- Google Trends for "supply chain" keyword
- Should show trending status if search interest is high
- Check percentage change

### 4. **Test Risks Tab:**
- Summary cards should show counts
- Supplier risk scores should be color-coded
- Click on suppliers to see detailed risk factors

---

## 🐛 Troubleshooting

### If data doesn't load:
1. **Check backend is running:** `http://localhost:8000/docs`
2. **Check console for errors:** Open browser DevTools (F12)
3. **Verify API endpoints:**
   - Weather: `GET /api/weather/organization/{id}/`
   - Shipping: `GET /api/enhanced/shipping/major-ports`
   - Trends: `GET /api/enhanced/social/trends?keyword=supply%20chain`
   - Risk: `GET /api/enhanced/risk/dashboard?organization_id={id}`

### If backend says "Module not found":
```bash
cd backend
pip install yfinance pytrends apscheduler httpx
```

### If frontend won't load:
```bash
cd frontend
npm install
npm run dev
```

---

## 📦 What Changed from Before

### Before (Roommate's Version):
- Tab name: **"Live Weather"**
- Only showed: Weather data for suppliers
- Single-purpose monitoring

### After (Your Enhanced Version):
- Tab name: **"Live Monitoring"** (more generic)
- Shows 4 categories:
  1. Weather (original functionality preserved)
  2. Shipping (NEW)
  3. Markets (NEW)
  4. Risks (NEW)
- Multi-source real-time intelligence
- Comprehensive supply chain visibility

---

## 🎯 Demo Tips

When presenting to class:
1. **Start with Weather tab** - "This is what my roommate built"
2. **Switch to Shipping tab** - "I added global port monitoring"
3. **Show Markets tab** - "Real-time market sentiment via Google Trends"
4. **Highlight Risks tab** - "Comprehensive risk dashboard combining all data sources"
5. **Click Refresh** - "All data updates in real-time"

### Good Test Organizations:
- **ACME Corporation** (if you have it)
- Any organization with multiple suppliers in different countries

### What to Highlight:
- ✅ Real-time data integration (4 API sources)
- ✅ Auto-refresh (30-second intervals)
- ✅ Color-coded risk indicators
- ✅ Comprehensive monitoring in one place
- ✅ Scalable architecture (easy to add more APIs)

---

## 🚀 Next Steps (Optional Enhancements)

If you want to make it even better:
1. **Enable background workers** - Uncomment lines in `backend/app/main.py`
2. **Add more suppliers** - More locations = more interesting weather data
3. **Add stock tickers** - Link suppliers to financial data
4. **Enable port tracking** - Add primary_port field to suppliers
5. **Historical charts** - Plot trends over time

---

## 📝 Files Modified

### Frontend:
- ✅ `frontend/src/components/events/LiveMonitoringFeed.jsx` (NEW)
- ✅ `frontend/src/pages/OrganizationPage.jsx` (updated imports and tab name)

### Backend (from earlier):
- ✅ `backend/app/services/enhanced_feeds.py`
- ✅ `backend/app/routers/enhanced_data.py`
- ✅ `backend/app/main.py`
- ✅ `backend/requirements.txt`

---

**Enjoy your comprehensive Supply Chain Risk Monitor! 🎉**
