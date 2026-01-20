import streamlit as st
from fpdf import FPDF
import wikipediaapi
import datetime
import io
import PyPDF2 # For PDF parsing
from docx import Document # For DOCX parsing (optional)
import requests # For Lottie animations

# ==========================================
# 1. CORE RESEARCH & DOCUMENT ENGINE
# ==========================================

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def get_academic_data_with_context(topic, context_text=""):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="AcademicResearchBot/1.0 (contact: support@assignmentbot.com)"
    )
    page = wiki_wiki.page(topic)
    
    if not page.exists() and not context_text:
        return None
        
    # Combine Wikipedia data with uploaded context
    full_text = page.text if page.exists() else ""
    
    # Simple strategy: Add context at the beginning
    combined_content = f"{context_text}\n\n{full_text}" 
    
    # Extract sections from combined content (simple approach for now)
    sections_content = []
    # If Wikipedia page exists, use its sections for structure
    if page.exists():
        for s in page.sections:
            if len(s.text) > 50:
                sections_content.append({"title": s.title, "text": s.text})
                for ss in s.sections:
                    sections_content.append({"title": f"{s.title} - {ss.title}", "text": ss.text})
    else: # If no Wikipedia page, just use context as one big section
        sections_content.append({"title": "Uploaded Document Analysis", "text": context_text})


    return {
        "title": page.title if page.exists() else topic,
        "summary": page.summary if page.exists() else context_text[:1000] + "...", # Summarize context
        "sections": sections_content,
        "full_content": combined_content
    }

class AssignmentPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(150)
            self.cell(0, 10, f"Research Report: {self.report_title}", 0, 1, 'R')
            self.line(10, 15, 200, 15)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100)
        self.cell(0, 10, f'Academic Session 2026 | Page {self.page_no()}', 0, 0, 'C')

def create_long_pdf(data):
    pdf = AssignmentPDF()
    pdf.report_title = data['title']
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- PAGE 1: PROFESSIONAL COVER PAGE ---
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font('helvetica', 'B', 36)
    pdf.set_text_color(26, 54, 104)
    pdf.multi_cell(0, 15, data['title'].upper(), align='C')
    
    pdf.ln(20)
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(100)
    pdf.cell(0, 10, "COMPREHENSIVE RESEARCH ASSIGNMENT", ln=True, align='C')
    
    pdf.ln(50)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(50)
    pdf.cell(0, 10, f"Submission Date: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align='C')
    pdf.cell(0, 10, "Status: Final Academic Submission", ln=True, align='C')

    # --- PAGE 2: TABLE OF CONTENTS ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(26, 54, 104)
    pdf.cell(0, 15, "Table of Contents", ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    for i, sec in enumerate(data['sections'], 2):
        pdf.cell(0, 8, f"{i}. {sec['title']}", ln=True)

    # --- PAGE 3: EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(26, 54, 104)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.ln(5)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(30)
    clean_summary = data['summary'].encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_summary)

    # --- PAGE 4+ : DETAILED SECTIONS ---
    for i, sec in enumerate(data['sections'], 2):
        pdf.ln(10)
        pdf.set_font('helvetica', 'B', 16)
        pdf.set_text_color(26, 54, 104)
        pdf.cell(0, 10, f"{i}. {sec['title']}", ln=True)
        pdf.ln(5)
        
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(0)
        section_text = sec['text'].encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(0, 7, section_text)
        pdf.ln(5)

    return bytes(pdf.output())

# ==========================================
# 2. ANIMATED & VISUAL UI (Lottie + CSS)
# ==========================================

st.set_page_config(page_title="Academic AI Pro", layout="wide")

# Lottie Animation Loader
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException:
        pass
    return None

# Lottie URLs
lottie_research_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ai9m8man.json")
lottie_file_upload_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_qf1t7kxe.json")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #add8e6 0%, #ffffff 50%, #e0ffff 100%);
        color: #1A1A2E; /* Dark Blue Text */
    }
    
    /* Animated Header */
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .stDownloadButton button {
        background-color: #007bff;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
    }
    /* Chat bubbles with light background */
    div.stChatMessage {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 1px solid #CED4DA;
        padding: 10px 15px;
        color: #1A1A2E;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INTERFACE EXECUTION
# ==========================================

# Animated Header
col_lottie, col_text = st.columns([1, 3])
with col_lottie:
    if lottie_research_animation:
        st_lottie(lottie_research_animation, height=120, key="main_research_anim")
with col_text:
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    st.markdown("<h1>🎓 AI Academic Studio Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h4>Your Personal Research & Assignment Assistant</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---") # Separator

# Document Upload Section (Animated)
st.markdown("### 📄 Upload Your Study Material")
st.write("Provide your notes, textbooks, or specific articles here. The AI will integrate this context into your assignment.")

col_upload_lottie, col_upload_func = st.columns([1, 3])
with col_upload_lottie:
    if lottie_file_upload_animation:
        st_lottie(lottie_file_upload_animation, height=100, key="file_upload_anim")
with col_upload_func:
    uploaded_file = st.file_uploader("Select a document (PDF, TXT, DOCX)", type=['pdf', 'txt', 'docx'])
    
    context_text = ""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == "pdf":
            context_text = extract_text_from_pdf(uploaded_file)
        elif file_extension == "txt":
            context_text = uploaded_file.getvalue().decode("utf-8")
        elif file_extension == "docx":
            context_text = extract_text_from_docx(uploaded_file)
        
        if context_text:
            st.success(f"'{uploaded_file.name}' loaded successfully! Content will be used for your assignment.")
        else:
            st.error("Could not extract text from the document. Please ensure it's a readable format.")

st.write("---") # Separator

st.markdown("### ✍️ Enter Your Assignment Topic")
st.write("The AI will generate a detailed, multi-page academic report based on your topic and uploaded documents.")

if "history" not in st.session_state:
    st.session_state.history = []

# Chat Interface
for msg in st.session_state.history:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if prompt := st.chat_input("Start by typing a topic like 'Impact of AI on Education'"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Generating multi-page academic report..."):
            data = get_academic_data_with_context(prompt, context_text)
            
            if data and (data['sections'] or context_text): # Ensure there's enough data
                st.markdown(f"**Report Title:** {data['title']}")
                st.markdown("---")
                st.markdown("### Executive Summary")
                st.write(data['summary'])
                
                with st.expander("Expand to see detailed sections"):
                    for i, sec in enumerate(data['sections']):
                        st.write(f"**{i+1}.** {sec['title']}")

                try:
                    pdf_data = create_long_pdf(data)
                    st.download_button(
                        label="📥 Download Full Academic Report (PDF)",
                        data=pdf_data,
                        file_name=f"Academic_Report_{data['title'].replace(' ','_')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("Your professional report is ready for download!")
                except Exception as e:
                    st.error(f"Error generating PDF: {e}. Please try again.")
            else:
                st.warning("Not enough data to create a detailed assignment. Try a broader topic or upload a more descriptive document.")
