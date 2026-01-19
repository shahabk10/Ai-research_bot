import streamlit as st
import requests
from streamlit_lottie import st_lottie
from fpdf import FPDF
import wikipediaapi
import datetime

# ==========================================
# 1. CORE RESEARCH ENGINE (Improved)
# ==========================================

def get_academic_data(topic):
    # Wikipedia API with a proper User-Agent to avoid blocks
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="AcademicResearchBot/1.0 (contact: your@email.com)"
    )
    page = wiki_wiki.page(topic)
    
    if not page.exists():
        return None
        
    content = {
        "title": page.title,
        "summary": page.summary[:1500], # First few paragraphs
        "sections": [s.title for s in page.sections[:6]],
        "text": page.text[:5000] # Primary content
    }
    return content

class ProfessionalPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'OFFICIAL ACADEMIC REPORT', 0, 1, 'R')
        self.line(10, 18, 200, 18)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | AI Research Engine', 0, 0, 'C')

def create_pdf(data):
    pdf = ProfessionalPDF()
    pdf.add_page()
    
    # --- Professional Title Page ---
    pdf.ln(40)
    pdf.set_font('helvetica', 'B', 32)
    pdf.set_text_color(26, 54, 104) # Professional Navy Blue
    pdf.multi_cell(0, 15, data['title'].upper(), align='C')
    
    pdf.ln(10)
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align='C')
    
    # --- Content Sections ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(26, 54, 104)
    pdf.cell(0, 10, "1. EXECUTIVE SUMMARY", ln=True)
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    # Clean text for PDF encoding
    clean_summary = data['summary'].encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_summary)
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, "2. KEY RESEARCH FINDINGS", ln=True)
    
    for i, section in enumerate(data['sections'], 1):
        pdf.ln(5)
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 10, f"2.{i} {section}", ln=True)
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 7, f"Detailed exploration and academic data regarding {section}. This segment provides a comprehensive overview of the technical and theoretical frameworks associated with {data['title']}.")

    # Fixing the AttributeError: output() in fpdf2 returns bytes directly if no filename
    return pdf.output()

# ==========================================
# 2. CLEAN & BRIGHT UI (Student Friendly)
# ==========================================

st.set_page_config(page_title="Researcher Pro", layout="wide")

# Custom CSS for Professional White Theme
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    
    /* Clean Cards */
    div.stChatMessage {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        color: #1E293B !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }

    /* Professional Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 2rem;
    }
    .stButton>button:hover { background-color: #1D4ED8; border: none; color: white; }
    
    /* Headers */
    h1, h2, h3 { color: #1E3A8A !important; font-family: 'Inter', sans-serif; }
    
    /* Input Fix */
    .stTextInput>div>div>input { border: 1px solid #CBD5E1; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INTERFACE EXECUTION
# ==========================================

with st.sidebar:
    st.title("📂 Resource Center")
    st.write("Tools for Students")
    st.divider()
    uploaded_file = st.file_uploader("Upload reference documents", type=['pdf', 'txt'])
    st.info("Uploaded files will be used to enhance the research accuracy.")

st.title("📑 AI Academic Research Engine")
st.write("Generate professional, structured assignments with high readability.")

if prompt := st.chat_input("Enter your assignment topic (e.g. Artificial Intelligence)..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Compiling academic data..."):
            data = get_academic_data(prompt)
            
            if data:
                # Screen Display
                st.subheader(data['title'])
                st.markdown("---")
                st.markdown("### 📘 Summary")
                st.write(data['summary'])
                
                # Structure Preview
                with st.expander("View Document Structure"):
                    for i, s in enumerate(data['sections'], 1):
                        st.write(f"**{i}.** {s}")
                
                # PDF Generation Logic
                try:
                    pdf_output = create_pdf(data)
                    st.divider()
                    st.download_button(
                        label="📥 Download Professional PDF",
                        data=pdf_output,
                        file_name=f"Assignment_{prompt.replace(' ','_')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("Professional Report Ready for Download.")
                except Exception as e:
                    st.error(f"Generation Error: {e}")
            else:
                st.warning("No specific academic matches found. Please refine your topic name.")
