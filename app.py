import streamlit as st
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF
import io

# ==========================================
# 1. CORE LOGIC FUNCTIONS
# ==========================================

def get_ai_response(history, user_input):
    # Sample logic - Yahan aap apni Gemini API call add kar sakte hain
    return f"MediCore AI Research Output:\n\nTopic: {user_input}\n\nDetailed assignment content generated successfully."

def generate_pdf(text_content):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="MediCore Research Assignment", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        # Latin-1 encoding issues se bachne ke liye clean text
        clean_text = text_content.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        st.error(f"PDF Error: {str(e)}")
        return None

def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# ==========================================
# 2. UI & THEME SETUP
# ==========================================

st.set_page_config(page_title="MediCore Pro AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }
    .stButton>button { border-radius: 20px; background: #e94e77; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Animation Loading with Safety Check
lottie_url = "https://assets5.lottiefiles.com/packages/lf20_0p6f0dzs.json"
lottie_coding = load_lottieurl(lottie_url)

# ==========================================
# 3. MAIN APP INTERFACE
# ==========================================

with st.sidebar:
    # AGAR ANIMATION LOAD HO TO DIKHAO, WARNA SKIP KARO (Taki error na aaye)
    if lottie_coding:
        st_lottie(lottie_coding, height=150, key="sidebar_anim")
    else:
        st.title("🏥 MediCore")
    
    st.title("⚙️ Control Panel")
    st.info("Upload documents for AI context.")

st.title("🏥 MediCore Pro AI")
st.caption("Advanced Assignment & Research System")

if "history" not in st.session_state:
    st.session_state.history = []

# File Upload
uploaded_file = st.file_uploader("📂 Reference Document (PDF/TXT)", type=["pdf", "txt"])
file_context = ""
if uploaded_file:
    file_context = f"\n[Document: {uploaded_file.name}]"
    st.success("File context loaded.")

# Chat Display
for msg in st.session_state.history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# Chat Input
if prompt := st.chat_input("Enter your research topic..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            full_query = prompt + file_context
            reply = get_ai_response(st.session_state.history, full_query)
            st.markdown(reply)
            
            # PDF Generation with Download Button
            pdf_bytes = generate_pdf(reply)
            if pdf_bytes:
                st.download_button(
                    label="📥 Download Assignment (PDF)",
                    data=pdf_bytes,
                    file_name="assignment_medicore.pdf",
                    mime="application/pdf"
                )

    st.session_state.history.append({"role": "assistant", "content": reply})
