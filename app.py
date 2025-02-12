from flask import Flask, request, jsonify, Response
import requests
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
GEMINI_PROMPT = os.getenv("GEMINI_PROMPT")

@app.route("/analyzeExpense", methods=["POST"])
def analyze_expense():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Không có văn bản được cung cấp"}), 400
    prompt = GEMINI_PROMPT + "\nVăn bản chi tiêu: " + text + "\n\nTrả về kết quả..."
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        gemini_response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        gemini_response.raise_for_status()
        raw_result = gemini_response.json()
    except requests.RequestException as e:
        print("Error calling Gemini API:", e)
        return jsonify({"error": "Gemini API error", "details": str(e)}), 500
    
    try:
        candidate = raw_result.get("candidates", [])[0]
        candidate_text = candidate.get("content", {}).get("parts", [])[0].get("text", "")
        candidate_text = candidate_text.strip()
        candidate_text = re.sub(r"^```json", "", candidate_text)
        candidate_text = re.sub(r"```$", "", candidate_text).strip()
        processed_result = json.loads(candidate_text)
        pretty_result = json.dumps(processed_result, indent=2, ensure_ascii=False)
    except Exception as ex:
        print("Post process error:", ex)
        pretty_result = candidate_text if candidate_text else str(raw_result)

    print("Final processed result:", pretty_result)
    return Response(pretty_result, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
