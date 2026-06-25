intents = {
    "select_planet": {
    "description": "User wants to select or focus on a specific planet in the simulation.",
        "examples": [
            "حدد المريخ",
            "اختر كوكب المشتري",
            "أريد رؤية زحل",
            "روح إلى عطارد",
            "اختار كوكب نبتون"
        ],
        "keywords": ["حدد", "اختر", "رؤية", "روح", "اختار"]
    },

    "ask_info": {
        "description": "User is asking general information about a planet.",
        "examples": [
            "أخبرني عن المريخ",
            "ما الذي تعرفه عن زحل؟",
            "أريد معلومات عن عطارد"
        ],
        "keywords": ["عن", "معلومات", "تعرف"]
    },
    "ask_distance": {
        "description": "User is asking about how far a planet is.",
        "examples": [
            "كم تبعد الأرض؟",
            "ما هي المسافة إلى نبتون؟",
            "المسافة بيننا وبين زحل"
        ],
        "keywords": ["كم", "يبعد", "المسافة"]
    },
    "ask_temp": {
        "description": "User is asking about the temperature of a planet.",
        "examples": [
            "ما هي درجة حرارة المريخ؟",
            "كم تبلغ حرارة الزهرة؟"
        ],
        "keywords": ["درجة", "حرارة", "الحرارة"]
    },
    "greeting": {
        "description": "User says hello.",
        "examples": [
            "مرحبا",
            "أهلاً",
            "السلام عليكم"
        ],
        "keywords": ["مرحبا", "أهلاً", "السلام"]
    },
    "farewell": {
        "description": "User says goodbye.",
        "examples": [
            "مع السلامة",
            "وداعاً",
            "إلى اللقاء",
            "انتهيت",
            "خلاص",
            "وداعا",
            "إغلاق"

        ],
        "keywords": ["سلامة", "وداع", "اللقاء"]
    },
    "ask_composition": {
        "description": "User is asking what a planet is made of.",
        "examples": [
            "مم يتكون المريخ؟",
            "ما مكونات زحل؟",
            "هل يتكون نبتون من غاز؟"
        ],
        "keywords": ["يتكون", "مكونات", "غاز", "صخور", "تركيب"]
    },
    "ask_orbit": {
        "description": "User is asking about a planet's orbit.",
        "examples": [
            "كم يستغرق المريخ ليدور حول الشمس؟",
            "ما مدة دورة الأرض؟",
            "ما زمن دوران عطارد؟"
        ],
        "keywords": ["يدور", "حول", "دورته", "مدار", "زمن", "مدة"]
    },
    "ask_moons": {
        "description": "User is asking about a planet's moons.",
        "examples": [
            "كم قمراً للمشتري؟",
            "ما أسماء أقمار أورانوس؟",
            "هل للمريخ أقمار؟"
        ],
        "keywords": ["قمر", "أقمار", "تابع", "أسماء"]
    },
    "ask_habitable": {
        "description": "User is asking if a planet can support life.",
        "examples": [
            "هل يمكن العيش على المريخ؟",
            "هل الحياة ممكنة على الزهرة؟",
            "هل زحل صالح للسكن؟"
        ],
        "keywords": ["العيش", "الحياة", "صالح", "سكن", "قابل"]
    },
    "ask_satellite": {
        "description": "User is asking about satellites or space missions.",
        "examples": [
            "هل هناك أقمار صناعية تدور حول المريخ؟",
            "ما هي البعثات التي استكشفت نبتون؟",
            "ما اسم القمر الصناعي الذي صور زحل؟"
        ],
        "keywords": [ "أقمار صناعية","قمر صناعي", "بعثات", "مهمات", "استكشاف", "صور"]
    },
    "thanks": {
        "description": "User is thanking the assistant.",
        "examples": [
            "شكراً",
            "أشكرك",
            "ممتن لك"
        ],
        "keywords": ["شكراً", "أشكرك", "ممتن", "شكر"]
    },
    "change_language": {
        "description": "User wants to change the language.",
        "examples": [
            "بدّل اللغة إلى الإنجليزية",
            "أريد استخدام اللغة الإنجليزية",
            "تكلم بالإنجليزية"
        ],
        "keywords": ["لغة", "الإنجليزية", "بدّل", "تكلم"]
    },
    "ask_gravity": {
        "description": "User is asking about gravity on a planet.",
        "examples": [
            "ما هي الجاذبية على زحل؟",
            "كم تبلغ الجاذبية على المريخ؟",
            "هل الجاذبية على عطارد ضعيفة؟"
        ],
        "keywords": ["جاذبية", "الثقل", "تجاذب"]
    },
    "ask_day_length": {
        "description": "User is asking how long a day lasts on a planet.",
        "examples": [
            "كم يبلغ طول اليوم على المريخ؟",
            "ما مدة اليوم في الزهرة؟",
            "كم ساعة في يوم نبتون؟"
        ],
        "keywords": ["طول اليوم", "مدة اليوم", "كم ساعة", "يوم"]
    },
    "ask_year_length": {
        "description": "User is asking how long a year is on a planet.",
        "examples": [
            "كم يستغرق العام على المشتري؟",
            "ما مدة السنة في أورانوس؟"
        ],
        "keywords": ["عام", "سنة", "مدة السنة", "كم يوم"]
    },
    "ask_atmosphere": {
        "description": "User is asking about a planet's atmosphere.",
        "examples": [
            "ما مكونات الغلاف الجوي للمريخ؟",
            "هل هناك هواء على الزهرة؟",
            "هل يحتوي نبتون على أكسجين؟"
        ],
        "keywords": ["الغلاف الجوي", "هواء", "أكسجين", "غازات"]
    },
    "ask_color": {
        "description": "User is asking about the color or appearance of a planet.",
        "examples": [
            "ما لون زحل؟",
            "لماذا المريخ أحمر؟",
            "هل أورانوس أزرق؟"
        ],
        "keywords": ["لون", "أحمر", "أزرق", "أخضر", "رمادي", "مظهر"]
    },
    "ask_size": {
        "description": "User is asking about the size or diameter of a planet.",
        "examples": [
            "كم حجم المشتري؟",
            "ما قطر الأرض؟",
            "هل زحل أكبر من أورانوس؟"
        ],
        "keywords": ["مساحة السطح","حجم", "قطر", "أكبر", "أصغر", "مساحة"]
    },
    "ask_rings": {
        "description": "User is asking if a planet has rings.",
        "examples": [
            "هل لزحل حلقات؟",
            "كم حلقة لكوكب أورانوس؟",
            "هل توجد حلقات حول نبتون؟"
        ],
        "keywords": ["حلقة", "حلقات", "حول"]
    },
    "ask_existence": {
        "description": "User is asking if a planet exists or is real.",
        "examples": [
            "هل كوكب بلوتو حقيقي؟",
            "هل نيبيرو موجود؟",
            "هل توجد كواكب أخرى لم نكتشفها؟"
        ],
        "keywords": ["يوجد", "موجود", "حقيقي", "خيالي", "غير مكتشف"]
    },
    "unknown": {
        "description": "Fallback intent when the system doesn't understand.",
        "examples": [],
        "keywords": []
    }
}