from flask import Flask, request
from werkzeug import secure_filename
import requests as rq

from email_util import create_draft_email

app = Flask(__name__)

remote_server_host = "12.27.0.0:5000"

@app.route("/summarize")
def summarize():
    if not request.is_json:
        return "Invalid JSON", 400
    
    req = request.get_json()

    file_path = req.get('transcript_file_path')

    if 'transcript_file' is None:
        return "Missing transcript file path", 400
    
    files = {'transcript_': open(file_path, 'rb')}

    response = rq.post(f"http://{remote_server_host}/summarize", files=files)

    if response.status_code != 200:
        return "Remote server failure", 400

    response_dict = json.loads(response.json())

    summary = response_dict['summary']

    create_draft_email(summary)
