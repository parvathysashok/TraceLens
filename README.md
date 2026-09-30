🔎 TraceLens
On-Device AI-Assisted Digital Forensics & Evidence Correlation

TraceLens is a privacy-conscious digital forensics platform for investigating suspicious PDF artifacts. It combines deterministic forensic analysis, evidence extraction, indicator correlation, risk assessment, and local AI-assisted reasoning in an interactive Streamlit dashboard.

The AI analysis runs locally using Qwen3-0.6B + ONNX Runtime, so sensitive forensic evidence does not need to be sent to a cloud AI service.

✨ Features

🔐 Artifact Fingerprinting

SHA-256

MD5

File type

File size

📄 PDF Forensic Analysis

Page count

PDF metadata

Creation/modification information

Producer and creator information

Extracted document text

🔎 Indicator Extraction

URLs

Email addresses

IP addresses

Suspicious keywords

Security-related language

🧩 Evidence Correlation

Combines multiple observable indicators

Shows indicator sources

Provides a structured investigation view

⚠️ Deterministic Risk Assessment

Evidence-based scoring

LOW / MEDIUM / HIGH severity levels

Independent of AI-generated guesses

🤖 Local AI Investigation

Qwen3-0.6B

ONNX Runtime

CPU inference

AI-assisted evidence interpretation

🕒 Artifact Timeline

Created

Modified

Accessed

🖥️ Interactive Dashboard

Streamlit-based interface

Dark cybersecurity-themed UI

Investigator-oriented presentation

🏗️ Architecture
                 ┌─────────────────────┐
                 │   Suspicious PDF    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  File Fingerprint   │
                 │ SHA-256 / MD5       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  PDF Forensic       │
                 │  Analysis           │
                 └──────────┬──────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
       ┌────────────────┐      ┌────────────────┐
       │ Indicator      │      │ PDF Metadata   │
       │ Extraction     │      │ & Text         │
       └───────┬────────┘      └───────┬────────┘
               │                       │
               └───────────┬───────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Evidence Correlation│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Deterministic Risk  │
                 │ Assessment           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Local Qwen3-0.6B    │
                 │ AI Investigation    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Streamlit Dashboard │
                 └─────────────────────┘

🛠️ Technology Stack
Component	Technology
Language	Python
Frontend	Streamlit
AI Model	Qwen3-0.6B
AI Runtime	ONNX Runtime
Inference	CPU
Document Analysis	PDF analysis libraries
Hashing	SHA-256 / MD5
Interface	Streamlit
📂 Project Structure
TraceLens/
│
├── ai/
│   └── local_llm.py
│
├── analyzer/
│   ├── file_analyzer.py
│   └── pdf_analyzer.py
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
└── test/


The exact structure may vary depending on the current project version.

⚙️ Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/TraceLens.git
cd TraceLens

2. Create a virtual environment
Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

🤖 Local AI Model

TraceLens uses Qwen3-0.6B through ONNX Runtime.

The model is loaded locally and inference is performed using:

CPUExecutionProvider


No external AI API is required for the forensic AI analysis.

Make sure the required model and tokenizer files are placed in the location expected by:

ai/local_llm.py

🚀 Running TraceLens

Start the Streamlit application:

streamlit run app.py


Then open the local Streamlit address shown in your terminal.

Upload a suspicious PDF and TraceLens will automatically perform the forensic analysis.

🔬 Investigation Workflow

TraceLens follows this workflow:

Upload Artifact
      ↓
Calculate File Hashes
      ↓
Analyze PDF Structure
      ↓
Extract Metadata
      ↓
Extract Document Text
      ↓
Detect Indicators
      ↓
Correlate Evidence
      ↓
Calculate Risk Score
      ↓
Local AI Investigation
      ↓
Generate Investigation Report

📊 Example Investigation

For a PDF containing account-verification language, TraceLens may identify:

Risk Score: 55/100
Risk Level: MEDIUM

URL:
https://example.com/login

Email:
security@example.com

Keywords:
verify your account
login
sign in
immediately
security alert


The system then presents the observations alongside the artifact fingerprint, metadata, timeline, correlation results, and local AI-assisted analysis.

Indicators are observations and should be independently validated during a complete investigation.

🔐 Privacy

TraceLens is designed with local processing in mind.

The forensic artifact and extracted evidence can remain on the investigator's machine while the local Qwen3-0.6B model provides AI-assisted analysis.

This architecture reduces dependence on external AI APIs and is particularly useful when working with sensitive documents.

⚠️ Disclaimer

TraceLens is an investigative assistance and research tool.

Risk scores and AI-generated explanations should not be treated as definitive proof of malicious activity. Findings should be validated using appropriate forensic procedures and additional evidence.

Do not open, execute, or interact with suspicious URLs or files outside an appropriate controlled environment.

🔮 Future Development

Planned or potential improvements include:

 OCR-based image analysis

 DOCX/XLSX artifact analysis

 YARA rule integration

 URL reputation analysis

 MITRE ATT&CK mapping

 Evidence graph visualization

 Multi-file investigations

 Case management

 Automated forensic report generation

 Additional local AI models

 Standardized evidence export

🎯 Project Goal

The goal of TraceLens is to demonstrate how traditional digital forensics and privacy-conscious local AI can work together to make suspicious artifact investigation faster, more structured, and easier to understand.

TraceLens

Extract. Correlate. Investigate.
