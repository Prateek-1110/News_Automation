# 📰 Autonomous News Aggregation, Summarization, and Publishing Agent

## 🚀 Overview
This project is an **AI-powered autonomous news agent** that dynamically crawls, summarizes, and publishes local news for major Indian cities. By transitioning from heavy local deep learning models to cloud-based APIs (Groq), the system starts instantaneously and streams localized summaries and authentic web images in real-time.

---

### **Core Features**
* 🌆 **City-Specific Feeds**: Select and fetch news dynamically for 22 major Indian cities (e.g. Pune, Delhi, Mumbai, Lucknow) plus national trending updates.
* ⚡ **Instant Boot & Zero Local Compute**: Bypassed PyTorch, BERT, and BART models in favor of Groq APIs, reducing server startup latency from minutes to under 0.1 seconds.
* 🔄 **On-Demand Background Scraping**: Crawls news dynamically when requested by a frontend user, caching results for 2 hours to optimize SerpAPI credits.
* 📈 **Progressive Article Rendering**: Writes and streams news articles progressively to the UI as they finish summarization, allowing users to start reading within 4–5 seconds.
* 🖼️ **Authentic Image Extraction**: Automatically extracts the featured image directly from crawled web page metadata (`og:image`, `twitter:image`) or search thumbnails, displaying real news pictures.
* 💬 **Real-time Status Updates**: Displays step-by-step crawl progress (e.g., `"Summarizing article 1 of 3..."`) directly on the UI spinner.

---

## 🏗 Tech Stack
* **Frontend**: React.js (Vite, Tailwind CSS, Lucide icons)
* **Backend**: Flask (Python)
* **Database**: Lightweight JSON cache (`News.json` / `News_list.json`)
* **LLM Summarization**: Groq API (`llama-3.3-70b-versatile` via OpenAI SDK)
* **Web Search**: SerpAPI
* **HTML Parsing**: BeautifulSoup4 & Requests

---

## 🛠 Installation and Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Prateek-1110/News_automation.git
cd News_Automation
```

### **2️⃣ Set Up Virtual Environment (Recommended)**
```bash
# Create a virtual environment
python -m venv myenv

# Activate it
# On Windows:
.\myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

### **3️⃣ Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Keys**
Create a **`.env`** file inside the `backend/` directory:
```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

# Search and Image Upload API Keys
SERP_API_KEY=your_serp_api_key
IMGBB_API_KEY=your_imgbb_api_key

# Server Port
PORT=5000
```

---

## 🖥 Running the App

### **1️⃣ Test Configuration (Optional)**
Verify that your API keys are working correctly before starting the server:
```bash
# Run from the root directory
python test_keys.py
```

### **2️⃣ Run the Flask Backend**
```bash
cd backend
python server.py
```
The backend will immediately start on `http://127.0.5000` (or `http://127.0.0.1:5000`) and initiate a background crawl for the default national trending ("All") news.

### **3️⃣ Run the React Frontend**
```bash
cd ../frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser. Use the **Select Location** dropdown to explore breaking updates!

---

## 📜 License
This project is open-source and available under the **MIT License**.
