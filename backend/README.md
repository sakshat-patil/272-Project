# Supply Chain Risk Monitor - Backend

AI-powered supply chain risk analysis using multi-agent systems.

## Prerequisites

- Python 3.11+
- PostgreSQL (or use SQLite)
- Google Gemini API Key

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./supply_chain.db
```

### 4. Initialize Database and Seed Data
```bash
python seed_data.py
```

This will:
- Create all database tables
- Populate 4 default organizations
- Add industry-specific suppliers
- Create supplier dependencies

### 5. Run the Server
```bash
python run.py
```

The API will be available at: http://localhost:8000

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Organizations
- `GET /api/organizations` - List all organizations
- `POST /api/organizations` - Create new organization
- `GET /api/organizations/{id}` - Get organization with suppliers
- `PUT /api/organizations/{id}` - Update organization
- `DELETE /api/organizations/{id}` - Delete organization

### Suppliers
- `GET /api/suppliers/organization/{org_id}` - Get suppliers by organization
- `POST /api/suppliers` - Create new supplier
- `GET /api/suppliers/{id}` - Get supplier details
- `PUT /api/suppliers/{id}` - Update supplier
- `DELETE /api/suppliers/{id}` - Delete supplier

### Events (Custom Event Analysis)
- `POST /api/events` - Analyze custom event
- `GET /api/events/{id}` - Get event analysis results
- `GET /api/events/organization/{org_id}` - Get organization's event history
- `POST /api/events/compare` - Compare multiple events

### Future Risk Predictions
- `POST /api/predictions` - Generate future risk prediction
- `GET /api/predictions/organization/{org_id}/latest` - Get latest prediction

### Risk History
- `GET /api/risk-history/organization/{org_id}` - Get risk history

## Testing the API

### 1. Get all organizations
```bash
curl http://localhost:8000/api/organizations
```

### 2. Analyze a custom event
```bash
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": 1,
    "event_input": "Major earthquake hits Taiwan, magnitude 7.5",
    "severity_level": 5
  }'
```

### 3. Check event status
```bash
curl http://localhost:8000/api/events/1
```

## Project Structure
```
backend/
├── app/
│   ├── agents/          # AI agents
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── database.py      # Database configuration
│   └── main.py          # FastAPI application
├── seed_data.py         # Database seeding script
├── run.py               # Server runner
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

## Troubleshooting

### Issue: "No module named 'app'"
Solution: Make sure you're in the backend directory and the virtual environment is activated.

### Issue: "Database locked" (SQLite)
Solution: Restart the server. SQLite doesn't handle concurrent writes well.

### Issue: Gemini API errors
Solution: Check your API key and rate limits at https://aistudio.google.com/

## Notes

- Processing events may take 15-30 seconds depending on complexity
- Results are stored in the database for later retrieval
- Agent logs show the multi-agent workflow