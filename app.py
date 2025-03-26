import streamlit as st
import requests

st.title("News Summarization & Sentiment Analysis")
company = st.text_input("Enter Company Name")

# Fetch News
if st.button("Fetch News"):
    if company:
        try:
            response = requests.get(f"http://127.0.0.1:5001/news?company={company}")  # Matches API port
            if response.status_code == 200:
                data = response.json()
                st.write(f"### News for {data['company']}")
                for article in data["articles"]:
                    st.write(f"**Title:** {article['title']}")
                    st.write(f"**Sentiment:** {article['sentiment']}")
                    st.write(f"[Read More]({article['link']})")
                    st.write("---")
            else:
                st.error("Error fetching news. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the API. Make sure the server is running.")
    else:
        st.error("Please enter a company name.")

# Generate Hindi Speech
if st.button("Generate Hindi Speech"):
    if company:
        text = f"{company} के समाचार विश्लेषण पूरा हुआ।"  # Proper Hindi sentence
        try:
            response = requests.post("http://127.0.0.1:5001/tts", json={"text": text})  # Matches API port
            if response.status_code == 200:
                audio_url = response.json()["audio_url"]
                st.audio(audio_url)
            else:
                st.error("Error generating speech. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the API. Make sure the server is running.")
    else:
        st.error("Please enter a company name before generating speech.")
