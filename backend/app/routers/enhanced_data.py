"""
API Router for Enhanced Data Sources
Provides endpoints for financial, shipping, geopolitical, and social media data
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from ..services.enhanced_feeds import (
    FinancialDataService,
    ShippingDataService,
    GeopoliticalRiskService,
    SocialMediaMonitor,
    EnhancedFeedAggregator
)
from .. import crud
from ..monitoring import monitor_api_call

router = APIRouter(prefix="/api/enhanced", tags=["Enhanced Data"])

# Pydantic models for request/response
class StockCheckRequest(BaseModel):
    ticker: str

class CommodityCheckRequest(BaseModel):
    commodities: List[str]

class PortCheckRequest(BaseModel):
    port_name: str

class ShippingRouteRequest(BaseModel):
    origin: str
    destination: str

class SanctionsCheckRequest(BaseModel):
    entity_name: str

class ConflictCheckRequest(BaseModel):
    country: str

class SupplierRiskRequest(BaseModel):
    supplier_id: int


# Financial Data Endpoints
@router.post("/financial/stock")
@monitor_api_call("enhanced_financial_stock")
async def get_stock_data(request: StockCheckRequest):
    """
    Get stock market data for a publicly traded supplier
    
    Example: {"ticker": "TSMC"}
    """
    service = FinancialDataService()
    data = await service.get_stock_data(request.ticker)
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    
    return data


@router.post("/financial/commodities")
@monitor_api_call("enhanced_financial_commodities")
async def get_commodity_prices(request: CommodityCheckRequest):
    """
    Get current commodity prices
    
    Example: {"commodities": ["oil", "copper", "lithium", "gold"]}
    """
    service = FinancialDataService()
    data = await service.get_commodity_prices(request.commodities)
    return data


@router.get("/financial/exchange-rates")
@monitor_api_call("enhanced_financial_exchange_rates")
async def get_exchange_rates(base_currency: str = "USD"):
    """
    Get current exchange rates
    
    Example: /api/enhanced/financial/exchange-rates?base_currency=USD
    """
    service = FinancialDataService()
    data = await service.get_exchange_rates(base_currency)
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    
    return data


# Shipping & Logistics Endpoints
@router.post("/shipping/port-status")
@monitor_api_call("enhanced_shipping_port_status")
async def check_port_status(request: PortCheckRequest):
    """
    Check current port congestion and delays
    
    Example: {"port_name": "Los Angeles"}
    """
    service = ShippingDataService()
    data = await service.check_port_status(request.port_name)
    return data


@router.post("/shipping/route-estimate")
async def get_shipping_route(request: ShippingRouteRequest):
    """
    Get shipping route estimate and current delays
    
    Example: {"origin": "Shanghai", "destination": "Los Angeles"}
    """
    service = ShippingDataService()
    data = await service.track_shipping_route(request.origin, request.destination)
    return data


@router.get("/shipping/major-ports")
@monitor_api_call("enhanced_shipping_major_ports")
async def get_major_ports_status():
    """
    Get status of major global ports
    """
    service = ShippingDataService()
    
    major_ports = ["Los Angeles", "Shanghai", "Rotterdam", "Singapore"]
    results = {}
    
    for port in major_ports:
        results[port] = await service.check_port_status(port)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "ports": results
    }


# Geopolitical Risk Endpoints
@router.post("/geopolitical/sanctions")
@monitor_api_call("enhanced_geopolitical_sanctions")
async def check_sanctions(request: SanctionsCheckRequest):
    """
    Check if entity is on sanctions lists
    
    Example: {"entity_name": "Company XYZ"}
    """
    service = GeopoliticalRiskService()
    data = await service.check_sanctions(request.entity_name)
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    
    return data


@router.post("/geopolitical/conflict")
async def get_conflict_data(request: ConflictCheckRequest):
    """
    Get conflict and political instability data for a country
    
    Example: {"country": "Ukraine"}
    """
    service = GeopoliticalRiskService()
    data = await service.get_conflict_data(request.country)
    return data


@router.get("/geopolitical/high-risk-countries")
@monitor_api_call("enhanced_geopolitical_high_risk")
async def get_high_risk_countries():
    """
    Get list of countries with heightened geopolitical risk
    """
    service = GeopoliticalRiskService()
    
    countries_to_check = ["Ukraine", "Israel", "Taiwan", "China", "Russia", "Iran"]
    results = {}
    
    for country in countries_to_check:
        results[country] = await service.get_conflict_data(country)
    
    # Sort by risk level
    high_risk = {k: v for k, v in results.items() if v.get("conflict_level", 0) >= 6}
    
    return {
        "timestamp": datetime.now().isoformat(),
        "high_risk_countries": high_risk,
        "all_countries": results
    }


# Social Media Endpoints
@router.get("/social/trends")
@monitor_api_call("enhanced_social_trends")
async def get_google_trends(keyword: str):
    """
    Check if a keyword is trending on Google
    
    Example: /api/enhanced/social/trends?keyword=TSMC
    """
    service = SocialMediaMonitor()
    data = await service.get_google_trends(keyword)
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    
    return data


# Comprehensive Risk Assessment
@router.post("/risk/comprehensive")
async def get_comprehensive_risk(request: SupplierRiskRequest, db: Session = Depends(get_db)):
    """
    Get comprehensive risk assessment for a supplier from all data sources
    
    Example: {"supplier_id": 1}
    """
    # Get supplier from database
    supplier = crud.get_supplier(db, request.supplier_id)
    
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Prepare supplier data for enhanced feed aggregator
    supplier_data = {
        "name": supplier.name,
        "country": supplier.country,
        "stock_ticker": None,  # Would need to add this field to supplier model
        "primary_port": None,  # Would need to add this field to supplier model
    }
    
    # Get comprehensive risk data
    aggregator = EnhancedFeedAggregator()
    risk_data = await aggregator.get_comprehensive_risk_data(supplier_data)
    
    return risk_data


@router.get("/risk/dashboard")
async def get_risk_dashboard(organization_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive risk dashboard for an organization
    
    Shows financial, shipping, geopolitical risks for all suppliers
    """
    # Get organization
    org = crud.get_organization(db, organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get all suppliers
    suppliers = crud.get_suppliers_by_organization(db, organization_id)
    
    # Aggregate risk data
    aggregator = EnhancedFeedAggregator()
    dashboard_data = {
        "organization": org.name,
        "timestamp": datetime.now().isoformat(),
        "supplier_count": len(suppliers),
        "risk_summary": {
            "financial_risks": 0,
            "shipping_delays": 0,
            "sanctions_alerts": 0,
            "geopolitical_risks": 0,
        },
        "suppliers": []
    }
    
    for supplier in suppliers:
        supplier_data = {
            "name": supplier.name,
            "country": supplier.country,
        }
        
        risk_data = await aggregator.get_comprehensive_risk_data(supplier_data)
        
        dashboard_data["suppliers"].append({
            "id": supplier.id,
            "name": supplier.name,
            "country": supplier.country,
            "aggregate_risk_score": risk_data.get("aggregate_risk_score", 0),
            "risk_data": risk_data.get("data_sources", {})
        })
        
        # Update summary counts
        if risk_data.get("data_sources", {}).get("sanctions", {}).get("sanctioned"):
            dashboard_data["risk_summary"]["sanctions_alerts"] += 1
        
        if risk_data.get("data_sources", {}).get("geopolitical", {}).get("conflict_level", 0) >= 6:
            dashboard_data["risk_summary"]["geopolitical_risks"] += 1
    
    return dashboard_data


# Test endpoints
@router.get("/test/all")
async def test_all_services():
    """
    Test all enhanced services with sample data
    Useful for verifying API integrations
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Test financial service
    try:
        financial = FinancialDataService()
        results["tests"]["stock_data"] = await financial.get_stock_data("AAPL")
        results["tests"]["commodities"] = await financial.get_commodity_prices(["oil", "gold"])
        results["tests"]["exchange_rates"] = await financial.get_exchange_rates()
    except Exception as e:
        results["tests"]["financial_error"] = str(e)
    
    # Test shipping service
    try:
        shipping = ShippingDataService()
        results["tests"]["port_status"] = await shipping.check_port_status("Los Angeles")
        results["tests"]["shipping_route"] = await shipping.track_shipping_route("Shanghai", "Los Angeles")
    except Exception as e:
        results["tests"]["shipping_error"] = str(e)
    
    # Test geopolitical service
    try:
        geopolitical = GeopoliticalRiskService()
        results["tests"]["sanctions"] = await geopolitical.check_sanctions("Test Company")
        results["tests"]["conflict"] = await geopolitical.get_conflict_data("USA")
    except Exception as e:
        results["tests"]["geopolitical_error"] = str(e)
    
    return results
