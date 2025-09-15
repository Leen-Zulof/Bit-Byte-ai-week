import sounddevice as sd
import numpy as np
import queue
import requests
import json
from vosk import Model, KaldiRecognizer
import requests
import cohere

COHERE_API_KEY = "QNUGOv4lou5BiKypRfpsUe1f5m7QVd9MmrAQED0u"
co = cohere.Client(COHERE_API_KEY)

model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def record_and_transcribe():
    print("🎤 Speak now (Ctrl+C to stop)...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print("📝 Transcribed:", text)
                    return text

def send_to_n8n(text):
    url = "https://mira-allawama.app.n8n.cloud/webhook-test/voice-agent"  
    payload = {"message": text}
    requests.post(url, json=payload)

def get_cohere_reply(text):
    try:
        response = co.chat(
            model="command-r",     
            message=text
        )
        return response.text.strip()
    except Exception as e:
        print("Error from Cohere:", e)
        return "Sorry, I could not process that."

if __name__ == "__main__":
    msg = record_and_transcribe()         
    ai_reply = get_cohere_reply(msg)      
    print("🤖 AI Reply:", ai_reply)
    send_to_n8n(ai_reply)                 

