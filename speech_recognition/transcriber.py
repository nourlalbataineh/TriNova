import os
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from fuzzywuzzy import process
from faster_whisper import WhisperModel
import noisereduce as nr

DURATION = 5  # seconds to record
SAMPLE_RATE = 16000  # required sample rate for Whisper
FUZZY_MATCH_THRESHOLD = 80  # Threshold for correcting planet names

planet_names = [  # List of planet names in Arabic
    "عطارد", "الزهرة", "الأرض", "المريخ",
    "المشتري", "زحل", "أورانوس", "نبتون", "بلوتو"
]

def record_audio_to_wav(duration=DURATION, sample_rate=SAMPLE_RATE):
    """Records audio and saves it to a temporary WAV file. Returns the file path."""
    try:
        print(f"Speak now... (Recording {duration} seconds)")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        print("Recording complete.")
    except Exception as e:
        print(f"Error during recording: {e}")
        return None

    # Noise reduction
    reduced_noise = nr.reduce_noise(y=recording.flatten(), sr=sample_rate)
    recording = reduced_noise.astype(np.int16)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav.write(temp_file.name, sample_rate, recording)
        return temp_file.name

def correct_planet_name(transcribed_text):
    """Function to correct planet names using fuzzy matching."""
    best_match, score = process.extractOne(transcribed_text, planet_names)
    if score > FUZZY_MATCH_THRESHOLD:
        return best_match
    return transcribed_text  # Return original if no close match


def transcribe_audio(audio_path):
    model = WhisperModel("large-v3", device="cpu", compute_type="float32") # "medium" for faster compute

    segments, info = model.transcribe(audio_path, language="ar")
    
    full_text = ""
    for segment in segments:
        full_text += segment.text.strip() + " "

    return full_text.strip()