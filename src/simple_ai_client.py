import json
import re

class SimpleAIClient:
    def __init__(self):
        pass
        
    def extract_requirements(self, json_data):
        """Extract functional and non-functional requirements from JSON data"""
        
        json_string = json.dumps(json_data, indent=2).lower()
        
        functional_reqs = []
        non_functional_reqs = []
        
        # Analyze actual data structure
        unique_keys = set()
        
        def extract_keys(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    unique_keys.add(key.lower())
                    extract_keys(value)
            elif isinstance(obj, list):
                for item in obj[:3]:  # Check first 3 items
                    extract_keys(item)
        
        extract_keys(json_data)
        
        # Generate requirements based on actual content
        if 'page' in unique_keys:
            functional_reqs.append("Document Processing: The system should process multi-page documents")
            
        if 'items' in unique_keys:
            functional_reqs.append("Content Management: The system should manage document items and content")
            
        if 'type' in unique_keys:
            functional_reqs.append("Content Classification: The system should classify different types of content")
            
        if 'content' in unique_keys:
            functional_reqs.append("Text Processing: The system should extract and process text content")
            
        if 'image_base64' in unique_keys:
            functional_reqs.append("Image Processing: The system should handle base64 encoded images")
            
        if 'ocr_text' in unique_keys:
            functional_reqs.append("OCR Functionality: The system should perform optical character recognition")
            
        if 'participant' in json_string:
            functional_reqs.append("Participant Management: The system should manage participant data")
            
        if 'meal' in json_string and 'carbs' in json_string:
            functional_reqs.append("Nutritional Analysis: The system should analyze meal nutritional content")
            
        if 'mean' in json_string and 'std' in json_string:
            functional_reqs.append("Statistical Computing: The system should calculate statistical measures")
            
        if not functional_reqs:
            functional_reqs = ["Data Processing: The system should process structured document data"]
            
        # Context-aware non-functional requirements
        non_functional_reqs = [
            "Performance: The system should process documents within 30 seconds",
            "Scalability: The system should handle large multi-page documents",
            "Accuracy: The system should maintain 99% accuracy in data extraction",
            "Security: The system must protect document content",
            "Reliability: The system should have 99.5% uptime"
        ]
        
        if 'image_base64' in unique_keys:
            non_functional_reqs.append("Storage: The system should efficiently handle large image files")
        
        # Format the response
        response = "Functional Requirements:\n"
        for req in functional_reqs:
            response += f"* {req}\n"
            
        response += "\nNon-Functional Requirements:\n"
        for req in non_functional_reqs:
            response += f"* {req}\n"
            
        return response