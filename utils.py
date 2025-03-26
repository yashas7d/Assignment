import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os

# Download required NLTK data
nltk.download("vader_lexicon")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def get_news(company_name):
    """Fetches news articles related to the given company name."""
    url = f"https://news.google.com/search?q={company_name}&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    news_items = soup.select("article")[:10]  # Get top 10 articles

    for item in news_items:
        title_element = item.find("h3")
        link_element = item.find("a", href=True)

        # Extract Title
        title = title_element.text.strip() if title_element else "Untitled News"

        # Extract Link
        if link_element:
            link = link_element["href"]
            if link.startswith("./"):
                link = "https://news.google.com" + link[1:]  # Fix relative URLs
        else:
            link = "No Link Available"

        # Add context for sentiment analysis
        full_text = f"{title}. This article discusses recent updates about {company_name}."

        # Get Sentiment
        sentiment = analyze_sentiment(full_text)

        articles.append({"title": title, "link": link, "sentiment": sentiment})
    
    return articles

def analyze_sentiment(text):
    """Performs sentiment analysis with better thresholds."""
    score = sia.polarity_scores(text)
    compound = score["compound"]

    # Adjusted sentiment thresholds
    if compound >= 0.1:  # Used to be 0.02
        return "Positive"
    elif compound <= -0.1:  # Used to be -0.02
        return "Negative"
    else:
        return "Neutral"

def generate_tts(text, lang="hi"):
    """Generates Hindi speech from text."""
    tts = gTTS(text=text, lang=lang)
    tts.save("static/output.mp3")
    return "static/output.mp3"
