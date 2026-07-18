# 🏦 AI Loan Advisory Chatbot

An AI-powered Loan Advisory Agent that allows users to ask loan-related
questions in natural language and instantly receive accurate, source-backed answers.

## 🎯 Features

- 💬 **Intelligent Chatbot** — Ask any loan question in natural language
- 🧮 **EMI Calculator** — Instant EMI calculation for all loan types
- 📊 **Loan Comparison** — Compare all loan products side by side
- 🎯 **Loan Recommender** — Get the right loan for your purpose
- 📄 **RAG Pipeline** — Answers grounded in actual financial documents
- 🔒 **Secure** — API keys never stored, all processing is private

## 🏠 Loan Types Covered

| Loan Type | Interest Rate | Max Amount | Max Tenure |
|-----------|--------------|------------|------------|
| Home Loan | 8.5% - 10.5% | Rs. 10 Crores | 30 years |
| Personal Loan | 10.5% - 24% | Rs. 40 Lakhs | 5 years |
| Car Loan | 7.5% - 12% | Rs. 1 Crore | 7 years |
| Education Loan | 9.5% - 13% | Rs. 1.5 Crores | 15 years |
| Business Loan | 10% - 26% | Rs. 5 Crores | 10 years |
| Gold Loan | 7% - 17% | Rs. 1 Crore | 3 years |

## 🛠️ Tech Stack

- **Cohere** — Embeddings (embed-english-v3.0) + LLM (command-r-plus)
- **Pinecone** — Vector Database for semantic search
- **Streamlit** — Interactive Web Interface
- **LangChain** — Text chunking and processing

## 📁 Project Structure

```
AI_Loan_Advisory_Chatbot/
├── app.py              ← Main Streamlit application
├── vectorstore.py      ← Document processing + Pinecone
├── chatbot.py          ← Answer generation + EMI calculator
├── loan_data.txt       ← Comprehensive loan policy dataset
├── requirements.txt    ← Dependencies
└── README.md           ← Documentation
```

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Bhoomi_Joshi_Jecrc_CEI.git
cd AI_Loan_Advisory_Chatbot
```

### 2. Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Open in browser
```
http://localhost:8501
```

## 📖 How to Use

1. Enter your **Cohere** and **Pinecone** API keys in the sidebar
2. Click **"Initialize Knowledge Base"** to load loan documents
3. Go to **Loan Chatbot** tab and ask any question
4. Use **EMI Calculator** for instant EMI calculations
5. Use **Loan Comparison** to compare all loan types

## 💡 Sample Questions

- "What is the eligibility for a home loan?"
- "What documents are needed for a personal loan?"
- "What is the interest rate for car loans?"
- "How to improve my CIBIL score?"
- "What is the MUDRA loan scheme?"
- "What is the tax benefit on education loan?"

## 📊 Dataset

The loan advisory dataset (`loan_data.txt`) is a comprehensive synthetic
financial document containing:
- Eligibility criteria for 6 loan types
- Interest rates and tenure details
- EMI calculation formulas with examples
- Required documentation lists
- Government scheme information
- CIBIL score guidelines
- FAQ section with 15+ common questions

## 🔑 API Keys

- **Cohere** (Free): [dashboard.cohere.com](https://dashboard.cohere.com)
- **Pinecone** (Free): [app.pinecone.io](https://app.pinecone.io)

## ⚠️ Disclaimer

This chatbot is for advisory purposes only.
Please consult a certified financial advisor before making loan decisions.
