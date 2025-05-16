import os
from typing import List, Dict
import requests
from datetime import datetime

class WebSearch:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/v1/search"
        
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform a web search using Tavily API.
        
        """
        # Check if API key is available
        if not self.api_key:
            print("Warning: TAVILY_API_KEY not set. Web search functionality disabled.")
            return [{
                "title": "API Key Not Found",
                "text": "Web search is currently unavailable. Please ensure the TAVILY_API_KEY environment variable is set.",
                "url": "",
                "score": 0.0
            }]
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "max_results": max_results,
            "search_depth": "advanced",
            "include_answer": True,
            "include_raw_content": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            results = response.json()
            
            # Format results for consistency
            formatted_results = []
            for result in results.get("results", []):
                formatted_results.append({
                    "title": result.get("title", ""),
                    "text": result.get("content", ""),
                    "url": result.get("url", ""),
                    "score": result.get("score", 0.0),
                    "timestamp": datetime.now().isoformat()
                })
            
            return formatted_results
            
        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            if response.status_code == 404:
                error_message = "Tavily API endpoint not found. Please check if the API URL is correct."
            elif response.status_code == 401:
                error_message = "API key authentication failed. Please check your Tavily API key."
            elif response.status_code == 429:
                error_message = "Rate limit exceeded for Tavily API. Please try again later."
                
            print(f"Error performing web search: {error_message}")
            return [{
                "title": "Search Error",
                "text": f"Web search encountered an error: {error_message}. Falling back to knowledge base only.",
                "url": "",
                "score": 0.0
            }]
            
        except requests.exceptions.ConnectionError:
            error_message = "Connection error. Please check your internet connection."
            print(f"Error performing web search: {error_message}")
            return [{
                "title": "Connection Error",
                "text": f"Web search encountered a connection error. Please check your internet connection. Falling back to knowledge base only.",
                "url": "",
                "score": 0.0
            }]
            
        except Exception as e:
            print(f"Error performing web search: {str(e)}")
            return [{
                "title": "Search Error", 
                "text": f"Web search encountered an error: {str(e)}. Falling back to knowledge base only.",
                "url": "",
                "score": 0.0
            }]
    
    def validate_search_results(self, results: List[Dict]) -> bool:
        """
        Validate the search results.
        """
        if not results:
            return False
            
        # Check if results have required fields
        required_fields = ["title", "text", "url", "score"]
        return all(
            all(field in result for field in required_fields)
            for result in results
        )