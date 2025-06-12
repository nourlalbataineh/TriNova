import asyncio
import edge_tts
import pygame
import os
import uuid
import time
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

async def edge_tts_generate(text, filename, voice="ar-SA-HamedNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

def speak_arabic_enhanced(text):
   
    temp_filename = f"temp_raw_{uuid.uuid4()}.mp3"
    enhanced_filename = f"temp_enhanced_{uuid.uuid4()}.mp3"
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        asyncio.run(edge_tts_generate(text, temp_filename))
        audio = AudioSegment.from_mp3(temp_filename)
        audio = normalize(audio)
        audio = compress_dynamic_range(audio)
        audio = audio + 3 
        
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * 0.95)
        }).set_frame_rate(audio.frame_rate)
        audio.export(enhanced_filename, format="mp3", bitrate="128k")
        
        pygame.mixer.music.load(enhanced_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except Exception as e:
        print(f"Enhanced TTS error: {e}")
        speak_arabic_basic(text)
    finally:
        
        for f in [temp_filename, enhanced_filename]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception as cleanup_e:
                print(f"Cleanup error: {cleanup_e}")

def speak_arabic_basic(text):
    
    filename = f"temp_{uuid.uuid4()}.mp3"
    try:
        pygame.mixer.init()
        asyncio.run(edge_tts_generate(text, filename))
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as cleanup_e:
            print(f"Cleanup error: {cleanup_e}")

def speak_arabic(text):
    
    try:
        speak_arabic_enhanced(text)
    except ImportError:
        print("pydub not available, using basic TTS")
        speak_arabic_basic(text)