import threading
from faster_whisper import WhisperModel
from nlp_module.intent_matcher import detect_intent
from nlp_module.intents import intents
import os
from speech_recognition.transcriber import record_audio_to_wav, transcribe_audio
from assistant_logic.assistant import respond, extract_planet
from utils.wake_word import wait_for_wake_word
from utils.text_to_speech import speak_arabic
from utils.planet_name_mapper import planet_names
from SocketConn.Socketconn import lock_object, sock
from HTedit.HT_last_edit import run_image_interaction

selected_planet_in_simulation = None

def process_user_interaction():
    global selected_planet_in_simulation

    audio_path = record_audio_to_wav()
    if not audio_path:
        print("Recording failed.")
        return

    print("Transcribing speech...")
    transcribed_text = transcribe_audio(audio_path)
    print(f"You said: {transcribed_text}")

    try:
        os.remove(audio_path)
    except Exception as e:
        print(f"Error removing audio file: {e}")

    print("Detecting intent...")
    intent = detect_intent(transcribed_text)
    print(f"Detected intent: {intent}")

    planet = extract_planet(transcribed_text)
    print(f"Identified planet: {planet if planet else 'None'}")

    if intent == "select_planet" and planet:
        selected_planet_in_simulation = planet_names.get(planet).capitalize()
        lock_object(sock, selected_planet_in_simulation)
        print(f"Updated selected planet to: {planet}")

    print("Generating response...")
    response = respond(intent, planet)
    print(f"Assistant (Arabic): {response}")

    return intent

def assistant_session():
    while True:
        wait_for_wake_word()
        print("Wake word detected! How can I help you?")
        speak_arabic("مرحبا، كيف يمكنني مساعدتك؟")
        while True:
            intent = process_user_interaction()
            if intent == "farewell":
                print("Farewell detected. Exiting assistant session.")
                break
        print("Say the wake word to activate the assistant again.")

def main():
    print("TriNova Voice Assistant is ready. Say the wake word to start.")

    assistant_thread = threading.Thread(target=assistant_session, daemon=True)
    assistant_thread.start()

    run_image_interaction()

    assistant_thread.join()

if __name__ == "__main__":
    main()

    #text_normalization.