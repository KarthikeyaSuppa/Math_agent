import os
import requests
from typing import List, Dict
from datetime import datetime
import logging

# Configure simple logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        """Initialize the WebSearch class."""
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"
        
        # Math-focused domains to include
        self.math_domains = [
            "mathworld.wolfram.com",
            "khanacademy.org", 
            "math.stackexchange.com", 
            "brilliant.org",
            "purplemath.com"
            # Excluding "en.wikipedia.org" as requested
        ]
        
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform a web search using Tavily API, focusing on math resources.
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of search results with relevant information
        """
        # Check if API key is available
        if not self.api_key:
            logger.warning("TAVILY_API_KEY not set. Web search functionality disabled.")
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
        
        # Enhance the query to focus on math solutions
        math_query = f"mathematics problem solution: {query}"
        
        payload = {
            "query": math_query,
            "max_results": max_results,
            "search_depth": "advanced",
            "include_answer": True,
            "include_domains": self.math_domains
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            
            # Format results for consistency
            formatted_results = []
            for result in results.get("results", []):
                formatted_results.append({
                    "title": result.get("title", ""),
                    "text": result.get("content", ""),  # API returns 'content' but we map to 'text'
                    "url": result.get("url", ""),
                    "score": result.get("score", 0.0),
                    "domain": self._extract_domain(result.get("url", "")),
                    "timestamp": datetime.now().isoformat()
                })
            
            return formatted_results
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error during web search: {http_err}")
            status_code = getattr(http_err.response, 'status_code', None)
            error_detail = f"Status code: {status_code}" if status_code else str(http_err)
            
            return [{
                "title": "Search Error",
                "text": f"Web search encountered an HTTP error: {error_detail}",
                "url": "",
                "score": 0.0
            }]
            
        except Exception as e:
            logger.error(f"Error performing web search: {str(e)}")
            return [{
                "title": "Search Error", 
                "text": f"Web search encountered an error: {str(e)}. Falling back to knowledge base only.",
                "url": "",
                "score": 0.0
            }]
    
    def _extract_domain(self, url: str) -> str:
        """
        Extract the domain name from a URL.
        """
        try:
            # Simple domain extraction
            if url.startswith('http'):
                parts = url.split('/')
                if len(parts) >= 3:
                    return parts[2]
            return ""
        except:
            return ""

# Example usage
if __name__ == "__main__":
    search = WebSearch()
    
    # Example math query
    results = search.search("solve quadratic equation x^2 + 5x + 6 = 0")
    
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"\nResult #{i+1} from {result.get('domain', 'unknown')}:")
        print(f"  • Title: {result['title']}")
        print(f"  • URL: {result['url']}")
        print(f"  • Score: {result['score']}")
        
        # Print a short snippet of the text
        text_snippet = result['text'][:150] + "..." if len(result['text']) > 150 else result['text']
        print(f"  • Text snippet: {text_snippet}")