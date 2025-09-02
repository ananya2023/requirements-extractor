import re

class RequirementsParser:
    def __init__(self):
        pass
    
    def parse_requirements(self, ai_response):
        """Parse AI response to extract functional and non-functional requirements"""
        
        functional_requirements = []
        non_functional_requirements = []
        
        # Split the response into sections
        sections = ai_response.split('\n')
        
        current_section = None
        current_requirement = ""
        
        for line in sections:
            line = line.strip()
            
            # Check for section headers
            if 'functional requirements' in line.lower() and 'non-functional' not in line.lower():
                current_section = 'functional'
                continue
            elif 'non-functional requirements' in line.lower():
                current_section = 'non-functional'
                continue
            
            # Skip empty lines and headers
            if not line or line.startswith('#') or line.startswith('**'):
                continue
            
            # Process bullet points or numbered items
            if line.startswith('*') or line.startswith('-') or re.match(r'^\d+\.', line):
                if current_requirement:
                    # Save previous requirement
                    if current_section == 'functional':
                        functional_requirements.append(current_requirement.strip())
                    elif current_section == 'non-functional':
                        non_functional_requirements.append(current_requirement.strip())
                
                # Start new requirement
                current_requirement = line.lstrip('*-0123456789. ')
            else:
                # Continue current requirement
                if current_requirement:
                    current_requirement += " " + line
        
        # Don't forget the last requirement
        if current_requirement:
            if current_section == 'functional':
                functional_requirements.append(current_requirement.strip())
            elif current_section == 'non-functional':
                non_functional_requirements.append(current_requirement.strip())
        
        return {
            'functional': functional_requirements,
            'non_functional': non_functional_requirements
        }