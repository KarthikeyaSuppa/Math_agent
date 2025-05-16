#guardrails.py
import re
from typing import Tuple, List
import json

class Guardrails:
    def __init__(self):
        # Define patterns for potentially harmful content
        self.harmful_patterns = [
            r"(?i)(password|api key|secret|token)",
            r"(?i)(hack|exploit|vulnerability)",
            r"(?i)(illegal|unlawful|criminal)",
            r"(?i)(porn|adult|nsfw)",
            r"(?i)(hate|racist|sexist)",
        ]
        
        # Compile patterns
        self.patterns = [re.compile(pattern) for pattern in self.harmful_patterns]
        
    def validate_input(self, query: str) -> Tuple[bool, str]:
        """
        Validate user input for safety and appropriateness.
         """
        # Check for empty or too short queries
        if not query or len(query.strip()) < 3:
            return False, "Query is too short"
            
        # Check for harmful patterns
        for pattern in self.patterns:
            if pattern.search(query):
                return False, "Query contains potentially harmful content"
                
        # Check for maximum length
        if len(query) > 1000:
            return False, "Query is too long"
            
        return True, ""
        
    def validate_output(self, response: str) -> Tuple[bool, str]:
        """
        Validate LLM output for safety and appropriateness.
        """
        # Check for empty responses
        if not response or len(response.strip()) < 10:
            return False, "Response is too short"
            
        # Check for harmful patterns
        for pattern in self.patterns:
            if pattern.search(response):
                return False, "Response contains potentially harmful content"
                
        # Check for maximum length
        if len(response) > 5000:
            return False, "Response is too long"
            
        return True, ""
        
    def sanitize_input(self, query: str) -> str:
        # Remove any matches of harmful patterns
        sanitized = query
        for pattern in self.patterns:
            sanitized = pattern.sub("[REDACTED]", sanitized)
            
        return sanitized
        
    def validate_context(self, context: List[dict]) -> Tuple[bool, str]:
        if not context:
            return False, "No context retrieved"
            
        # Check each context item
        for item in context:
            if not isinstance(item, dict):
                return False, "Invalid context format"
                
            if "text" not in item:
                return False, "Missing text in context"
                
            # Validate text content
            is_valid, error = self.validate_output(item["text"])
            if not is_valid:
                return False, f"Invalid context content: {error}"
                
        return True, "" 