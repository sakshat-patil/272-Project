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
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.agent_name = "Event Parser Agent"
    
    def parse_event(self, event_input: str, severity_level: int) -> Dict[str, Any]:
        """
        Parse natural language event description into structured data
        """
        prompt = f"""
You are a supply chain risk analysis expert. Parse the following incident description and extract key details.

Incident Description: {event_input}
Severity Level (1-5): {severity_level}

Extract and return ONLY a valid JSON object with the following structure:
{{
    "event_type": "<one of: Natural Disaster, Geopolitical, Labor Strike, Logistics, Economic, Cyber Security, Regulatory, Other>",
    "location": {{
        "country": "<country name>",
        "city": "<city name if mentioned>",
        "region": "<broader region like 'East Asia', 'Europe'>",
        "estimated_latitude": <float or null>,
        "estimated_longitude": <float or null>
    }},
    "severity_assessment": {{
        "level": {severity_level},
        "description": "<brief description of severity>",
        "estimated_duration": "<e.g., '2-3 days', '1-2 weeks', '1+ month'>",
        "affected_radius_km": <estimated radius in km>
    }},
    "key_industries_affected": ["<industry1>", "<industry2>"],
    "summary": "<2-3 sentence summary of the incident>",
    "keywords": ["<keyword1>", "<keyword2>", "<keyword3>"]
}}

CRITICAL: Return ONLY the JSON object, no markdown, no explanations, no additional text.
"""
        
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