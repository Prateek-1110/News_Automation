import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

const App = () => {
  const [news, setNews] = useState([]);
  const [selectedCity, setSelectedCity] = useState("All");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isBackgroundLoading, setIsBackgroundLoading] = useState(false);
  const [statusText, setStatusText] = useState("Crawling news articles...");

  // Helper function to extract title and paragraphs
  const parseContent = (content) => {
    if (!content) return { title: "", paragraphs: [] };
    const lines = content.split("\n").filter((line) => line.trim());
    
    // Check if there is a Title line
    const titleLine = lines.find(l => l.startsWith("Title: "));
    const title = titleLine ? titleLine.replace("Title: ", "") : lines[0] || "";
    
    const paragraphs = lines.reduce((acc, line) => {
      if (line.startsWith("Title: ")) return acc;
      // Skip section headers ending in ':'
      if (!line.endsWith(":")) {
        acc.push(line);
      }
      return acc;
    }, []);

    return { title, paragraphs };
  };

  useEffect(() => {
    let active = true;
    
    const fetchNews = async (showMainLoader = false) => {
      if (showMainLoader) {
        setLoading(true);
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/news?city=${encodeURIComponent(selectedCity)}`);
        if (!response.ok) throw new Error("Failed to fetch news");
        const data = await response.json();
        
        if (!active) return;
        
        setIsBackgroundLoading(data.loading);
        setStatusText(data.status || "Crawling news articles...");
        
        const formattedNews = data.news.map((item) => {
          const { title, paragraphs } = parseContent(item.content);
          return {
            city: item.city || "All",
            title: title || "News Article",
            paragraphs: paragraphs || [],
            image_urls: item.image_urls,
          };
        });

        setNews(formattedNews);
        setError(null);
      } catch (err) {
        if (active) {
          setError(err.message);
        }
      } finally {
        if (active && showMainLoader) {
          setLoading(false);
        }
      }
    };

    // If cache belongs to a different city, clear it first
    const hasCache = news.length > 0 && news[0].city.toLowerCase() === selectedCity.toLowerCase();
    if (!hasCache) {
      setNews([]);
      setStatusText("Crawling news articles...");
    }
    
    fetchNews(!hasCache);

    const pollInterval = isBackgroundLoading ? 3000 : 45000;
    const timer = setInterval(() => {
      fetchNews(false);
    }, pollInterval);

    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [selectedCity, isBackgroundLoading]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-between">
      <Navbar
        selectedCity={selectedCity}
        onCityChange={setSelectedCity}
      />

      <main className="container mx-auto px-4 py-8 flex-grow max-w-4xl">
        {error && (
          <div className="bg-red-150 border border-red-300 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">
            {selectedCity === "All" ? "National Trending News" : `${selectedCity} Local News`}
          </h1>
          
          {isBackgroundLoading && news.length > 0 && (
            <div className="flex items-center space-x-2 text-blue-600 bg-blue-50 px-3 py-1.5 rounded-full text-xs font-semibold animate-pulse border border-blue-100">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-600"></span>
              </span>
              <span>{statusText}</span>
            </div>
          )}
        </div>

        {loading || (news.length === 0 && isBackgroundLoading) ? (
          <div className="flex flex-col justify-center items-center py-24 space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="text-gray-500 text-sm font-medium animate-pulse text-center">
              {statusText}
            </p>
          </div>
        ) : (
          <>
            {news.length === 0 ? (
              <div className="bg-white rounded-lg shadow-sm border border-gray-150 p-12 text-center text-gray-500">
                <p className="text-lg font-medium text-gray-600">No articles found for {selectedCity}.</p>
                <p className="text-sm text-gray-400 mt-1">
                  Please try selecting another location or check back in a moment.
                </p>
              </div>
            ) : (
              <div className="grid gap-8">
                {news.map((item, index) => (
                  <article
                    key={index}
                    className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200 overflow-hidden"
                  >
                    {item.image_urls && (
                      <div className="w-full h-64 overflow-hidden relative bg-gray-100">
                        <img
                          src={item.image_urls}
                          alt={item.title}
                          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800";
                          }}
                        />
                      </div>
                    )}
                    <div className="p-6">
                      <h2 className="text-2xl font-bold text-gray-900 leading-tight mb-4">
                        {item.title}
                      </h2>
                      <div className="space-y-4">
                        {item.paragraphs.map((paragraph, pIndex) => (
                          <p key={pIndex} className="text-gray-650 leading-relaxed text-base">
                            {paragraph}
                          </p>
                        ))}
                      </div>
                      <div className="mt-6 flex items-center justify-between border-t border-gray-100 pt-4">
                        <span className="inline-block px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-semibold uppercase tracking-wider">
                          {item.city}
                        </span>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default App;
