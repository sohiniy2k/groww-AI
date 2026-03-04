# 📊 Groww — Mutual Fund FAQ Assistant (RAG-based)

A Streamlit chatbot that answers **factual questions** about Mirae Asset Mutual Fund schemes using RAG (Retrieval-Augmented Generation). Powered by OpenAI GPT-3.5.

---

## 🏦 Scope

| Field        | Details                                                   |
|-------------|-----------------------------------------------------------|
| **Platform** | Groww                                                     |
| **AMC**      | Mirae Asset Mutual Fund                                   |
| **Schemes**  | Large Cap Fund · Flexi Cap Fund · ELSS Tax Saver Fund    |
| **Sources**  | Official AMC (miraeassetmf.co.in), AMFI, SEBI pages only |

---

## 🚀 Setup & Run

### 1. Clone / download this folder

```bash
cd mf_faq_chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Enter your OpenAI API Key in the sidebar when the app opens.

---

## 🗂️ Project Structure

```
mf_faq_chatbot/
├── app.py               # Main Streamlit app (RAG chatbot)
├── requirements.txt     # Python dependencies
├── sources.md           # 15–25 official source URLs used
├── sample_qa.md         # 10 sample Q&A with answers + citation links
└── README.md            # This file
```

---

## ✅ Features

- **Facts-only answers** — expense ratio, exit load, minimum SIP, lock-in, benchmark, riskometer
- **One source citation** in every answer (official AMC/AMFI/SEBI link)
- **Polite refusal** for opinion/advice questions (e.g., "Should I buy?")
- **No PII** — does not accept or store PAN, Aadhaar, email, phone, OTP, or account numbers
- **No performance claims** — no return comparisons; links to official factsheet instead
- **Last updated timestamp** on every answer

---

## ⚠️ Known Limits

- Expense ratios are not hardcoded (TER changes daily with AUM); the app directs users to the official page for live TER
- No real-time NAV or returns data
- Knowledge base covers 3 schemes of Mirae Asset only (Large Cap, Flexi Cap, ELSS)
- Retrieval is keyword-based (not vector/embedding-based) for simplicity

---

## 📋 Disclaimer

> This tool provides factual information only, sourced from official AMC/AMFI/SEBI public pages. It does not provide investment advice, recommendations, or return projections. Mutual Fund investments are subject to market risks. Please read all scheme-related documents carefully before investing. Consult a SEBI-registered investment adviser for personalised guidance.
