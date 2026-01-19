import streamlit as st
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF
import io

# ==========================================
# 1. CORE LOGIC FUNCTIONS (Pehle modules mein the)
# ==========================================

def get_ai_response(history, user_input):
    # Yahan aapki Gemini ya OpenAI ki logic aayegi
    # Filhal sample response:
    return f"This is a generated assignment based on: {user_input}\n\n[Full Research Content Here...]"

def generate_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="MediCore Research Assignment", ln=True, align='C')
    pdf.ln(10)
    # Content
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text_content)
    return pdf.output(dest='S').encode('latin-1')

def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# ==========================================
# 2. UI & ANIMATION SETUP
# ==========================================

st.set_page_config(page_title="MediCore Pro AI", layout="wide")

# Custom CSS for Glassmorphism & Colors
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; }
    .stTextInput>div>div>input { background-color: #f0f2f6; border-radius: 10px; }
    .stButton>button { 
        background: linear-gradient(45deg, #FF512F, #DD2476); 
        color: white; border-radius: 20px; width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Lottie Animation
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_0p6f0dzs.json")

# Sidebar
with st.sidebar:
    st_lottie(lottie_coding, height=150)
    st.title("⚙️ Control Panel")
    mode = st.selectbox("Select Mode", ["Assignment", "Research Paper", "Quick Summary"])
    st.divider()
    st.info("Files uploaded here will be used as context for the AI.")

# ==========================================
# 3. MAIN APP INTERFACE
# ==========================================

st.title("🏥 MediCore Pro AI")
st.subheader("High-Fidelity Research & Assignment Engine")

if "history" not in st.session_state:
    st.session_state.history = []

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload reference document (PDF/TXT)", type=["pdf", "txt"])
file_context = ""
if uploaded_file:
    file_context = f"\n[Context from file: {uploaded_file.name}]"
    st.success("Document attached to AI brain!")

# Chat History Display
for msg in st.session_state.history:
    avatar = "🧑‍💼" if msg['role'] == "user" else "🩺"
    with st.chat_message(msg['role'], avatar=avatar):
        st.markdown(msg['content'])

# Logic
if prompt := st.chat_input("Enter assignment topic..."):
    # User Input
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Dr. AI is researching and writing..."):
            full_prompt = f"{prompt} {file_context}"
            reply = get_ai_response(st.session_state.history, full_prompt)
            st.markdown(reply)
            
            # PDF Generation
            pdf_data = generate_pdf(reply)
            
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_data,
                file_name="assignment.pdf",
                mime="application/pdf"
            )

    st.session_state.history.append({"role": "assistant", "content": reply})
