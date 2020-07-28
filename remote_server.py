import os

from flask import Flask, request, make_response, jsonify
from werkzeug import secure_filename
from transcribe import transcribe_text, summarize_text

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

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(raw_transcript_file.filename))

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
