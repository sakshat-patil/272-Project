import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import google.generativeai as genai
from app.models import Supplier, Organization, SupplierTier, CriticalityLevel


class FutureRiskPredictorAgent:
    """
    Agent responsible for predicting future supply chain risks
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.agent_name = "Future Risk Predictor Agent"
    
    def predict_future_risks(
        self,
        db: Session,
        organization_id: int,
        prediction_period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Predict potential risks in the next 30/60/90 days
        """
        # Get organization data
        organization = db.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        
        if not organization:
            return {"success": False, "error": "Organization not found"}
        
        # Get all suppliers
        suppliers = db.query(Supplier).filter(
            Supplier.organization_id == organization_id
        ).all()
        
        # Analyze supplier portfolio
        risk_factors = self._analyze_supplier_portfolio(suppliers, organization)
        
        # Predict future risks using AI
        predicted_risks = self._generate_risk_predictions(
            organization,
            suppliers,
            risk_factors,
            prediction_period_days
        )
        
        # Calculate predicted risk score
        predicted_risk_score = self._calculate_predicted_risk_score(risk_factors)
        
        return {
            "success": True,
            "agent": self.agent_name,
            "prediction_period_days": prediction_period_days,
            "predicted_risk_score": predicted_risk_score,
            "risk_factors": risk_factors,
            "predictions": predicted_risks,
            "recommendations": self._generate_proactive_recommendations(risk_factors),
            "confidence_level": self._calculate_confidence_level(suppliers)
        }
    
    def _analyze_supplier_portfolio(
        self,
        suppliers: List[Supplier],
        organization: Organization
    ) -> List[Dict[str, Any]]:
        """
        Analyze supplier portfolio for risk factors
        """
        risk_factors = []
        
        # 1. Geographic concentration risk
        country_counts = {}
        for supplier in suppliers:
            country_counts[supplier.country] = country_counts.get(supplier.country, 0) + 1
        
        max_concentration = max(country_counts.values()) if country_counts else 0
        concentration_percentage = (max_concentration / len(suppliers) * 100) if suppliers else 0
        
        if concentration_percentage > 50:
            risk_factors.append({
                "risk_type": "Geographic Concentration",
                "severity": "high" if concentration_percentage > 70 else "medium",
                "description": f"{concentration_percentage:.0f}% of suppliers concentrated in {max(country_counts, key=country_counts.get)}",
                "likelihood": 0.6,
                "potential_impact": 75
            })
        
        # 2. Critical supplier dependency
        critical_suppliers = [s for s in suppliers if s.criticality == CriticalityLevel.CRITICAL]
        critical_percentage = (len(critical_suppliers) / len(suppliers) * 100) if suppliers else 0
        
        if critical_percentage > 20:
            risk_factors.append({
                "risk_type": "Critical Supplier Dependency",
                "severity": "high",
                "description": f"{len(critical_suppliers)} critical suppliers ({critical_percentage:.0f}% of portfolio)",
                "likelihood": 0.4,
                "potential_impact": 85
            })
        
        # 3. Tier 1 supplier concentration
        tier_1_suppliers = [s for s in suppliers if s.tier == SupplierTier.TIER_1]
        tier_1_percentage = (len(tier_1_suppliers) / len(suppliers) * 100) if suppliers else 0
        
        if tier_1_percentage > 60:
            risk_factors.append({
                "risk_type": "Tier 1 Concentration",
                "severity": "medium",
                "description": f"{tier_1_percentage:.0f}% of suppliers are Tier 1 (limited backup options)",
                "likelihood": 0.5,
                "potential_impact": 60
            })
        
        # 4. Low reliability suppliers
        low_reliability = [s for s in suppliers if s.reliability_score < 70]
        if len(low_reliability) > 0:
            risk_factors.append({
                "risk_type": "Supplier Reliability",
                "severity": "medium",
                "description": f"{len(low_reliability)} suppliers with reliability score <70",
                "likelihood": 0.7,
                "potential_impact": 50
            })
        
        # 5. High capacity utilization
        high_utilization = [s for s in suppliers if s.capacity_utilization > 85]
        if len(high_utilization) > 0:
            risk_factors.append({
                "risk_type": "Capacity Constraints",
                "severity": "medium",
                "description": f"{len(high_utilization)} suppliers operating at >85% capacity",
                "likelihood": 0.6,
                "potential_impact": 55
            })
        
        # 6. Long lead times
        long_lead_times = [s for s in suppliers if s.lead_time_days > 60]
        if len(long_lead_times) > 0:
            risk_factors.append({
                "risk_type": "Extended Lead Times",
                "severity": "low",
                "description": f"{len(long_lead_times)} suppliers with lead times >60 days",
                "likelihood": 0.3,
                "potential_impact": 40
            })
        
        return risk_factors
    
    def _generate_risk_predictions(
        self,
        organization: Organization,
        suppliers: List[Supplier],
        risk_factors: List[Dict[str, Any]],
        prediction_period_days: int
    ) -> List[Dict[str, Any]]:
        """
        Use AI to generate specific risk predictions
        """
        # Prepare context for AI
        supplier_summary = {
            "total_suppliers": len(suppliers),
            "countries": list(set(s.country for s in suppliers)),
            "industry": organization.industry.value,
            "risk_factors": [rf["risk_type"] for rf in risk_factors]
        }
        
        prompt = f"""
You are a supply chain risk prediction expert. Based on the following supplier portfolio, predict potential risks in the next {prediction_period_days} days.

Organization Industry: {organization.industry.value}
Supplier Portfolio Summary: {json.dumps(supplier_summary, indent=2)}

Identified Risk Factors: {json.dumps([rf["risk_type"] + ": " + rf["description"] for rf in risk_factors], indent=2)}

Generate predictions in JSON format:
{{
    "predictions": [
        {{
            "timeframe": "<e.g., 'Next 30 days', 'Next 60 days'>",
            "risk_scenario": "<description of potential risk>",
            "probability": <0.0-1.0>,
            "estimated_impact": "<low/medium/high/critical>",
            "early_warning_signs": ["<sign 1>", "<sign 2>"],
            "preventive_actions": ["<action 1>", "<action 2>"]
        }}
    ]
}}

Generate 3-5 realistic predictions. Return ONLY valid JSON.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            predictions_data = json.loads(response_text)
            return predictions_data.get("predictions", [])
        
        except Exception as e:
            # Fallback predictions
            return [
                {
                    "timeframe": f"Next {prediction_period_days} days",
                    "risk_scenario": "Potential disruption due to geographic concentration",
                    "probability": 0.4,
                    "estimated_impact": "medium",
                    "early_warning_signs": [
                        "Weather alerts in concentrated region",
                        "Political instability indicators"
                    ],
                    "preventive_actions": [
                        "Diversify supplier base",
                        "Increase safety stock"
                    ]
                }
            ]
    
    def _calculate_predicted_risk_score(self, risk_factors: List[Dict[str, Any]]) -> float:
        """
        Calculate overall predicted risk score based on risk factors
        """
        if not risk_factors:
            return 20.0  # Baseline low risk
        
        # Weight risk by likelihood and impact
        total_risk = 0
        for factor in risk_factors:
            likelihood = factor.get('likelihood', 0.5)
            impact = factor.get('potential_impact', 50)
            total_risk += likelihood * impact
        
        # Average and normalize to 0-100
        avg_risk = total_risk / len(risk_factors)
        return min(100, avg_risk)
    
    def _generate_proactive_recommendations(
        self,
        risk_factors: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate proactive recommendations based on risk factors
        """
        recommendations = []
        
        for factor in risk_factors:
            if factor['risk_type'] == "Geographic Concentration":
                recommendations.append({
                    "risk_addressed": "Geographic Concentration",
                    "recommendation": "Diversify supplier base across multiple regions",
                    "priority": "high",
                    "estimated_timeline": "3-6 months",
                    "expected_benefit": "Reduce geographic risk by 40-50%"
                })
            
            elif factor['risk_type'] == "Critical Supplier Dependency":
                recommendations.append({
                    "risk_addressed": "Critical Supplier Dependency",
                    "recommendation": "Establish backup suppliers for critical components",
                    "priority": "high",
                    "estimated_timeline": "1-3 months",
                    "expected_benefit": "Ensure business continuity"
                })
            
            elif factor['risk_type'] == "Capacity Constraints":
                recommendations.append({
                    "risk_addressed": "Capacity Constraints",
                    "recommendation": "Negotiate capacity reservations or identify additional suppliers",
                    "priority": "medium",
                    "estimated_timeline": "1-2 months",
                    "expected_benefit": "Ensure supply availability during demand spikes"
                })
            
            elif factor['risk_type'] == "Supplier Reliability":
                recommendations.append({
                    "risk_addressed": "Supplier Reliability",
                    "recommendation": "Implement supplier performance monitoring and improvement program",
                    "priority": "medium",
                    "estimated_timeline": "2-4 months",
                    "expected_benefit": "Improve overall supplier reliability by 15-20%"
                })
        
        # Add general recommendations
        recommendations.append({
            "risk_addressed": "General Supply Chain Resilience",
            "recommendation": "Implement supply chain visibility and monitoring system",
            "priority": "medium",
            "estimated_timeline": "3-6 months",
            "expected_benefit": "Early detection of potential disruptions"
        })
        
        return recommendations[:5]  # Return top 5
    
    def _calculate_confidence_level(self, suppliers: List[Supplier]) -> float:
        """
        Calculate confidence level of predictions based on data quality
        """
        if not suppliers:
            return 50.0
        
        # Factors that increase confidence
        confidence_score = 50  # Base confidence
        
        # More suppliers = more data = higher confidence
        if len(suppliers) > 20:
            confidence_score += 15
        elif len(suppliers) > 10:
            confidence_score += 10
        elif len(suppliers) > 5:
            confidence_score += 5
        
        # Geographic coordinates available
        with_coords = sum(1 for s in suppliers if s.latitude and s.longitude)
        coord_percentage = (with_coords / len(suppliers)) * 20
        confidence_score += coord_percentage
        
        # Reliability data available
        avg_reliability = sum(s.reliability_score for s in suppliers) / len(suppliers)
        if avg_reliability > 0:
            confidence_score += 15
        
        return min(100, confidence_score)