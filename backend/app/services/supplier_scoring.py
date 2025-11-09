from typing import List, Dict, Any
from math import radians, cos, sin, asin, sqrt
from app.models import Supplier, SupplierTier, CriticalityLevel


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on earth (in km)
    using the Haversine formula
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def score_alternative_supplier(
    alternative: Supplier,
    affected_supplier: Supplier,
    event_location: tuple = None
) -> Dict[str, Any]:
    """
    Score an alternative supplier based on multiple criteria
    Returns a score from 0-100 and breakdown of scoring
    """
    scores = {
        "geographic_distance": 0,
        "capacity_availability": 0,
        "reliability": 0,
        "lead_time": 0,
        "tier_match": 0
    }
    
    weights = {
        "geographic_distance": 0.25,
        "capacity_availability": 0.20,
        "reliability": 0.25,
        "lead_time": 0.20,
        "tier_match": 0.10
    }
    
    # 1. Geographic Distance Score (higher score = farther from incident)
    if event_location and alternative.latitude and alternative.longitude:
        event_lat, event_lon = event_location
        distance = calculate_distance(
            event_lat, event_lon,
            alternative.latitude, alternative.longitude
        )
        # Suppliers >2000km away get full score
        scores["geographic_distance"] = min(100, (distance / 2000) * 100)
    else:
        # If no coordinates, give moderate score if different country
        if alternative.country != affected_supplier.country:
            scores["geographic_distance"] = 70
        else:
            scores["geographic_distance"] = 30
    
    # 2. Capacity Availability (lower utilization = higher score)
    capacity_available = 100 - alternative.capacity_utilization
    scores["capacity_availability"] = capacity_available
    
    # 3. Reliability Score (direct mapping)
    scores["reliability"] = alternative.reliability_score
    
    # 4. Lead Time Score (shorter lead time = higher score)
    # Assume max acceptable lead time is 90 days
    lead_time_score = max(0, 100 - (alternative.lead_time_days / 90) * 100)
    scores["lead_time"] = lead_time_score
    
    # 5. Tier Match (same tier as affected supplier)
    if alternative.tier == affected_supplier.tier:
        scores["tier_match"] = 100
    elif abs(alternative.tier.value - affected_supplier.tier.value) == 1:
        scores["tier_match"] = 50
    else:
        scores["tier_match"] = 20
    
    # Calculate weighted total score
    total_score = sum(scores[key] * weights[key] for key in scores)
    
    return {
        "supplier_id": alternative.id,
        "supplier_name": alternative.name,
        "total_score": round(total_score, 2),
        "score_breakdown": {k: round(v, 2) for k, v in scores.items()},
        "details": {
            "country": alternative.country,
            "city": alternative.city,
            "category": alternative.category.value,
            "tier": alternative.tier.value,
            "lead_time_days": alternative.lead_time_days,
            "reliability_score": alternative.reliability_score,
            "capacity_utilization": alternative.capacity_utilization,
            "contact_info": alternative.contact_info
        }
    }


def rank_alternative_suppliers(
    alternatives: List[Supplier],
    affected_supplier: Supplier,
    event_location: tuple = None,
    top_n: int = 3
) -> List[Dict[str, Any]]:
    """
    Score and rank alternative suppliers
    """
    scored_alternatives = []
    
    for alt in alternatives:
        score_data = score_alternative_supplier(alt, affected_supplier, event_location)
        scored_alternatives.append(score_data)
    
    # Sort by total score descending
    scored_alternatives.sort(key=lambda x: x["total_score"], reverse=True)
    
    return scored_alternatives[:top_n]