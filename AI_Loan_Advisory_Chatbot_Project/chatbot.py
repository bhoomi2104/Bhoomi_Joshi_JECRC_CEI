import cohere
import math

def calculate_emi(principal, annual_rate, tenure_years):
    """Calculate EMI using standard formula"""
    if annual_rate == 0:
        return principal / (tenure_years * 12)
    monthly_rate = annual_rate / 12 / 100
    n = tenure_years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate)**n) / \
          ((1 + monthly_rate)**n - 1)
    total_payment = emi * n
    total_interest = total_payment - principal
    return {
        "emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2),
        "months": n
    }

def detect_emi_query(query):
    """Detect if user is asking for EMI calculation"""
    keywords = ["emi", "monthly payment", "installment",
                "calculate", "how much per month", "monthly emi"]
    return any(k in query.lower() for k in keywords)

def generate_answer(query, context_chunks, cohere_api_key):
    """Generate answer using Cohere Chat API"""
    co = cohere.ClientV2(cohere_api_key)

    if not context_chunks:
        context = "No specific document context found for this query."
    else:
        context = "\n\n---\n\n".join(context_chunks)

    system_prompt = """You are an expert AI Loan Advisory Assistant for an Indian 
financial institution. You help users understand loan products, eligibility, 
EMI calculations, interest rates, documentation requirements, and financial 
planning.

Guidelines:
- Answer based on the provided document context
- Use Indian currency format (Rs. / Lakhs / Crores)
- Be clear, accurate, and helpful
- If asked about EMI, show the calculation
- If information is not in context, say so politely
- Keep answers concise but complete
- Use bullet points for lists"""

    user_message = f"""Context from Loan Policy Documents:
{context}

User Question: {query}

Please provide a helpful, accurate answer based on the context above."""

    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[
            {"role": "user", "content": system_prompt + "\n\n" + user_message}
        ]
    )

    return response.message.content[0].text.strip()
