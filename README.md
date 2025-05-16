# AI Knowledge Assistant for Mathematics

An intelligent question-answering system specialized in mathematics that combines knowledge base retrieval with focused web search capabilities.

## Features

* **RAG Implementation**: Retrieves relevant information from both a specialized math knowledge base and math-focused web search
* **LLM Integration**: Uses Groq's Llama3-70B (Mixtral) model for high-quality, step-by-step math solutions with proper notation
* **Web Search**: Integrates Tavily API targeting reputable mathematics domains like Khan Academy, Math Stack Exchange, and Wolfram MathWorld
* **Smart Routing**: Automatically decides whether to query the knowledge base or perform a web search based on similarity scores
* **Vector Database**: Uses Pinecone for efficient similarity search of mathematical content
* **Safety Guardrails**: Input/output validation, filtering, and content safety checks
* **User Feedback**: Collects and analyzes user feedback for continuous improvement, tracking response quality and source effectiveness
* **Modern UI**: Clean, intuitive Streamlit interface with context display and feedback mechanisms

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
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=your_pinecone_index_name
   ```

4. Prepare the knowledge base:
   * Create a `Data` directory in the project root
   * Add mathematics PDF files to the `Data` directory
   * Run the knowledge base initialization script:
     ```bash
     python kb.py
     ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

* `app.py`: Main Streamlit application
* `kb.py`: Knowledge base management using Pinecone vector database
* `web_search.py`: Tavily API integration with math domain filtering
* `router.py`: Smart query routing logic
* `llm_integration.py`: Groq LLM integration with specialized math system prompting
* `guardrails.py`: Input/output validation and safety checks
* `feedback.py`: User feedback collection and analysis system

## Usage

1. Open the application in your web browser (usually at `http://localhost:8501`)
2. Enter your mathematics question in the input area
3. Click **Get Answer** to receive a detailed, step-by-step response
4. Review the source information and context used to generate the answer
5. Provide feedback on response quality using thumbs up/down buttons

## System Flow

1. User inputs a math question
2. Input is validated and sanitized by guardrails
3. Router decides to query knowledge base or perform web search based on similarity threshold (≥ 0.7)
4. Relevant context is retrieved and validated
5. LLM generates a clear and concise answer with math notation
6. Response is displayed along with source context
7. User feedback is collected and stored for analysis

## Feedback System

The feedback mechanism:
* Tracks response quality and helpfulness
* Analyzes performance by source (knowledge base vs web search)
* Identifies improvement areas
* Suggests specific enhancements based on collected data

## Math-Focused Domains

The system searches these trusted mathematics websites:
* mathworld.wolfram.com
* khanacademy.org
* math.stackexchange.com
* brilliant.org
* purplemath.com
