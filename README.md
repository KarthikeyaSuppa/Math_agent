AI Math Knowledge Assistant
An intelligent question-answering system specialized in mathematics that combines knowledge base retrieval with focused web search capabilities.

Overview
The AI Math Knowledge Assistant is designed to provide accurate and helpful responses to mathematical questions by leveraging both a specialized knowledge base and targeted web searches from math-focused domains. The system intelligently routes queries to the most appropriate source and generates clear, concise responses using advanced language models.

Key Features
Dual-Source Information Retrieval: Combines a specialized math knowledge base with targeted web search across math-focused domains

Intelligent Query Routing: Automatically determines whether to use the knowledge base or web search based on similarity scores

Math-Focused Web Search: Targets reputable mathematics domains like Khan Academy, Math Stack Exchange, and Wolfram MathWorld

Vector Database Integration: Uses Pinecone for efficient similarity search of mathematical content

LLM Integration: Leverages Groq's Llama3-70B model for high-quality responses

Step-by-Step Math Solutions: Focuses on providing clear explanations with proper mathematical notation

Comprehensive Safety Guardrails: Input/output validation and content filtering

User Feedback Collection: Gathers and analyzes feedback for continuous improvement

Clean Streamlit Interface: Intuitive UI with context display and feedback mechanisms

Technical Architecture
Components
Knowledge Base (kb.py): PDF-based knowledge repository using Pinecone vector database

Web Search (web_search.py): Tavily API integration with math domain filtering

Router (router.py): Smart query routing between knowledge base and web search

LLM Integration: Groq API integration with specialized math system prompting

Guardrails (guardrails.py): Input/output validation and safety checks

Feedback Collection: User feedback tracking and analysis system

Streamlit App: User interface with question input and response display

Setup Instructions
Clone the repository:

bash
Copy
Edit
git clone <repository-url>
cd math-knowledge-assistant
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables: Create a .env file with the following variables:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
Prepare knowledge base data:

Create a Data directory in the project root

Add mathematics PDF files to the Data directory

Run the knowledge base initialization script:

bash
Copy
Edit
python kb.py
Run the application:

bash
Copy
Edit
streamlit run app.py
Usage Guide
Open the application in your web browser (typically at http://localhost:8501)

Enter your mathematics question in the text area

Click Get Answer to receive a detailed response

Review the source information and context used to generate the answer

Provide feedback on the response quality using the thumbs up/down buttons

System Flow
User inputs a mathematics question

Input is validated and sanitized through guardrails

Router determines whether to query the knowledge base or perform a web search

If the knowledge base has relevant information (similarity score ≥ 0.7), it’s used as the primary source

Otherwise, the system falls back to web search across math-focused domains

Retrieved context is validated and processed

LLM generates a response based on the retrieved context

Response is validated and displayed to the user

User feedback is collected and stored for analysis

Feedback System
The feedback collection mechanism:

Tracks response quality and helpfulness metrics

Analyzes performance by information source

Identifies patterns and areas for improvement

Generates specific improvement suggestions based on analysis

Math-Focused Domains
The system is configured to search the following mathematics-focused websites:

mathworld.wolfram.com

khanacademy.org

math.stackexchange.com

brilliant.org

purplemath.com
