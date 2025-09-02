import google.generativeai as genai
import json
import os

class VertexAIClient:
    def __init__(self, project_id="my-project-patchamomma", location="global"):
        api_key = os.getenv('GOOGLE_API_KEY', 'api_key')
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        genai.configure(api_key=api_key)
        self.model = "gemini-2.5-pro"
        
    def extract_requirements(self, json_data):
        """Extract functional and non-functional requirements from JSON data"""
        
        try:
            json_string = json.dumps(json_data, indent=2)
            
            # Truncate if too large
            if len(json_string) > 40000:
                json_string = json_string[:40000] + "\n... [truncated due to size]"
            
            prompt = f"""Analyze this healthcare data and generate requirements:

{json_string}

Functional Requirements:
* What the system should do

Non-Functional Requirements:
* How the system should perform
"""
            
            response = genai.generate_text(
                model=f"models/{self.model}",
                prompt=prompt,
                temperature=0.7,
                max_output_tokens=1000
            )
            return response.result
        except Exception as e:
            # Fallback mock response for testing
            return """Functional Requirements:
* User Authentication: The system should allow users to log in securely
* Data Processing: The system should process uploaded JSON files
* Report Generation: The system should generate requirement reports
* File Upload: The system should accept JSON file uploads

Non-Functional Requirements:
* Security: The system must protect user data and comply with healthcare regulations
* Performance: The system should process files within 30 seconds
* Usability: The system should have an intuitive web interface
* Reliability: The system should have 99% uptime"""