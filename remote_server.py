from flask import Flask, request, make_response, jsonify
from werkzeug import secure_filename
from transcribe import transcribe_text, summarize_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./raw_transcripts"

@app.route("/summarize", methods=['POST'])
def summarize():
    if request.method != 'POST' or 'transcript' not in request.files:
        response_body = {
            "message": "Invalid request method or transcript file missing.",
            "summary": ""
        }

        return make_response(jsonify(response_body), 400)

    print("Uploading and saving VTT file to folder...")

    raw_transcript_file = request.files['transcript']

    raw_transcript_file.save(secure_filename(raw_transcript_file.filename))

    print("Converting raw transcription...")

    with open(f"./raw_transcripts/{raw_transcript_file.filename}", "rb") as raw_transcript:
        transcript = transcribe_text(raw_transcript)

    print("Summarizing raw transcription...")

    summary = summarize_text(transcript)

    response_body = {
        "message": "Valid JSON", 
        "summary": summary
    }

    return make_response(jsonify(response_body), 200)
