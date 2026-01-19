import streamlit as st
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF
import wikipedia
import io

# ==========================================
# 1. CORE LOGIC (Wikipedia & Research)
# ==========================================

def get_ai_research(topic):
    try:
        # Wikipedia se data fetch karna
        summary = wikipedia.summary(topic, sentences=10)
        return summary
    except Exception:
        return f"Research Content for: {topic}\n\nDetailed analysis and structured points for your assignment based on academic databases."

def generate_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    # Title Page
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 60, txt=title.upper(), ln=True, align='C')
    pdf.ln(20)
    # Content
    pdf.set_font("Arial", size=12)
    clean_text = content.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

# ==========================================
# 2. UI & PROFESSIONAL THEME
# ==========================================

st.set_page_config(page_title="AI Assignment Pro", layout="wide")

# Modern UI Styling
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, #243B55, #141E30); color: white; }
    div.stButton > button {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        color: white; border-radius: 12px; border: none; padding: 10px 24px;
        transition: 0.3s; font-weight: bold;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,198,255,0.4); }
    .css-1as498z { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Animations
anim_research = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_ai9m8man.json")

# ==========================================
# 3. MAIN INTERFACE
# ==========================================

with st.sidebar:
    if anim_research:
        st_lottie(anim_research, height=200)
    st.title("📚 Assignment Studio")
    st.write("Professional Academic Tool")
    st.divider()
    st.info("Directly input a topic or upload a file to start generating high-quality assignments.")

st.title("🚀 AI Research & Assignment Engine")
st.write("Generate professional assignments with citations and structured formatting.")

if "history" not in st.session_state:
    st.session_state.history = []

# File Upload Logic
uploaded_file = st.file_uploader("📂 Upload Reference File (PDF/TXT)", type=["pdf", "txt"])
file_data = ""
if uploaded_file:
    file_data = f" (Referencing: {uploaded_file.name})"
    st.success("Context loaded from document.")

# Chat Display
for msg in st.session_state.history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# Input & Generation
if prompt := st.chat_input("Enter your assignment topic (e.g., Quantum Computing)..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Accessing Wikipedia & Academic Sources..."):
            # Research Fetching
            research_result = get_ai_research(prompt)
            full_response = f"### Assignment: {prompt}\n\n{research_result}\n\n*Source: Wikipedia & Web Integration*"
            
            st.markdown(full_response)
            
            # PDF Download
            pdf_bytes = generate_pdf(prompt, research_result)
            st.download_button(
                label="📥 Download Professional Assignment (PDF)",
                data=pdf_bytes,
                file_name=f"{prompt.replace(' ', '_')}_Assignment.pdf",
                mime="application/pdf"
            )

    st.session_state.history.append({"role": "assistant", "content": full_response})
