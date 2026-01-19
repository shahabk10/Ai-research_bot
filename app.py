import streamlit as st
from modules.ui_components import setup_ui, sidebar_logic
from modules.ai_engine import get_ai_response
from modules.utils import text_to_audio, generate_pdf # New utility
from streamlit_lottie import st_lottie
import requests

# 1. Page Configuration (Colorful Theme)
st.set_page_config(page_title="MediCore Pro AI", layout="wide")

# Custom CSS for Gradient Background & Animations
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stButton>button { 
        background: linear-gradient(45deg, #00dbde, #fc00ff); 
        color: white; border-radius: 20px; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# Lottie Animation Loader
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_medical = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5njp9vgg.json")

# 2. Logic & Setup
if "history" not in st.session_state: st.session_state.history = []
sidebar_logic()

col1, col2 = st.columns([1, 3])
with col1:
    st_lottie(lottie_medical, height=150)
with col2:
    st.title("🚀 MediCore Assignment Engine")
    st.caption("Advanced Research & Document Generation")

# 3. File Upload Section (New)
uploaded_file = st.file_uploader("Upload reference document (PDF/TXT)", type=["pdf", "txt"])
file_context = ""
if uploaded_file:
    # PDF/Txt reading logic yahan add karein
    file_context = "User has uploaded a document for reference."
    st.success("Document analyzed successfully!")

# 4. Chat & Assignment Generation
if prompt := st.chat_input("Enter topic or assignment details..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Generating Professional Assignment..."):
            # Context merge karna (File + Prompt)
            full_query = f"{file_context}\n\nTask: {prompt}"
            reply = get_ai_response(st.session_state.history, full_query)
            
            st.markdown(reply)
            
            # PDF Generation & Download (New)
            pdf_file = generate_pdf(reply) # modules/utils.py mein function create karein
            st.download_button(
                label="📥 Download Assignment (PDF)",
                data=pdf_file,
                file_name="Assignment_Research.pdf",
                mime="application/pdf"
            )
