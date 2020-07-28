import json
import requests as rq

if __name__ == "__main__":
    files = {'transcript': open('transcript.vtt', 'rb')}

    response_json = rq.Request('POST', '0.0.0.0:5000/summarize', files=files)

    response = json.loads(response_json)

    print(response)
