from typing import Dict, Any
from sqlalchemy.orm import Session
import time
from datetime import datetime
import traceback

from app.agents.event_parser import EventParserAgent
from app.agents.supplier_matcher import SupplierMatcherAgent
from app.agents.risk_analyzer import RiskAnalyzerAgent
from app.agents.recommendation_generator import RecommendationGeneratorAgent
from app.agents.playbook_generator import PlaybookGeneratorAgent
from app.agents.future_risk_predictor import FutureRiskPredictorAgent
from app.services.dependency_analyzer import (
    build_dependency_graph,
    find_downstream_impact
)
from app.models import Supplier
from app import crud, schemas


class AgentOrchestrator:
    """
    Orchestrates the multi-agent workflow for event analysis
    """
    
    def __init__(self):
        self.event_parser = EventParserAgent()
        self.supplier_matcher = SupplierMatcherAgent()
        self.risk_analyzer = RiskAnalyzerAgent()
        self.recommendation_generator = RecommendationGeneratorAgent()
        self.playbook_generator = PlaybookGeneratorAgent()
        self.future_risk_predictor = FutureRiskPredictorAgent()
    
    async def process_event(
        self,
        db: Session,
        event_id: int,
        organization_id: int,
        event_input: str,
        severity_level: int
    ) -> Dict[str, Any]:
        """
        Main orchestration method - processes event through all agents
        """
        start_time = time.time()
        agent_logs = []
        
        try:
            # Update event status
            crud.update_event(db, event_id, processing_status="processing")
            
            # Step 1: Parse Event
            print(f"🤖 Step 1: Parsing event...")
            log_entry = {"agent": "Event Parser", "status": "processing", "timestamp": datetime.utcnow().isoformat()}
            agent_logs.append(log_entry)
            
            try:
                parse_result = self.event_parser.parse_event(event_input, severity_level)
                print(f"✅ Parse result: {parse_result.get('success')}")
                
                if not parse_result.get("success"):
                    error_msg = parse_result.get('error', 'Unknown parsing error')
                    print(f"❌ Parsing failed: {error_msg}")
                    raise Exception(f"Event parsing failed: {error_msg}")
                
                parsed_event = parse_result["parsed_event"]
                log_entry["status"] = "completed"
                log_entry["output"] = "Event successfully parsed"
                
                # Update event with parsed data
                crud.update_event(
                    db,
                    event_id,
                    parsed_event=parsed_event,
                    event_type=parsed_event.get("event_type"),
                    location=f"{parsed_event.get('location', {}).get('city', '')}, {parsed_event.get('location', {}).get('country', '')}",
                    description=parsed_event.get("summary")
                )
            except Exception as e:
                print(f"❌ Error in Step 1: {str(e)}")
                log_entry["status"] = "failed"
                log_entry["error"] = str(e)
                raise
            
            # Step 2: Find Affected Suppliers
            print(f"🤖 Step 2: Finding affected suppliers...")
            log_entry = {"agent": "Supplier Matcher", "status": "processing", "timestamp": datetime.utcnow().isoformat()}
            agent_logs.append(log_entry)
            
            try:
                suppliers = crud.get_suppliers_by_organization(db, organization_id)
                print(f"📊 Total suppliers: {len(suppliers)}")
                
                matcher_result = self.supplier_matcher.find_affected_suppliers(
                    parsed_event,
                    suppliers,
                    severity_level
                )
                
                affected_suppliers = matcher_result["affected_suppliers"]
                print(f"✅ Found {len(affected_suppliers)} affected suppliers")
                log_entry["status"] = "completed"
                log_entry["output"] = f"Found {len(affected_suppliers)} affected suppliers"
            except Exception as e:
                print(f"❌ Error in Step 2: {str(e)}")
                log_entry["status"] = "failed"
                log_entry["error"] = str(e)
                raise
            
            # Step 3: Analyze Cascading Effects
            print(f"🤖 Step 3: Analyzing cascading effects...")
            try:
                dependency_graph = build_dependency_graph(db, organization_id)
                affected_ids = {s["supplier_id"] for s in affected_suppliers}
                cascading_ids = find_downstream_impact(affected_ids, dependency_graph)
                
                cascading_suppliers = []
                if cascading_ids:
                    for supp_id in cascading_ids:
                        supplier = crud.get_supplier(db, supp_id)
                        if supplier:
                            cascading_suppliers.append({
                                "supplier_id": supplier.id,
                                "supplier_name": supplier.name,
                                "country": supplier.country,
                                "tier": supplier.tier.value,
                                "reason": "Cascading impact from affected dependencies"
                            })
                print(f"✅ Found {len(cascading_suppliers)} cascading impacts")
            except Exception as e:
                print(f"⚠️ Warning in Step 3: {str(e)} - Continuing without cascading analysis")
                cascading_suppliers = []
            
            # Step 4: Risk Analysis
            print(f"🤖 Step 4: Analyzing risk...")
            log_entry = {"agent": "Risk Analyzer", "status": "processing", "timestamp": datetime.utcnow().isoformat()}
            agent_logs.append(log_entry)
            
            try:
                risk_result = self.risk_analyzer.analyze_risk(
                    parsed_event,
                    affected_suppliers,
                    len(suppliers),
                    severity_level,
                    cascading_suppliers
                )
                
                print(f"✅ Risk score: {risk_result['overall_risk_score']:.2f}")
                log_entry["status"] = "completed"
                log_entry["output"] = f"Risk Score: {risk_result['overall_risk_score']:.2f}/100"
            except Exception as e:
                print(f"❌ Error in Step 4: {str(e)}")
                log_entry["status"] = "failed"
                log_entry["error"] = str(e)
                raise
            
            # Step 5: Generate Recommendations
            print(f"🤖 Step 5: Generating recommendations...")
            log_entry = {"agent": "Recommendation Generator", "status": "processing", "timestamp": datetime.utcnow().isoformat()}
            agent_logs.append(log_entry)
            
            try:
                recommendation_result = self.recommendation_generator.generate_recommendations(
                    db,
                    organization_id,
                    parsed_event,
                    risk_result,
                    affected_suppliers
                )
                
                alt_count = len(recommendation_result.get('alternative_suppliers', []))
                print(f"✅ Generated {alt_count} alternative recommendations")
                log_entry["status"] = "completed"
                log_entry["output"] = f"Generated {alt_count} alternative supplier recommendations"
            except Exception as e:
                print(f"❌ Error in Step 5: {str(e)}")
                log_entry["status"] = "failed"
                log_entry["error"] = str(e)
                raise
            
            # Step 6: Generate Playbook
            print(f"🤖 Step 6: Generating playbook...")
            log_entry = {"agent": "Playbook Generator", "status": "processing", "timestamp": datetime.utcnow().isoformat()}
            agent_logs.append(log_entry)
            
            try:
                playbook_result = self.playbook_generator.generate_playbook(
                    parsed_event,
                    risk_result,
                    recommendation_result,
                    affected_suppliers
                )
                
                print(f"✅ Playbook generated")
                log_entry["status"] = "completed"
                log_entry["output"] = "Incident response playbook generated"
            except Exception as e:
                print(f"❌ Error in Step 6: {str(e)}")
                log_entry["status"] = "failed"
                log_entry["error"] = str(e)
                raise
            
            # Calculate processing time
            processing_time = time.time() - start_time
            print(f"✅ Total processing time: {processing_time:.2f}s")
            
            # Update event with all results
            crud.update_event(
                db,
                event_id,
                affected_supplier_count=len(affected_suppliers),
                overall_risk_score=risk_result["overall_risk_score"],
                affected_suppliers=affected_suppliers,
                risk_analysis=risk_result,
                recommendations=recommendation_result,
                alternative_suppliers=recommendation_result.get("alternative_suppliers", []),
                playbook=playbook_result["playbook"],
                agent_logs=agent_logs,
                processing_status="completed",
                processing_time_seconds=processing_time,
                completed_at=datetime.utcnow()
            )
            
            # Update organization risk score - FIXED VERSION
            print(f"📊 Updating organization risk score...")
            try:
                organization = crud.get_organization(db, organization_id)
                if organization:
                    # Direct update without using Pydantic model
                    organization.current_risk_score = risk_result["overall_risk_score"]
                    organization.updated_at = datetime.utcnow()
                    db.commit()
                    db.refresh(organization)
                    print(f"✅ Organization risk score updated to {risk_result['overall_risk_score']:.2f}")
                    
                    # Add to risk history - FIXED VERSION
                    print(f"📝 Adding to risk history...")
                    risk_history_data = schemas.RiskHistoryCreate(
                        organization_id=organization_id,
                        risk_score=risk_result["overall_risk_score"],
                        event_id=event_id,
                        notes=f"Risk analysis for: {event_input[:100]}"
                    )
                    crud.create_risk_history(db, risk_history_data)
                    print(f"✅ Risk history recorded")
            except Exception as e:
                print(f"⚠️ Warning updating organization: {str(e)}")
                # Don't fail the whole process if this fails
            
            print(f"🎉 Event processing completed successfully!")
            return {
                "success": True,
                "event_id": event_id,
                "processing_time_seconds": processing_time,
                "agent_logs": agent_logs,
                "results": {
                    "parsed_event": parsed_event,
                    "affected_suppliers": affected_suppliers,
                    "cascading_suppliers": cascading_suppliers,
                    "risk_analysis": risk_result,
                    "recommendations": recommendation_result,
                    "playbook": playbook_result["playbook"]
                }
            }
        
        except Exception as e:
            # Handle failure
            processing_time = time.time() - start_time
            error_detail = traceback.format_exc()
            
            print(f"❌ Event processing failed: {str(e)}")
            print(f"📝 Full error trace:\n{error_detail}")
            
            crud.update_event(
                db,
                event_id,
                processing_status="failed",
                processing_time_seconds=processing_time,
                agent_logs=agent_logs + [{
                    "agent": "Orchestrator",
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }]
            )
            
            return {
                "success": False,
                "event_id": event_id,
                "error": str(e),
                "agent_logs": agent_logs
            }
    
    async def predict_future_risks(
        self,
        db: Session,
        organization_id: int,
        prediction_period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Generate future risk predictions for an organization
        """
        try:
            result = self.future_risk_predictor.predict_future_risks(
                db,
                organization_id,
                prediction_period_days
            )
            
            if result.get("success"):
                # Save prediction to database
                prediction_data = {
                    "organization_id": organization_id,
                    "prediction_period_days": prediction_period_days,
                    "predicted_risk_score": result["predicted_risk_score"],
                    "risk_factors": result["risk_factors"],
                    "recommendations": result["recommendations"],
                    "confidence_level": result["confidence_level"]
                }
                
                crud.create_future_prediction(db, prediction_data)
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }