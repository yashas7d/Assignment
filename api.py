from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_news, analyze_sentiment, generate_tts

app = Flask(__name__)
CORS(app)

@app.route("/news", methods=["GET"])
def fetch_news():
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400
    
    articles = get_news(company)
    
    return jsonify({"company": company, "articles": articles})

@app.route("/tts", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    audio_path = generate_tts(text)
    return jsonify({"audio_url": audio_path})

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Running on port 5001
