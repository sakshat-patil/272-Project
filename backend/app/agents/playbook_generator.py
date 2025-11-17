import json
from typing import Dict, Any, List
import google.generativeai as genai


class PlaybookGeneratorAgent:
    """
    Agent responsible for generating structured incident response playbooks
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.agent_name = "Playbook Generator Agent"
    
    def generate_playbook(
        self,
        parsed_event: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        recommendations: Dict[str, Any],
        affected_suppliers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive incident response playbook
        """
        playbook = {
            "playbook_id": f"PB-{parsed_event.get('summary', 'incident')[:20].replace(' ', '-')}",
            "incident_summary": parsed_event.get('summary', ''),
            "risk_level": risk_analysis.get('risk_level', 'MEDIUM'),
            "created_at": "auto-generated",
            "phases": self._generate_phases(
                parsed_event,
                risk_analysis,
                recommendations,
                affected_suppliers
            ),
            "success_metrics": self._generate_success_metrics(risk_analysis),
            "escalation_criteria": self._generate_escalation_criteria(risk_analysis),
            "communication_plan": self._generate_communication_plan(affected_suppliers)
        }
        
        return {
            "success": True,
            "agent": self.agent_name,
            "playbook": playbook
        }
    
    def _generate_phases(
        self,
        parsed_event: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        recommendations: Dict[str, Any],
        affected_suppliers: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate time-phased action plans
        """
        phases = []
        
        # Phase 1: Day 1 (0-24 hours)
        day_1_actions = [
            {
                "action": "Activate incident response team",
                "owner": "Supply Chain Manager",
                "status": "pending",
                "priority": "critical"
            },
            {
                "action": f"Contact all {len(affected_suppliers)} affected suppliers",
                "owner": "Procurement Team",
                "status": "pending",
                "priority": "critical"
            },
            {
                "action": "Assess current inventory levels",
                "owner": "Inventory Manager",
                "status": "pending",
                "priority": "high"
            },
            {
                "action": "Review production schedule and identify at-risk orders",
                "owner": "Production Manager",
                "status": "pending",
                "priority": "high"
            }
        ]
        
        # Add immediate actions from recommendations
        immediate = recommendations.get('strategic_recommendations', {}).get('immediate_actions', [])
        for item in immediate[:3]:
            if isinstance(item, dict):
                day_1_actions.append({
                    "action": item.get('action', ''),
                    "owner": "Response Team",
                    "status": "pending",
                    "priority": item.get('priority', 'medium')
                })
        
        phases.append({
            "phase": "Day 1: Immediate Response",
            "timeline": "0-24 hours",
            "objective": "Assess situation and activate response protocols",
            "actions": day_1_actions
        })
        
        # Phase 2: Week 1 (1-7 days)
        week_1_actions = [
            {
                "action": "Activate alternative suppliers",
                "owner": "Procurement Team",
                "status": "pending",
                "priority": "high"
            },
            {
                "action": "Expedite orders from backup suppliers",
                "owner": "Procurement Team",
                "status": "pending",
                "priority": "high"
            },
            {
                "action": "Adjust production schedule based on material availability",
                "owner": "Production Manager",
                "status": "pending",
                "priority": "medium"
            },
            {
                "action": "Communicate timeline updates to customers",
                "owner": "Customer Service",
                "status": "pending",
                "priority": "medium"
            }
        ]
        
        # Add short-term strategies
        short_term = recommendations.get('strategic_recommendations', {}).get('short_term_strategies', [])
        for item in short_term[:2]:
            if isinstance(item, dict):
                week_1_actions.append({
                    "action": item.get('strategy', ''),
                    "owner": "Operations Team",
                    "status": "pending",
                    "priority": "medium"
                })
        
        phases.append({
            "phase": "Week 1: Mitigation & Recovery",
            "timeline": "1-7 days",
            "objective": "Implement mitigation strategies and restore operations",
            "actions": week_1_actions
        })
        
        # Phase 3: Month 1 (1-4 weeks)
        month_1_actions = [
            {
                "action": "Monitor supplier recovery progress",
                "owner": "Supply Chain Manager",
                "status": "pending",
                "priority": "medium"
            },
            {
                "action": "Evaluate alternative supplier performance",
                "owner": "Procurement Team",
                "status": "pending",
                "priority": "medium"
            },
            {
                "action": "Conduct lessons learned session",
                "owner": "Leadership Team",
                "status": "pending",
                "priority": "low"
            },
            {
                "action": "Update risk mitigation plans",
                "owner": "Risk Manager",
                "status": "pending",
                "priority": "low"
            }
        ]
        
        # Add long-term improvements
        long_term = recommendations.get('strategic_recommendations', {}).get('long_term_improvements', [])
        for item in long_term[:2]:
            if isinstance(item, dict):
                month_1_actions.append({
                    "action": item.get('improvement', ''),
                    "owner": "Strategy Team",
                    "status": "pending",
                    "priority": "low"
                })
        
        phases.append({
            "phase": "Month 1: Recovery & Improvement",
            "timeline": "1-4 weeks",
            "objective": "Return to normal operations and implement improvements",
            "actions": month_1_actions
        })
        
        return phases
    
    def _generate_success_metrics(self, risk_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Define success metrics for the response
        """
        return [
            {
                "metric": "Supplier Contact Rate",
                "target": "100% within 24 hours",
                "importance": "critical"
            },
            {
                "metric": "Production Continuity",
                "target": "Maintain >80% capacity",
                "importance": "high"
            },
            {
                "metric": "Alternative Supplier Activation",
                "target": "Within 48 hours",
                "importance": "high"
            },
            {
                "metric": "Customer Order Fulfillment",
                "target": ">95% on-time delivery",
                "importance": "medium"
            },
            {
                "metric": "Risk Score Reduction",
                "target": f"Reduce from {risk_analysis.get('overall_risk_score', 0):.0f} to <40",
                "importance": "medium"
            }
        ]
    
    def _generate_escalation_criteria(self, risk_analysis: Dict[str, Any]) -> List[str]:
        """
        Define when to escalate the incident
        """
        criteria = [
            "More than 50% of critical suppliers are affected",
            "Production stoppage exceeds 48 hours",
            "Customer commitments cannot be met",
            "Financial impact exceeds $1M",
            "Incident duration extends beyond 2 weeks"
        ]
        
        if risk_analysis.get('risk_level') == 'CRITICAL':
            criteria.insert(0, "IMMEDIATE ESCALATION: Critical risk level detected")
        
        return criteria
    
    def _generate_communication_plan(self, affected_suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate communication plan for stakeholders
        """
        return {
            "internal_stakeholders": [
                {
                    "stakeholder": "Executive Leadership",
                    "frequency": "Daily updates",
                    "method": "Email + Status Dashboard",
                    "key_info": ["Overall status", "Risk level", "Financial impact"]
                },
                {
                    "stakeholder": "Operations Team",
                    "frequency": "Real-time updates",
                    "method": "Slack/Teams channel",
                    "key_info": ["Supplier status", "Production impacts", "Action items"]
                },
                {
                    "stakeholder": "Sales & Customer Service",
                    "frequency": "As needed",
                    "method": "Email briefs",
                    "key_info": ["Customer impact", "Delivery timelines", "Talking points"]
                }
            ],
            "external_stakeholders": [
                {
                    "stakeholder": "Affected Suppliers",
                    "frequency": "Daily contact",
                    "method": "Phone/Email",
                    "key_info": ["Status updates", "Support needed", "Recovery timeline"]
                },
                {
                    "stakeholder": "Key Customers",
                    "frequency": "As needed",
                    "method": "Direct contact",
                    "key_info": ["Order status", "Delivery impacts", "Mitigation actions"]
                }
            ],
            "communication_templates": {
                "executive_summary": "Daily incident status report template",
                "customer_notification": "Customer impact notification template",
                "supplier_inquiry": "Supplier status inquiry template"
            }
        }