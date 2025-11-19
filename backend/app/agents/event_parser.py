import os
import json
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class EventParserAgent:
    """
    Agent responsible for parsing and understanding incident events
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.agent_name = "Event Parser Agent"
    
    def parse_event(self, event_input: str, severity_level: int) -> Dict[str, Any]:
        """
        Parse natural language event description into structured data
        """
        prompt = f"""Parse this supply chain incident into JSON (no markdown):

Incident: {event_input}
Severity: {severity_level}/5

Return JSON:
{{
    "event_type": "Natural Disaster|Geopolitical|Labor Strike|Logistics|Economic|Cyber Security|Regulatory|Other",
    "location": {{"country": "...", "city": "...", "region": "...", "estimated_latitude": 0.0, "estimated_longitude": 0.0}},
    "severity_assessment": {{"level": {severity_level}, "description": "...", "estimated_duration": "...", "affected_radius_km": 0}},
    "key_industries_affected": ["..."],
    "summary": "...",
    "keywords": ["..."]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up response (remove markdown if present)
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            parsed_data = json.loads(response_text)
            
            return {
                "success": True,
                "agent": self.agent_name,
                "parsed_event": parsed_data,
                "raw_input": event_input
            }
        
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "agent": self.agent_name,
                "error": f"Failed to parse JSON: {str(e)}",
                "raw_response": response_text if 'response_text' in locals() else None
            }
        except Exception as e:
            return {
                "success": False,
                "agent": self.agent_name,
                "error": str(e)
            }