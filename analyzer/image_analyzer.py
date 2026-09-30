import re
from pathlib import Path

from PIL import Image

from utils.ocr import extract_text_from_image


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
    "verify",
    "verification",
    "login",
    "log in",
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
    "reset password",
    "credential",
    "bank",
    "wallet",
    "invoice",
    "otp",
    "one time password",
    "authentication",
]


def analyze_image(image_path: str) -> dict:
    """
    Perform basic forensic analysis of an image/screenshot.
    """

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = Image.open(image_path)

    width, height = image.size

    image_format = image.format
    color_mode = image.mode

    ocr_text = extract_text_from_image(image_path)

    urls = sorted(
        set(
            re.findall(
                URL_PATTERN,
                ocr_text,
                re.IGNORECASE
            )
        )
    )

    emails = sorted(
        set(
            re.findall(
                EMAIL_PATTERN,
                ocr_text
            )
        )
    )

    ips = sorted(
        set(
            re.findall(
                IP_PATTERN,
                ocr_text
            )
        )
    )

    text_lower = ocr_text.lower()

    suspicious_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword.lower() in text_lower:

            suspicious_keywords.append(keyword)

    return {
        "file_name": path.name,
        "image_format": image_format,
        "width": width,
        "height": height,
        "color_mode": color_mode,
        "ocr_text": ocr_text,
        "urls": urls,
        "emails": emails,
        "ip_addresses": ips,
        "suspicious_keywords": suspicious_keywords,
    }
