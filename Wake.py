import pyaudio
import numpy as np
import openwakeword
from openwakeword.model import Model

print("Verifying and downloading pre-trained wake word models...")
openwakeword.utils.download_models()

# 1. Audio Configuration Parameters
# openWakeWord strictly requires 16000Hz sample rate and Mono audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280  # 1280 samples = exactly 80ms frame size

# 2. Initialize the PyAudio Microphone Stream
audio_interface = pyaudio.PyAudio()
mic_stream = audio_interface.open(
    format=FORMAT, 
    channels=CHANNELS, 
    rate=RATE, 
    input=True, 
    frames_per_buffer=CHUNK
)

# 3. Load the wake word engine (Loading the pre-trained 'hey jarvis' model)
print("Loading openWakeWord model...")
model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

print("\n" + "="*40)
print(" Microphone is now LIVE. Say 'Hey Jarvis'...")
print("="*40 + "\n")

try:
    while True:
        # Read raw binary data from the running microphone stream
        raw_data = mic_stream.read(CHUNK, exception_on_overflow=False)
        
        # Convert raw binary audio bytes into a flat 1D integer NumPy array
        audio_frame = np.frombuffer(raw_data, dtype=np.int16)
        
        # Feed the 80ms frame to openWakeWord
        prediction = model.predict(audio_frame)
        
        # Pull the specific confidence score for our wake word
        jarvis_score = prediction.get("hey_jarvis", 0.0)
        
        # Thresholding: 0.5 is usually the sweet spot for responsiveness vs false alarms
        if jarvis_score > 0.3:
            print(f" Wake Word Detected! (Confidence: {jarvis_score:.2f})")
            
            # This is where you trigger actions, e.g., kick off your Faster-Whisper script!

except KeyboardInterrupt:
    print("\nStopping live microphone stream...")
finally:
    # Clean up hardware resources cleanly on exit
    mic_stream.stop_stream()
    mic_stream.close()
    audio_interface.terminate()