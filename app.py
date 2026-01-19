import streamlit as st
from fpdf import FPDF
import wikipediaapi
import datetime
import io

# ==========================================
# 1. CORE RESEARCH ENGINE
# ==========================================

def get_academic_data(topic):
    # Proper User-Agent for Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="AcademicResearchBot/1.0 (contact: support@assignmentbot.com)"
    )
    page = wiki_wiki.page(topic)
    
    if not page.exists():
        return None
        
    return {
        "title": page.title,
        "summary": page.summary[:2000],
        "sections": [s.title for s in page.sections[:6]],
        "full_content": page.text[:10000]
    }

class ProfessionalPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'OFFICIAL ACADEMIC REPORT', 0, 1, 'R')
        self.line(10, 18, 200, 18)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | AI Academic Engine', 0, 0, 'C')

def create_pdf(data):
    pdf = ProfessionalPDF()
    pdf.add_page()
    
    # --- Professional Title Page ---
    pdf.ln(50)
    pdf.set_font('helvetica', 'B', 30)
    pdf.set_text_color(26, 54, 104) # Deep Professional Blue
    pdf.multi_cell(0, 15, data['title'].upper(), align='C')
    
    pdf.ln(10)
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align='C')
    
    # --- Content Page ---
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(26, 54, 104)
    pdf.cell(0, 10, "1. EXECUTIVE SUMMARY", ln=True)
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    # Cleaning text for latin-1 compatibility
    clean_summary = data['summary'].encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, clean_summary)
    
    # --- Structured Sections ---
    pdf.ln(10)
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, "2. CORE ANALYSIS & FINDINGS", ln=True)
    
    for i, section in enumerate(data['sections'], 1):
        pdf.ln(5)
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 10, f"2.{i} {section}", ln=True)
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 7, f"Detailed academic exploration regarding {section}. This report segment evaluates the key theoretical and practical implications of {data['title']} within this specific domain.")

    # FIX: Using bytes conversion to avoid "Invalid binary data format"
    return bytes(pdf.output())

# ==========================================
# 2. PROFESSIONAL BRIGHT UI
# ==========================================

st.set_page_config(page_title="AI Researcher Pro", layout="wide")

st.markdown("""
    <style>
    /* Professional Clean Theme */
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    
    /* Content Cards */
    div.stChatMessage {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Typography Fix */
    p, span, div { color: #1E293B !important; font-size: 16px; }
    h1, h2, h3 { color: #1E3A8A !important; }
    
    /* Professional Blue Button */
    .stButton>button {
        background-color: #2563EB;
        color: white !important;
        border-radius: 8px;
        padding: 0.7rem 2.5rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover { background-color: #1D4ED8; }
    
    /* Sidebar Fix */
    section[data-testid="stSidebar"] { background-color: #F1F5F9; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INTERFACE EXECUTION
# ==========================================

with st.sidebar:
    st.title("📂 Project Assets")
    st.write("Academic Tools v2.1")
    st.divider()
    uploaded_file = st.file_uploader("Upload reference documents", type=['pdf', 'txt'])

st.title("📑 AI Professional Assignment Engine")
st.write("Structured, Readable, and Academic-Grade Research Reports.")

if prompt := st.chat_input("Enter your research topic..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Compiling structured research..."):
            data = get_academic_data(prompt)
            
            if data:
                st.subheader(data['title'])
                st.markdown("---")
                
                # Display Summary on Screen
                st.markdown("### 🔍 Summary Overview")
                st.write(data['summary'])
                
                # Structure Details
                with st.expander("Show Document Table of Contents"):
                    for i, s in enumerate(data['sections'], 1):
                        st.write(f"**{i}.** {s}")
                
                # PDF Generation Logic
                try:
                    pdf_data = create_pdf(data)
                    st.divider()
                    st.download_button(
                        label="📥 Download Professional Assignment (PDF)",
                        data=pdf_data,
                        file_name=f"Assignment_{prompt.replace(' ','_')}.pdf",
                        mime="application/pdf"
                    )
                    st.success("PDF generated successfully. Ready for download.")
                except Exception as e:
                    st.error(f"Generation Error: {e}")
            else:
                st.warning("Could not find academic matches for this topic. Please try a standard academic term.")
