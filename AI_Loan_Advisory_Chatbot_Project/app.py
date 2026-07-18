import streamlit as st
import math
from vectorstore import (
    load_loan_document,
    split_text_into_chunks,
    create_embeddings,
    store_in_pinecone,
    retrieve_relevant_chunks
)
from chatbot import generate_answer, calculate_emi

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="AI Loan Advisory Chatbot",
    page_icon="🏦",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1a3a5c, #2e86c1);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.chat-user {
    background: #e8f4fd;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 4px solid #2e86c1;
}
.chat-bot {
    background: #f0f9f0;
    padding: 12px 16px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 4px solid #27ae60;
}
.emi-box {
    background: #fff3cd;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #ffc107;
    margin: 10px 0;
}
.metric-card {
    background: white;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #dee2e6;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏦 AI Loan Advisory Chatbot</h1>
    <p>Your intelligent assistant for all loan-related queries</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/bank-building.png", width=80)
st.sidebar.header("⚙️ Configuration")

cohere_api_key = st.sidebar.text_input(
    "Cohere API Key",
    type="password",
    placeholder="Enter Cohere API Key"
)
pinecone_api_key = st.sidebar.text_input(
    "Pinecone API Key",
    type="password",
    placeholder="Enter Pinecone API Key"
)

st.sidebar.markdown("---")

# Initialize knowledge base button
if st.sidebar.button("🚀 Initialize Knowledge Base", use_container_width=True):
    if not cohere_api_key or not pinecone_api_key:
        st.sidebar.error("Please enter both API keys!")
    else:
        with st.sidebar:
            with st.spinner("Loading loan documents..."):
                try:
                    text = load_loan_document("loan_data.txt")
                    st.success("✅ Documents loaded")

                    chunks = split_text_into_chunks(text)
                    st.success(f"✅ Created {len(chunks)} chunks")

                    embeddings = create_embeddings(chunks, cohere_api_key)
                    st.success("✅ Embeddings created")

                    store_in_pinecone(chunks, embeddings, pinecone_api_key)
                    st.success("✅ Knowledge base ready!")

                    st.session_state["kb_ready"] = True
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Status indicator
if st.session_state.get("kb_ready"):
    st.sidebar.success("🟢 Knowledge Base: Ready")
else:
    st.sidebar.warning("🔴 Knowledge Base: Not initialized")

st.sidebar.markdown("---")
st.sidebar.markdown("**📋 Loan Types Covered:**")
st.sidebar.markdown("""
- 🏠 Home Loan
- 💳 Personal Loan
- 🚗 Car Loan
- 🎓 Education Loan
- 💼 Business Loan
- 🥇 Gold Loan
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Get API Keys:**")
st.sidebar.markdown("- [Cohere](https://cohere.com)")
st.sidebar.markdown("- [Pinecone](https://pinecone.io)")

# ── Main Tabs ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬 Loan Chatbot", "🧮 EMI Calculator", "📊 Loan Comparison"])

# ── TAB 1: CHATBOT ────────────────────────────────────────
with tab1:
    st.subheader("Ask me anything about loans!")

    # Sample questions
    st.markdown("**💡 Try asking:**")
    cols = st.columns(3)
    sample_questions = [
        "What is the eligibility for home loan?",
        "What documents are needed for personal loan?",
        "What is the interest rate for car loan?",
        "How to improve my CIBIL score?",
        "What is the education loan moratorium?",
        "What is MUDRA loan scheme?"
    ]
    for i, q in enumerate(sample_questions):
        if cols[i % 3].button(q, key=f"sample_{i}", use_container_width=True):
            st.session_state["sample_query"] = q

    st.markdown("---")

    # Chat input
    if "sample_query" in st.session_state:
        default_query = st.session_state.pop("sample_query")
    else:
        default_query = ""

    query = st.text_input(
        "Your question:",
        value=default_query,
        placeholder="E.g., What is the minimum salary for a home loan?",
        key="chat_input"
    )

    col1, col2 = st.columns([1, 5])
    ask_btn = col1.button("🔍 Ask", use_container_width=True)
    col2.button("🗑️ Clear Chat", on_click=lambda: st.session_state.pop("chat_history", None))

    if ask_btn and query:
        if not cohere_api_key or not pinecone_api_key:
            st.warning("⚠️ Please enter API keys in the sidebar.")
        elif not st.session_state.get("kb_ready"):
            st.warning("⚠️ Please click 'Initialize Knowledge Base' first.")
        else:
            with st.spinner("🤔 Finding answer..."):
                try:
                    context = retrieve_relevant_chunks(
                        query, cohere_api_key, pinecone_api_key
                    )
                    answer = generate_answer(query, context, cohere_api_key)

                    if "chat_history" not in st.session_state:
                        st.session_state["chat_history"] = []

                    st.session_state["chat_history"].append({
                        "question": query,
                        "answer": answer
                    })
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # Display chat history
    if st.session_state.get("chat_history"):
        st.markdown("### 📝 Conversation")
        for chat in reversed(st.session_state["chat_history"]):
            st.markdown(f"""
            <div class="chat-user">👤 <b>You:</b> {chat['question']}</div>
            <div class="chat-bot">🏦 <b>Advisor:</b> {chat['answer']}</div>
            """, unsafe_allow_html=True)

# ── TAB 2: EMI CALCULATOR ─────────────────────────────────
with tab2:
    st.subheader("🧮 Loan EMI Calculator")
    st.markdown("Calculate your monthly EMI instantly")

    col1, col2 = st.columns(2)

    with col1:
        loan_type = st.selectbox("Loan Type", [
            "Home Loan", "Personal Loan", "Car Loan",
            "Education Loan", "Business Loan", "Gold Loan"
        ])

        # Default interest rates by loan type
        default_rates = {
            "Home Loan": 9.0,
            "Personal Loan": 14.0,
            "Car Loan": 9.5,
            "Education Loan": 10.5,
            "Business Loan": 16.0,
            "Gold Loan": 10.0
        }

        principal = st.number_input(
            "Loan Amount (Rs.)",
            min_value=10000,
            max_value=10000000,
            value=500000,
            step=10000,
            format="%d"
        )

        interest_rate = st.slider(
            "Interest Rate (% per annum)",
            min_value=5.0,
            max_value=30.0,
            value=default_rates[loan_type],
            step=0.25
        )

        max_tenure = 30 if loan_type == "Home Loan" else 7
        tenure = st.slider(
            "Loan Tenure (Years)",
            min_value=1,
            max_value=max_tenure,
            value=min(5, max_tenure)
        )

        calculate_btn = st.button("Calculate EMI", use_container_width=True)

    with col2:
        if calculate_btn or True:
            result = calculate_emi(principal, interest_rate, tenure)

            st.markdown("### 📊 EMI Breakdown")

            m1, m2 = st.columns(2)
            m1.metric("Monthly EMI", f"Rs. {result['emi']:,.0f}")
            m2.metric("Total Interest", f"Rs. {result['total_interest']:,.0f}")

            m3, m4 = st.columns(2)
            m3.metric("Total Payable", f"Rs. {result['total_payment']:,.0f}")
            m4.metric("Loan Tenure", f"{tenure} Years ({result['months']} months)")

            # Progress bar showing interest vs principal ratio
            interest_pct = (result['total_interest'] / result['total_payment']) * 100
            principal_pct = 100 - interest_pct

            st.markdown("**Principal vs Interest Split:**")
            st.progress(principal_pct / 100)
            st.markdown(f"""
            - 🔵 **Principal:** {principal_pct:.1f}% 
              (Rs. {principal:,.0f})
            - 🔴 **Interest:** {interest_pct:.1f}% 
              (Rs. {result['total_interest']:,.0f})
            """)

            st.markdown(f"""
            <div class="emi-box">
            <b>💡 Summary:</b><br>
            For a <b>{loan_type}</b> of <b>Rs. {principal:,.0f}</b> at 
            <b>{interest_rate}% p.a.</b> for <b>{tenure} years</b>:<br><br>
            Your Monthly EMI = <b>Rs. {result['emi']:,.0f}</b><br>
            You will pay <b>Rs. {result['total_interest']:,.0f}</b> as interest
            </div>
            """, unsafe_allow_html=True)

# ── TAB 3: LOAN COMPARISON ────────────────────────────────
with tab3:
    st.subheader("📊 Loan Products Comparison")

    data = {
        "Feature": [
            "Min Age", "Max Age", "Min Income",
            "Min CIBIL", "Min Amount", "Max Amount",
            "Interest Rate", "Max Tenure",
            "Processing Fee", "Collateral"
        ],
        "🏠 Home Loan": [
            "21 yrs", "65 yrs", "Rs. 25,000/mo",
            "700", "Rs. 5 Lakhs", "Rs. 10 Crores",
            "8.5% - 10.5%", "30 years",
            "0.5% - 1%", "Property"
        ],
        "💳 Personal Loan": [
            "21 yrs", "60 yrs", "Rs. 20,000/mo",
            "720", "Rs. 50,000", "Rs. 40 Lakhs",
            "10.5% - 24%", "5 years",
            "1% - 3%", "None (Unsecured)"
        ],
        "🚗 Car Loan": [
            "21 yrs", "65 yrs", "Rs. 20,000/mo",
            "680", "Rs. 1 Lakh", "Rs. 1 Crore",
            "7.5% - 12%", "7 years",
            "0.5% - 1%", "Vehicle"
        ],
        "🎓 Education Loan": [
            "16 yrs", "35 yrs", "Co-applicant needed",
            "N/A", "Rs. 50,000", "Rs. 1.5 Crores",
            "9.5% - 13%", "15 years",
            "Nil", "Above Rs. 7.5L"
        ],
        "💼 Business Loan": [
            "21 yrs", "65 yrs", "Turnover Rs. 10L+",
            "700", "Rs. 1 Lakh", "Rs. 5 Crores",
            "10% - 26%", "10 years",
            "1% - 2%", "Optional"
        ],
        "🥇 Gold Loan": [
            "18 yrs", "No limit", "Not required",
            "Not required", "Rs. 1,500", "Rs. 1 Crore",
            "7% - 17%", "3 years",
            "Nominal", "Gold Jewellery"
        ]
    }

    import pandas as pd
    df = pd.DataFrame(data)
    df = df.set_index("Feature")
    st.dataframe(df, use_container_width=True, height=420)

    st.markdown("---")
    st.markdown("### 🎯 Which loan is right for you?")

    purpose = st.selectbox("What do you need the loan for?", [
        "Buy a house",
        "Buy a car",
        "Fund education",
        "Personal expenses / Emergency",
        "Start or expand business",
        "Quick cash against gold"
    ])

    recommendations = {
        "Buy a house": "🏠 **Home Loan** — Best option with lowest interest rates (8.5-10.5%) and longest tenure (up to 30 years). Also offers tax benefits under Section 80C and 24(b).",
        "Buy a car": "🚗 **Car Loan** — Purpose-built for vehicle purchase. Low rates (7.5-12%) with the car as collateral. Up to 90% funding of on-road price.",
        "Fund education": "🎓 **Education Loan** — Covers all educational expenses. Moratorium period during study. Tax benefit under Section 80E. Girl students get 0.5% concession.",
        "Personal expenses / Emergency": "💳 **Personal Loan** — No collateral needed, fast approval (1-3 days). Higher rate (10.5-24%) but maximum flexibility of use.",
        "Start or expand business": "💼 **Business Loan** or **MUDRA Loan** — Business loan for established businesses. MUDRA loan for new/small businesses with government backing.",
        "Quick cash against gold": "🥇 **Gold Loan** — Fastest approval, no income proof needed, no CIBIL required. Get up to 75% of gold value instantly."
    }

    st.info(recommendations[purpose])

# ── Footer ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    AI Loan Advisory Chatbot | Built with Cohere + Pinecone + Streamlit<br>
    ⚠️ This is an advisory tool. Please consult a financial advisor for final decisions.
</div>
""", unsafe_allow_html=True)
