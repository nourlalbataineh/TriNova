from nlp_module.intents import intents
from utils.text_to_speech import speak_arabic
# from utils.translator import translate_to_arabic, translate_with_context
from data_sources.api_fetcher import intent_handlers

planets = ["المريخ", "المشتري", "زحل", "عطارد", "نبتون", "الأرض", "أورانوس", "الزهرة"]

class AssistantConfig:
    def __init__(self):
        self.enable_tts = True 
        self.enable_translation = False  # Enable if you need to translate responses
        self.auto_speak = True 
        self.voice = "ar-SA-HamedNeural"

config = AssistantConfig()

def extract_planet(text):
    for planet in planets:
        if planet in text:
            return planet
    return None

def respond(intent, planet):

    static_responses = {
        "select_planet": lambda p: f"تم اختيار {p} في المحاكاة." if p else "يرجى تحديد كوكب.",
        "greeting": lambda p: "مرحبًا! كيف يمكنني مساعدتك؟",
        "farewell": lambda p: "إلى اللقاء! إذا احتجت أي مساعدة أخرى أنا هنا.",
        "thanks": lambda p: "على الرحب والسعة!",
        "change_language": lambda p: "تم تغيير اللغة.",
        "unknown": lambda p: "عذرًا، لم أفهم طلبك. هل يمكنك إعادة الصياغة؟"
    }

    if intent in static_responses:
        response = static_responses[intent](planet)
        if config.enable_tts:
            speak_arabic(response)
        return response

    if intent in intent_handlers:
        if not planet:
            error_messages = {
                "ask_info": "يرجى تحديد اسم الكوكب للحصول على معلومات.",
                "ask_temp": "يرجى تحديد الكوكب لمعرفة درجة حرارته.",
                "ask_distance": "لم يتم تحديد الكوكب الذي تريد معرفة مسافته.",
                "ask_composition": "يرجى تحديد الكوكب لمعرفة مكوناته.",
                "ask_orbit": "يرجى تحديد الكوكب لمعرفة تفاصيل مداره.",
                "ask_moons": "لم يتم تحديد الكوكب لمعرفة عدد أقمره.",
                "ask_habitable": "يرجى تحديد الكوكب لمعرفة إمكانيات العيش عليه.",
                "ask_gravity": "يرجى تحديد الكوكب لمعرفة معلومات الجاذبية.",
                "ask_day_length": "يرجى تحديد الكوكب لمعرفة طول اليوم.",
                "ask_year_length": "يرجى تحديد الكوكب لمعرفة طول السنة.",
                "ask_atmosphere": "يرجى تحديد الكوكب لمعرفة تفاصيل الغلاف الجوي.",
                "ask_color": "يرجى تحديد الكوكب لمعرفة لونه.",
                "ask_size": "يرجى تحديد الكوكب لمعرفة حجمه.",
                "ask_rings": "يرجى تحديد الكوكب لمعرفة إذا كان لديه حلقات.",
                "ask_existence": "يرجى تحديد اسم الكوكب للتحقق من وجوده.",
                "ask_satellite": "يرجى تحديد الكوكب لمعرفة المعلومات عن الأقمار الصناعية والبعثات."
            }
            response = error_messages.get(intent, "يرجى تحديد الكوكب المطلوب.")
            if config.enable_tts:
                speak_arabic(response)
            return response
        
        response = intent_handlers[intent](planet)
        if config.enable_tts:
            speak_arabic(response)
        return response

    response = "عذرًا، لم أفهم طلبك."
    if config.enable_tts:
        speak_arabic(response)
    return response