import face_recognition
import cv2
import os
import pickle
import datetime

def start_voice_agent():
    """
    Runs the voice_handler.py script to activate the voice agent.
    """
    print("[🎤] Starting Voice Agent...")
    subprocess.run(["python", "voice_handler.py"])

def main():
    print("=== AI Land Authentication Gateway ===")
    username = input("Enter your username: ").strip()
    image_path = input("Enter path to your image: ").strip()

    if not os.path.exists(image_path):
        print("[❌] Image not found.")
        speak_text("Image not found. Please try again.")
        return

    status, confidence = verify_user(username, image_path)

    if status == "Access Granted":
        speak_text(f"Welcome {username}, Access Granted.")
        start_voice_agent()
    else:
        speak_text("Access Denied. Authorities have been alerted.")
        print("[🚨] Access attempt blocked.")

if __name__ == "__main__":
    train_face_encodings(dataset_path="train")
