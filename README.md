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
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `llm_integration.py`: Groq LLM integration
- `web_search.py`: Tavily web search integration
- `router.py`: Query routing logic
- `guardrails.py`: Input/output safety checks
- `feedback.py`: User feedback collection and analysis
- `kb.py`: Knowledge base management (from previous implementation)

## Usage

1. Open the application in your web browser
2. Enter your question in the text area
3. Click "Get Answer" to receive a response
4. Provide feedback on the response quality
5. View the source of information and context used

## Feedback System

The system collects user feedback to:
- Track response quality
- Identify areas for improvement
- Analyze source effectiveness
- Generate improvement suggestions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 