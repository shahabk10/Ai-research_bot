import streamlit as st
from fpdf import FPDF
import wikipediaapi
import datetime
import io
import PyPDF2
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. CORE ENGINE & PDF GENERATION
# ==========================================

def get_academic_data(topic, context=""):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent="AcademicBot/2.0 (contact: support@assignmentbot.com)"
    )
    page = wiki_wiki.page(topic)
    
    sections = []
    if page.exists():
        for s in page.sections[:8]:
            if len(s.text) > 100:
                sections.append({"title": s.title, "text": s.text})
    
    # Context integration from files
    if context:
        sections.insert(0, {"title": "Integrated Document Analysis", "text": context[:8000]})

    return {
        "title": page.title if page.exists() else topic,
        "summary": page.summary if page.exists() else "Context-driven research report.",
        "sections": sections,
        "url": page.fullurl if page.exists() else "Internal Evidence"
    }

class ProfessionalPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(150)
            self.cell(0, 10, 'Academic Research Protocol', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | AI Research Studio', 0, 0, 'C')

def create_assignment_pdf(data):
    pdf = ProfessionalPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- PAGE 1: PROFESSIONAL COVER ---
    pdf.add_page()
    pdf.set_fill_color(26, 54, 104) # Professional Navy
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_text_color(255)
    pdf.set_font('helvetica', 'B', 32)
    pdf.ln(80)
    pdf.multi_cell(0, 15, data['title'].upper(), align='C')
    
    pdf.ln(10)
    pdf.set_font('helvetica', '', 14)
    pdf.cell(0, 10, f"Date: {datetime.date.today()}", ln=True, align='C')

    # --- PAGE 2+ : STRUCTURED CONTENT ---
    pdf.add_page()
    pdf.set_text_color(0)
    pdf.set_font('helvetica', 'B', 18)
    pdf.cell(0, 20, "1. Executive Overview", ln=True)
    pdf.set_font('helvetica', '', 11)
    # Binary fix: encoding handle karna
    clean_summary = data['summary'].encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_summary)
    
    for i, sec in enumerate(data['sections'], 2):
        pdf.ln(10)
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(26, 54, 104)
        pdf.cell(0, 10, f"{i}. {sec['title']}", ln=True)
        pdf.ln(5)
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(30)
        clean_text = sec['text'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 7, clean_text)

    # Output as bytes to fix "Invalid binary data format"
    return bytes(pdf.output())

# ==========================================
# 2. PREMIUM WHITE INTERFACE (Highly Readable)
# ==========================================

st.set_page_config(page_title="AI Studio Pro", layout="wide")

# CSS for Clarity and Visual Appeal
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    h1, h2, h3 { color: #1E3A8A !important; font-family: 'Inter', sans-serif; }
    div.stChatMessage {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563EB, #4F46E5);
        color: white !important; border-radius: 10px; border: none; font-weight: bold;
    }
    section[data-testid="stSidebar"] { background-color: #F1F5F9; }
    </style>
    """, unsafe_allow_html=True)

# Safety check for Lottie to prevent StreamlitAPIException
def safe_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_anim = safe_lottie("https://assets5.lottiefiles.com/packages/lf20_ai9m8man.json")

# ==========================================
# 3. APP LOGIC
# ==========================================

with st.sidebar:
    if lottie_anim: st_lottie(lottie_anim, height=150)
    st.title("📂 Research Files")
    files = st.file_uploader("Upload reference documents", type=['pdf', 'txt'], accept_multiple_files=True)
    context_text = ""
    if files:
        for f in files:
            if f.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(f)
                for p in reader.pages: context_text += p.extract_text()
            st.success(f"Context from {f.name} loaded.")

st.title("🎓 Professional Academic Engine")
st.write("Generating structured 4-5 page research papers with deep analysis.")

if prompt := st.chat_input("Enter your assignment topic..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Synthesizing multi-page report..."):
            data = get_academic_data(prompt, context_text)
            
            if data:
                st.header(data['title'])
                st.write(data['summary'][:500] + "...")
                
                with st.expander("Preview Document Structure"):
                    for i, s in enumerate(data['sections'], 1):
                        st.write(f"**{i}.** {s['title']}")
                
                # PDF Generation logic with robust bytes output
                try:
                    pdf_bytes = create_assignment_pdf(data)
                    st.divider()
                    st.download_button(
                        label="📥 DOWNLOAD 5-PAGE ASSIGNMENT (PDF)",
                        data=pdf_bytes,
                        file_name=f"Report_{prompt.replace(' ','_')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("Assignment rendered in professional academic format.")
                except Exception as e:
                    st.error(f"Render Error: {e}")
