from .intents import intents
import re

def normalize_arabic(text):
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'[ًٌٍَُِّْ]', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def detect_intent(text):
    text = normalize_arabic(text)

    best_intent = "unknown"
    max_score = 0

    for intent_name, data in intents.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in text:
                score += 1
        if score > max_score:
            best_intent = intent_name
            max_score = score

    return best_intent