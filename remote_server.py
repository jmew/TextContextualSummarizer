import os

from flask import Flask, request, make_response, jsonify
from transcribe import transcribe_text, summarize_text
import requests as rq

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./raw_transcripts"

@app.route("/")
def hello_world():
    return "hello world from Kalmiya API"

@app.route("/upload_transcript", methods=['POST'])
def upload_transcript():
    if request.method != 'POST' or 'transcript' not in request.files:
        response_body = {
            "message": "Invalid request method or transcript file missing.",
            "summary": ""
        }

        return make_response(jsonify(response_body), 400)

    print("Uploading and saving VTT file to folder...")

    raw_transcript_file = request.files['transcript']

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], raw_transcript_file.filename)

    raw_transcript_file.save(filepath)

    response_body = {
        "message": "File uploaded!",
        "transcript_filepath": filepath 
    }

    return make_response(jsonify(response_body), 200)

@app.route("/summarize", methods=['POST'])
def summarize():
    if request.method != 'POST' or not request.is_json:
        response_body = {
            "message": "Invalid request method or request is not JSON.",
            "summary": ""
        }

        return make_response(jsonify(response_body), 400)

    req = request.get_json()

    transcript_filepath = req.get('transcript_filepath')

    print("Converting raw transcription...")

    with open(f"./{transcript_filepath}", "rb") as raw_transcript:
        transcript = transcribe_text(raw_transcript)

    print("Summarizing raw transcription...")

    summary = summarize_text(transcript)

    response_body = {
        "message": "Valid JSON", 
        "summary": summary
    }

    return make_response(jsonify(response_body), 200)

@app.route("/url_summarize", methods=['POST'])
def url_summarize():
    if request.method != 'POST' or not request.is_json:
        response_body = {
            "message": "Invalid request method or request is not JSON.",
            "summary": ""
        }

        return make_response(jsonify(response_body), 400)

    req = request.get_json()

    transcript_url = req.get('downloadUrl')
    transcript_filepath = os.path.join(app.config['UPLOAD_FOLDER'], req.get('fileName'))

    res = rq.get(transcript_url)

    print("Received transcript URL...")

    print("Downloading transcript...")

    with open(transcript_filepath, 'wb') as transcript_file:
        transcript_file.write(res.content)

    print("Transcript downloaded...")

    print("Converting raw transcription...")

    with open(transcript_filepath, "rb") as raw_transcript:
        transcript = transcribe_text(raw_transcript)

    print("Summarizing raw transcription...")

    summary = summarize_text(transcript)

    response_body = {
        "message": "Valid JSON", 
        "summary": summary
    }

    return make_response(jsonify(response_body), 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)