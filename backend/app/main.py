from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.routers import organizations, suppliers, events, predictions, risk_history, weather, auth, enhanced_data, monitoring
from app.services.weather_worker import start_weather_worker, stop_weather_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: Initialize database
    print("🚀 Starting Supply Chain Risk Monitor API...")
    init_db()
    print("✅ Database initialized")
    
    # Start weather monitoring worker
    await start_weather_worker()
    print("🌦️ Weather monitoring worker started")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    stop_weather_worker()
    print("🛑 Weather worker stopped")


# Create FastAPI app
app = FastAPI(
    title="Supply Chain Risk Monitor API",
    description="AI-powered supply chain risk analysis using multi-agent systems",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://main.dfvn6xpowx1mj.amplifyapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(suppliers.router)
app.include_router(events.router)
app.include_router(predictions.router)
app.include_router(risk_history.router)
app.include_router(weather.router)
app.include_router(enhanced_data.router)  # Tier 1 Enhanced APIs
app.include_router(monitoring.router)  # Monitoring & Logging


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Supply Chain Risk Monitor API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}