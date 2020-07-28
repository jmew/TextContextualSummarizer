from summarizer import Summarizer

class Message:
    def __init__(self, user, message):
        self.user = user
        self.message = message
    
    def append(self, message):
        self.message = self.message + " " + message

class Transcript:
    def __init__(self):
        self.conversation = []

    def addMessage(self, user, message):
        if len(self.conversation) > 0 and self.conversation[-1].user == user:
            prevMessage = self.conversation[-1]
            prevMessage.append(message)
        else:
            newMessage = Message(user, message)
            self.conversation.append(newMessage)

    def exportAsTxt(self):
        with open("output.txt", "w") as txt_file:
            for msg in self.conversation:
                txt_file.write("".join(msg.message) + " ")
            
    def toString(self):
        output = ""
        for msg in self.conversation:
            output += "".join(msg.message) + " "
        return output

def transcribe_text(raw_transcript):
    transcript = Transcript()

    for count, line in enumerate(raw_transcript, start=0):
        if count % 3 == 0:
            line = str(line)
            if line.find('<') == -1:
                continue
            
            user = line[line.find('<') + 1 : line.find('>')]
            msg = line[line.find('>') + 1 : -9]
            transcript.addMessage(user, msg)
    
    return transcript

def summarize_text(transcript):
    model = Summarizer()
    result = model(transcript.toString(), min_length=60)
    full = ''.join(result)
    
    return full

if __name__ == "__main__":
    # rely on local testing transcript
    with open("transcript.vtt", "rb") as raw_transcript:
        transcript = transcribe_text(raw_transcript)

        summary = summarize_text(transcript)

        print(summary)
