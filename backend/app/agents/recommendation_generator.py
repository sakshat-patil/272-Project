import json
from typing import List, Dict, Any
import google.generativeai as genai
from sqlalchemy.orm import Session
from app.models import Supplier
from app.services.supplier_scoring import rank_alternative_suppliers


class RecommendationGeneratorAgent:
    """
    Agent responsible for generating mitigation strategies and recommendations
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.agent_name = "Recommendation Generator Agent"
    
    def generate_recommendations(
        self,
        db: Session,
        organization_id: int,
        parsed_event: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        affected_suppliers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive mitigation recommendations
        """
        # Get alternative suppliers
        alternative_suppliers = self._find_alternative_suppliers(
            db,
            organization_id,
            affected_suppliers,
            parsed_event
        )
        
        # Generate strategic recommendations using AI
        strategic_recommendations = self._generate_strategic_recommendations(
            parsed_event,
            risk_analysis,
            affected_suppliers
        )
        
        return {
            "success": True,
            "agent": self.agent_name,
            "alternative_suppliers": alternative_suppliers,
            "strategic_recommendations": strategic_recommendations,
            "immediate_actions": self._generate_immediate_actions(affected_suppliers),
            "long_term_strategies": self._generate_long_term_strategies(risk_analysis)
        }
    
    def _find_alternative_suppliers(
        self,
        db: Session,
        organization_id: int,
        affected_suppliers: List[Dict[str, Any]],
        parsed_event: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Find and score alternative suppliers for each affected supplier
        """
        affected_ids = {s['supplier_id'] for s in affected_suppliers}
        
        # Get all suppliers in the organization
        all_suppliers = db.query(Supplier).filter(
            Supplier.organization_id == organization_id
        ).all()
        
        event_location = None
        event_loc_data = parsed_event.get('location', {})
        if event_loc_data.get('estimated_latitude') and event_loc_data.get('estimated_longitude'):
            event_location = (
                event_loc_data['estimated_latitude'],
                event_loc_data['estimated_longitude']
            )
        
        alternatives_by_supplier = {}
        
        for affected in affected_suppliers:
            affected_supplier = db.query(Supplier).filter(
                Supplier.id == affected['supplier_id']
            ).first()
            
            if not affected_supplier:
                continue
            
            # Find potential alternatives (same category, not affected)
            potential_alternatives = [
                s for s in all_suppliers
                if s.id not in affected_ids
                and s.category == affected_supplier.category
            ]
            
            if potential_alternatives:
                ranked_alternatives = rank_alternative_suppliers(
                    potential_alternatives,
                    affected_supplier,
                    event_location,
                    top_n=3
                )
                
                alternatives_by_supplier[affected['supplier_id']] = {
                    "affected_supplier_name": affected['supplier_name'],
                    "affected_supplier_id": affected['supplier_id'],
                    "category": affected['category'],
                    "alternatives": ranked_alternatives
                }
        
        return list(alternatives_by_supplier.values())
    
    def _generate_strategic_recommendations(
        self,
        parsed_event: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        affected_suppliers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Use AI to generate strategic recommendations
        """
        prompt = f"""Supply chain recommendations (no markdown):
Incident: {parsed_event.get('summary', 'Supply chain disruption')}
Risk: {risk_analysis.get('risk_level', 'MEDIUM')} ({risk_analysis.get('overall_risk_score', 50)}/100)
Affected: {len(affected_suppliers)} suppliers

JSON format:
{{
    "immediate_actions": [{{"action": "...", "priority": "high/medium/low", "timeline": "..."}}],
    "short_term_strategies": [{{"strategy": "...", "expected_impact": "...", "timeline": "1-7 days"}}],
    "long_term_improvements": [{{"improvement": "...", "rationale": "...", "timeline": "1+ months"}}],
    "contingency_plans": ["..."]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            recommendations = json.loads(response_text)
            return recommendations
        
        except Exception as e:
            pass
            # Fallback recommendations
            # return {
            #     "immediate_actions": [
            #         {"action": "Contact all affected suppliers to assess status", "priority": "high", "timeline": "0-24 hours"},
            #         {"action": "Review current inventory levels", "priority": "high", "timeline": "0-24 hours"},
            #         {"action": "Activate backup suppliers", "priority": "medium", "timeline": "24-48 hours"}
            #     ],
            #     "short_term_strategies": [
            #         {"strategy": "Expedite orders from alternative suppliers", "expected_impact": "Maintain production continuity", "timeline": "1-7 days"},
            #         {"strategy": "Adjust production schedule based on available materials", "expected_impact": "Optimize resource utilization", "timeline": "1-7 days"}
            #     ],
            #     "long_term_improvements": [
            #         {"improvement": "Diversify supplier base geographically", "rationale": "Reduce concentration risk", "timeline": "1+ months"},
            #         {"improvement": "Increase safety stock for critical components", "rationale": "Buffer against future disruptions", "timeline": "1+ months"}
            #     ],
            #     "contingency_plans": [
            #         "Establish secondary suppliers for all critical components",
            #         "Implement supplier monitoring and early warning system"
            #     ]
            # }
    
    def _generate_immediate_actions(self, affected_suppliers: List[Dict[str, Any]]) -> List[str]:
        """Generate immediate action items"""
        actions = [
            f"Contact {len(affected_suppliers)} affected suppliers immediately",
            "Assess current inventory levels for affected products",
            "Activate alternative sourcing plans"
        ]
        
        critical_count = len([s for s in affected_suppliers if s['criticality'] in ['Critical', 'High']])
        if critical_count > 0:
            actions.insert(0, f"URGENT: {critical_count} critical suppliers affected - escalate to executive team")
        
        return actions
    
    def _generate_long_term_strategies(self, risk_analysis: Dict[str, Any]) -> List[str]:
        """Generate long-term strategic improvements"""
        return [
            "Implement supplier diversification program",
            "Establish strategic inventory reserves",
            "Develop comprehensive business continuity plans",
            "Invest in supply chain visibility technology",
            "Create supplier relationship management program"
        ]