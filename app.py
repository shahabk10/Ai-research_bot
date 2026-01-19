import streamlit as st
from fpdf import FPDF
import wikipediaapi
import datetime
import io

# ==========================================
# 1. DEEP RESEARCH ENGINE (Extended Data)
# ==========================================

def get_detailed_academic_data(topic):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="AcademicResearchBot/1.0 (contact: support@assignmentbot.com)"
    )
    page = wiki_wiki.page(topic)
    
    if not page.exists():
        return None
        
    # Extracting all sections for massive data
    sections_content = []
    for s in page.sections:
        if len(s.text) > 50: # Only meaningful sections
            sections_content.append({"title": s.title, "text": s.text})
            # Sub-sections bhi include karna
            for ss in s.sections:
                sections_content.append({"title": f"{s.title} - {ss.title}", "text": ss.text})

    return {
        "title": page.title,
        "summary": page.summary,
        "sections": sections_content,
        "full_text": page.text
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
        # New section on new page if it's substantial
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
# 2. BRIGHT & CLEAN UI
# ==========================================

st.set_page_config(page_title="Academic Engine Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    p, span, div { color: #1E293B !important; font-size: 16px; }
    h1, h2, h3 { color: #1E3A8A !important; }
    .stButton>button {
        background-color: #2563EB; color: white !important;
        border-radius: 8px; padding: 0.7rem 3rem; font-weight: bold; border: none;
    }
    div.stChatMessage { background-color: #F1F5F9; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. INTERFACE
# ==========================================

st.title("📑 Full-Length Assignment Generator")
st.write("Generating structured 4-5 page research reports automatically.")

if prompt := st.chat_input("Enter a broad topic (e.g., Global Warming, History of Rome, Artificial Intelligence)..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Extracting deep research data... This may take a moment for 4-5 pages."):
            data = get_detailed_academic_data(prompt)
            
            if data and len(data['sections']) > 2:
                st.success(f"Extracted {len(data['sections'])} detailed sections for {data['title']}.")
                
                # Preview structure
                with st.expander("Preview Table of Contents"):
                    for sec in data['sections']:
                        st.write(f"- {sec['title']}")
                
                # Long PDF Generation
                try:
                    pdf_data = create_long_pdf(data)
                    st.divider()
                    st.download_button(
                        label="📥 Download Full 4-Page Assignment (PDF)",
                        data=pdf_data,
                        file_name=f"Full_Assignment_{prompt.replace(' ','_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error during formatting: {e}")
            else:
                st.warning("Topic is too narrow for a 4-page assignment. Try a broader subject.")
