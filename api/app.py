from flask import Flask, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator import run_pipeline
from db.database import get_all_runs, init_db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
init_db()

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    
    if not data or 'code' not in data:
        return jsonify({"error": "No code provided"}), 400
    
    # Code file mein save karo
    with open("temp_input.py", "w") as f:
        f.write(data['code'])
    
    # Pipeline chalao
    result = run_pipeline("temp_input.py")
    
    if result:
        return jsonify({
            "status": "success",
            "bug_found": result['bug_report'].get('bug_description'),
            "pr_url": result.get('pr_url') or "PR already exists"
        })
    else:
        return jsonify({"status": "failed"}), 500

@app.route('/runs', methods=['GET'])
def get_runs():
    rows = get_all_runs()
    runs = []
    for row in rows:
        runs.append({
            "id": row[0],
            "timestamp": row[1],
            "input_file": row[2],
            "bug_found": row[3],
            "fixed": bool(row[4]),
            "pr_url": row[5],
            "status": row[6]
        })
    return jsonify(runs)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bug-to-PR Agent API is running!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000) 
