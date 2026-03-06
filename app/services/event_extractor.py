import re

THREAT_KEYWORDS = {
    "cyber": ["ransomware", "malware", "data breach", "hack"],
    "conflict": ["attack", "missile", "strike", "military", "war"],
    "intel": ["espionage", "spy", "leak"]
}

COUNTRY_COORDS = {
    "Ukraine": (48.3794, 31.1656),
    "Russia": (61.5240, 105.3188),
    "Israel": (31.0461, 34.8516),
    "China": (35.8617, 104.1954),
    "India": (20.5937, 78.9629),
    "United States": (37.0902, -95.7129)
}

def classify_event(text):
    text = text.lower()

    for category, words in THREAT_KEYWORDS.items():
        for word in words:
            if word in text:
                return category

    return "general"


def detect_country(text):
    for country in COUNTRY_COORDS:
        if country.lower() in text.lower():
            lat, lon = COUNTRY_COORDS[country]
            return country, lat, lon

    return None, None, None


def extract_event(article):
    title = article["title"]

    category = classify_event(title)
    country, lat, lon = detect_country(title)

    if not country:
        return None

    return {
        "title": title,
        "source": article["source"],
        "country": country,
        "latitude": lat,
        "longitude": lon,
        "category": category
    }