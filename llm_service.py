import requests
import logging
from config import config

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.model = "gemini-2.0-flash-exp" 
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def _is_llm_available(self):
        """Check if LLM API is properly configured"""
        return (self.api_key and 
                self.api_key != 'your_gemini_api_key_here' and 
                len(self.api_key) > 20)
    
    async def decide_action(self, query: str, memory_context: str = "") -> dict:
        """
        Use LLM to decide whether to:
        - Answer directly using LLM,
        - Call external API for factual data
        """
        try:
            if not self._is_llm_available():
                logger.info("LLM not available, using rule-based decision")
                return self._rule_based_decision(query)
            
            prompt = f"""Analyze this user query and decide the best approach:

Current Query: "{query}"

{memory_context}

Available external APIs:
- Weather API: For current weather in specific cities
- Wikipedia API: For factual information about specific topics
- News API: For latest news about specific topics

Decision Guidelines:
- Use EXTERNAL_API if the query needs REAL-TIME data (weather, news) or SPECIFIC FACTS (Wikipedia)
- Use LLM_DIRECT if it's general knowledge, explanations, or creative tasks

Respond in this exact JSON format:
{{
  "decision": "LLM_DIRECT" or "EXTERNAL_API",
  "reasoning": "Brief explanation considering conversation history",
  "api_type": "weather", "wikipedia", "news" or null
}}"""

            response = await self._call_gemini(prompt)
            
            # Parse the response
            if "{" in response and "}" in response:
                import json
                try:
                    # Extract JSON from response
                    start = response.find('{')
                    end = response.rfind('}') + 1
                    json_str = response[start:end]
                    result = json.loads(json_str)
                    
                    # Validate the response has required fields
                    if all(key in result for key in ['decision', 'reasoning', 'api_type']):
                        return result
                except Exception as parse_error:
                    logger.warning(f"Failed to parse LLM JSON response: {parse_error}")
            
            # Fallback to rule-based if parsing fails
            return self._rule_based_decision(query)
            
        except Exception as e:
            logger.error(f"LLM decision error: {str(e)}")
            return self._rule_based_decision(query)
    
    async def generate_direct_answer(self, query: str, memory_context: str = "") -> str:
        """Use LLM to answer directly for general knowledge"""
        try:
            if not self._is_llm_available():
                return "I can help with general knowledge questions when configured with an LLM API key."
            
            prompt = f"""Provide a helpful, concise answer to this question:

{memory_context}

Current Question: {query}

Answer:"""
            
            return await self._call_gemini(prompt)
            
        except Exception as e:
            logger.error(f"LLM direct answer error: {str(e)}")
            return "I encountered an error while generating a response."
    
    async def generate_final_answer(self, query: str, reasoning: str, api_data: dict, memory_context: str = "") -> str:
        """Use LLM to combine reasoning and API data into final coherent answer"""
        try:
            if not self._is_llm_available():
                return self._format_fallback_answer(query, api_data)
            
            prompt = f"""Create a coherent final answer by combining:

{memory_context}

User Question: {query}
My Reasoning: {reasoning}
API Data: {api_data}

Instructions:
- Create a natural, helpful answer
- Use the API data meaningfully
- Be concise and direct
- Acknowledge limitations if data has errors
- Consider conversation history if relevant

Final Answer:"""
            
            return await self._call_gemini(prompt)
            
        except Exception as e:
            logger.error(f"LLM final answer error: {str(e)}")
            return self._format_fallback_answer(query, api_data)
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API with correct headers and format"""
        try:
            # Use the exact same format as your working curl command
            url = f"{self.base_url}/{self.model}:generateContent"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            logger.info(f"Calling Gemini API with model: {self.model}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()
            
            if response.status_code == 200:
                if 'candidates' in data and len(data['candidates']) > 0:
                    return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    raise Exception("No response candidates in API response")
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Gemini API Error {response.status_code}: {error_msg}")
                raise Exception(f"Gemini API error: {error_msg}")
                    
        except requests.exceptions.Timeout:
            logger.error("Gemini API request timed out")
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error calling Gemini: {str(e)}")
            raise
    
    def _rule_based_decision(self, query: str) -> dict:
        """Rule-based fallback when LLM is unavailable"""
        query_lower = query.lower()
        
        # Weather queries
        if any(word in query_lower for word in ['weather', 'temperature', 'umbrella', 'rain']):
            return {
                "decision": "EXTERNAL_API",
                "reasoning": "Query requires real-time weather data",
                "api_type": "weather"
            }
        
        # News queries
        elif any(word in query_lower for word in ['news', 'latest', 'current events', 'headlines']):
            return {
                "decision": "EXTERNAL_API", 
                "reasoning": "Query requires current news data",
                "api_type": "news"
            }
        
        # Wikipedia queries
        elif any(word in query_lower for word in ['who invented', 'what is', 'capital of', 'define']):
            return {
                "decision": "EXTERNAL_API",
                "reasoning": "Query requires factual information",
                "api_type": "wikipedia"
            }
        
        # Default to LLM for general knowledge
        else:
            return {
                "decision": "LLM_DIRECT",
                "reasoning": "General knowledge question suitable for LLM",
                "api_type": None
            }
    
    def _format_fallback_answer(self, query: str, api_data: dict) -> str:
        """Fallback answer formatting when LLM fails"""
        if api_data.get('error'):
            return f"I tried to find information but encountered an issue: {api_data['error']}"
        
        if 'weather' in str(api_data):
            return f"Current weather in {api_data['city']}: {api_data['weather']}, {api_data['temperature']}°C"
        
        elif 'articles' in api_data:
            response = "Latest news:\n"
            for article in api_data['articles']:
                response += f"• {article['title']}\n"
            return response
        
        elif 'summary' in api_data:
            return f"According to Wikipedia: {api_data['summary']}"
        
        else:
            return "Here's the information I found."