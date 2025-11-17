import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import google.generativeai as genai
from app.models import Supplier
from app.services.supplier_scoring import calculate_distance


class SupplierMatcherAgent:
    """
    Agent responsible for identifying which suppliers are affected by an incident
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.agent_name = "Supplier Matcher Agent"
    
    def find_affected_suppliers(
        self,
        parsed_event: Dict[str, Any],
        suppliers: List[Supplier],
        severity_level: int
    ) -> Dict[str, Any]:
        """
        Identify which suppliers are affected by the incident
        """
        # Extract event details
        event_location = parsed_event.get("location", {})
        event_country = event_location.get("country", "")
        event_city = event_location.get("city", "")
        event_lat = event_location.get("estimated_latitude")
        event_lon = event_location.get("estimated_longitude")
        affected_radius = parsed_event.get("severity_assessment", {}).get("affected_radius_km", 500)
        
        affected_suppliers = []
        
        for supplier in suppliers:
            is_affected = False
            proximity_score = 0.0
            reason = ""
            
            # Check 1: Exact country match
            if supplier.country.lower() == event_country.lower():
                is_affected = True
                proximity_score = 0.8
                reason = f"Located in affected country: {event_country}"
                
                # Check 2: Exact city match (higher impact)
                if event_city and supplier.city and supplier.city.lower() == event_city.lower():
                    proximity_score = 1.0
                    reason = f"Located in directly affected city: {event_city}"
            
            # Check 3: Geographic proximity (if coordinates available)
            if event_lat and event_lon and supplier.latitude and supplier.longitude:
                distance = calculate_distance(
                    event_lat, event_lon,
                    supplier.latitude, supplier.longitude
                )
                
                if distance <= affected_radius:
                    is_affected = True
                    proximity_score = max(proximity_score, 1.0 - (distance / affected_radius))
                    reason = f"Within {int(distance)}km of incident (radius: {affected_radius}km)"
            
            # Check 4: Industry-specific impact using AI
            if not is_affected:
                industry_affected = self._check_industry_impact(
                    parsed_event,
                    supplier
                )
                if industry_affected:
                    is_affected = True
                    proximity_score = 0.5
                    reason = industry_affected
            
            if is_affected:
                affected_suppliers.append({
                    "supplier_id": supplier.id,
                    "supplier_name": supplier.name,
                    "country": supplier.country,
                    "city": supplier.city,
                    "category": supplier.category.value,
                    "criticality": supplier.criticality.value,
                    "tier": supplier.tier.value,
                    "proximity_score": round(proximity_score, 2),
                    "impact_reason": reason,
                    "lead_time_days": supplier.lead_time_days,
                    "reliability_score": supplier.reliability_score
                })
        
        return {
            "success": True,
            "agent": self.agent_name,
            "affected_count": len(affected_suppliers),
            "affected_suppliers": affected_suppliers,
            "analysis_notes": f"Found {len(affected_suppliers)} suppliers affected out of {len(suppliers)} total"
        }
    
    def _check_industry_impact(self, parsed_event: Dict[str, Any], supplier: Supplier) -> str:
        """
        Use AI to determine if supplier's industry is affected by the incident
        """
        industries_affected = parsed_event.get("key_industries_affected", [])
        supplier_category = supplier.category.value
        
        # Simple keyword matching
        for industry in industries_affected:
            if industry.lower() in supplier_category.lower() or supplier_category.lower() in industry.lower():
                return f"Industry affected: {industry}"
        
        return ""