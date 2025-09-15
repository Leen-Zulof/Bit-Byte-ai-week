from flask import Flask, request
import pyttsx3

app = Flask(__name__)

engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1.0)  

def speak_text(reply):
    print("🤖 AI Reply:", reply)
    engine.say(reply)
    engine.runAndWait()

@app.route("/reply", methods=["POST"])
def handle_reply():
    data = request.json
    reply = data.get("answer", "")
    if reply:
        speak_text(reply)
    return {"status": "ok"}

if __name__ == "__main__":
    print("🗣️ TTS Server running on port 5000...")
    app.run(port=5000)
