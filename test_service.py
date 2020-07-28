import json
import requests as rq

if __name__ == "__main__":
    files = {'transcript': open('transcript.vtt', 'rb')}

    response = rq.post(f"http://localhost:5000/summarize", files=files)

    if response.status_code != 200:
        print("Invalid response...")
        
    else:
        response = json.loads(response.json())

        print(response)
