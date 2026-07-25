# -*- coding: utf-8 -*-
from SRC.Summary_Generator import NewsSearcher, ArticleScraper, ContentSummarizer
from SRC.Prompts import system_prompt

import yaml
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import ssl
import time
import threading
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
CORS(app)

# Load configuration (optional fallback)
topic = "news"
location = "India"
if os.path.exists('configs.yaml'):
    try:
        with open('configs.yaml', 'r') as file:
            config = yaml.safe_load(file)
            topic = config.get('topic', 'news')
            location = config.get('location', 'India')
    except Exception as e:
        print(f"Error loading configs.yaml: {e}")

groq_api_key = os.environ.get("GROQ_API_KEY")
groq_model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
serp_api_key = os.environ.get("SERP_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set!")
if not serp_api_key:
    raise ValueError("SERP_API_KEY environment variable is not set!")

NEWS_FILE = os.path.join(os.path.dirname(__file__), "News.json")
NEWS_LOCK = threading.Lock()

# Track active background scrapes and their status messages
active_scrapes = set()
active_scrapes_lock = threading.Lock()
scrape_status = {}
scrape_status_lock = threading.Lock()

def scrape_city_news(city):
    """
    Background worker to scrape news for a specific city, summarize, and cache them.
    Saves articles progressively as they are processed.
    """
    print(f"[Scraper] Starting background news collection for city: '{city}'")
    try:
        # Initialize status
        with scrape_status_lock:
            scrape_status[city] = "Crawling news articles..."
            
        # 1. Determine search query
        if city.lower() == "all":
            search_query = "India breaking national news"
        else:
            search_query = f"{city} latest local news"
            
        searcher = NewsSearcher(location="", topic=search_query, serp_api_key=serp_api_key)
        scraper = ArticleScraper()
        summarizer = ContentSummarizer(system_prompt, groq_api_key, groq_model)
        
        # 2. Get top 3 news articles from SerpAPI
        results = searcher.search_news("", num_results=3)
        print(f"[SerpAPI] Found {len(results)} articles for city: '{city}'")
        
        # Clear existing cached items for this city before writing new ones
        with NEWS_LOCK:
            news_data = {"news": []}
            if os.path.exists(NEWS_FILE):
                try:
                    with open(NEWS_FILE, "r", encoding="utf-8") as f:
                        news_data = json.load(f)
                except Exception:
                    pass
            
            # Remove old cached records for this city
            filtered_news = [item for item in news_data.get("news", []) if item.get("city", "").lower() != city.lower()]
            news_data["news"] = filtered_news
            
            with open(NEWS_FILE, "w", encoding="utf-8") as f:
                json.dump(news_data, f, indent=4)
        
        # If no search results, we exit early
        if not results:
            print(f"[Scraper] No search results found for '{city}'")
            return
            
        # 3. Process each article and append it immediately (Progressive/Streaming style)
        for idx, result in enumerate(results):
            url = result['url']
            title = result['title']
            serp_thumbnail = result.get('thumbnail', '')
            
            # Update status to summarization
            with scrape_status_lock:
                scrape_status[city] = f"Summarizing article {idx+1} of {len(results)}..."
            print(f"[Scraper] Processing ({idx+1}/{len(results)}): {title} ({url})")
            
            # Scrape webpage text
            scraped_data = scraper.scrape_article(url)
            if not scraped_data or not scraped_data.get('content') or len(scraped_data['content'].strip()) < 100:
                print(f"[Scraper] Scraping content failed or text too short. Skipping.")
                continue
                
            # Summarize content
            summary = summarizer.summarize_article(scraped_data['content'])
            if not summary or len(summary.strip()) < 50:
                print(f"[LLM] Groq summary generation failed. Skipping.")
                continue
                
            # Formatting title check
            if not summary.strip().startswith("Title:"):
                summary = f"Title: {title}\n\n{summary}"
                
            # Update status to image extraction
            with scrape_status_lock:
                scrape_status[city] = f"Extracting image for article {idx+1} of {len(results)}..."
                
            # Determine the image URL (Featured Meta Tag -> SerpAPI Thumbnail -> Fallback Image)
            image_url = ""
            if scraped_data.get('image'):
                image_url = scraped_data['image']
                print(f"[Image] Found article featured image: {image_url}")
            elif serp_thumbnail:
                image_url = serp_thumbnail
                print(f"[Image] Using SerpAPI thumbnail image: {image_url}")
            else:
                image_url = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800"
                print(f"[Image] Using fallback image: {image_url}")
                
            # Create the single news item
            news_item = {
                "city": city,
                "content": summary,
                "image_urls": image_url,
                "timestamp": time.time()
            }
            
            # Save this news item immediately to News.json
            with NEWS_LOCK:
                current_data = {"news": []}
                if os.path.exists(NEWS_FILE):
                    try:
                        with open(NEWS_FILE, "r", encoding="utf-8") as f:
                            current_data = json.load(f)
                    except Exception:
                        pass
                
                current_data.setdefault("news", []).append(news_item)
                
                with open(NEWS_FILE, "w", encoding="utf-8") as f:
                    json.dump(current_data, f, indent=4)
                    
            print(f"[Scraper] Saved article {idx+1} progressively for '{city}'")
            
            # Brief delay between scrapes
            time.sleep(1.0)
            
        print(f"[Scraper] Successfully completed progressive scraping for '{city}'")
            
    except Exception as e:
        print(f"[Scraper] Error in background scrape process for '{city}': {e}")
    finally:
        with active_scrapes_lock:
            active_scrapes.discard(city)
        with scrape_status_lock:
            scrape_status.pop(city, None)
        print(f"[Scraper] Background scrape thread closed for: '{city}'")

@app.route("/news", methods=["GET"])
def get_news():
    city = request.args.get('city', 'All').strip()
    
    # 1. Read existing news from cache file
    cached_items = []
    with NEWS_LOCK:
        if os.path.exists(NEWS_FILE):
            try:
                with open(NEWS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cached_items = data.get("news", [])
            except Exception:
                pass
                
    # 2. Filter news by requested city
    city_articles = [item for item in cached_items if item.get("city", "").lower() == city.lower()]
    
    # 3. Check cache validity (must exist and be less than 2 hours / 7200 seconds old)
    cache_valid = False
    if city_articles:
        newest_timestamp = max(item.get("timestamp", 0) for item in city_articles)
        if (time.time() - newest_timestamp) < 7200:
            cache_valid = True
            
    # 4. Trigger background scrape if cache is stale or empty
    loading = False
    if not cache_valid:
        with active_scrapes_lock:
            if city not in active_scrapes:
                active_scrapes.add(city)
                threading.Thread(target=scrape_city_news, args=(city,), daemon=True).start()
        loading = True
        
    # Get current status message
    current_status = "Idle"
    if loading:
        with scrape_status_lock:
            current_status = scrape_status.get(city, "Initializing scraper...")
        
    return jsonify({
        "news": city_articles,
        "loading": loading,
        "status": current_status
    })

# Start default scrape for "All" on start if empty or stale
def init_all_news():
    time.sleep(2)
    cached_items = []
    if os.path.exists(NEWS_FILE):
        try:
            with open(NEWS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                cached_items = data.get("news", [])
        except Exception:
            pass
            
    all_articles = [item for item in cached_items if item.get("city", "").lower() == "all"]
    all_valid = False
    if all_articles:
        newest_timestamp = max(item.get("timestamp", 0) for item in all_articles)
        if (time.time() - newest_timestamp) < 7200:
            all_valid = True
            
    if not all_valid:
        with active_scrapes_lock:
            if "All" not in active_scrapes:
                active_scrapes.add("All")
                threading.Thread(target=scrape_city_news, args=("All",), daemon=True).start()

threading.Thread(target=init_all_news, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=False, port=5000)
