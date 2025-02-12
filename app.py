# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/analyzeExpense", methods=["POST"])
def analyze_expense():
    data = request.get_json()
    text = data.get("text", "")
    response = {
        "description": "mua cơm",
        "amount": 30000,
        "currency": "VND",
        "category": "food"
    }
    print(response)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
