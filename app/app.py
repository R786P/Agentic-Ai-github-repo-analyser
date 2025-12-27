from flask import Flask, request, jsonify
from agents import run_analysis_agent
import os

app = Flask(__name__)

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    repo_url = data.get('repo_url')
    analysis_mode = data.get('analysis_mode')
    
    if not repo_url or not analysis_mode:
        return jsonify({"error": "Missing repo_url or analysis_mode"}), 400

    try:
        result = run_analysis_agent(repo_url, analysis_mode)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
