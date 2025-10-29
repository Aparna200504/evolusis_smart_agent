import logging
import time
from typing import List, Dict
from tools import get_weather, get_wikipedia_summary, get_news
from llm_service import LLMService

logger = logging.getLogger(__name__)

class SmartAgent:
    def __init__(self, memory_size: int = 5):
        self.memory_size = memory_size
        self.memory: List[Dict] = []
        self.llm = LLMService()
    
    async def process_query(self, query: str):
        """
        Complete agent workflow with memory:
        1. Check memory for similar queries
        2. Decide: LLM direct vs External API
        3. Execute decision
        4. Combine data with reasoning
        5. Store in memory
        6. Return JSON response
        """
        try:
            # Check memory for similar recent queries
            memory_context = self._get_memory_context(query)
            
            # Step 1: Intelligent decision making (with memory context)
            decision_result = await self.llm.decide_action(query, memory_context)
            reasoning = decision_result["reasoning"]
            decision = decision_result["decision"]
            api_type = decision_result["api_type"]
            
            logger.info(f"Decision: {decision}, Reasoning: {reasoning}, API Type: {api_type}")
            
            # Step 2: Execute the decided action
            if decision == "LLM_DIRECT":
                # Use LLM alone for general knowledge
                final_answer = await self.llm.generate_direct_answer(query, memory_context)
                api_data = {}
            else:
                # Call external API for factual data
                api_data = await self._call_external_api(query, api_type)
                # Combine API data with LLM reasoning
                final_answer = await self.llm.generate_final_answer(query, reasoning, api_data, memory_context)
            
            # Step 3 & 4: Return JSON response and store in memory
            response = {
                "reasoning": reasoning,
                "answer": final_answer
            }
            
            self._add_to_memory(query, reasoning, final_answer)
            return response
            
        except Exception as e:
            logger.error(f"Agent processing error: {str(e)}")
            return {
                "reasoning": "Error in decision-making process",
                "answer": "Sorry, I encountered an error while processing your request."
            }
    
    def _get_memory_context(self, current_query: str) -> str:
        """Get relevant context from recent memory"""
        if not self.memory:
            return "No previous conversation history."
        
        # Get last few interactions
        recent_memory = self.memory[-3:]  # Last 3 interactions
        
        context = "Previous conversation context:\n"
        for i, item in enumerate(recent_memory, 1):
            context += f"{i}. User: {item['query']}\n"
            context += f"   Answer: {item['answer'][:100]}...\n"
        
        # Check for similar queries in memory
        similar_queries = self._find_similar_queries(current_query)
        if similar_queries:
            context += f"\nSimilar previous queries: {', '.join(similar_queries)}"
        
        return context
    
    def _find_similar_queries(self, current_query: str) -> List[str]:
        """Find similar queries in memory"""
        current_lower = current_query.lower()
        similar = []
        
        for item in self.memory:
            query_lower = item['query'].lower()
            # Simple similarity check based on common words
            current_words = set(current_lower.split())
            memory_words = set(query_lower.split())
            common_words = current_words.intersection(memory_words)
            
            if len(common_words) >= 2:  # At least 2 common words
                similar.append(item['query'])
        
        return similar[:2]  # Return max 2 similar queries
    
    async def _call_external_api(self, query: str, api_type: str) -> dict:
        """Call the appropriate external API based on decision"""
        try:
            if api_type == "weather":
                city = self._extract_city(query)
                return get_weather(city)
            
            elif api_type == "wikipedia":
                topic = self._extract_topic(query)
                return get_wikipedia_summary(topic)
            
            elif api_type == "news":
                topic = self._extract_news_topic(query)
                return get_news(topic)
            
            else:
                return {"error": "Unknown API type"}
                
        except Exception as e:
            logger.error(f"External API call error: {str(e)}")
            return {"error": f"Failed to fetch data: {str(e)}"}
    
    def _add_to_memory(self, query: str, reasoning: str, answer: str):
        """Add interaction to memory with timestamp"""
        memory_item = {
            "timestamp": time.time(),
            "query": query,
            "reasoning": reasoning,
            "answer": answer
        }
        
        self.memory.append(memory_item)
        
        # Keep only the most recent items
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)
        
        logger.info(f"Added to memory. Total items: {len(self.memory)}")
    
    def get_memory(self) -> List[Dict]:
        """Get complete memory with formatted timestamps"""
        formatted_memory = []
        for item in self.memory:
            formatted_item = item.copy()
            # Convert timestamp to readable format
            formatted_item["time_ago"] = self._format_time_ago(item["timestamp"])
            formatted_memory.append(formatted_item)
        
        return formatted_memory
    
    def clear_memory(self):
        """Clear all memory"""
        self.memory.clear()
        logger.info("Memory cleared")
    
    def _format_time_ago(self, timestamp: float) -> str:
        """Format timestamp as human-readable time ago"""
        current_time = time.time()
        diff_seconds = current_time - timestamp
        
        if diff_seconds < 60:
            return "just now"
        elif diff_seconds < 3600:
            minutes = int(diff_seconds / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff_seconds < 86400:
            hours = int(diff_seconds / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = int(diff_seconds / 86400)
            return f"{days} day{'s' if days > 1 else ''} ago"
    
    def _extract_city(self, query: str) -> str:
        words = query.lower().split()
        if 'in' in words:
            idx = words.index('in')
            if idx + 1 < len(words):
                return words[idx + 1].title()
        return 'London'
    
    def _extract_topic(self, query: str) -> str:
        stop_words = {'what', 'is', 'who', 'when', 'the', 'a', 'tell', 'me', 'about'}
        words = [word for word in query.lower().split() if word not in stop_words]
        return ' '.join(words[:3]) if words else query
    
    def _extract_news_topic(self, query: str) -> str:
        news_words = {'news', 'latest', 'current', 'recent'}
        words = [word for word in query.lower().split() if word not in news_words]
        return ' '.join(words) if words else 'technology'