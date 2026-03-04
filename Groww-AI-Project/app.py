import streamlit as st
import google.generativeai as genai
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Groww MF FAQ Assistant",
    page_icon="📊",
    layout="centered"
)

# ─────────────────────────────────────────────
# KNOWLEDGE BASE  (RAG corpus – hardcoded chunks from official sources)
# Each chunk: {text, source_url, scheme}
# ─────────────────────────────────────────────
KNOWLEDGE_BASE = [
    # ── MIRAE ASSET LARGE CAP FUND ──────────────────────────────────────
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "minimum SIP",
        "text": "Minimum SIP amount for Mirae Asset Large Cap Fund is ₹1,000 per month (and in multiples of ₹1 thereafter). Minimum lump-sum purchase is ₹5,000.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-large-cap-fund"
    },
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "exit load",
        "text": "Exit load for Mirae Asset Large Cap Fund: If redeemed within 1 year (365 days) from the date of allotment – 1%. If redeemed after 1 year – NIL.",
        "source_url": "https://www.miraeassetmf.co.in/docs/default-source/fund-detail-exitload/entry-exit-load-(1).pdf"
    },
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "riskometer",
        "text": "The risk profile of Mirae Asset Large Cap Fund is 'Very High'. Investors should understand that their principal investment will be at very high risk.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-large-cap-fund"
    },
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "benchmark",
        "text": "The benchmark for Mirae Asset Large Cap Fund is Nifty 100 TRI (Total Return Index), as the fund predominantly invests in Top 100 companies by market capitalization.",
        "source_url": "https://www.miraeassetmf.co.in/docs/default-source/sid/sid-mirae-asset-largecap-fund.pdf"
    },
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "expense ratio TER",
        "text": "The Total Expense Ratio (TER) for Mirae Asset Large Cap Fund differs between Regular Plan and Direct Plan. For the latest TER, refer to the official AMC website or AMFI portal.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-large-cap-fund"
    },
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "lock-in",
        "text": "Mirae Asset Large Cap Fund is an open-ended equity scheme with NO lock-in period. Investors can redeem at any time subject to applicable exit loads.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-large-cap-fund"
    },
    {
        "scheme": "Mirae Asset Large Cap Fund",
        "topic": "category type",
        "text": "Mirae Asset Large Cap Fund is an open-ended equity scheme predominantly investing across large cap stocks (Top 100 companies by market capitalization as defined by SEBI).",
        "source_url": "https://www.miraeassetmf.co.in/docs/default-source/sid/sid-mirae-asset-largecap-fund.pdf"
    },

    # ── MIRAE ASSET FLEXI CAP FUND ──────────────────────────────────────
    {
        "scheme": "Mirae Asset Flexi Cap Fund",
        "topic": "minimum SIP",
        "text": "Minimum SIP amount for Mirae Asset Flexi Cap Fund is ₹1,000 per month. Minimum lump-sum purchase is ₹5,000.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund"
    },
    {
        "scheme": "Mirae Asset Flexi Cap Fund",
        "topic": "exit load",
        "text": "Exit load for Mirae Asset Flexi Cap Fund: If redeemed within 1 year (365 days) – 1%. If redeemed after 1 year – NIL.",
        "source_url": "https://www.miraeassetmf.co.in/docs/default-source/fund-detail-exitload/entry-exit-load-(1).pdf"
    },
    {
        "scheme": "Mirae Asset Flexi Cap Fund",
        "topic": "riskometer",
        "text": "The risk profile of Mirae Asset Flexi Cap Fund is 'Very High'. The fund dynamically invests across large cap, mid cap, and small cap stocks.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund"
    },
    {
        "scheme": "Mirae Asset Flexi Cap Fund",
        "topic": "benchmark",
        "text": "Mirae Asset Flexi Cap Fund is benchmarked against the NIFTY 500 TRI (Total Return Index), reflecting its mandate to invest across all market capitalizations.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund"
    },
    {
        "scheme": "Mirae Asset Flexi Cap Fund",
        "topic": "category type",
        "text": "Mirae Asset Flexi Cap Fund is an open-ended dynamic equity scheme investing across large cap, mid cap, and small cap stocks, with minimum 65% in Indian equities.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund"
    },
    {
        "scheme": "Mirae Asset Flexi Cap Fund",
        "topic": "lock-in",
        "text": "Mirae Asset Flexi Cap Fund has NO lock-in period. It is an open-ended scheme and investors can redeem at any time subject to applicable exit loads.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-flexi-cap-fund"
    },

    # ── MIRAE ASSET ELSS TAX SAVER FUND ────────────────────────────────
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "lock-in ELSS",
        "text": "Mirae Asset ELSS Tax Saver Fund has a mandatory statutory lock-in period of 3 years from the date of allotment. For SIP investments, each instalment is locked in for 3 years from its respective investment date.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "exit load",
        "text": "Exit load for Mirae Asset ELSS Tax Saver Fund is NIL. However, units cannot be redeemed before the mandatory 3-year lock-in period.",
        "source_url": "https://www.miraeassetmf.co.in/docs/default-source/fund-detail-exitload/entry-exit-load-(1).pdf"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "minimum SIP",
        "text": "Minimum SIP amount for Mirae Asset ELSS Tax Saver Fund is ₹500 per month. Minimum lump-sum investment is ₹500.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "tax benefit 80C",
        "text": "Investments in Mirae Asset ELSS Tax Saver Fund qualify for tax deduction up to ₹1,50,000 per financial year under Section 80C of the Income Tax Act, 1961. Investors in the 30% bracket can save up to ₹46,800* in income tax. (*Under old tax regime.)",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "riskometer",
        "text": "The risk profile of Mirae Asset ELSS Tax Saver Fund is 'Very High'. The fund invests predominantly in equity and equity-related instruments.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "benchmark",
        "text": "Mirae Asset ELSS Tax Saver Fund is benchmarked against the NIFTY 500 TRI (Total Return Index).",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "expense ratio TER",
        "text": "The TER for Mirae Asset ELSS Tax Saver Fund varies between Regular and Direct Plan. For the latest TER, visit the AMC website or the AMFI portal.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },
    {
        "scheme": "Mirae Asset ELSS Tax Saver Fund",
        "topic": "portfolio allocation",
        "text": "Mirae Asset ELSS Tax Saver Fund invests minimum 80% in equity and equity-related securities across market capitalizations. The remaining 0–20% may be in money market instruments, debt securities, and G-Secs.",
        "source_url": "https://www.miraeassetmf.co.in/mutual-fund-scheme/equity-fund/mirae-asset-elss-tax-saver-fund"
    },

    # ── GENERAL / AMFI / GROWW ──────────────────────────────────────────
    {
        "scheme": "General",
        "topic": "download capital gains statement Groww",
        "text": "To download your Capital Gains Statement on Groww: Log in to Groww → Go to 'Reports' → Select 'Capital Gains Statement' → Choose the financial year → Download as PDF or Excel. For CAMS/KFintech consolidated statements, visit camsonline.com or kfintech.com.",
        "source_url": "https://groww.in/p/tax/capital-gains-statement"
    },
    {
        "scheme": "General",
        "topic": "download account statement Groww",
        "text": "To download your mutual fund account statement on Groww: Login → Portfolio → Mutual Funds → Statements → Select date range and fund → Download. You can also get a consolidated CAMS statement from camsonline.com free of charge.",
        "source_url": "https://groww.in/p/tax/capital-gains-statement"
    },
    {
        "scheme": "General",
        "topic": "what is expense ratio TER",
        "text": "The expense ratio (Total Expense Ratio or TER) is the annual fee charged by the mutual fund scheme to cover operating costs. It is expressed as a percentage of daily AUM. For example, a TER of 1.5% means ₹1,500 per year on a ₹1,00,000 investment is deducted from the fund's NAV.",
        "source_url": "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-expense-ratio.html"
    },
    {
        "scheme": "General",
        "topic": "what is ELSS",
        "text": "ELSS (Equity Linked Savings Scheme) is a category of equity mutual funds that offer tax deduction under Section 80C of the Income Tax Act, 1961. They have a mandatory 3-year lock-in period, which is the shortest among all 80C investment options.",
        "source_url": "https://www.amfiindia.com/investor-corner/knowledge-center/elss.html"
    },
    {
        "scheme": "General",
        "topic": "what is riskometer",
        "text": "The Riskometer is a SEBI-mandated risk label displayed on every mutual fund scheme. It classifies funds into six risk levels: Low, Low to Moderate, Moderate, Moderately High, High, and Very High. It helps investors assess the risk of a scheme before investing.",
        "source_url": "https://www.sebi.gov.in/legal/circulars/oct-2020/product-labeling-in-mutual-funds-schemes-riskometer_47804.html"
    },
    {
        "scheme": "General",
        "topic": "what is exit load",
        "text": "Exit load is a fee charged by a mutual fund when an investor redeems (sells) their units before a specified time period. It is deducted from the redemption amount. For example, a 1% exit load on a ₹1,00,000 redemption means ₹1,000 is deducted.",
        "source_url": "https://www.amfiindia.com/investor-corner/knowledge-center/exit-load.html"
    },
    {
        "scheme": "General",
        "topic": "what is SIP minimum",
        "text": "SIP (Systematic Investment Plan) is a method of investing a fixed amount in a mutual fund at regular intervals (monthly, weekly, etc.). The minimum SIP amount varies by scheme and AMC, typically starting from ₹100 to ₹1,000.",
        "source_url": "https://www.amfiindia.com/investor-corner/knowledge-center/sip.html"
    },
    {
        "scheme": "General",
        "topic": "factsheet download Mirae Asset",
        "text": "Mirae Asset Mutual Fund factsheets can be downloaded from the official AMC website at: https://www.miraeassetmf.co.in/downloads/factsheet. Factsheets are updated monthly and contain NAV, portfolio, expense ratio, and benchmark information.",
        "source_url": "https://www.miraeassetmf.co.in/downloads/factsheet"
    },
    {
        "scheme": "General",
        "topic": "SID KIM download Mirae Asset",
        "text": "Scheme Information Document (SID) and Key Information Memorandum (KIM) for all Mirae Asset funds can be downloaded from: https://www.miraeassetmf.co.in. These documents contain complete scheme details including investment objective, asset allocation, risks, fees, and loads.",
        "source_url": "https://www.miraeassetmf.co.in"
    },
]

# ─────────────────────────────────────────────
# OPINION / ADVICE KEYWORDS (triggers polite refusal)
# ─────────────────────────────────────────────
OPINION_KEYWORDS = [
    "should i", "should i buy", "should i sell", "should i invest",
    "recommend", "which is better", "better fund", "best fund",
    "worth investing", "is it good", "will it grow", "will it give",
    "future returns", "expected returns", "will i get", "good investment",
    "advice", "suggest", "portfolio advice", "which fund should",
    "compare performance", "outperform", "beat the market"
]

EDUCATIONAL_LINK = "https://www.amfiindia.com/investor-corner/knowledge-center"

# ─────────────────────────────────────────────
# RETRIEVAL: find top-k relevant chunks
# ─────────────────────────────────────────────
def retrieve_chunks(query: str, top_k: int = 3) -> list:
    """Simple keyword-based retrieval from our knowledge base."""
    query_lower = query.lower()
    scored = []
    for chunk in KNOWLEDGE_BASE:
        score = 0
        # Scheme name match
        if chunk["scheme"].lower() in query_lower:
            score += 5
        # Topic keyword match
        for word in chunk["topic"].split():
            if word.lower() in query_lower:
                score += 2
        # Text keyword overlap
        for word in query_lower.split():
            if len(word) > 3 and word in chunk["text"].lower():
                score += 1
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:top_k] if s > 0]

def is_opinion_query(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in OPINION_KEYWORDS)

# ─────────────────────────────────────────────
# LLM CALL
# ─────────────────────────────────────────────
def get_answer(query: str, api_key: str) -> dict:
    """Returns dict with 'answer', 'source_url', 'refused'."""

    # Check if opinion/advice query
    if is_opinion_query(query):
        return {
            "answer": "I can only provide factual information about mutual fund schemes — such as expense ratios, exit loads, SIP minimums, lock-in periods, and benchmarks. I'm not able to offer investment advice or recommendations. Please consult a SEBI-registered investment adviser for personalised guidance.",
            "source_url": EDUCATIONAL_LINK,
            "source_label": "AMFI Investor Education",
            "refused": True
        }

    # Retrieve relevant chunks
    chunks = retrieve_chunks(query)
    if not chunks:
        return {
            "answer": "I couldn't find factual information on that topic in my current knowledge base. Please refer to the official Mirae Asset website or AMFI for detailed information.",
            "source_url": "https://www.miraeassetmf.co.in",
            "source_label": "Mirae Asset Mutual Fund",
            "refused": False
        }

    # Build context
    context_parts = []
    for c in chunks:
        context_parts.append(f"[Source: {c['source_url']}]\n{c['text']}")
    context = "\n\n".join(context_parts)
    best_source = chunks[0]["source_url"]
    best_label = chunks[0]["scheme"] if chunks[0]["scheme"] != "General" else "Official Source"

    # Call Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""You are a mutual fund FAQ assistant for Groww users.
You answer ONLY factual questions about Mirae Asset mutual fund schemes using the provided context.
Rules:
1. Answer in maximum 3 sentences.
2. Use ONLY the facts from the context provided. Do not invent numbers.
3. Never give investment advice, recommendations, or performance predictions.
4. If the answer is in the context, give it clearly and concisely.
5. Always be factual and neutral.

Context from official sources:
{context}

User question: {query}

Answer the question using only the context above. Keep it under 3 sentences. Be factual and neutral."""

    response = model.generate_content(prompt)
    answer = response.text.strip()
    return {
        "answer": answer,
        "source_url": best_source,
        "source_label": best_label,
        "refused": False
    }

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #00b386 0%, #004d40 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .disclaimer-box {
        background: black;
        border-left: 4px solid #f9a825;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-bottom: 1.2rem;
    }
    .source-box {
        background: black;
        border-left: 4px solid #00b386;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        font-size: 0.82rem;
        margin-top: 0.5rem;
    }
    .refusal-box {
        background: #fce4ec;
        border-left: 4px solid #e91e63;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
    }
    .example-chip {
        display: inline-block;
        background: #e3f2fd;
        border: 1px solid #90caf9;
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.82rem;
        margin: 0.2rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h2 style="margin:0; font-size:1.5rem;">📊 Groww — Mutual Fund FAQ Assistant</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.9; font-size:0.9rem;">
        Mirae Asset Mutual Fund · Large Cap · Flexi Cap · ELSS Tax Saver
    </p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-box">
    ⚠️ <strong>Facts-only. No investment advice.</strong> This tool provides factual information about mutual fund scheme parameters (expense ratio, exit load, SIP minimum, lock-in, benchmark, riskometer) sourced from official AMC/AMFI/SEBI pages only. It does not provide investment advice, recommendations, or return projections. Please consult a SEBI-registered investment adviser before making any investment decisions.
</div>
""", unsafe_allow_html=True)

# Try to get the API key securely from environment variables or Streamlit secrets
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except FileNotFoundError:
        pass

# API Key input
with st.sidebar:
    if not api_key:
        api_key = st.text_input("Google AI Studio API Key", type="password", help="Enter your API key or set GOOGLE_API_KEY securely in .streamlit/secrets.toml")
    
    st.markdown("---")
    st.markdown("**Scope**")
    st.markdown("- **AMC:** Mirae Asset Mutual Fund")
    st.markdown("- **Schemes:** Large Cap, Flexi Cap, ELSS Tax Saver")
    st.markdown("- **Sources:** Official AMC, AMFI, SEBI pages only")
    st.markdown("---")
    st.markdown("**Known Limits**")
    st.markdown("- No real-time NAV or returns data")
    st.markdown("- No PII collected or stored")
    st.markdown("- No performance comparisons")
    st.caption("Last updated from sources: Feb 2025")

# Example questions
st.markdown("**💡 Try these example questions:**")
examples = [
    "What is the exit load for Mirae Asset Large Cap Fund?",
    "What is the ELSS lock-in period?",
    "What is the minimum SIP for Mirae Asset ELSS Tax Saver Fund?",
]

col1, col2, col3 = st.columns(3)
selected_example = None
with col1:
    if st.button("Exit load — Large Cap?", use_container_width=True):
        selected_example = examples[0]
with col2:
    if st.button("ELSS lock-in period?", use_container_width=True):
        selected_example = examples[1]
with col3:
    if st.button("Min SIP — ELSS fund?", use_container_width=True):
        selected_example = examples[2]

st.markdown("---")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask a factual question about a Mirae Asset fund...")

# Handle example button click
if selected_example:
    user_input = selected_example

if user_input:
    if not api_key:
        st.warning("Please enter your Google AI Studio API key in the sidebar to continue.")
    else:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Looking up official sources..."):
                result = get_answer(user_input, api_key)

            if result["refused"]:
                st.markdown(f"""
<div class="refusal-box">
🚫 <strong>Facts-only assistant:</strong><br>
{result['answer']}
</div>
""", unsafe_allow_html=True)
                st.markdown(f"""
<div class="source-box">
📚 <strong>Educational resource:</strong> <a href="{result['source_url']}" target="_blank">AMFI Investor Education Centre</a>
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown(result["answer"])
                st.markdown(f"""
<div class="source-box">
🔗 <strong>Source ({result['source_label']}):</strong> <a href="{result['source_url']}" target="_blank">{result['source_url']}</a><br>
<em style="font-size:0.78rem;">Last updated from sources: Feb 2025</em>
</div>
""", unsafe_allow_html=True)

            # Store in history
            display_content = result["answer"] + f"\n\n🔗 **Source:** [{result['source_label']}]({result['source_url']})"
            st.session_state.messages.append({"role": "assistant", "content": display_content})

# Footer
st.markdown("---")
st.caption("📌 This assistant uses publicly available information from Mirae Asset Mutual Fund (miraeassetmf.co.in), AMFI (amfiindia.com), and SEBI (sebi.gov.in). No PII is collected or stored. | Mutual Fund investments are subject to market risks. Please read all scheme related documents carefully.")
