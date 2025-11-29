# Supply Chain Risk Monitor - Onboarding Use Case

## 📋 Overview

This document outlines the **use case** and **onboarding flow** implemented for the Supply Chain Risk Monitor platform, designed to address professor feedback and enhance the user experience.

---

## 🎯 Use Case: Electronics Manufacturing Supply Chain

### Scenario
**TechCore Electronics** - A mid-sized electronics manufacturing company based in San Jose, California

### Business Context
- **Industry**: Consumer Electronics
- **Primary Products**: Smartphones, tablets, IoT devices
- **Key Challenge**: Managing supply chain risks across complex Pacific trade routes

### Supply Chain Structure
TechCore sources critical components from multiple Asian suppliers:

1. **Semiconductor Chips** 
   - Source: Taiwan (TSMC, MediaTek suppliers)
   - Criticality: HIGH
   - Lead Time: 45-60 days

2. **Display Panels**
   - Source: South Korea, China
   - Criticality: HIGH
   - Lead Time: 30 days

3. **Circuit Boards & Components**
   - Source: Singapore, Malaysia
   - Criticality: MEDIUM
   - Lead Time: 20-30 days

4. **Final Assembly**
   - Shipping Route: **Singapore → Los Angeles**
   - Transit Time: 18-22 days
   - Volume: 10,000+ units/month

### Risk Factors
- **Typhoons & Natural Disasters**: Frequent in Pacific region (Taiwan, Hong Kong, Philippines)
- **Port Congestion**: Los Angeles port delays during peak seasons
- **Geopolitical Tensions**: Taiwan-China relations affecting semiconductor supply
- **Earthquakes**: Taiwan & Japan seismic activity impacting production
- **Labor Strikes**: Port worker strikes in US West Coast

---

## 🚀 Onboarding Flow Implementation

### Step 1: Company Information
Users input basic company details:
- Company Name (e.g., "TechCore Electronics")
- Industry (Electronics, Pharmaceutical, Automotive, etc.)
- Headquarters Location
- Business Description

**Purpose**: Establish organizational context for risk analysis

### Step 2: Shipping Route Definition
Users define their primary shipping route:

**Quick Select Options** (pre-configured common routes):
- Singapore → Los Angeles (Pacific Electronics Route)
- Shanghai → Rotterdam (Europe Trade Route)
- Hong Kong → Long Beach (Pacific Trade Route)

**Or Manual Entry**:
- **Origin Port**: Name, Country, Latitude, Longitude
- **Destination Port**: Name, Country, Latitude, Longitude

**Purpose**: Enable location-based historical event analysis

### Step 3: Historical Risk Analysis
System automatically:
1. **Queries Historical Events** within 500km radius of shipping route
2. **Displays Past Disruptions**:
   - Event Title (e.g., "Typhoon Mangkhut - Port Closures")
   - Description & Impact Assessment
   - Date & Location
   - Severity Level (High/Medium/Low)
   - Distance from Route

3. **Provides Context**: Users see historical patterns before committing to platform

**Sample Historical Events Shown**:
- **Typhoon Mangkhut (2018)**: Category 5 typhoon closed Hong Kong ports for 2 weeks
- **Port of LA Congestion (2021)**: COVID-19 caused 3+ week delays with 100+ ships anchored
- **Taiwan Earthquake (2022)**: 6.4 magnitude quake affected semiconductor production
- **Suez Canal Blockage (2021)**: Ever Given blocked canal for 6 days (global impact)

**Purpose**: Demonstrate value proposition with real historical data

---

## 🔧 Technical Implementation

### Backend API

#### New Endpoint: `/api/events/historical`
**Request**:
```json
{
  "origin_latitude": 1.2644,
  "origin_longitude": 103.8215,
  "destination_latitude": 33.7405,
  "destination_longitude": -118.2716,
  "radius_km": 500
}
```

**Response**:
```json
{
  "events": [
    {
      "title": "Typhoon Mangkhut - Port Closures",
      "description": "Category 5 typhoon caused widespread port closures...",
      "date": "2018-09-16",
      "location": "Hong Kong / Guangdong, China",
      "severity": "High",
      "event_type": "Natural Disaster",
      "distance_km": 245
    }
  ],
  "total_found": 5,
  "search_radius_km": 500
}
```

#### Haversine Distance Calculation
Uses great circle distance formula to match events within radius of shipping route endpoints.

#### Database Schema Updates

**Organization Model**:
```python
class Organization(Base):
    # ... existing fields ...
    shipping_route = Column(JSON)  # Stores route data from onboarding
```

**Event Model**:
```python
class Event(Base):
    # ... existing fields ...
    title = Column(String(300))
    latitude = Column(Float)
    longitude = Column(Float)
    event_date = Column(DateTime)
    impact_assessment = Column(Text)
```

### Frontend Implementation

#### New Page: `/onboarding`
**Features**:
- 3-step wizard with progress indicator
- Form validation & error handling
- Pre-configured route templates
- Real-time historical event fetching
- Smooth navigation with React Router

#### Integration with Existing Flow
- **HomePage**: Shows onboarding banner for new users
- **SignupPage**: Can redirect to onboarding after registration
- **OrganizationPage**: Displays shipping route info in organization details

---

## 📊 Sample Historical Events Database

### For Pacific Routes (Singapore/Hong Kong/Taiwan → Los Angeles)
1. **Typhoon Mangkhut (2018)**: Hong Kong port closures, High severity
2. **Port of LA Congestion (2021)**: COVID-19 pandemic delays, High severity
3. **Taiwan Earthquake (2022)**: Semiconductor production impact, Medium severity
4. **Singapore Port Strike (2020)**: 3-day labor strike, Medium severity

### For Global Routes
1. **Suez Canal Blockage (2021)**: Ever Given incident, High severity
2. **COVID-19 Pandemic (2020)**: Global shipping crisis, High severity
3. **Semiconductor Shortage (2021)**: Global chip shortage, High severity

---

## 🎓 Demo Script Enhancement

### Updated Introduction (3 minutes)

**Opening (30 sec)**:
"Welcome to the Supply Chain Risk Monitor - an AI-powered platform that helps companies predict and mitigate supply chain disruptions before they impact business operations."

**Use Case Introduction (45 sec)**:
"Let me show you how this works with TechCore Electronics, a fictional company manufacturing smartphones and tablets. Like many electronics companies, TechCore sources semiconductor chips from Taiwan, ships components from Singapore, and assembles products for the US market. Their biggest concern? Disruptions along the Singapore to Los Angeles shipping route - one of the world's busiest trade lanes."

**Onboarding Demo (60 sec)**:
"When TechCore first signs up, we guide them through a simple onboarding process:
1. They tell us about their company
2. They define their primary shipping route - in this case, Singapore to LA
3. We immediately show them historical risk patterns for that route

For example, they see the 2021 Port of Los Angeles congestion crisis caused by COVID-19, where over 100 ships were anchored offshore with 3+ week delays. They see Typhoon Mangkhut in 2018 that shut down Hong Kong ports. They see the Taiwan earthquake in 2022 that affected semiconductor production.

This historical context helps them understand: these aren't hypothetical risks - they're real events that have disrupted companies just like theirs."

**Platform Value (45 sec)**:
"Now that TechCore is onboarded, our platform continuously monitors their supply chain with 6 AI agents. Let me show you how this works in real-time..."

[Continue with existing demo showing the 6 agents analyzing a new event]

---

## 🔄 User Journey

### New User Flow
1. User visits platform → Sees onboarding banner
2. Clicks "Start Onboarding" → Enters company info
3. Defines shipping route (quick select or manual)
4. **Reviews historical events** → Sees value proposition
5. Completes onboarding → Organization created
6. Redirected to Organization page → Can analyze new events

### Returning User Flow
1. User logs in → Sees existing organizations
2. Can add new organizations via onboarding
3. Each organization retains shipping route data
4. Historical context available in organization details

---

## 💡 Value Proposition

### Before Onboarding
- User unsure if platform is relevant to their business
- No context on historical risk patterns
- Generic risk assessment

### After Onboarding
✅ **Immediate Value**: See historical disruptions for their specific route  
✅ **Contextualized Risk**: Platform knows their shipping lanes  
✅ **Proactive Monitoring**: 6 AI agents watching their route 24/7  
✅ **Historical Patterns**: Learn from past events to prevent future losses

---

## 🚢 Common Shipping Routes Supported

| Route | Origin | Destination | Use Case |
|-------|--------|-------------|----------|
| Singapore → LA | Port of Singapore | Port of Los Angeles | Electronics, Consumer Goods |
| Shanghai → Rotterdam | Port of Shanghai | Port of Rotterdam | Manufacturing, Automotive |
| Hong Kong → Long Beach | Port of Hong Kong | Port of Long Beach | Textiles, Electronics |

---

## 📈 Next Steps

### Potential Enhancements
1. **Multi-Route Support**: Allow organizations to define multiple shipping routes
2. **Supplier Geolocation**: Automatically map suppliers along route corridors
3. **Predictive Risk Heatmaps**: Visualize risk zones on interactive map
4. **Historical Event Import**: Integrate with GDELT/ACLED databases for richer historical data
5. **Route Optimization**: Suggest alternative routes based on historical risk patterns

---

## 🎯 Success Metrics

### Onboarding Effectiveness
- % of users completing onboarding vs. skipping
- Time spent reviewing historical events
- Correlation between historical events shown and user retention

### Platform Value
- Organizations with shipping routes vs. without
- Engagement with route-specific risk alerts
- User feedback on historical context relevance

---

## 📝 Conclusion

The onboarding flow transforms the Supply Chain Risk Monitor from a generic risk platform into a **personalized supply chain intelligence system**. By focusing on the **Electronics Manufacturing use case** and the **Singapore → Los Angeles route**, we demonstrate concrete value with real historical events, setting the stage for ongoing AI-powered monitoring and risk mitigation.

---

**Last Updated**: November 28, 2025  
**Implementation Status**: ✅ Complete (Backend + Frontend)  
**Demo Ready**: ✅ Yes
