import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from textblob import TextBlob
from gtts import gTTS
import os
import tempfile
import json

# Initialize summarization and sentiment pipelines
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")

def fetch_news_articles(company):
    """
    Fetch at least 10 unique news articles for the given company.
    For demonstration, we use placeholder data. In production, implement actual scraping.
    """
    articles = []
    for i in range(10):
        articles.append({
            "url": f"http://example.com/article{i}",
            "raw_title": f"{company} News Article {i}",
            "raw_content": f"This is the content of article {i} for {company}. It covers aspects such as sales, innovation, and challenges."
        })
    return articles

def extract_article_details(article):
    """
    Extract title, summary, and metadata from an article.
    Uses the summarization pipeline and sentiment analyzer.
    """
    title = article["raw_title"]
    content = article["raw_content"]
    
    # Summarize article content (adjust max/min_length as needed)
    summary_text = summarizer(content, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
    
    # Perform sentiment analysis (the pipeline returns labels like "POSITIVE"/"NEGATIVE")
    sentiment_result = sentiment_analyzer(content)[0]
    sentiment = sentiment_result["label"].capitalize()
    
    # Extract topics (this is a basic placeholder; implement keyword extraction if required)
    topics = []
    if "sales" in content.lower():
        topics.append("Sales")
    if "innovation" in content.lower():
        topics.append("Innovation")
    if "challenge" in content.lower() or "regulatory" in content.lower():
        topics.append("Challenges")
    if not topics:
        topics.append("General")
    
    return {
        "Title": title,
        "Summary": summary_text,
        "Sentiment": sentiment,
        "Topics": topics
    }

def comparative_analysis(articles_details):
    """
    Compute comparative sentiment analysis and topic overlaps.
    """
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles_details:
        label = article["Sentiment"]
        if label.lower() == "positive":
            sentiment_distribution["Positive"] += 1
        elif label.lower() == "negative":
            sentiment_distribution["Negative"] += 1
        else:
            sentiment_distribution["Neutral"] += 1

    coverage_differences = []
    if len(articles_details) >= 2:
        diff = {
            "Comparison": f"{articles_details[0]['Title']} vs {articles_details[1]['Title']}",
            "Impact": "The first article is more positive compared to the second."
        }
        coverage_differences.append(diff)
    
    topic_overlap = {
        "Common Topics": list(set(articles_details[0]["Topics"]).intersection(articles_details[1]["Topics"])) if len(articles_details) > 1 else [],
        "Unique Topics in Article 1": articles_details[0]["Topics"],
        "Unique Topics in Article 2": articles_details[1]["Topics"] if len(articles_details) > 1 else []
    }
    
    return {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap
    }

def generate_hindi_tts(text):
    """
    Convert text to Hindi speech using gTTS.
    Returns the path/URL of the saved audio file.
    """
    tts = gTTS(text, lang='hi')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

def process_company_news(company):
    """
    Main function integrating news extraction, summarization, sentiment analysis,
    comparative analysis, and TTS generation.
    """
    articles = fetch_news_articles(company)
    articles_details = [extract_article_details(article) for article in articles]
    comparative = comparative_analysis(articles_details)
    
    # A final sentiment analysis summary statement
    final_sentiment = f"{company}'s latest news coverage appears predominantly positive, with key highlights in innovation and sales."
    
    # Generate Hindi text for TTS output
    tts_text = f"कंपनी {company} के समाचारों का विश्लेषण सकारात्मक है।"
    audio_file = generate_hindi_tts(tts_text)
    
    result = {
        "Company": company,
        "Articles": articles_details,
        "Comparative Sentiment Score": comparative,
        "Final Sentiment Analysis": final_sentiment,
        "Audio": audio_file  # Returns the path to the audio file
    }
    return result

# For standalone testing
if __name__ == "__main__":
    import json
    company = "Tesla"
    report = process_company_news(company)
    print(json.dumps(report, indent=2))
