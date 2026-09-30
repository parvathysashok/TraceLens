from collections import Counter


def correlate_evidence(
    file_evidence: dict,
    pdf_evidence: dict | None = None,
    image_evidence: dict | None = None,
) -> dict:
    """
    Combine evidence from multiple forensic analyzers.

    The goal is not to decide whether something is malicious.
    The goal is to organize observable evidence so an AI
    reasoning layer can interpret it later.
    """

    pdf_evidence = pdf_evidence or {}
    image_evidence = image_evidence or {}

    indicators = []

    # -----------------------------------------------------
    # FILE
    # -----------------------------------------------------

    if file_evidence:

        indicators.append({
            "type": "FILE",
            "name": "SHA-256",
            "value": file_evidence.get("sha256"),
            "source": "file_fingerprint",
        })


    # -----------------------------------------------------
    # PDF URLS
    # -----------------------------------------------------

    for url in pdf_evidence.get("urls", []):

        indicators.append({
            "type": "URL",
            "name": "Embedded URL",
            "value": url,
            "source": "pdf_text",
        })


    # -----------------------------------------------------
    # IMAGE URLS
    # -----------------------------------------------------

    for url in image_evidence.get("urls", []):

        indicators.append({
            "type": "URL",
            "name": "OCR URL",
            "value": url,
            "source": "image_ocr",
        })


    # -----------------------------------------------------
    # EMAILS
    # -----------------------------------------------------

    emails = set()

    emails.update(pdf_evidence.get("emails", []))
    emails.update(image_evidence.get("emails", []))

    for email in sorted(emails):

        indicators.append({
            "type": "EMAIL",
            "name": "Email address",
            "value": email,
            "source": "artifact_analysis",
        })


    # -----------------------------------------------------
    # IP ADDRESSES
    # -----------------------------------------------------

    ips = set()

    ips.update(pdf_evidence.get("ip_addresses", []))
    ips.update(image_evidence.get("ip_addresses", []))

    for ip in sorted(ips):

        indicators.append({
            "type": "IP",
            "name": "IP address",
            "value": ip,
            "source": "artifact_analysis",
        })


    # -----------------------------------------------------
    # SUSPICIOUS KEYWORDS
    # -----------------------------------------------------

    keywords = []

    keywords.extend(
        pdf_evidence.get(
            "suspicious_keywords",
            []
        )
    )

    keywords.extend(
        image_evidence.get(
            "suspicious_keywords",
            []
        )
    )

    keyword_counts = Counter(
        keyword.lower()
        for keyword in keywords
    )


    # -----------------------------------------------------
    # BEHAVIORAL INDICATORS
    # -----------------------------------------------------

    behavioral_indicators = []

    if pdf_evidence.get("javascript_detected"):

        behavioral_indicators.append(
            "JavaScript-related content detected"
        )


    if pdf_evidence.get("urls"):

        behavioral_indicators.append(
            "External URL detected"
        )


    if image_evidence.get("urls"):

        behavioral_indicators.append(
            "URL visible in image content"
        )


    # -----------------------------------------------------
    # CORRELATION RULES
    # -----------------------------------------------------

    correlations = []


    # PDF + image both contain URLs

    if (
        pdf_evidence.get("urls")
        and image_evidence.get("urls")
    ):

        correlations.append({
            "finding": "URL correlation",
            "description": (
                "Both document content and visual "
                "content contain URLs."
            ),
            "severity": "medium",
        })


    # Login-related keywords

    login_terms = {
        "login",
        "log in",
        "sign in",
        "signin",
        "password",
        "verify",
        "verification",
    }

    detected_login_terms = (
        set(keyword_counts.keys())
        & login_terms
    )

    if detected_login_terms:

        correlations.append({
            "finding": "Credential-related language",
            "description": (
                "Credential or account-verification "
                "language was detected."
            ),
            "severity": "medium",
            "evidence": sorted(
                detected_login_terms
            ),
        })


    # Urgency

    urgency_terms = {
        "urgent",
        "immediately",
        "account suspended",
        "security alert",
    }

    detected_urgency = (
        set(keyword_counts.keys())
        & urgency_terms
    )

    if detected_urgency:

        correlations.append({
            "finding": "Urgency indicators",
            "description": (
                "The artifact contains language "
                "designed to create urgency."
            ),
            "severity": "medium",
            "evidence": sorted(
                detected_urgency
            ),
        })


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {

        "artifact": {
            "file_name": file_evidence.get(
                "file_name"
            ),
            "sha256": file_evidence.get(
                "sha256"
            ),
            "mime_type": file_evidence.get(
                "mime_type"
            ),
        },

        "indicators": indicators,

        "keyword_counts": dict(
            keyword_counts
        ),

        "behavioral_indicators": (
            behavioral_indicators
        ),

        "correlations": correlations,

        "evidence_summary": {
            "total_indicators": len(
                indicators
            ),
            "unique_keywords": len(
                keyword_counts
            ),
            "correlation_count": len(
                correlations
            ),
        },
    }
