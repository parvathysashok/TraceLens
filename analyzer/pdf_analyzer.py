import re
from pathlib import Path

import pymupdf


URL_PATTERN = r"https?://[^\s<>\"]+"

EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

IP_PATTERN = (
    r"\b(?:"
    r"(?:25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\."
    r"){3}"
    r"(?:25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\b"
)


SUSPICIOUS_KEYWORDS = [
    "password",
    "verify your account",
    "verify account",
    "login",
    "sign in",
    "signin",
    "urgent",
    "immediately",
    "click here",
    "confirm your identity",
    "account suspended",
    "security alert",
    "update payment",
    "payment failed",
    "invoice",
    "reset password",
    "credential",
    "download",
    "enable macros",
]


def analyze_pdf(file_path: str) -> dict:
    """
    Perform static forensic analysis of a PDF.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    document = pymupdf.open(file_path)

    full_text = ""

    for page in document:
        full_text += page.get_text() + "\n"

    metadata = document.metadata

    urls = sorted(set(re.findall(URL_PATTERN, full_text, re.IGNORECASE)))
    emails = sorted(set(re.findall(EMAIL_PATTERN, full_text)))
    ips = sorted(set(re.findall(IP_PATTERN, full_text)))

    text_lower = full_text.lower()

    suspicious_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword.lower() in text_lower:
            suspicious_keywords.append(keyword)

    javascript_detected = False

    for page in document:
        page_text = page.get_text()

        if "javascript" in page_text.lower():
            javascript_detected = True

    raw_pdf_text = full_text[:10000]

    result = {
        "page_count": len(document),
        "metadata": {
            "title": metadata.get("title"),
            "author": metadata.get("author"),
            "subject": metadata.get("subject"),
            "creator": metadata.get("creator"),
            "producer": metadata.get("producer"),
            "creation_date": metadata.get("creationDate"),
            "modification_date": metadata.get("modDate"),
        },
        "urls": urls,
        "emails": emails,
        "ip_addresses": ips,
        "suspicious_keywords": suspicious_keywords,
        "javascript_detected": javascript_detected,
        "text_preview": raw_pdf_text,
    }

    document.close()

    return result
