import requests
from app.config import ABUSEIPDB_API_KEY


def analyze_ip(ip):

    # AbuseIPDB call
    abuse_url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": ABUSEIPDB_API_KEY
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    abuse_response = requests.get(abuse_url, headers=headers, params=params)
    abuse_data = abuse_response.json()["data"]

    abuse_score = abuse_data.get("abuseConfidenceScore", 0)
    country_code = abuse_data.get("countryCode")

    # ipwho.is call
    geo_response = requests.get(f"https://ipwho.is/{ip}")
    geo_data = geo_response.json()

    country = geo_data.get("country")
    region = geo_data.get("region")
    city = geo_data.get("city")
    isp = geo_data.get("isp")
    latitude = geo_data.get("latitude")
    longitude = geo_data.get("longitude")
    asn = geo_data.get("connection", {}).get("asn")

    # Threat scoring logic
    if abuse_score > 75:
        risk = "High"
        threat_score = 90
    elif abuse_score > 40:
        risk = "Medium"
        threat_score = 60
    else:
        risk = "Low"
        threat_score = 20

    return {
        "ip": ip,
        "country": country or country_code,
        "region": region,
        "city": city,
        "isp": isp,
        "asn": asn,
        "latitude": latitude,
        "longitude": longitude,
        "abuse_score": abuse_score,
        "threat_score": threat_score,
        "risk_level": risk
    }