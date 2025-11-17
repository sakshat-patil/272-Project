import json
from typing import List, Dict, Any
import google.generativeai as genai


class RiskAnalyzerAgent:
    """
    Agent responsible for analyzing risk levels and business impact
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.agent_name = "Risk Analyzer Agent"
    
    def analyze_risk(
        self,
        parsed_event: Dict[str, Any],
        affected_suppliers: List[Dict[str, Any]],
        total_suppliers: int,
        severity_level: int,
        cascading_suppliers: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis
        """
        # Simple impact score calculation
        for supplier in affected_suppliers:
            # Base score from severity
            base_score = (severity_level / 5) * 50
            
            # Criticality bonus
            crit = supplier.get('criticality', 'Medium')
            crit_bonus = {
                'Low': 10,
                'Medium': 20,
                'High': 30,
                'Critical': 40
            }.get(crit, 20)
            
            # Tier bonus
            tier = supplier.get('tier', 1)
            tier_bonus = {1: 15, 2: 10, 3: 5}.get(tier, 10)
            
            # Proximity bonus
            proximity = supplier.get('proximity_score', 0.5)
            proximity_bonus = proximity * 10
            
            impact_score = base_score + crit_bonus + tier_bonus + proximity_bonus
            supplier['impact_score'] = round(min(100, impact_score), 2)
        
        # Sort by impact
        affected_suppliers.sort(key=lambda x: x.get('impact_score', 0), reverse=True)
        
        # Calculate overall risk
        if affected_suppliers:
            avg_impact = sum(s['impact_score'] for s in affected_suppliers) / len(affected_suppliers)
            affected_pct = len(affected_suppliers) / max(total_suppliers, 1)
            overall_risk = avg_impact * (0.7 + 0.3 * affected_pct)
        else:
            overall_risk = 0.0
        
        overall_risk = round(min(100, overall_risk), 2)
        
        # Critical suppliers
        critical_suppliers = [
            s for s in affected_suppliers
            if s.get('criticality') in ['Critical', 'High']
        ]
        
        # Financial impact
        financial_impact = {
            "daily_revenue_at_risk": len(affected_suppliers) * 10000,
            "estimated_resolution_days": 7 + len(critical_suppliers) * 3,
            "total_estimated_loss": len(affected_suppliers) * 10000 * (7 + len(critical_suppliers) * 3),
            "expedited_shipping_cost": len(affected_suppliers) * 5000,
            "alternative_sourcing_cost": len(affected_suppliers) * 10000,
            "total_mitigation_cost": len(affected_suppliers) * 15000,
            "net_impact": (len(affected_suppliers) * 10000 * (7 + len(critical_suppliers) * 3)) - (len(affected_suppliers) * 15000)
        }
        
        # Risk summary
        risk_summary = {
            "executive_summary": f"Supply chain disruption affecting {len(affected_suppliers)} suppliers with overall risk score of {overall_risk}/100.",
            "top_3_concerns": [
                f"{len(affected_suppliers)} suppliers in affected region",
                f"{len(critical_suppliers)} critical suppliers impacted",
                "Potential production delays and increased costs"
            ],
            "immediate_priorities": [
                "Contact affected suppliers for status updates",
                "Assess current inventory levels",
                "Activate backup suppliers"
            ],
            "estimated_timeline": f"{7 + len(critical_suppliers) * 3} days for recovery"
        }
        
        return {
            "success": True,
            "agent": self.agent_name,
            "overall_risk_score": overall_risk,
            "risk_level": self._categorize_risk_level(overall_risk),
            "affected_suppliers": affected_suppliers,
            "critical_suppliers": critical_suppliers,
            "cascading_affected": cascading_suppliers or [],
            "financial_impact": financial_impact,
            "risk_summary": risk_summary,
            "key_metrics": {
                "total_affected": len(affected_suppliers),
                "critical_affected": len(critical_suppliers),
                "average_impact_score": round(
                    sum(s['impact_score'] for s in affected_suppliers) / len(affected_suppliers), 2
                ) if affected_suppliers else 0,
                "tier_1_affected": len([s for s in affected_suppliers if s.get('tier') == 1])
            }
        }
    
    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize risk score into levels"""
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        elif risk_score >= 20:
            return "LOW"
        else:
            return "MINIMAL"