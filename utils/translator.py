from deep_translator import GoogleTranslator

# Planet name mappings to preserve correct Arabic names
planet_replacements = {
    "mercury": "عطارد",
    "venus": "الزهرة", 
    "earth": "الأرض",
    "mars": "المريخ",
    "jupiter": "المشتري",
    "saturn": "زحل",
    "uranus": "أورانوس",
    "neptune": "نبتون",
    "pluto": "بلوتو"
}

def translate_to_arabic(text):
    """
    Translate English text to Arabic while preserving planet names
    """
    try:
        # First translate the text
        translated = GoogleTranslator(source='en', target='ar').translate(text)
        
        # Then replace any incorrectly translated planet names
        for english_planet, arabic_planet in planet_replacements.items():
            # Check for common mistranslations and replace them
            if english_planet.lower() in text.lower():
                # The planet was mentioned in English, ensure Arabic version is correct
                translated = ensure_planet_name_in_arabic(translated, arabic_planet)
        
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def ensure_planet_name_in_arabic(arabic_text, correct_planet_name):
    """
    Ensure the correct Arabic planet name appears in the translated text
    """
    # Common mistranslations we want to fix
    wrong_translations = [
        "الشفرة",  # "code" - common mistranslation for Earth
        "الارض",   # Earth without proper diacritics
        "كوكب الأرض",  # Sometimes gets mangled
        "هذا الكوكب"   # "this planet" - we want the actual name
    ]
    
    # Replace "this planet" with the actual planet name
    arabic_text = arabic_text.replace("هذا الكوكب", correct_planet_name)
    
    # Fix other mistranslations
    for wrong in wrong_translations:
        if wrong in arabic_text and correct_planet_name not in arabic_text:
            arabic_text = arabic_text.replace(wrong, correct_planet_name)
    
    return arabic_text

def translate_with_context(text, planet_name_arabic=None):
    """
    Enhanced translation function that provides better context
    """
    try:
        # Add context to help translation
        if planet_name_arabic:
            context_text = f"About the planet {planet_name_arabic}: {text}"
            translated = GoogleTranslator(source='en', target='ar').translate(context_text)
            # Remove the context part, keeping only the translated response
            if ":" in translated:
                translated = translated.split(":", 1)[1].strip()
        else:
            translated = GoogleTranslator(source='en', target='ar').translate(text)
        
        # Apply planet name corrections if a specific planet was mentioned
        if planet_name_arabic:
            translated = ensure_planet_name_in_arabic(translated, planet_name_arabic)
            
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text