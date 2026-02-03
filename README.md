# 📊 DocuMind: Business Intelligence Engine

**A GenAI-powered analytics dashboard that transforms unstructured business documents into structured risk metrics and strategic insights.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vighnesh-shetty-vs-documind-bi-engine-app-e02umc.streamlit.app/)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-blue)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Built%20with-Python-yellow)](https://www.python.org/)

---

## ⚡ Quick Start (Demo Access)

Want to try the app immediately? You can use this **Test API Key** to unlock the dashboard features without creating your own Google Cloud account.

* **Test Key:** `AIzaSyCQ9ShPiz3f1avJ4v_zpm21nAlbd7g4IFE`
    *(Note: This key is for demonstration/testing purposes only. Please use your own key for production use.)*

---

## 🚀 Overview

**DocuMind** is not just a chatbot; it is an **Automated Risk Auditor**. 

In the modern enterprise, critical data is often locked inside unstructured PDFs (contracts, internal memos, financial reports). DocuMind utilizes **Google's Gemini 1.5 Flash** model to ingest these documents, perform cross-reference analysis, and output quantifiable business metrics.

**Key Value Proposition:**
* **Structured Data Extraction:** Converts "legalese" text into JSON-based risk scores (0-100).
* **Cross-Document Intelligence:** Detects contradictions between multiple files (e.g., *Contract A* says Net-0 payment, but *Internal Memo B* promises Net-60).
* **Visual Analytics:** Visualizes risk severity and compliance gaps using dynamic dataframes.

---

## 📸 Project Demo

### 1. Automated Risk Audit (Compliance Dashboard)
*The AI acts as a Senior Risk Analyst, scanning contracts for unlimited liability, zero warranties, and ambiguous terms.*
![Risk Dashboard](screenshots/risk_audit_1.png)

*Visualizing the severity of detected risks in real-time.*
![Risk Factors](screenshots/risk_audit_2.png)

### 2. Strategic Cross-Referencing (RAG)
*Instead of simple Q&A, the engine finds discrepancies across different file types (Contracts vs. Internal Memos).*
![Cross Reference Chat](screenshots/cross_reference_2.png)

### 3. Executive Briefing
*Generates C-Suite level summaries highlighting contradictions and financial exposure.*
![Executive Brief](screenshots/executive_brief_2.png)

---

## 🛠️ Technical Architecture

This project bridges the gap between **Data Analytics** and **Generative AI**.

* **LLM Engine:** `Google Gemini 1.5 Flash` (Optimized for long-context windows).
* **Frontend:** `Streamlit` (Python-based interactive dashboard).
* **Data Processing:** `Pandas` (Dataframe manipulation) & `PyPDF2` (Text extraction).
* **Prompt Engineering:** Specialized "System Instructions" that force the LLM to output valid **JSON** for data visualization, rather than just text.
* **Resiliency:** Implements custom "Retry Logic" to handle API rate limits (HTTP 429) gracefully.

---

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/vighnesh-shetty-vs/documind_bi_engine.git](https://github.com/vighnesh-shetty-vs/documind_bi_engine.git)
    cd documind_bi_engine
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```
    *When prompted, enter the Demo Key provided above or your own personal API key.*

---

## 🧪 Test Data (Mock Scenarios)

To see the "Risk Analysis" in action, try uploading these conflicting documents:

1.  **Vendor Contract (Apex Systems):** Contains "Unlimited Liability" and "Net-0 Payment" terms.
2.  **Internal Memo:** Claims "We negotiated Net-60 payment terms" (Direct Contradiction).
3.  **Safe Contract:** A standard low-risk agreement for comparison.

**The Result:** DocuMind will flag the payment discrepancy immediately in the "Strategic Chat" tab.

---

## 👤 Author

**Vighnesh Shetty**
*MSc Data Analytics for Business | KEDGE Business School*

Building tools that turn **Unstructured Data** into **Business Decisions**.

[LinkedIn Profile](https://www.linkedin.com/in/vighnesh-shetty-vs/)
