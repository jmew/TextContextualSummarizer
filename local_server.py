import os

from flask import Flask, request
from werkzeug import secure_filename
import requests as rq
import pythoncom

from email_util import create_draft_email

app = Flask(__name__)

remote_server_host = "52.252.106.91:5000"
local_filepath = "C:/Users/siunnith/Downloads"

@app.route("/")
def hello_world():
    return "hello world from local server"

@app.route("/test_mail_client")
def test_mail_client():
    pythoncom.CoInitialize()
    create_draft_email("hello world from local Kalmiya server")
    return "created draft mail"

@app.route("/summarize", methods=['POST'])
def summarize():
    if not request.is_json:
        return "Invalid JSON", 400
    else:
        print("Valid JSON")

    req = request.get_json()

    file_path = req.get('transcript_filepath')

    if 'transcript_file' is None:
        return "Missing transcript file path", 400
    
    files = {'transcript': open(os.path.join(local_filepath, file_path), 'rb')}

    print(f"Upload URL: http://{remote_server_host}/upload_transcript")

    upload_response = rq.post(f"http://{remote_server_host}/upload_transcript", files=files)

    if upload_response.status_code != 200:
        return "Remote server upload failure", 400
    else:
        print("Successfully uploaded file")

    upload_response_dict = upload_response.json()

    server_transcript_filepath = upload_response_dict['transcript_filepath']

    summary_request_body = {
        "transcript_filepath": server_transcript_filepath
    }

    summarize_response = rq.post(f"http://{remote_server_host}/summarize", json=summary_request_body)

    if summarize_response.status_code != 200:
        return "Remote server summarize failure", 400
    else:
        print("Successfully transcribed and summarized")

    summarize_response_dict = summarize_response.json()

    summary = summarize_response_dict['summary']

    pythoncom.CoInitialize()
    create_draft_email(summary)

    return "Successfully created email!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
