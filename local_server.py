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

    upload_response = rq.post(f"http://{remote_server_host}/upload_transcript", files=files)

    if upload_response.status_code != 200:
        return "Remote server upload failure", 400

    upload_response_dict = json.loads(upload_response.json())

    server_transcript_filepath = upload_response_dict['transcript_filepath']

    summary_request_body = {
        "transcript_filepath": server_transcript_filepath
    }

    summarize_response = rq.post(f"http://{remote_server_host}/summarize", json=summary_request_body)

    if summarize_response.status_code != 200:
        return "Remote server summarize failure", 400

    summarize_response_dict = json.loads(summarize_response.json())

    summary = summarize_response_dict['summary']

    create_draft_email(summary)
