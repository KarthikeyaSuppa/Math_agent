from typing import List, Dict, Tuple
from kb import MathKnowledgeBase
from web_search import WebSearch

class Router:
    def __init__(self, similarity_threshold: float = 0.7):
        self.kb = MathKnowledgeBase()
        self.web_search = WebSearch()
        self.similarity_threshold = similarity_threshold
        
    def route_query(self, query: str) -> Tuple[str, List[Dict]]:
        """
        Route the query to either knowledge base or web search based on similarity scores.
        Primary source is knowledge base, with web search as fallback.
        If both fail, returns a graceful error message.
        """
        # First try knowledge base
        kb_results = []
        try:
            kb_results = self.kb.search_knowledge_base(query)
        except Exception as e:
            print(f"Error searching knowledge base: {str(e)}")
        
        if kb_results and self._check_similarity_scores(kb_results):
            # Convert (Document, score) tuples to dictionary format for consistency
            formatted_results = []
            for doc, score in kb_results:
                formatted_results.append({
                    "text": doc.page_content,
                    "source": doc.metadata.get("source", ""),
                    "page": doc.metadata.get("page", 0),
                    "score": score
                })
            return "kb", formatted_results
            
        # If no good matches in KB, use web search
        web_results = self.web_search.search(query)
        
        # If web results don't indicate an error and have actual content
        if web_results and not (len(web_results) == 1 and "Search Error" in web_results[0].get("title", "")):
            return "web", web_results
            
        # If KB had some results but below threshold, use them anyway as fallback
        if kb_results:
            formatted_results = []
            for doc, score in kb_results:
                formatted_results.append({
                    "text": doc.page_content,
                    "source": doc.metadata.get("source", ""),
                    "page": doc.metadata.get("page", 0),
                    "score": score
                })
            return "kb", formatted_results
            
        # If both KB and web search failed, return an informative message
        if not web_results:
            web_results = [{
                "text": "Sorry, I couldn't find any relevant information for your query. Please try asking a different question or providing more details.",
                "title": "No Results Found",
                "url": "",
                "score": 0.0
            }]
        
        return "error", web_results
    
    def _check_similarity_scores(self, results: List[Tuple]) -> bool:
        """
        Check if any of the results have a similarity score above threshold.
        """
        if not results:
            return False
            
        # Get the highest similarity score
        max_score = max(score for _, score in results)
        return max_score >= self.similarity_threshold
    
    def get_combined_context(self, kb_results: List[Dict], web_results: List[Dict]) -> List[Dict]:
        """
        Combine and deduplicate results from both sources.
        
        Args:
            kb_results (List[Dict]): Results from knowledge base
            web_results (List[Dict]): Results from web search
            
        Returns:
            List[Dict]: Combined and deduplicated results
        """
        all_results = kb_results + web_results
        
        # Remove duplicates based on text content
        seen_texts = set()
        unique_results = []
        
        for result in all_results:
            text = result.get("text", "").strip()
            if text and text not in seen_texts:
                seen_texts.add(text)
                unique_results.append(result)
        
        # Sort by score
        return sorted(unique_results, key=lambda x: x.get("score", 0.0), reverse=True)