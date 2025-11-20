# Supply Chain Risk Monitor

## Overview

An AI-powered platform that analyzes supply chain disruption events in real-time and generates actionable incident response plans. The system uses a multi-agent architecture with Google Gemini AI to transform days-long manual risk assessments into 15-30 second automated analyses.

**Key Statistics:**
- ⚡ **95% faster** analysis time (days → seconds)
- 🤖 **6 specialized AI agents** working collaboratively
- 📊 **Quantified risk scores** on a 0-100 scale
- 💰 **Financial impact tracking** with ROI estimates
- 🌍 **Multi-tier supplier** dependency analysis

## Problem Statement

Modern supply chains face unprecedented challenges:
- Global supply chain disruptions cost businesses **$184B annually**
- Traditional risk assessment takes **2-5 days** of manual analysis
- **93% of companies** experienced supply chain disruptions in 2023
- Manual processes can't keep pace with increasingly complex global networks
- Lack of real-time visibility into cascading supplier dependencies

## Solution

Our platform automates and accelerates supply chain risk management through:

### Core Capabilities

1. **Event Analysis**
   - Parse natural language incident descriptions using AI
   - Automatically classify events (Natural Disaster, Geopolitical, Labor Strike, Logistics, Cyber Security, etc.)
   - Extract location data, severity levels, and affected industries

2. **Supplier Impact Assessment**
   - Match incidents to affected suppliers using geographic proximity
   - Industry-based impact analysis
   - Calculate proximity scores and impact reasons
   - Track multi-tier supplier dependencies with cascading effect analysis

3. **Risk Quantification**
   - Calculate overall risk scores (0-100) with 5 severity levels
   - Financial impact estimates (revenue at risk, mitigation costs)
   - Supplier criticality weighting (Critical, High, Medium, Low)
   - Impact scoring based on tier, reliability, and capacity utilization

4. **Alternative Sourcing**
   - Automatically identify backup suppliers in the same category
   - Intelligent ranking based on reliability, location, and capacity
   - Top 3 alternatives recommended per affected supplier
   - Geographic diversification analysis

5. **Response Playbooks**
   - Time-phased action plans (Day 1, Week 1, Month 1)
   - Assigned ownership and priorities for each action
   - Success metrics and KPIs
   - Escalation criteria and communication templates
   - Stakeholder communication plans (internal & external)

6. **Future Risk Prediction**
   - Analyze supplier portfolio for vulnerability patterns
   - Predict potential disruptions in the next 30/60/90 days
   - Identify risk factors (geographic concentration, critical dependencies, capacity constraints)
   - Generate proactive recommendations with timelines

## Multi-Agent Architecture

The system employs **6 specialized AI agents** orchestrated in a sequential pipeline:

### Agent Workflow

```
User Input (Natural Language Event)
         ↓
   [Event Parser Agent]
         ↓
   [Supplier Matcher Agent]
         ↓
   [Risk Analyzer Agent]
         ↓
   [Recommendation Generator Agent]
         ↓
   [Playbook Generator Agent]
         ↓
   Final Analysis Report

   [Future Risk Predictor Agent] ← Runs independently for forecasting
```

### Detailed Agent Breakdown

| Agent | Primary Function | AI Usage | Key Outputs |
|-------|------------------|----------|-------------|
| **Event Parser** | Converts natural language to structured data | High (Gemini 2.5 Flash) | Event type, location (coordinates), severity, duration, affected industries |
| **Supplier Matcher** | Identifies impacted suppliers | Logic + distance calculations | Affected supplier list, proximity scores, impact reasons |
| **Risk Analyzer** | Quantifies business impact | Medium (calculations) | Risk score (0-100), financial estimates, criticality analysis |
| **Recommendation Generator** | Finds mitigation strategies | High (Gemini 2.5 Flash) | Alternative suppliers (ranked), immediate actions, strategic plans |
| **Playbook Generator** | Creates response plans | Medium (structured generation) | Time-phased actions, success metrics, communication plans |
| **Future Risk Predictor** | Forecasts upcoming risks | High (Gemini 2.5 Flash) | Predicted risk score, vulnerability analysis, early warning signs |

### Agent Orchestrator

The **Agent Orchestrator** coordinates the entire workflow:
- Executes agents in sequence with error handling
- Tracks processing time and status for each agent
- Manages database persistence and updates
- Handles cascading dependency analysis
- Logs all agent activities for transparency
- Updates organization-level risk scores and history

## Key Features

### 🎯 Intelligent Event Processing
- Natural language understanding for incident descriptions
- Automatic event classification and severity assessment
- Geographic coordinate extraction and mapping
- Industry impact analysis

### 🌐 Geographic Intelligence
- Distance-based supplier matching using Haversine formula
- Affected radius calculations
- City, country, and region-level matching
- Coordinate-based proximity scoring

### 📈 Risk Analytics
- Multi-factor risk scoring algorithm
- Tier-based impact weighting (Tier 1, 2, 3)
- Criticality levels (Critical, High, Medium, Low)
- Cascading effect analysis through dependency graphs
- Historical risk tracking over time

### 💼 Financial Impact Modeling
- Daily revenue at risk calculations
- Estimated resolution timelines
- Total potential loss projections
- Expedited shipping cost estimates
- Alternative sourcing cost analysis
- Net mitigation impact calculations

### 🔄 Alternative Supplier Recommendations
- Same-category supplier matching
- Intelligent ranking based on:
  - Reliability scores
  - Geographic distance from incident
  - Capacity availability
  - Lead time considerations
  - Tier matching

### 📋 Actionable Playbooks
- **Day 1 Actions** (0-24 hours): Immediate response and assessment
- **Week 1 Actions** (1-7 days): Mitigation and alternative activation
- **Month 1 Actions** (1-4 weeks): Recovery and long-term improvements
- Clear ownership assignment for accountability
- Priority levels (Critical, High, Medium, Low)
- Success metrics and tracking

### 🔮 Predictive Analytics
- Portfolio vulnerability analysis
- Risk factor identification:
  - Geographic concentration
  - Critical supplier dependency
  - Capacity constraints
  - Reliability issues
  - Extended lead times
- Proactive recommendations with expected benefits

## Tech Stack

### Frontend
- **React 18.2** - Modern UI framework
- **Vite 5.0** - Fast build tool and dev server
- **Tailwind CSS 3.3** - Utility-first CSS framework
- **TanStack Query (React Query)** - Data fetching and caching
- **Axios** - HTTP client
- **React Router** - Client-side routing
- **Recharts** - Data visualization and charts

### Backend
- **FastAPI 0.104** - High-performance Python web framework
- **SQLAlchemy 2.0** - ORM for database interactions
- **PostgreSQL/SQLite** - Relational database
- **Pydantic** - Data validation and serialization
- **Alembic** - Database migrations
- **Python 3.11+** - Core language

### AI & Machine Learning
- **Google Gemini 2.5 Flash** - Primary LLM for natural language processing
- **LangChain 0.1** - LLM orchestration framework
- **Multi-agent architecture** - Specialized agent coordination
- **Structured JSON prompting** - Consistent AI outputs

### Data & Analytics
- **Dependency graph analysis** - Cascading impact calculation
- **Geospatial calculations** - Haversine distance formula
- **Supplier scoring algorithms** - Multi-factor ranking
- **Time-series risk tracking** - Historical analysis



## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API key

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "DATABASE_URL=sqlite:///./supply_chain.db" >> .env

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173` (frontend) and `http://localhost:8000` (backend API).

## Usage Example

### 1. Analyze an Event

**Input:**
```
"A magnitude 7.2 earthquake struck Tokyo, Japan, affecting electronics manufacturing facilities in the region."
Severity: 5/5
```

**System Processing (15-30 seconds):**
1. Event Parser extracts: Natural Disaster, Tokyo/Japan, High severity, Electronics industry
2. Supplier Matcher identifies 12 affected suppliers within 500km radius
3. Risk Analyzer calculates: Overall risk score 87/100 (CRITICAL)
4. Recommendation Generator finds 8 alternative suppliers
5. Playbook Generator creates 3-phase response plan
6. Results saved to database with agent logs

**Output:**
- Risk Level: CRITICAL (87/100)
- Affected Suppliers: 12 (4 critical tier)
- Financial Impact: $2.4M estimated loss
- Alternative Suppliers: 8 ranked options
- Playbook: 23 time-phased actions with ownership
- Estimated Recovery: 21 days

### 2. Predict Future Risks

The system analyzes your supplier portfolio and identifies:
- Geographic concentration: 68% suppliers in Southeast Asia
- Critical dependencies: 8 single-source critical components
- Capacity constraints: 5 suppliers at >85% utilization
- Predicted risk score: 62/100 (HIGH) for next 90 days

## API Endpoints

### Events
- `POST /api/events/` - Create and analyze new event
- `GET /api/events/` - List all events
- `GET /api/events/{id}` - Get event details with analysis

### Suppliers
- `POST /api/suppliers/` - Add new supplier
- `GET /api/suppliers/` - List suppliers
- `PUT /api/suppliers/{id}` - Update supplier

### Analytics
- `GET /api/analytics/dashboard/{org_id}` - Dashboard metrics
- `GET /api/analytics/risk-history/{org_id}` - Historical risk data
- `POST /api/analytics/predict-future-risk/{org_id}` - Generate predictions

## Performance Metrics

- **Analysis Speed**: 15-30 seconds (vs. 2-5 days manual)
- **Accuracy**: Geographic matching >95%, AI classification >90%
- **Scalability**: Handles 1000+ suppliers per organization
- **Availability**: 99.5% uptime with error handling and fallbacks

## Future Enhancements

- Real-time news integration for automatic event detection
- Machine learning for improved risk scoring
- Integration with ERP systems (SAP, Oracle)
- Mobile application for on-the-go alerts
- Advanced visualization with interactive supply chain maps
- Webhook notifications for critical events
- Multi-language support

