import streamlit as st
import wikipedia
import textwrap
from datetime import datetime
import time

# --- 1. Page Config (Tab Title & Icon) ---
st.set_page_config(
    page_title="Pro Research AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Custom CSS for Styling (Sundar Design) ---
st.markdown("""
    <style>
    .main_title {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .report_box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar (Controls) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040946.png", width=100)
    st.title("⚙️ Control Panel")
    st.write("---")
    
    # Interactivity: Slider for Summary Length
    summary_len = st.slider("Summary Length (Sentences)", min_value=3, max_value=10, value=5)
    
    # Interactivity: Language (Future feature placeholder)
    language = st.selectbox("Select Language", ["English", "Urdu (Coming Soon)", "Spanish (Coming Soon)"])
    
    st.write("---")
    st.caption("🚀 Powered by Wikipedia API")
    st.caption("👨‍💻 Developed by You")

# --- 4. Main Page UI ---
st.markdown('<div class="main_title">🧠 AI Assignment & Research Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate Professional Reports in Seconds</div>', unsafe_allow_html=True)

# Input Section (Center Aligned using Columns)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    topic = st.text_input("Enter Topic Name:", placeholder="e.g., Artificial Intelligence, Black Holes, History of Bitcoin")
    generate_btn = st.button("✨ Generate Assignment", use_container_width=True, type="primary")

# --- 5. Logic & Result Display ---
if generate_btn and topic:
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    try:
        # Simulation of processing (UI effect)
        status_text.text("🔍 Scanning Database...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        status_text.text(f"📖 Reading articles about '{topic}'...")
        progress_bar.progress(50)
        
        # Wikipedia Fetching
        page = wikipedia.page(topic, auto_suggest=False)
        title = page.title
        url = page.url
        content = page.content
        
        status_text.text("✍️ Writing Professional Report...")
        progress_bar.progress(80)
        
        # Data Processing
        summary = wikipedia.summary(topic, sentences=summary_len)
        body_text = content.split('== See also ==')[0][:4000] # Clean content
        
        # Final Report Format
        report_text = f"""
        TOPIC: {title.upper()}
        Date Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        Source: {url}
        
        1. EXECUTIVE SUMMARY
        ---------------------
        {textwrap.fill(summary, width=80)}
        
        2. DETAILED ANALYSIS
        ---------------------
        {textwrap.fill(body_text, width=80)}
        
        3. CONCLUSION
        --------------
        The topic '{title}' is verified and researched using open-source intelligence.
        """
        
        progress_bar.progress(100)
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        # --- Display Results (Designing Part) ---
        st.success("✅ Research Completed Successfully!")
        
        # 2 Columns for result (Left: Summary, Right: Details)
        r_col1, r_col2 = st.columns([2, 1])
        
        with r_col1:
            st.markdown(f"### 📄 {title}")
            st.info(summary)
            
            with st.expander("📖 Read Full Research (Detailed)"):
                st.write(body_text)
                
        with r_col2:
            st.markdown("### 📥 Actions")
            st.write(f"**Source:** [Wikipedia Link]({url})")
            
            # Download Button
            st.download_button(
                label="💾 Download Assignment (.txt)",
                data=report_text,
                file_name=f"{topic.replace(' ', '_')}_Assignment.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.success("Ready for submission!")

    except wikipedia.exceptions.DisambiguationError as e:
        st.error("⚠️ Topic too vague! Did you mean one of these?")
        st.write(e.options[:5])
    except wikipedia.exceptions.PageError:
        st.error("❌ No page found! Please check spelling.")
    except Exception as e:
        st.error(f"Error: {e}")

elif generate_btn and not topic:
    st.warning("⚠️ Please enter a topic first!")