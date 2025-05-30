import requests
from utils.planet_name_mapper import planet_names

API_URL = "https://api.le-systeme-solaire.net/rest/bodies/"

def get_planet_data(planet_en):
    try:
        response = requests.get(f"{API_URL}{planet_en.lower()}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data for {planet_en}, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"API Error: {e}")
        return None

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def get_planet_info_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data:
        return f"عذرًا، لم أتمكن من الحصول على معلومات {planet_ar}."
    mass = data.get("mass", {}).get("massValue", "غير متوفر")
    gravity = data.get("gravity", "غير متوفر")
    moons_count = len(data.get("moons", [])) if data.get("moons") else 0
    return f"{planet_ar} هو كوكب بكتلة تقريبية {mass}×10ⁿ كجم، جاذبيته حوالي {gravity} م/ث²، وله {moons_count} قمرًا."

def get_planet_temperature_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data or "avgTemp" not in data:
        return f"عذرًا، لا يمكنني الحصول على درجة الحرارة على {planet_ar}."
    temp_celsius = kelvin_to_celsius(data["avgTemp"])
    return f"درجة الحرارة المتوسطة على {planet_ar} هي حوالي {temp_celsius} درجة مئوية."

def get_planet_distance_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data or "semimajorAxis" not in data:
        return f"عذرًا، لا أملك معلومات عن المسافة إلى {planet_ar}."
    distance_km = data["semimajorAxis"]
    return f"{planet_ar} يبعد عن الشمس حوالي {distance_km:,} كيلومتر."

def get_planet_composition_arabic(planet_ar):
    composition_data = {
        "المريخ": "الحديد والصخور البازلتية وثاني أكسيد الكربون",
        "الزهرة": "الصخور السيليكاتية وحمض الكبريتيك في الغلاف الجوي",
        "الأرض": "الحديد والنيكل في النواة، الصخور السيليكاتية في القشرة",
        "عطارد": "الحديد والنيكل مع قشرة رقيقة من الصخور",
        "المشتري": "الهيدروجين والهيليوم بشكل أساسي",
        "زحل": "الهيدروجين والهيليوم مع كثافة منخفضة",
        "أورانوس": "الماء والميثان والأمونيا المجمدة",
        "نبتون": "الماء والميثان والأمونيا مع الهيدروجين والهيليوم"
    }
    composition = composition_data.get(planet_ar)
    if composition:
        return f"{planet_ar} يتكون بشكل أساسي من {composition}."
    else:
        return f"عذرًا، لا توجد معلومات دقيقة عن تركيب {planet_ar}."

def get_planet_orbit_duration_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data or "sideralOrbit" not in data:
        return f"عذرًا، لا أستطيع تحديد مدة دورة {planet_ar}."
    days = round(data["sideralOrbit"], 1)
    years = round(days / 365.25, 2)
    if years < 1:
        return f"{planet_ar} يستغرق حوالي {days} يومًا ليدور حول الشمس."
    else:
        return f"{planet_ar} يستغرق حوالي {years} سنة ({days} يومًا) ليدور حول الشمس."

def get_planet_moons_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data:
        return f"عذرًا، لم أتمكن من الوصول إلى بيانات {planet_ar}."
    moons = data.get("moons")
    if not moons:
        return f"{planet_ar} لا يملك أي أقمار."
    moon_names = ", ".join([moon["moon"] for moon in moons[:5]])  # Show first 5 moons
    total_moons = len(moons)
    if total_moons <= 5:
        return f"{planet_ar} لديه {total_moons} قمرًا وهي: {moon_names}."
    else:
        return f"{planet_ar} لديه {total_moons} قمرًا، من أشهرها: {moon_names}."

def get_planet_habitability_arabic(planet_ar):
    if planet_ar == "الأرض":
        return "بالطبع، الأرض صالحة للحياة وهي الكوكب الوحيد المعروف بوجود الحياة عليه."
    elif planet_ar == "المريخ":
        return f"{planet_ar} قد يكون صالحًا للحياة في الماضي، ولا يزال العلماء يدرسون إمكانية وجود حياة ميكروبية عليه."
    else:
        return f"حاليًا، لا يوجد دليل على إمكانية العيش على {planet_ar} بالظروف الحالية."

def get_planet_gravity_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data or "gravity" not in data:
        return f"عذرًا، لا يمكنني الحصول على معلومات الجاذبية على {planet_ar}."
    gravity = data["gravity"]
    earth_gravity = 9.8
    gravity_ratio = round(gravity / earth_gravity, 2)
    return f"الجاذبية على {planet_ar} هي {gravity} م/ث² (حوالي {gravity_ratio} ضعف جاذبية الأرض)."

def get_planet_day_length_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data or "sideralRotation" not in data:
        return f"عذرًا، لا أستطيع تحديد طول اليوم على {planet_ar}."
    hours = round(data["sideralRotation"], 2)
    return f"طول اليوم على {planet_ar} هو حوالي {hours} ساعة."

def get_planet_year_length_arabic(planet_ar):
    return get_planet_orbit_duration_arabic(planet_ar)

def get_planet_atmosphere_arabic(planet_ar):
    atmosphere_data = {
        "الأرض": "النيتروجين (78%) والأكسجين (21%) مع غازات أخرى",
        "المريخ": "ثاني أكسيد الكربون (95%) مع غلاف جوي رقيق",
        "الزهرة": "ثاني أكسيد الكربون (96%) مع ضغط جوي عالي جداً",
        "عطارد": "غلاف جوي رقيق جداً يحتوي على الأكسجين والصوديوم",
        "المشتري": "الهيدروجين والهيليوم مع عواصف عملاقة",
        "زحل": "الهيدروجين والهيليوم مع رياح قوية",
        "أورانوس": "الهيدروجين والهيليوم والميثان",
        "نبتون": "الهيدروجين والهيليوم والميثان مع رياح سريعة جداً"
    }
    atmosphere = atmosphere_data.get(planet_ar)
    if atmosphere:
        return f"الغلاف الجوي لـ {planet_ar} يتكون من {atmosphere}."
    else:
        return f"عذرًا، لا توجد معلومات دقيقة عن الغلاف الجوي لـ {planet_ar}."

def get_planet_color_arabic(planet_ar):
    color_knowledge = {
        "المريخ": "أحمر بسبب أكسيد الحديد (الصدأ)",
        "زحل": "مصفر ذهبي",
        "أورانوس": "أزرق مائل للأخضر بسبب الميثان",
        "نبتون": "أزرق غامق بسبب الميثان",
        "الزهرة": "أصفر باهت مع سحب بيضاء",
        "الأرض": "أزرق وأخضر وبني مع سحب بيضاء",
        "عطارد": "رمادي مائل للبني",
        "المشتري": "برتقالي وبني مع خطوط ملونة",
        "بلوتو": "بني محمر"
    }
    color = color_knowledge.get(planet_ar)
    if color:
        return f"{planet_ar} يبدو {color}."
    else:
        return f"ليس لدي معلومات دقيقة عن لون {planet_ar}."

def get_planet_size_arabic(planet_ar):
    planet_en = planet_names.get(planet_ar)
    if not planet_en:
        return f"عذرًا، لا أملك معلومات عن {planet_ar}."
    data = get_planet_data(planet_en)
    if not data or "meanRadius" not in data:
        return f"لا توجد بيانات دقيقة عن حجم {planet_ar}."
    radius = data["meanRadius"]
    earth_radius = 6371  # km
    size_ratio = round(radius / earth_radius, 2)
    return f"نصف قطر {planet_ar} هو حوالي {radius:,} كيلومتر (حوالي {size_ratio} ضعف حجم الأرض)."

def get_planet_rings_arabic(planet_ar):
    ringed_planets = {
        "زحل": "نعم، زحل مشهور بحلقاته الجميلة المكونة من الجليد والصخور.",
        "أورانوس": "نعم، أورانوس لديه حلقات رقيقة تم اكتشافها في عام 1977.",
        "نبتون": "نعم، نبتون لديه حلقات رقيقة وغير مكتملة.",
        "المشتري": "نعم، المشتري لديه حلقات رقيقة جداً تم اكتشافها في عام 1979."
    }
    if planet_ar in ringed_planets:
        return ringed_planets[planet_ar]
    else:
        return f"لا، {planet_ar} لا يحتوي على حلقات معروفة."

def get_planet_existence_arabic(planet_ar):
    if planet_ar in planet_names:
        return f"نعم، {planet_ar} هو كوكب حقيقي ومعروف في نظامنا الشمسي."
    elif planet_ar == "نيبيرو":
        return "نيبيرو هو كوكب خيالي ولا يوجد دليل علمي على وجوده."
    else:
        return f"لا توجد معلومات مؤكدة عن كوكب يسمى {planet_ar} في نظامنا الشمسي."

def get_planet_satellites_missions_arabic(planet_ar):
    known_missions = {
        "المريخ": "مثل مسبار كيوريوسيتي، برسفيرنس، ومارس إكسبريس، وإنسايت",
        "الزهرة": "مثل بعثات فينيرا السوفيتية وماجلان الأمريكية",
        "نبتون": "مثل مسبار فوياجر 2 الذي زاره في عام 1989",
        "أورانوس": "مثل مسبار فوياجر 2 الذي زاره في عام 1986",
        "زحل": "مثل مسبار كاسيني الذي درسه لمدة 13 عامًا",
        "المشتري": "مثل مسابير فوياجر وجونو وجاليليو",
        "عطارد": "مثل مسبار مسنجر وبيبي كولومبو"
    }
    missions = known_missions.get(planet_ar)
    if missions:
        return f"تمت دراسة {planet_ar} من خلال بعثات فضائية {missions}."
    else:
        return f"لا توجد بيانات دقيقة لدي عن البعثات التي استكشفت {planet_ar}."

# Intent to handler mapping for use in assistant.py
intent_handlers = {
    "ask_info": get_planet_info_arabic,
    "ask_temp": get_planet_temperature_arabic,
    "ask_distance": get_planet_distance_arabic,
    "ask_composition": get_planet_composition_arabic,
    "ask_orbit": get_planet_orbit_duration_arabic,
    "ask_moons": get_planet_moons_arabic,
    "ask_habitable": get_planet_habitability_arabic,
    "ask_gravity": get_planet_gravity_arabic,
    "ask_day_length": get_planet_day_length_arabic,
    "ask_year_length": get_planet_year_length_arabic,
    "ask_atmosphere": get_planet_atmosphere_arabic,
    "ask_color": get_planet_color_arabic,
    "ask_size": get_planet_size_arabic,
    "ask_rings": get_planet_rings_arabic,
    "ask_existence": get_planet_existence_arabic,
    "ask_satellite": get_planet_satellites_missions_arabic
}