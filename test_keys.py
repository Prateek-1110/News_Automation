import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join("backend", ".env"))

print("=== Starting API Key Verification ===")

# 1. Groq API Verification
groq_key = os.environ.get("GROQ_API_KEY")
groq_model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
if not groq_key:
    print("❌ GROQ_API_KEY is not configured in backend/.env")
else:
    print(f"Checking Groq API with model '{groq_model}'...")
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=groq_key,
            base_url="https://api.groq.com/openai/v1"
        )
        response = client.chat.completions.create(
            model=groq_model,
            messages=[
                {"role": "user", "content": "Respond with the word 'Success'."}
            ],
            max_tokens=10
        )
        result_text = response.choices[0].message.content.strip()
        print(f"✅ Groq API verified successfully! Response: {result_text}")
    except Exception as e:
        print(f"❌ Groq API verification failed: {e}")

# 2. SerpAPI Verification
serp_key = os.environ.get("SERP_API_KEY")
if not serp_key:
    print("❌ SERP_API_KEY is not configured in backend/.env")
else:
    print("Checking SerpAPI query...")
    try:
        params = {
            "api_key": serp_key,
            "q": "Delhi Political news",
            "tbm": "nws",
            "num": 1
        }
        res = requests.get("https://serpapi.com/search.json", params=params)
        data = res.json()
        if 'error' in data:
            print(f"❌ SerpAPI returned error: {data['error']}")
        elif 'news_results' in data or 'organic_results' in data:
            print("✅ SerpAPI verified successfully! Search query returned results.")
        else:
            print(f"⚠️ SerpAPI completed, but response was unexpected: {list(data.keys())}")
    except Exception as e:
        print(f"❌ SerpAPI verification failed: {e}")

# 3. ImgBB Verification
imgbb_key = os.environ.get("IMGBB_API_KEY")
if not imgbb_key:
    print("❌ IMGBB_API_KEY is not configured in backend/.env")
else:
    print("Checking ImgBB API connection...")
    try:
        # Create a tiny 1x1 pixel red GIF in memory to test upload
        import io
        tiny_gif = b'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
        files = {
            "image": ("test_pixel.gif", io.BytesIO(tiny_gif))
        }
        payload = {
            "key": imgbb_key,
            "name": "test_pixel.gif"
        }
        res = requests.post("https://api.imgbb.com/1/upload", data=payload, files=files)
        data = res.json()
        if data.get("success"):
            print(f"✅ ImgBB verified successfully! Direct URL: {data['data']['url']}")
        else:
            print(f"❌ ImgBB returned failure: {data}")
    except Exception as e:
        print(f"❌ ImgBB verification failed: {e}")

print("=== Verification Complete ===")
