from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import SmartAgent
import logging
import uvicorn
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Evolusis Smart Agent",
    description="AI agent with intelligent decision-making and conversation memory",
    version="1.0.0"
)

agent = SmartAgent(memory_size=5)  # Store last 5 interactions

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    reasoning: str
    answer: str

class MemoryItem(BaseModel):
    timestamp: float
    time_ago: str
    query: str
    reasoning: str
    answer: str

class MemoryResponse(BaseModel):
    total_items: int
    memory_size: int
    items: List[MemoryItem]

class ClearMemoryResponse(BaseModel):
    message: str
    cleared_items: int

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Main endpoint that demonstrates intelligent decision-making:
    - Uses LLM to decide between direct answer vs external API call
    - Combines reasoning with data for coherent responses
    - Maintains conversation memory
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    logger.info(f"Processing query: {request.query}")
    response = await agent.process_query(request.query)
    return QueryResponse(**response)

@app.get("/memory", response_model=MemoryResponse)
async def get_memory():
    """Get the agent's conversation memory"""
    memory_items = agent.get_memory()
    
    return MemoryResponse(
        total_items=len(memory_items),
        memory_size=agent.memory_size,
        items=memory_items
    )

@app.delete("/memory", response_model=ClearMemoryResponse)
async def clear_memory():
    """Clear the agent's conversation memory"""
    cleared_count = len(agent.memory)
    agent.clear_memory()
    
    return ClearMemoryResponse(
        message="Memory cleared successfully",
        cleared_items=cleared_count
    )

@app.get("/")
async def root():
    return {
        "message": "Evolusis Smart Agent is running!",
        "features": [
            "Intelligent decision-making between LLM and external APIs",
            "Uses Google Gemini for reasoning",
            "Integrates Weather, Wikipedia, and News APIs", 
            "Returns reasoning and answer in JSON format",
            "Short-term memory for last 5 conversations"
        ],
        "endpoints": {
            "ask": "POST /ask",
            "get_memory": "GET /memory", 
            "clear_memory": "DELETE /memory",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "agent": "SmartAgent",
        "memory_usage": f"{len(agent.memory)}/{agent.memory_size} items"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)