import re
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="cythreatlens")

geo_cache = {}

KNOWN_COUNTRIES = {
    "Iran","Israel","Ukraine","Russia","China","India","USA",
    "Spain","Germany","Iraq","Jordan","UAE","Kuwait"
}

STOP_WORDS = {
    "JUST","BREAKING","UPDATE","LIVE","USS","FOX","NEWS",
    "TRUMP","WHITE","HOUSE","SMOKE","DAMAGED","ARMY",
    "FORCE","AIR","DRONE","MISSILE","ATTACK"
}
COUNTRY_COORDS = {
    "USA": (37.0902, -95.7129),
    "India": (20.5937, 78.9629),
    "China": (35.8617, 104.1954),
    "Russia": (61.5240, 105.3188),
    "France": (46.2276, 2.2137),
    "Ukraine": (48.3794, 31.1656),
    "Israel": (31.0461, 34.8516),
    "Iran": (32.4279, 53.6880),
    "Germany": (51.1657, 10.4515),
    "Spain": (40.4637, -3.7492)
}
VALID_COUNTRIES = list(COUNTRY_COORDS.keys())

def detect_location(text):
    for country in VALID_COUNTRIES:
        if country.lower() in text.lower():
            lat, lon = COUNTRY_COORDS[country]
            return country, lat, lon

    return None, None, None


def geocode_location(place):

    if place in geo_cache:
        return geo_cache[place]

    try:
        location = geolocator.geocode(place, timeout=2)

        if location:
            result = (place, location.latitude, location.longitude)
            geo_cache[place] = result
            return result

    except:
        pass

    return None, None, None

THREAT_KEYWORDS = {
    "cyber": ["ransomware", "malware", "breach", "hack"],
    "conflict": ["attack", "missile", "strike", "drone", "war"],
    "intel": ["spy", "espionage", "leak"]
}

def classify_event(text):

    text = text.lower()

    for category, words in THREAT_KEYWORDS.items():
        for word in words:
            if word in text:
                return category

    return "general"


def extract_event(article):

    title = article["title"]

    category = classify_event(title)

    country, lat, lon = detect_location(title) 
    if country == None : country="unk"
    if (lat == None or lon == None) : lat,lon=0,0
    return {
        "title": title,
        "source": article["source"],
        "url": article.get("url") or article["source"],
        "country": country,
        "latitude": lat,
        "longitude": lon,
        "category": category,
        "date": article.get("date")
    }