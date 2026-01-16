import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    msg = request.json.get('message', '').strip()
    if not msg:
        return jsonify({'response': 'Say something!'}) 
    
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": msg}]}
        )
        return jsonify({"response": resp.json()["choices"][0]["message"]["content"]})
    except:
        return jsonify({"response": "Oops! Try again?"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
