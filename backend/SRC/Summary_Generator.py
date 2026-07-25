import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import re
from openai import OpenAI

class NewsSearcher:
    def __init__(self, location: str, topic: str, serp_api_key: str):
        self.location = location
        self.topic = topic
        self.api_key = serp_api_key
        self.base_url = "https://serpapi.com/search.json"
        
    def search_news(self, query: str, num_results: int = 3) -> List[Dict]:
        """
        Search for news articles using SERP API.
        Returns list of dictionaries with title, url, and thumbnail.
        """
        search_query = f"{self.location} {self.topic} {query}".strip()
        
        try:
            params = {
                "api_key": self.api_key,
                "q": search_query,
                "tbm": "nws",
                "num": num_results
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            results = []
            if 'news_results' in data:
                for result in data['news_results'][:num_results]:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('link', ''),
                        'thumbnail': result.get('thumbnail', '')
                    })
            return results
            
        except Exception as e:
            print(f"Error in SERP API search: {str(e)}")
            return []

class ArticleScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    def scrape_article(self, url):
        """
        Scrapes the given URL and returns the text content, description, and article image.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text_content = soup.get_text(separator="\n", strip=True)
                
                # Extract description and image
                description = None
                image_url = None
                
                meta_tags = [
                    {'property': 'og:title'}, 
                    {'name': 'twitter:title'},
                    {'name': 'description'}, 
                    {'property': 'og:description'},
                    {'name': 'twitter:description'}
                ]
                
                for tag in meta_tags:
                    meta = soup.find('meta', tag)
                    if meta and meta.get('content'):
                        description = meta['content']
                        break
                
                # Extract og:image or twitter:image
                img_meta_tags = [
                    {'property': 'og:image'},
                    {'name': 'twitter:image'},
                    {'property': 'og:image:secure_url'}
                ]
                for tag in img_meta_tags:
                    meta = soup.find('meta', tag)
                    if meta and meta.get('content'):
                        image_url = meta['content'].strip()
                        if image_url.startswith('http'):
                            break
                
                # Fallback to first non-logo, non-ad img on page
                if not image_url:
                    for img in soup.find_all('img'):
                        src = img.get('src', '')
                        if src.startswith('http') and not any(x in src.lower() for x in ['logo', 'icon', 'ad', 'badge', 'avatar', 'loader', 'banner']):
                            image_url = src
                            break
                
                if not description:
                    paragraphs = soup.find_all('p')
                    if paragraphs:
                        description = paragraphs[0].get_text()
                
                if description:
                    description = description.encode('latin1', 'ignore').decode('utf-8', 'ignore')
                    description = description.strip()
                    description = re.split(r'\s*\|\s*', description)[0]
                    description = (description[:147] + '...') if len(description) > 150 else description
                
                return {
                    "url": url,
                    "content": text_content,
                    "description": description if description else "",
                    "image": image_url if image_url else ""
                }
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        return None

class ContentSummarizer:
    def __init__(self, system_prompt, groq_api_key: str, groq_model: str = "llama-3.3-70b-versatile"):
        self.client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.groq_model = groq_model
        self.system_prompt = system_prompt
    
    def summarize_article(self, article: str) -> str:
        """
        Summarize a single article using Groq API.
        """
        prompt = f"{self.system_prompt}\n\nHere is the article to summarize:\n\n{article}"
        try:
            response = self.client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content if response.choices[0].message.content else None
        except Exception as e:
            print(f"Error in summarization with Groq: {str(e)}")
            return None