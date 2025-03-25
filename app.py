import streamlit as st
import requests
import json

st.set_page_config(page_title="News Summarization & Sentiment Analysis", layout="wide")
st.title("News Summarization & Sentiment Analysis for Companies")

# User input
company = st.text_input("Enter Company Name", "Tesla")

if st.button("Generate Report"):
    payload = {"company": company}
    
    try:
        response = requests.post("http://localhost:8000/analyze", json=payload)
        
        if response.status_code == 200:
            data = response.json()

            if "Company" in data and "Articles" in data:
                st.subheader(f"Sentiment Report for {data['Company']}")

                # Display each article's details
                for article in data.get("Articles", []):
                    st.markdown(f"**Title:** {article.get('Title', 'N/A')}")
                    st.markdown(f"**Summary:** {article.get('Summary', 'N/A')}")
                    st.markdown(f"**Sentiment:** {article.get('Sentiment', 'N/A')}")
                    st.markdown(f"**Topics:** {', '.join(article.get('Topics', []))}")
                    st.write("---")

                # Comparative sentiment analysis
                if "Comparative Sentiment Score" in data:
                    st.subheader("Comparative Sentiment Analysis")
                    st.json(data["Comparative Sentiment Score"])
                
                # Final sentiment analysis summary
                if "Final Sentiment Analysis" in data:
                    st.markdown("### Final Sentiment Analysis")
                    st.markdown(data["Final Sentiment Analysis"])
                
                # Audio playback
                if "Audio" in data:
                    st.markdown("### Hindi TTS Output")
                    st.audio(data["Audio"])
            else:
                st.error("Unexpected API response format.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {str(e)}")
    
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
