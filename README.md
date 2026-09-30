# 🔎 TraceLens
## On-Device AI-Assisted Digital Forensics

TraceLens is a lightweight cybersecurity forensic investigation tool that analyzes suspicious PDF artifacts using deterministic evidence extraction, indicator correlation, risk scoring, and local AI-assisted analysis.

The project is designed to help investigators quickly understand the contents and characteristics of a suspicious digital artifact without relying on cloud-based AI services.

## 🚀 Features

### 📄 PDF Forensic Analysis

- Extracts document metadata
- Detects embedded JavaScript
- Extracts document text
- Reports page count

### 🔐 File Fingerprinting

- SHA-256 hash
- MD5 hash
- File type
- File size
- Original filename

### 🌐 Indicator Extraction

- URLs
- Email addresses
- IP addresses
- Suspicious security-related keywords

### 🧩 Evidence Correlation

- Combines multiple indicators extracted from the same artifact
- Displays evidence sources
- Provides an investigator-friendly evidence view

### 🕒 Artifact Timeline

- Created timestamp
- Modified timestamp
- Accessed timestamp

### ⚠️ Deterministic Risk Assessment

- Calculates a reproducible risk score
- Classifies artifacts as LOW, MEDIUM, or HIGH risk
- Risk calculation is performed by the forensic engine rather than the AI model

### 🤖 Local AI Investigation

- Uses Qwen3-0.6B locally
- Runs through ONNX Runtime
- CPU inference supported
- No external AI API required
- Provides an AI-assisted explanation of extracted evidence

### 🖥️ Interactive Streamlit Dashboard

- Professional dark cybersecurity interface
- Organized forensic sections
- Upload-and-analyze workflow
- Investigator-friendly presentation

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Suspicious PDF    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   File Analyzer     │
                    │                     │
                    │ • Hashes            │
                    │ • File type         │
                    │ • File metadata     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PDF Analyzer     │
                    │                     │
                    │ • Metadata          │
                    │ • Text              │
                    │ • URLs              │
                    │ • Emails            │
                    │ • IP addresses      │
                    │ • Keywords         │
                    │ • JavaScript        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Evidence Correlation│
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Deterministic    │        │ Local AI Engine  │
       │ Risk Engine      │        │                  │
       │                  │        │ Qwen3-0.6B       │
       │ Risk Score       │        │ ONNX Runtime     │
       │ Risk Level       │        │ CPU Inference    │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    └─────────────────────┘
```

## 🛠️ Technology Stack
Technology	Purpose
Python	Core application
Streamlit	Web dashboard
ONNX Runtime	Local AI inference
Qwen3-0.6B	Local language model
PyMuPDF	PDF processing
Transformers	Tokenization/model utilities
NumPy	Numerical processing

```
📁 Project Structure
TraceLens/
│
├── app.py
│
├── analyzer/
│   ├── file_analyzer.py
│   └── pdf_analyzer.py
│
├── ai/
│   └── local_llm.py
│
├── models/
│   └── qwen3-0.6b/
│
├── requirements.txt
│
├── README.md
│
└── ...
```

## ⚙️ Installation
1. Clone the repository
```
git clone https://github.com/YOUR_USERNAME/TraceLens.git
cd TraceLens
```
3. Create a virtual environment
```
python -m venv .venv
```
4. Activate the virtual environment
Windows PowerShell
```
.\.venv\Scripts\Activate.ps1
```
Windows CMD
```
.venv\Scripts\activate
```
Linux / macOS
```
source .venv/bin/activate
```
4. Install dependencies
```
pip install -r requirements.txt
```
## 🤖 Local AI Model
TraceLens uses a locally hosted Qwen3-0.6B model through ONNX Runtime.

The AI component is designed to explain already-extracted forensic evidence rather than independently determine whether an artifact is malicious.

The architecture intentionally separates:
```
Forensic Evidence
       ↓
Deterministic Risk Calculation
       ↓
Local AI Explanation
```
This makes the risk score reproducible while allowing the local model to provide a human-readable investigation summary.

## ▶️ Running TraceLens
Start the Streamlit application:
```
streamlit run app.py
```
Then open the local Streamlit URL shown in the terminal.

Upload a suspicious PDF and TraceLens will perform the forensic analysis automatically.

## 🔍 Investigation Workflow
TraceLens follows a structured investigation pipeline:
```
1. Upload PDF
        ↓
2. Calculate file fingerprints
        ↓
3. Analyze PDF structure
        ↓
4. Extract metadata
        ↓
5. Extract URLs / emails / IPs
        ↓
6. Detect suspicious keywords
        ↓
7. Detect embedded behavior indicators
        ↓
8. Build artifact timeline
        ↓
9. Correlate evidence
        ↓
10. Calculate deterministic risk score
        ↓
11. Run local AI investigation
        ↓
12. Display forensic dashboard
```

## 📊 Example Investigation
For a sample PDF containing account-verification language, TraceLens may identify indicators such as:
```
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
```

The dashboard then presents these observations alongside:

File hashes

PDF metadata

Timeline information

Risk score

Risk level

Evidence correlation

Local AI investigation

## 🔐 Privacy
TraceLens is designed with a local-first architecture.

The forensic analysis and AI investigation can run locally on the user's machine.

No external AI API is required for the local Qwen3 inference component.

This makes the architecture suitable for demonstrations and controlled forensic analysis where sending potentially sensitive documents to external AI services may not be desirable.

## ⚠️ Important Notes
TraceLens is an investigation and analysis tool, not a definitive malware classifier.

An extracted URL, keyword, email address, or metadata field should be treated as an indicator requiring investigation rather than automatic proof of malicious activity.

The deterministic risk score is based on the project's configured rules and should not be interpreted as a universally validated threat score.

The local AI component provides an explanation of supplied evidence and should be reviewed by a human investigator.

## 🎯 Project Goals
TraceLens was developed to demonstrate how traditional digital forensics can be combined with local AI assistance.

The main goals are:

Make forensic evidence easier to understand

Reduce manual inspection time

Correlate multiple artifact indicators

Provide reproducible risk scoring

Demonstrate privacy-preserving local AI

Present forensic findings through an accessible dashboard

## 🚧 Future Improvements
Potential future enhancements include:

🔗 Advanced URL reputation analysis

🧬 Malware and file signature detection

🖼️ OCR-based visual phishing detection

📧 Email artifact analysis

🌐 Domain and IP reputation checks

📈 Advanced evidence correlation graphs

🗺️ Geographic infrastructure visualization

🧠 Improved local forensic language models

📋 Automated investigation reports

📤 PDF/HTML forensic report export

🔎 IOC search and enrichment

🧪 Sandboxed artifact analysis

## 🏆 Why TraceLens?
Traditional file analysis often produces large amounts of raw technical information.

TraceLens attempts to bridge the gap between:
```
Raw Digital Artifact
        ↓
Forensic Evidence
        ↓
Correlated Indicators
        ↓
Risk Assessment
        ↓
AI-Assisted Explanation
        ↓
Human Investigation
```
The result is a single interface for examining suspicious digital artifacts while keeping the analysis structured, explainable, and local-first.

## 👨‍💻 Author
Parvathy S Ashok

TraceLens — On-Device AI-Assisted Digital Forensics
