import streamlit as st
from main import LLMIntegration
from router import Router
from guardrails import Guardrails
import json
from typing import Dict, List
import time

# Initialize components
@st.cache_resource
def init_components():
    return {
        "llm": LLMIntegration(),
        "router": Router(),
        "guardrails": Guardrails()
    }

def display_response(response: str, source: str, context: List[Dict]):
    """Display the response and its source information."""
    st.markdown("### Response")
    st.write(response)
    
    st.markdown("### Source")
    st.write(f"Information retrieved from: {source.upper()}")
    
    if context:
        st.markdown("### Context")
        for i, item in enumerate(context, 1):
            with st.expander(f"Context {i}"):
                st.write(item.get("text", ""))
                if source == "kb":
                    st.write(f"Source: {item.get('source', '')}")
                    if "page" in item:
                        st.write(f"Page: {item.get('page', '')}")
                elif "url" in item:
                    st.write(f"Source: {item['url']}")

def main():
    st.title("AI Math Knowledge Assistant")
    st.write("Ask any math question and I'll try to help you find the answer!")
    
    # Initialize components
    components = init_components()
    
    # Input area
    query = st.text_area("Enter your question:", height=100)
    
    if st.button("Get Answer"):
        if not query:
            st.error("Please enter a question!")
            return
            
        # Validate input
        is_valid, error = components["guardrails"].validate_input(query)
        if not is_valid:
            st.error(f"Invalid input: {error}")
            return
            
        # Sanitize input
        sanitized_query = components["guardrails"].sanitize_input(query)
        
        with st.spinner("Searching for answers..."):
            # Route query
            source, context = components["router"].route_query(sanitized_query)
            
            # Validate context
            is_valid, error = components["guardrails"].validate_context(context)
            if not is_valid:
                st.error(f"Error retrieving context: {error}")
                return
                
            # Generate response
            response = components["llm"].generate_response(sanitized_query, context)
            
            # Validate response
            is_valid, error = components["guardrails"].validate_output(response)
            if not is_valid:
                st.error(f"Error generating response: {error}")
                return
                
            # Display results
            display_response(response, source, context)
            
            # Add feedback mechanism
            st.markdown("### Feedback")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Helpful"):
                    st.success("Thank you for your feedback!")
            with col2:
                if st.button("👎 Not Helpful"):
                    st.error("Thank you for your feedback. We'll try to improve!")

if __name__ == "__main__":
    main()