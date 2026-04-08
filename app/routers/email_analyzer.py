from fastapi import APIRouter, UploadFile, File
from email import policy
from email.parser import BytesParser
import re

router = APIRouter(prefix="/email", tags=["Email Analyzer"])


SUSPICIOUS_KEYWORDS = [
    "verify", "login", "urgent", "bank", "password", "click"
]


def extract_links(text):
    return re.findall(r'https?://\S+', text)


def analyze_headers(msg):

    headers = dict(msg.items())

    from_addr = headers.get("From")
    return_path = headers.get("Return-Path")
    received = headers.get("Received")
    subject = headers.get("Subject")

    spoof_flag = False

    if return_path and from_addr and return_path not in from_addr:
        spoof_flag = True

    return {
        "from": from_addr,
        "return_path": return_path,
        "subject": subject,
        "spoof_possible": spoof_flag
    }


def analyze_body(msg):

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    links = extract_links(body)

    keyword_flag = any(word in body.lower() for word in SUSPICIOUS_KEYWORDS)

    return {
        "links": links,
        "suspicious_keywords": keyword_flag
    }


# @router.post("/analyze-eml")
# async def analyze_eml(file: UploadFile = File(...)):

#     content = await file.read()

#     msg = BytesParser(policy=policy.default).parsebytes(content)

#     header_analysis = analyze_headers(msg)
#     body_analysis = analyze_body(msg)

#     # Risk scoring
#     risk = "Low"

#     if header_analysis["spoof_possible"]:
#         risk = "High"
#     elif body_analysis["suspicious_keywords"]:
#         risk = "Medium"

#     return {
#         "headers": header_analysis,
#         "body": body_analysis,
#         "risk_level": risk
#     }
@router.post("/analyze-eml")
async def analyze_eml(file: UploadFile = File(...)):

    content = await file.read()

    msg = BytesParser(policy=policy.default).parsebytes(content)

    header_analysis = analyze_headers(msg)
    body_analysis = analyze_body(msg)

    reasons = []

    #  Spoof detection
    if header_analysis["spoof_possible"]:
        reasons.append("Return-Path does not match From address (possible spoofing)")

    #  Suspicious keywords
    if body_analysis["suspicious_keywords"]:
        reasons.append("Suspicious keywords detected (login / verify / urgent)")

    #  Suspicious links
    suspicious_links = [
        link for link in body_analysis["links"]
        if any(k in link.lower() for k in ["login", "verify", "secure"])
    ]

    if suspicious_links:
        reasons.append("Suspicious links detected")

    #  Risk logic
    if header_analysis["spoof_possible"]:
        risk = "High"
    elif body_analysis["suspicious_keywords"] or suspicious_links:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "headers": header_analysis,
        "body": body_analysis,
        "risk_level": risk,
        "reasons": reasons  
    }