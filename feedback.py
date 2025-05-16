import dspy
from typing import Dict, List, Optional
import json
from datetime import datetime
import os

class FeedbackCollector:
    def __init__(self, feedback_file: str = "feedback_data.json"):
        self.feedback_file = feedback_file
        self.feedback_data = self._load_feedback()
        
    def _load_feedback(self) -> List[Dict]:
        """Load existing feedback data from file."""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
        
    def _save_feedback(self):
        """Save feedback data to file."""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
            
    def collect_feedback(self, 
                        query: str,
                        response: str,
                        context: List[Dict],
                        source: str,
                        is_helpful: bool,
                        user_comment: Optional[str] = None):
        """
        Collect feedback for a query-response pair.
        """
        # Format context for feedback storage
        formatted_context = []
        for item in context:
            context_item = {"text": item.get("text", "")}
            if "source" in item:
                context_item["source"] = item["source"]
            if "page" in item:
                context_item["page"] = item["page"]
            if "url" in item:
                context_item["url"] = item["url"]
            formatted_context.append(context_item)
            
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "context": formatted_context,
            "source": source,
            "is_helpful": is_helpful,
            "user_comment": user_comment
        }
        
        self.feedback_data.append(feedback_entry)
        self._save_feedback()
        
    def analyze_feedback(self) -> Dict:
        """
        Analyze collected feedback to identify patterns and areas for improvement.
        
        Returns:
            Dict: Analysis results
        """
        if not self.feedback_data:
            return {"error": "No feedback data available"}
            
        total_feedback = len(self.feedback_data)
        helpful_count = sum(1 for entry in self.feedback_data if entry["is_helpful"])
        
        # Calculate source distribution
        source_distribution = {}
        for entry in self.feedback_data:
            source = entry["source"]
            source_distribution[source] = source_distribution.get(source, 0) + 1
            
        # Calculate average helpfulness by source
        source_helpfulness = {}
        for source in source_distribution:
            source_entries = [entry for entry in self.feedback_data if entry["source"] == source]
            helpful_count = sum(1 for entry in source_entries if entry["is_helpful"])
            source_helpfulness[source] = helpful_count / len(source_entries)
            
        return {
            "total_feedback": total_feedback,
            "helpfulness_rate": helpful_count / total_feedback,
            "source_distribution": source_distribution,
            "source_helpfulness": source_helpfulness
        }
        
    def get_improvement_suggestions(self) -> List[str]:
        """
        Generate suggestions for improvement based on feedback analysis.
        
        Returns:
            List[str]: List of improvement suggestions
        """
        analysis = self.analyze_feedback()
        suggestions = []
        
        # Check overall helpfulness
        if analysis.get("helpfulness_rate", 0) < 0.7:
            suggestions.append("Consider improving response quality and relevance")
            
        # Check source-specific performance
        for source, helpfulness in analysis.get("source_helpfulness", {}).items():
            if helpfulness < 0.6:
                suggestions.append(f"Improve quality of {source} responses")
                
        return suggestions