import requests
import os

VT_API_KEY = os.getenv("VT_API_KEY")

def analyze_md5(md5_hash: str):

    url = f"https://www.virustotal.com/api/v3/files/{md5_hash}"

    headers = {
        "x-apikey": VT_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Hash not found or API error"}

    data = response.json()

    stats = data["data"]["attributes"]["last_analysis_stats"]

    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    harmless = stats.get("harmless", 0)
    undetected = stats.get("undetected", 0)

    total_engines = malicious + suspicious + harmless + undetected
    total_detected = malicious + suspicious

    risk_level = "Low"

    if malicious >= 10:
        risk_level = "High"
    elif malicious > 0:
        risk_level = "Medium"

    return {
        "hash": md5_hash,
        "malicious": malicious,
        "suspicious": suspicious,
        "harmless": harmless,
        "undetected": undetected,
        "total_engines": total_engines,
        "total_detected": total_detected,
        "risk_level": risk_level
    }