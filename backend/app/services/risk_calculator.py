from typing import List, Dict, Any
from app.models import Supplier, CriticalityLevel, SupplierTier


CRITICALITY_WEIGHTS = {
    CriticalityLevel.LOW: 0.25,
    CriticalityLevel.MEDIUM: 0.50,
    CriticalityLevel.HIGH: 0.75,
    CriticalityLevel.CRITICAL: 1.0
}

TIER_MULTIPLIERS = {
    SupplierTier.TIER_1: 1.0,
    SupplierTier.TIER_2: 0.7,
    SupplierTier.TIER_3: 0.4
}


def calculate_supplier_impact_score(
    supplier: Supplier,
    severity_level: int,
    proximity_score: float = 1.0
) -> float:
    """
    Calculate impact score for a single supplier
    Score ranges from 0-100
    
    Args:
        supplier: Supplier object
        severity_level: Event severity (1-5)
        proximity_score: How close supplier is to incident (0-1)
    """
    # Base severity contribution (0-50 points)
    severity_contribution = (severity_level / 5) * 50
    
    # Criticality contribution (0-30 points)
    criticality_weight = CRITICALITY_WEIGHTS[supplier.criticality]
    criticality_contribution = criticality_weight * 30
    
    # Tier contribution (0-15 points)
    tier_multiplier = TIER_MULTIPLIERS[supplier.tier]
    tier_contribution = tier_multiplier * 15
    
    # Proximity contribution (0-5 points)
    proximity_contribution = proximity_score * 5
    
    # Total impact score
    impact_score = (
        severity_contribution +
        criticality_contribution +
        tier_contribution +
        proximity_contribution
    )
    
    return min(100, impact_score)


def calculate_overall_risk_score(
    affected_suppliers: List[Dict[str, Any]],
    total_suppliers: int
) -> float:
    """
    Calculate overall organizational risk score based on affected suppliers
    """
    if not affected_suppliers or total_suppliers == 0:
        return 0.0
    
    # Calculate weighted impact
    total_impact = sum(supplier["impact_score"] for supplier in affected_suppliers)
    
    # Calculate percentage of suppliers affected
    affected_percentage = len(affected_suppliers) / total_suppliers
    
    # Risk score considers both total impact and breadth of disruption
    risk_score = (total_impact / len(affected_suppliers)) * (0.7 + 0.3 * affected_percentage)
    
    return min(100, risk_score)


def calculate_cascading_impact(
    affected_suppliers: List[Supplier],
    all_suppliers: List[Supplier],
    dependencies: Dict[int, List[int]]
) -> List[Dict[str, Any]]:
    """
    Calculate cascading effects through supplier dependencies
    
    Args:
        affected_suppliers: Initially affected suppliers
        all_suppliers: All suppliers in organization
        dependencies: Dict mapping supplier_id to list of supplier_ids it depends on
    
    Returns:
        List of additionally affected suppliers with cascading impact scores
    """
    affected_ids = {s.id for s in affected_suppliers}
    cascading_affected = []
    
    # Check each supplier to see if it depends on affected suppliers
    for supplier in all_suppliers:
        if supplier.id in affected_ids:
            continue  # Already directly affected
        
        supplier_deps = dependencies.get(supplier.id, [])
        affected_deps = [dep_id for dep_id in supplier_deps if dep_id in affected_ids]
        
        if affected_deps:
            # Calculate cascading impact based on how many dependencies are affected
            impact_ratio = len(affected_deps) / len(supplier_deps)
            cascading_score = impact_ratio * 60  # Max 60 for cascading (lower than direct)
            
            cascading_affected.append({
                "supplier_id": supplier.id,
                "supplier_name": supplier.name,
                "cascading_impact_score": cascading_score,
                "affected_dependencies": affected_deps,
                "reason": f"Depends on {len(affected_deps)} affected supplier(s)"
            })
    
    return cascading_affected


def calculate_financial_impact(
    affected_suppliers: List[Dict[str, Any]],
    avg_order_value: float = 100000  # Default average order value
) -> Dict[str, Any]:
    """
    Estimate financial impact of supply chain disruption
    """
    total_suppliers = len(affected_suppliers)
    
    # Estimate daily revenue at risk
    daily_revenue_at_risk = total_suppliers * avg_order_value * 0.1  # 10% daily impact
    
    # Estimate costs
    expedited_shipping_cost = total_suppliers * 5000  # $5k per supplier
    alternative_sourcing_cost = total_suppliers * 10000  # $10k per supplier
    
    # Estimate timeline
    critical_count = sum(1 for s in affected_suppliers if s.get("criticality") == "Critical")
    estimated_resolution_days = 7 + (critical_count * 3)  # Base 7 days + 3 per critical
    
    total_estimated_loss = daily_revenue_at_risk * estimated_resolution_days
    total_mitigation_cost = expedited_shipping_cost + alternative_sourcing_cost
    
    return {
        "daily_revenue_at_risk": round(daily_revenue_at_risk, 2),
        "estimated_resolution_days": estimated_resolution_days,
        "total_estimated_loss": round(total_estimated_loss, 2),
        "expedited_shipping_cost": round(expedited_shipping_cost, 2),
        "alternative_sourcing_cost": round(alternative_sourcing_cost, 2),
        "total_mitigation_cost": round(total_mitigation_cost, 2),
        "net_impact": round(total_estimated_loss - total_mitigation_cost, 2)
    }