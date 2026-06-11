import pyaudio
import numpy as np
import pandas as pd
import wave
import io
import keyboard
import time
from faster_whisper import WhisperModel
from Config import projects

# 1. Audio Recording Configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024  # Standard buffer size for push-to-talk responsiveness

audio_interface = pyaudio.PyAudio()
vocab_words=[]
for entry in projects:
    for project_name, apps in entry.items():
        vocab_words.append(project_name)
        for app in apps:
            if isinstance(app, str):
                vocab_words.append(app)
vocabs=', '.join(vocab_words)

df=pd.read_excel('Train_data.xlsx',header=None)
all_text=df[0].astype(str).tolist()
string=" ".join(all_text).lower()
raw_words=string.split()
cleaned_words=[word.strip(".,!?()\"';:") for word in raw_words]
words=list(set(cleaned_words))
vocab=", ".join(words)
vocabs += vocab


# 2. Load Whisper Text Transcriber (CPU-Int8)
print("Loading Whisper Text Transcriber (CPU-Int8)...")
whisper_model = WhisperModel("small", device="cpu", compute_type="int8")

TRIGGER_KEY = 'insert'  # Change this to 'caps lock', 'f4', etc., if desired

print("\n" + "="*60)
print(f" SYSTEM READY: Press and HOLD [{TRIGGER_KEY.upper()}] to speak your command...")
print("="*60 + "\n")

try:
    while True: 
        # Wait until the user physically presses the trigger key down
        keyboard.wait(TRIGGER_KEY)
        
        print("\n[ Recording started... Speak now! ]")
        command_frames = []
        
        # Open a live, volatile microphone input stream
        mic_stream = audio_interface.open(
            format=FORMAT, 
            channels=CHANNELS, 
            rate=RATE, 
            input=True, 
            frames_per_buffer=CHUNK
        )
        
        # Keep pulling audio chunks as long as the user holds the key down
        while keyboard.is_pressed(TRIGGER_KEY):
            raw_data = mic_stream.read(CHUNK, exception_on_overflow=False)
            command_frames.append(raw_data)
            
        print("[ Key released. Processing speech... ]")
        
        # Clean up the mic hardware immediately so it doesn't hang open
        mic_stream.stop_stream()
        mic_stream.close()
        
        # Guard clause: Make sure they didn't just accidentally tap the key
        if len(command_frames) < 10: 
            print("Recording too short, ignoring.")
            continue

        # --- CONVERT RAM BUFFER TO IN-MEMORY WAV FILE ---
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(command_frames))
        
        wav_buffer.seek(0)
        
        # --- PASS TO WHISPER FOR TRANSCRIPTION ---
        segments, info = whisper_model.transcribe(wav_buffer, beam_size=5,language="en",initial_prompt=vocabs)
        transcript = " ".join([segment.text for segment in segments]).strip()
        
        if transcript:
            print(f"-> Transcribed Command: \"{transcript}\"")
            from Jarvis import ContinueWith
            ContinueWith(transcript)
       

            
        else:
            print("-> (No speech detected)")
            
        print(f"\nReady again. Hold [{TRIGGER_KEY.upper()}] to talk...")
        time.sleep(0.2) # Small cooldown sleep to prevent bounce double-triggers

except KeyboardInterrupt:
    print("\nShutting down keyboard assistant safely...")
finally:
    audio_interface.terminate()