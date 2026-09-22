
# Evolusis AI Agent

A FastAPI-based intelligent AI agent that integrates LLM reasoning with external APIs to demonstrate decision-making capabilities between using the LLM directly or fetching real-time data from external services.

---

## Features

- Intelligent decision-making using Google Gemini 2.0 Flash  
- Multiple API integrations:  
  - OpenWeatherMap for real-time weather data  
  - Wikipedia API for factual information retrieval  
  - NewsAPI for the latest news and current events  
- Short-term memory that remembers the last 5 user interactions  
- Clean, modular architecture  
- Graceful error handling and fallback logic  
- Auto-generated Swagger/OpenAPI documentation  

---

## Technical Stack

- Backend: FastAPI (Python)  
- LLM: Google Gemini 2.0 Flash  
- External APIs: OpenWeatherMap, Wikipedia REST API, NewsAPI  
- Memory: In-memory storage with timestamps  
- Documentation: Auto-generated via OpenAPI  

---

## API Endpoints

### Main Endpoint
POST /ask – Process user queries with intelligent routing between LLM and APIs

### Supporting Endpoints
GET / – API information and features  
GET /health – Check service health  
GET /memory – View last 5 user interactions  
DELETE /memory – Clear memory  
GET /docs – Interactive API documentation  

---

## Quick Start

### Prerequisites
- Python 3.8 or above  
- API keys for:
  - Google Gemini: https://aistudio.google.com/app/apikey  
  - OpenWeatherMap: https://openweathermap.org/api  
  - NewsAPI: https://newsapi.org/  

### Installation

1. Clone repository
git clone <repository-url>
cd evolusis-agent

2. Create and activate virtual environment  
python -m venv venv
venv\Scripts\activate  \# Windows
source venv/bin/activate  \# Linux/Mac

3. Install dependencies  
pip install -r requirements.txt

4. Configure environment variables  
Create a .env file:
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
NEWS_API_KEY=your_newsapi_key_here

5. Run the application  
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

6. Access the API  
- Main API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Health Check: http://localhost:8000/health  

## Testing the Agent

### Example Queries

Weather Query:
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"weather in london\"}"

Factual Query:
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"who invented the telephone\"}"

News Query:
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"latest technology news\"}"

General Knowledge Query:
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"explain quantum computing\"}"

### Response Format
All responses use this structure:
{
"reasoning": "LLM-generated explanation of decision process",
"answer": "Final formatted response combining API data and LLM reasoning"
}

## Project Structure
evolusis-agent/
├── main.py            \# FastAPI application and routes
├── agent.py           \# Core agent with decision logic
├── llm_service.py     \# Google Gemini integration
├── tools.py           \# External API integrations
├── config.py          \# Configuration management
├── requirements.txt   \# Python dependencies
├── .env               \# Environment variables
└── README.md          \# Project documentation

## How It Works
1. User sends a query to the /ask endpoint  
2. The LLM analyzes the query and decides whether to use an external API or respond directly  
3. The system fetches data from APIs when necessary  
4. The agent combines LLM reasoning with the fetched data to form the final response  
5. The interaction is stored in memory for contextual awareness  

## Configuration

### API Keys

- Google Gemini: https://aistudio.google.com/app/apikey  
- OpenWeatherMap: https://openweathermap.org/api  
- NewsAPI (optional): https://newsapi.org/  

## Requirements Satisfaction

FastAPI Backend – Implemented with /ask endpoint  
LLM Integration – Google Gemini 2.0 Flash  
External APIs – Weather, Wikipedia, News  
Intelligent Decision Logic – LLM-based query routing  
JSON Response Format – reasoning and answer fields  
Clean Architecture – Modular services  
Error Handling – Graceful degradation  
Short-term Memory – Stores last 5 user queries  
Multiple APIs – Integrated successfully  
Error Logging – Comprehensive logs  

## Demo Commands
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"weather in london\"}"
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"what is blockchain\"}"
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"query\": \"latest ai news\"}"
curl -X GET "http://localhost:8000/memory"


## License
This project was developed as part of the Evolusis Backend Developer Assignment.

## Contributing

This is a demonstration project. For improvements or bug reports, please follow standard GitHub contribution guidelines.


