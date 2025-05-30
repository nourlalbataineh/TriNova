from faster_whisper import WhisperModel
from nlp_module.intent_matcher import detect_intent
from nlp_module.intents import intents
import os
from speech_recognition.transcriber import record_audio_to_wav, transcribe_audio
from assistant_logic.assistant import respond, extract_planet
from utils.wake_word import wait_for_wake_word  # <-- Import your wake word function
from utils.text_to_speech import speak_arabic

# Global variable to store currently selected planet
selected_planet_in_simulation = None

def assistant_loop():
    global selected_planet_in_simulation

    # Define exit phrases (add Arabic if you want)
    exit_phrases = [
        "that's all", "that's it", "exit", "quit", "goodbye", "bye",
        "انتهيت", "خلاص", "وداعا", "إغلاق"
    ]

    while True:
        # Record audio from user
        audio_path = record_audio_to_wav()
        if not audio_path:
            print("Recording failed.")
            continue

        print("Transcribing speech...")
        transcribed_text = transcribe_audio(audio_path)
        print(f"You said: {transcribed_text}")

        # Check for exit command
        if any(phrase in transcribed_text.lower() for phrase in exit_phrases):
            print("Exiting assistant. Goodbye!")
            break

        # Clean up audio file
        try:
            os.remove(audio_path)
        except Exception as e:
            print(f"Error removing audio file: {e}")

        # Detect user intent
        print("Detecting intent...")
        intent = detect_intent(transcribed_text)
        print(f"Detected intent: {intent}")

        # Extract planet name from text
        planet = extract_planet(transcribed_text)
        print(f"Identified planet: {planet if planet else 'None'}")

        # Handle planet selection intent by updating and notifying Unity
        if intent == "select_planet" and planet:
            selected_planet_in_simulation = planet
            # send_planet_to_unity(selected_planet_in_simulation)
            print(f"Updated selected planet to: {selected_planet_in_simulation}")

        # Generate and speak assistant response
        print("Generating response...")
        response = respond(intent, planet)
        print(f"Assistant (Arabic): {response}")

        print("\n--- Say something else or press Ctrl+C to exit ---\n")

def main():
    print("TriNova Voice Assistant is ready. Say the wake word to start.")
    while True:
        wait_for_wake_word()  # Block here until wake word is detected
        print("Wake word detected! How can I help you?")
        speak_arabic("مرحبا، كيف يمكنني مساعدتك؟")  # <-- Add this line
        assistant_loop()
        print("Say the wake word to activate the assistant again.")

if __name__ == "__main__":
    main()