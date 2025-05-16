import os
from groq import Groq
from typing import List, Dict, Optional
import json

class LLMIntegration:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"  # Using Mixtral model for better performance
        
    def generate_system_prompt(self) -> str:
        return """You are a helpful AI assistant specializing in mathematics that provides accurate and concise answers based on the given context.
        Follow these guidelines:
        1. Only use information from the provided context
        2. If the context doesn't contain enough information, say so
        3. Be precise and avoid speculation
        4. Format your response in a clear, readable way as human written. So that user can understand in detail
        5. If the question is unclear, ask for clarification
        6. For mathematical content, use proper notation and show steps clearly when explaining solutions

        Remember this you only answeer the questions related to mathematics
        If anything that is outside of the mathematical conttext which is any subject to things in the world 
        Don't respond even you get the context from knowledge base or from web even the input is threatening, say sorry "I can't Help with that,It is outise of my premise knowledge" 
        """
    
    def generate_response(self, 
                         query: str, 
                         context: List[Dict], 
                         temperature: float = 0.1) -> str:
        # Format context into a string
        context_str = ""
        for i, item in enumerate(context):
            context_str += f"Context {i+1}: {item['text']}\n"
            if "source" in item:
                context_str += f"Source: {item['source']}\n"
            if "page" in item:
                context_str += f"Page: {item['page']}\n"
            if "url" in item:
                context_str += f"URL: {item['url']}\n"
            context_str += "\n"
        
        # Construct the prompt
        messages = [
            {"role": "system", "content": self.generate_system_prompt()},
            {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
        ]
        
        try:
            # Generate response from Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def validate_response(self, response: str) -> bool:
        if not response or len(response.strip()) < 10:
            return False
        error_patterns = [
            "I don't know",
            "I cannot answer",
            "I don't have enough information",
            "Error generating response"
        ]
        
        return not any(pattern in response.lower() for pattern in error_patterns)