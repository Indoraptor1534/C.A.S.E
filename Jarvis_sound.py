import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import numpy as np
import pyaudio
import speech_recognition as sr
from openwakeword.model import Model
from Jarvis import ContinueWith  # Your custom backend classifier

# 1. Setup the Wake Word Listener
CHUNK_SIZE = 1280 
audio = pyaudio.PyAudio()
mic_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=CHUNK_SIZE)

oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")
recognizer = sr.Recognizer()

print("\n🎙️ Passive listening active... Just say 'Hey Jarvis'!")

while True:
    # Look for the wake word in rapid 80ms chunks
    raw_data = mic_stream.read(CHUNK_SIZE, exception_on_overflow=False)
    audio_frame = np.frombuffer(raw_data, dtype=np.int16)
    
    if oww_model.predict(audio_frame)["hey_jarvis"] > 0.6:
        print("\n⚡ Wake Word Detected!")
        
        # Pause the raw wake-word stream so it doesn't fight for the microphone
        mic_stream.stop_stream()
        
        # 2. Let SpeechRecognition handle the smart recording
        with sr.Microphone(sample_rate=16000) as source:
            print("🎤 Listening for your command...")
            # Adjusts for ambient room noise, then listens until you stop talking
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            captured_audio = recognizer.listen(source)
            
        print("🤫 Silence detected. Processing...")
        
        try:
            # 3. Transcribe your voice (Switch to local whisper/offline engine if needed)
            command_text = recognizer.recognize_google(captured_audio)
            print(f"-> Transcribed Command: '{command_text}'")
            
            # 4. Pass it straight to your lightning-fast local weights pipeline
            ContinueWith(command_text)
            
        except Exception as e:
            print("⚠️ Could not understand the speech or transcriber timed out.")

        # Restart the wake-word microphone stream
        mic_stream.start_stream()
        print("\n🎙️ Returning to background listening...")