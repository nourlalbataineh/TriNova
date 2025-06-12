import sounddevice as sd
import numpy as np
import tempfile
import wave
import os
from faster_whisper import WhisperModel
import noisereduce as nr
from fuzzywuzzy import fuzz

model = WhisperModel("base", device="cpu", compute_type="int8")

# List of accepted wake word variations
wake_words = [
    "Hey TriNova",
    "Hey tri nova",
    "trinova",
    "tri nova",
    "تراي نوفا",
    "تري نوفا",
    "تراينوفا",
    "تري نوفاء"
]

DURATION = 3.0  
SAMPLE_RATE = 16000
FUZZY_THRESHOLD = 60 

def record_audio(duration=DURATION, samplerate=SAMPLE_RATE, reduce_noise=False):
    print("Listening for wake word...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()

    # Optional noise reduction
    if reduce_noise:
        float_audio = audio.flatten().astype(np.float32)
        denoised = nr.reduce_noise(y=float_audio, sr=samplerate)
        audio = denoised.astype(np.int16).reshape(-1, 1)

    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_wav.name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())

    return temp_wav.name

def contains_wake_word(text):
    text = text.lower().strip()
    for wake_word in wake_words:
        score = fuzz.token_set_ratio(text, wake_word)
        print(f"Checking '{text}' vs '{wake_word}' → Score: {score}")
        if score >= FUZZY_THRESHOLD:
            print(f"Fuzzy match with '{wake_word}' (score {score})")
            return True
    return False

def transcribe_and_check(file_path):
    segments, _ = model.transcribe(file_path)
    for segment in segments:
        print(f"Transcript: {segment.text}")
        if contains_wake_word(segment.text):
            return True
    return False

def main_loop():
    try:
        while True:
            audio_file = record_audio(reduce_noise=True)  # Set True to test denoising
            if transcribe_and_check(audio_file):
                print("Wake word 'TriNova' detected!")
                break
            os.remove(audio_file)
    except KeyboardInterrupt:
        print("\n Exiting.")
    finally:
        sd.stop()
        
def wait_for_wake_word():
   
    try:
        while True:
            audio_file = record_audio(reduce_noise=True)
            if transcribe_and_check(audio_file):
                print("Wake word 'TriNova' detected!")
                os.remove(audio_file)
                break
            os.remove(audio_file)
    except KeyboardInterrupt:
        print("\n Exiting.")
    finally:
        sd.stop()