import streamlit as st
import tempfile
import os
from pathlib import Path

from analyzer.file_analyzer import analyze_file
from analyzer.pdf_analyzer import analyze_pdf
from ai.local_llm import analyze_evidence



# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="TraceLens",
    page_icon="🔎",
    layout="wide"
)

# -------------------------------------------------
# TRACELENS PROFESSIONAL DARK UI
# -------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #050b18;
    --bg2: #081426;
    --card: rgba(10, 25, 48, 0.82);
    --card-border: rgba(38, 160, 255, 0.20);
    --blue: #19b5ff;
    --cyan: #00e5ff;
    --text: #e8f1ff;
    --muted: #8da4c2;
    --green: #20e3a2;
    --yellow: #ffc857;
    --red: #ff5577;
}

/* Main application background */
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(0, 180, 255, 0.12), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(30, 80, 255, 0.10), transparent 30%),
        linear-gradient(135deg, #030814 0%, #061226 50%, #020711 100%);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* Subtle grid */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.08;
    background-image:
        linear-gradient(rgba(0, 180, 255, .18) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 180, 255, .18) 1px, transparent 1px);
    background-size: 45px 45px;
    mask-image: linear-gradient(to bottom, black, transparent 85%);
}

/* Main content width */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Headings */
h1, h2, h3 {
    color: #f1f7ff !important;
    letter-spacing: -0.02em;
}

h1 {
    font-weight: 800 !important;
}

h2, h3 {
    font-weight: 700 !important;
}

/* Paragraphs */
p, li, label {
    color: #c9d8eb !important;
}

/* Dividers */
hr {
    border-color: rgba(50, 150, 255, 0.16) !important;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background: rgba(7, 22, 43, 0.75);
    border: 1px solid rgba(0, 205, 255, 0.25);
    border-radius: 18px;
    padding: 12px;
    box-shadow:
        0 0 35px rgba(0, 160, 255, 0.07),
        inset 0 0 25px rgba(0, 100, 255, 0.025);
    transition: all .25s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(0, 220, 255, 0.55);
    box-shadow:
        0 0 35px rgba(0, 190, 255, 0.15),
        inset 0 0 30px rgba(0, 100, 255, 0.05);
}

/* Metric cards */
[data-testid="stMetric"] {
    background:
        linear-gradient(145deg,
            rgba(11, 31, 59, .92),
            rgba(5, 17, 35, .92));
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px;
    box-shadow:
        0 12px 30px rgba(0, 0, 0, .25),
        inset 0 1px 0 rgba(255,255,255,.035);
    transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(25, 181, 255, .5);
    box-shadow:
        0 15px 35px rgba(0, 130, 255, .13);
}

[data-testid="stMetricLabel"] {
    color: #8da4c2 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #f4f9ff !important;
    font-weight: 800;
}

/* Code blocks */
[data-testid="stCodeBlock"] {
    border: 1px solid rgba(0, 180, 255, .18);
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,.2);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #087fce, #0755b8);
    color: white;
    border: 1px solid rgba(70, 200, 255, .45);
    border-radius: 10px;
    font-weight: 700;
    transition: all .2s ease;
    box-shadow: 0 5px 18px rgba(0, 120, 255, .18);
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #19caff;
    box-shadow:
        0 8px 25px rgba(0, 180, 255, .3);
}

/* Info / success / warning boxes */
[data-testid="stAlert"] {
    background: rgba(8, 24, 46, .8);
    border-radius: 12px;
    border: 1px solid rgba(30, 150, 255, .2);
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(7, 22, 43, .7);
    border: 1px solid rgba(30, 150, 255, .18);
    border-radius: 14px;
}

/* AI report */
.ai-report {
    background:
        linear-gradient(145deg,
            rgba(8, 25, 48, .95),
            rgba(4, 14, 29, .95));
    border: 1px solid rgba(0, 220, 255, .25);
    border-radius: 18px;
    padding: 24px;
    margin-top: 12px;
    box-shadow:
        0 0 35px rgba(0, 180, 255, .08),
        inset 0 1px 0 rgba(255,255,255,.035);
}

/* Glow animation */
@keyframes pulseGlow {
    0%, 100% {
        box-shadow: 0 0 12px rgba(0, 210, 255, .12);
    }
    50% {
        box-shadow: 0 0 28px rgba(0, 210, 255, .25);
    }
}

.ai-report {
    animation: pulseGlow 4s ease-in-out infinite;
}

/* TraceLens badge */
.tracelens-badge {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 999px;
    background: rgba(0, 190, 255, .08);
    border: 1px solid rgba(0, 210, 255, .25);
    color: #56dfff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #030914;
}

::-webkit-scrollbar-thumb {
    background: #12385e;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #176da8;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #00e5ff;
        margin-bottom: 0;
    }

    .subtitle {
        color: #9aa4b2;
        font-size: 18px;
        margin-top: 0;
        margin-bottom: 30px;
    }

    .risk-high {
        background-color: #3b1111;
        border: 1px solid #ff4b4b;
        padding: 18px;
        border-radius: 10px;
        color: #ff7777;
        font-size: 24px;
        font-weight: 700;
    }

    .risk-medium {
        background-color: #3b2d0b;
        border: 1px solid #ffa500;
        padding: 18px;
        border-radius: 10px;
        color: #ffb84d;
        font-size: 24px;
        font-weight: 700;
    }

    .risk-low {
        background-color: #0d3320;
        border: 1px solid #00cc66;
        padding: 18px;
        border-radius: 10px;
        color: #33dd88;
        font-size: 24px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🔎 TraceLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'On-device AI-assisted digital forensics'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Investigate suspicious digital artifacts using "
    "evidence extraction, indicator correlation, and AI-assisted reasoning."
)


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a suspicious PDF",
    type=["pdf"]
)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:

        with st.spinner("Performing forensic analysis..."):

            file_evidence = analyze_file(temp_path)
            file_evidence["file_name"] = uploaded_file.name
            pdf_evidence = analyze_pdf(temp_path)

        # -------------------------------------------------
        # LOCAL AI INVESTIGATION
        # -------------------------------------------------

        combined_evidence = {
            "file_fingerprint": file_evidence,
            "pdf_forensic_evidence": pdf_evidence
        }

        with st.spinner("Running local AI investigation..."):

            ai_report = analyze_evidence(
                str(combined_evidence)
            )

        # -------------------------------------------------
        # RISK CALCULATION
        # -------------------------------------------------

        risk_score = 0

        risk_score += len(pdf_evidence["urls"]) * 15
        risk_score += len(pdf_evidence["suspicious_keywords"]) * 8

        if pdf_evidence["javascript_detected"]:
            risk_score += 30

        risk_score = min(risk_score, 100)


        if risk_score >= 60:
            risk_level = "HIGH"
            risk_class = "risk-high"

        elif risk_score >= 30:
            risk_level = "MEDIUM"
            risk_class = "risk-medium"

        else:
            risk_level = "LOW"
            risk_class = "risk-low"

        
        # -------------------------------------------------
        # THREAT SUMMARY
        # -------------------------------------------------

        st.divider()

        st.subheader("Threat Assessment")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )

        with col2:
            st.metric(
                "Risk Level",
                risk_level
            )

        with col3:
            st.metric(
                "Pages",
                pdf_evidence["page_count"]
            )


        st.markdown(
            f'<div class="{risk_class}">'
            f'⚠ {risk_level} RISK'
            f'</div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # RISK BREAKDOWN
        # -------------------------------------------------
        
        st.subheader("🧮 Risk Analysis")
        
        url_points = len(pdf_evidence["urls"]) * 15
        keyword_points = len(pdf_evidence["suspicious_keywords"]) * 8
        javascript_points = 30 if pdf_evidence["javascript_detected"] else 0
        
        risk_breakdown = [
            ("🌐 URL detected", url_points),
            ("⚠️ Suspicious keywords", keyword_points),
            ("🧩 JavaScript detected", javascript_points),
        ]
        
        for label, points in risk_breakdown:
            if points > 0:
                st.write(f"**{label}** — +{points} points")
            else:
                st.write(f"{label} — +0 points")
        
        st.divider()
        
        st.write(f"**Total calculated risk: {risk_score}/100**")

        # -------------------------------------------------
        # FILE INFORMATION
        # -------------------------------------------------

        st.divider()

        st.subheader("Artifact Fingerprint")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Filename**")
            st.code(file_evidence["file_name"])

            st.write("**File Type**")
            st.code(file_evidence["mime_type"])

            st.write("**Size**")
            st.code(f'{file_evidence["file_size_kb"]} KB')

        with col2:

            st.write("**SHA-256**")
            st.code(file_evidence["sha256"])

            st.write("**MD5**")
            st.code(file_evidence["md5"])

        # -------------------------------------------------
        # ARTIFACT TIMELINE
        # -------------------------------------------------

        st.divider()

        st.subheader("🕒 Artifact Timeline")

        timeline_events = [
            ("📄 Created", file_evidence.get("created", "Unknown")),
            ("✏️ Modified", file_evidence.get("modified", "Unknown")),
            ("👁️ Accessed", file_evidence.get("accessed", "Unknown")),
        ]

        for event_name, event_time in timeline_events:
            col1, col2 = st.columns([1, 4])

            with col1:
                st.markdown(f"**{event_name}**")

            with col2:
                st.code(str(event_time))


        # -------------------------------------------------
        # INDICATORS
        # -------------------------------------------------

        st.divider()

        st.subheader("Indicators of Interest")

        col1, col2 = st.columns(2)

        with col1:

            st.write("### 🌐 URLs")

            if pdf_evidence["urls"]:

                for url in pdf_evidence["urls"]:
                    st.warning(url)

            else:
                st.success("No URLs detected.")


            st.write("### 📧 Email Addresses")

            if pdf_evidence["emails"]:

                for email in pdf_evidence["emails"]:
                    st.info(email)

            else:
                st.write("None detected.")


        with col2:

            st.write("### ⚠ Suspicious Keywords")

            if pdf_evidence["suspicious_keywords"]:

                for keyword in pdf_evidence["suspicious_keywords"]:
                    st.warning(keyword)

            else:
                st.success("No suspicious keywords detected.")


            st.write("### 🧩 IP Addresses")

            if pdf_evidence["ip_addresses"]:

                for ip in pdf_evidence["ip_addresses"]:
                    st.warning(ip)

            else:
                st.write("None detected.")

        # -------------------------------------------------
        # EVIDENCE CORRELATION
        # -------------------------------------------------

        st.divider()

        st.subheader("🧩 Evidence Correlation")

        # Collect observable indicators
        correlation_items = []

        # URL evidence
        for url in pdf_evidence.get("urls", []):
            correlation_items.append({
                "type": "URL",
                "value": url,
                "source": "PDF text"
            })

        # Email evidence
        for email in pdf_evidence.get("emails", []):
            correlation_items.append({
                "type": "EMAIL",
                "value": email,
                "source": "PDF text"
            })

        # IP evidence
        for ip in pdf_evidence.get("ip_addresses", []):
            correlation_items.append({
                "type": "IP ADDRESS",
                "value": ip,
                "source": "PDF text"
            })

        # Keyword evidence
        for keyword in pdf_evidence.get("suspicious_keywords", []):
            correlation_items.append({
                "type": "KEYWORD",
                "value": keyword,
                "source": "Text analysis"
            })

        # JavaScript evidence
        if pdf_evidence.get("javascript_detected", False):
            correlation_items.append({
                "type": "BEHAVIOR",
                "value": "JavaScript detected",
                "source": "PDF structure"
            })


        # Display correlation count
        st.metric(
            "Observed Indicators",
            len(correlation_items)
        )

        if correlation_items:

            st.write(
                "Multiple evidence sources extracted from the artifact "
                "are shown below. These are observations, not proof of malicious activity."
            )

            for item in correlation_items:

                if item["type"] == "URL":
                    icon = "🌐"
                elif item["type"] == "EMAIL":
                    icon = "📧"
                elif item["type"] == "IP ADDRESS":
                    icon = "🖥️"
                elif item["type"] == "KEYWORD":
                    icon = "⚠️"
                else:
                    icon = "🧩"

                st.markdown(
                    f"""
                    <div style="
                        background-color:#111827;
                        border:1px solid #263244;
                        border-radius:10px;
                        padding:12px;
                        margin-bottom:8px;
                    ">
                        <b>{icon} {item["type"]}</b><br>
                        <span style="color:#00e5ff;">
                            {item["value"]}
                        </span><br>
                        <small style="color:#9aa4b2;">
                            Source: {item["source"]}
                        </small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info("No observable correlation indicators detected.")

        # -------------------------------------------------
        # AI INVESTIGATION
        # -------------------------------------------------

        st.divider()
        

        st.subheader("🤖 AI Investigation")

        st.caption(
            "Local Qwen3-0.6B analysis running on-device via ONNX Runtime"
        )

        st.markdown(
            f"""
            <div style="
                background-color:#111827;
                border:1px solid #00e5ff;
                border-radius:12px;
                padding:20px;
                color:#e5e7eb;
                line-height:1.6;
            ">
                {ai_report.replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # PDF METADATA
        # -------------------------------------------------

        st.divider()

        st.subheader("Document Metadata")

        metadata = pdf_evidence["metadata"]

        st.json(metadata)


        # -------------------------------------------------
        # TEXT EVIDENCE
        # -------------------------------------------------

        st.divider()

        st.subheader("📄 Extracted Document Text")

        st.caption("Text recovered directly from the uploaded artifact.")

        with st.expander("View extracted document text", expanded=False):
            st.markdown(
                f"""
                <div style="
                    background: #0b1730;
                    border: 1px solid #1e4f8a;
                    border-radius: 12px;
                    padding: 18px;
                    color: #dbeafe;
                    font-family: 'Consolas', 'Courier New', monospace;
                    font-size: 14px;
                    line-height: 1.7;
                    white-space: pre-wrap;
                    max-height: 450px;
                    overflow-y: auto;
                    box-shadow: 0 0 18px rgba(0, 140, 255, 0.12);
                ">
        {pdf_evidence["text_preview"]}
                """,
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # JAVASCRIPT
        # -------------------------------------------------

        st.divider()

        st.subheader("Embedded Behavior Indicators")

        if pdf_evidence["javascript_detected"]:

            st.error(
                "⚠ JavaScript-related content detected."
            )

        else:

            st.success(
                "No JavaScript indicator detected."
            )


    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


else:

    st.info(
        "Upload a PDF to begin a forensic investigation."
    )
