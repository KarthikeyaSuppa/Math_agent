# AI Knowledge Assistant

An intelligent question-answering system that combines knowledge base retrieval with web search capabilities.

## Features

- **RAG Implementation**: Retrieves relevant information from both knowledge base and web search  
- **LLM Integration**: Uses Groq's Mixtral model for high-quality responses  
- **Web Search**: Integrates Tavily API for up-to-date information  
- **Smart Routing**: Automatically decides between knowledge base and web search  
- **Safety Guardrails**: Input/output filtering and content safety checks  
- **User Feedback**: Collects and analyzes user feedback for continuous improvement  
- **Modern UI**: Clean and intuitive Streamlit interface  

## Setup

1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd <repository-name>
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables:
Create a .env file with the following variables:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
Run the application:

bash
Copy
Edit
streamlit run app.py
Project Structure
app.py — Main Streamlit application

llm_integration.py — Groq LLM integration

web_search.py — Tavily web search integration

router.py — Query routing logic

guardrails.py — Input/output safety checks

feedback.py — User feedback collection and analysis

kb.py — Knowledge base management (from previous implementation)

Usage
Open the application in your web browser

Enter your question in the text area

Click Get Answer to receive a response

Provide feedback on the response quality

View the source of information and context used

Feedback System
The system collects user feedback to:

Track response quality

Identify areas for improvement

Analyze source effectiveness

Generate improvement suggestions
