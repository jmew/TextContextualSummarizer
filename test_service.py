import json
import requests as rq

if __name__ == "__main__":
    files = {'transcript': open('transcript.vtt', 'rb')}

    upload_response = rq.post(f"http://localhost:5000/upload_transcript", files=files)

    if upload_response.status_code != 200:
        print("Invalid upload_response...")
        
    else:
        print("Valid upload response")

        upload_response_dict = upload_response.json()
    
        server_transcript_filepath = upload_response_dict['transcript_filepath']

        summary_request_body = {
            "transcript_filepath": server_transcript_filepath
        }

        summarize_response = rq.post(f"http://localhost:5000/summarize", json=summary_request_body)

        if summarize_response.status_code != 200:
            print("Remote server summarize failure")

        else:
            print("Valid summarize response")

            summarize_response_dict = summarize_response.json()

            summary = summarize_response_dict['summary']

            print(summary)
