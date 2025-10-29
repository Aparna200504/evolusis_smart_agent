import requests
import logging
from config import config

logger = logging.getLogger(__name__)

def get_weather(city: str) -> dict:
    """Get current weather data from OpenWeather API"""
    try:
        if not config.OPENWEATHER_API_KEY:
            return {"error": "Weather API not configured"}
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json() 
        if response.status_code == 200:
            return {
                "city": data.get('name'),
                "weather": data['weather'][0]['description'],
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity'],
                "wind_speed": data['wind']['speed']
            }
        else:
            error_msg = data.get('message', 'Unknown error')
            return {"error": f"Weather API error: {error_msg}"}
            
    except Exception as e:
        logger.error(f"Weather API error: {str(e)}")
        return {"error": f"Weather fetch failed: {str(e)}"}

def get_wikipedia_summary(topic: str) -> dict:
    """Get factual data from Wikipedia API"""
    try:
        headers = {'User-Agent': 'EvolusisAIAgent/1.0'}
        
        # Try REST API first
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "title": data.get('title'),
                "summary": data.get('extract'),
                "url": data.get('content_urls', {}).get('desktop', {}).get('page')
            }
        else:
            return {"error": "Wikipedia data not available"}
            
    except Exception as e:
        logger.error(f"Wikipedia API error: {str(e)}")
        return {"error": f"Wikipedia fetch failed: {str(e)}"}

def get_news(topic: str) -> dict:
    """Get news data from NewsAPI"""
    try:
        if not config.NEWS_API_KEY or config.NEWS_API_KEY == 'your_newsapi_key_here':
            return {"error": "News API not configured"}
        
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=3&apiKey={config.NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and data.get('articles'):
            articles = []
            for article in data['articles'][:3]:
                if article.get('title') and article['title'] != '[Removed]':
                    articles.append({
                        "title": article.get('title'),
                        "source": article.get('source', {}).get('name'),
                        "url": article.get('url')
                    })
            
            return {"articles": articles}
        else:
            error_msg = data.get('message', 'Unknown error')
            return {"error": f"News API error: {error_msg}"}
            
    except Exception as e:
        logger.error(f"News API error: {str(e)}")
        return {"error": f"News fetch failed: {str(e)}"}