import streamlit as st
import io
import html
import pypdf
import docx
from utils.summarizer import load_summarizer, generate_summary
from utils.text_analysis import analyze_document, extract_important_info

st.set_page_config(
    page_title="CivicLens AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium SaaS style
st.markdown("""
<style>
    /* Global Typography & Spacing */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe 0%, #3b82f6 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        filter: drop-shadow(0px 4px 12px rgba(59, 130, 246, 0.4));
    }
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        color: #334155;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .hero-description {
        font-size: 1.125rem;
        color: #64748B;
        margin-bottom: 1.5rem;
        max-width: 800px;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        background-color: #ECFDF5;
        color: #059669;
        font-size: 0.875rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        margin-bottom: 2rem;
        border: 1px solid #D1FAE5;
    }
    
    /* Cards */
    .modern-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }
    
    /* Summary Box */
    .summary-box {
        background: linear-gradient(to right, #F8FAFC, #FFFFFF);
        border-left: 4px solid #3B82F6;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem 2rem;
        font-size: 1.125rem;
        line-height: 1.7;
        color: #1E293B;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 2rem;
    }
    
    /* Sections */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.5rem;
    }
    .section-subtitle {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    
    /* Empty State */
    .empty-state {
        background-color: #F8FAFC;
        border: 1px dashed #CBD5E1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-top: 1rem;
    }
    .empty-state h4 {
        color: #334155;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .empty-state ol {
        text-align: left;
        display: inline-block;
        color: #475569;
        margin: 0 auto;
    }
    .empty-state li {
        margin-bottom: 0.5rem;
    }
    
    /* Footer Disclaimer */
    .disclaimer-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-top: 3rem;
        font-size: 0.875rem;
        color: #64748B;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .disclaimer-icon {
        font-size: 1.25rem;
        color: #94A3B8;
    }
    
    /* Sidebar styling */
    .sidebar-footer {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E2E8F0;
        font-size: 0.875rem;
        color: #64748B;
    }
    
    /* Button Override */
    .stButton>button[kind="primary"] {
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.2s ease;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Metric Cards Override */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        padding: 1.5rem 1rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        font-size: 3.5rem !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        margin-bottom: 0.25rem;
    }
    [data-testid="stMetricLabel"] * {
        font-size: 1.1rem !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Load model
    with st.spinner("Initializing system..."):
        summarizer = load_summarizer()
        
    model_ready = summarizer is not None
    
    # Hero Section
    st.markdown('<div class="hero-title">🔍 CivicLens AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Understand important documents in seconds.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-description">AI-powered document summarization and key-information extraction for students, citizens, and everyday users.</div>', unsafe_allow_html=True)
    
    if model_ready:
        st.markdown('<div class="status-badge">● AI Model Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge" style="background-color: #FEF2F2; color: #DC2626; border-color: #FECACA;">● Model Error</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("### CIVICLENS AI")
    st.sidebar.markdown("#### ⚙ Settings & Samples")
    
    st.sidebar.markdown("**Model Status**")
    if model_ready:
        st.sidebar.markdown("🟢 Model Ready")
    else:
        st.sidebar.markdown("🔴 Failed to load model")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Sample Documents**")
    
    sample_options = {
        "None": "",
        "College Scholarship Notification": "Dear Student,\n\nWe are pleased to inform you that you have been selected to receive the Merit Scholarship for the upcoming academic year. The scholarship amount is $5,000, which will be credited directly to your student account.\n\nTo accept this scholarship, you must submit the signed acceptance form by August 15, 2024. Failure to do so will result in forfeiture of the award. Additionally, you are required to maintain a minimum GPA of 3.5 throughout the academic year to remain eligible.\n\nPlease attend the scholarship orientation session on September 1, 2024, at the main auditorium. Congratulations on your outstanding achievements!\n\nSincerely,\nThe Scholarship Committee",
        "Government Application Notice": "Notice of Application Status: Incomplete\n\nYour application for the Small Business Assistance Grant (Ref: 994-B) has been reviewed. At this time, we cannot process your application because several required documents are missing.\n\nYou must provide the following documentation:\n1. A copy of your 2023 tax return.\n2. Proof of business registration.\n3. A valid photo ID of the primary applicant.\n\nPlease submit these documents via the online portal no later than October 30th, 2024. If we do not receive the requested information by the deadline, your application will be closed. For any questions, you may contact the support desk at 555-0199.\n\nDepartment of Economic Assistance",
        "College Examination Notice": "Important Notice Regarding Final Examinations\n\nAll students are advised that the final examination schedule for the Spring 2024 semester has been published. Exams will commence on May 10th and conclude on May 24th.\n\nStudents must arrive at the examination hall at least 15 minutes prior to the scheduled start time. A valid student ID is mandatory for entry into the examination hall. Use of electronic devices, including smartwatches, is strictly prohibited during the exam.\n\nIf you have two exams scheduled at the same time, you must report this conflict to the registrar's office by April 20th. Special accommodations requests must also be submitted by this date. Good luck with your preparations."
    }
    
    selected_sample = st.sidebar.selectbox("Select a sample:", list(sample_options.keys()), label_visibility="collapsed")
    
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        <p><strong>Open Source AI Project</strong></p>
        <p>Built with Python, Streamlit & Hugging Face</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Document Workspace (Card layout using st.container)
    with st.container():
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📄 Your Document</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Paste a document or upload a .txt, .pdf, or .docx file to extract its key information.</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Paste Text", "Upload File"])
        
        input_text = ""
        input_text_uploaded = ""
        
        with tab1:
            text_area_val = sample_options[selected_sample] if selected_sample != "None" else ""
            input_text_pasted = st.text_area("Document Content", value=text_area_val, height=250, label_visibility="collapsed")
        
        with tab2:
            uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"], label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.lower().endswith(".txt"):
                        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                        input_text_uploaded = stringio.read()
                    elif uploaded_file.name.lower().endswith(".pdf"):
                        reader = pypdf.PdfReader(uploaded_file)
                        extracted_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
                        input_text_uploaded = "\n".join(extracted_pages)
                    elif uploaded_file.name.lower().endswith(".docx"):
                        doc = docx.Document(uploaded_file)
                        input_text_uploaded = "\n".join([para.text for para in doc.paragraphs])
                    
                    if not input_text_uploaded.strip():
                        st.error("Could not extract readable text from this document. Please try another file or paste the text manually.")
                    else:
                        st.success("File uploaded successfully!")
                        with st.expander("View uploaded text"):
                            st.write(input_text_uploaded)
                except Exception as e:
                    st.error("Could not extract readable text from this document. Please try another file or paste the text manually.")
                    
        # Determine which text to use
        if input_text_uploaded:
            input_text = input_text_uploaded
        else:
            input_text = input_text_pasted
            
        st.markdown('</div>', unsafe_allow_html=True)

    # Analyze Button and Results
    if st.button("✨ Analyze Document", type="primary", use_container_width=True):
        if not input_text.strip():
            st.warning("Please enter or upload some text to analyze.")
        elif not summarizer:
            st.error("The summarization model is not loaded. Please wait or check for errors.")
        else:
            with st.spinner("Analyzing document..."):
                summary = generate_summary(summarizer, input_text)
                analysis = analyze_document(input_text, summary)
                important_info = extract_important_info(input_text)
                
            st.markdown('<div class="section-title" style="margin-top: 2rem;">✨ Analysis Complete</div>', unsafe_allow_html=True)
            
            st.write("### 📝 AI Summary")
            safe_summary = html.escape(summary)
            st.markdown(f'<div class="summary-box">{safe_summary}</div>', unsafe_allow_html=True)
            
            st.write("### 📊 Document Metrics")
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            metric_col1.metric("Original Words", analysis["original_word_count"])
            metric_col2.metric("Summary Words", analysis["summary_word_count"])
            metric_col3.metric("Reduction", f"{analysis['reduction_percentage']}%")
            metric_col4.metric("Sentences", analysis["sentence_count"])
            
            st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
            st.write("### 📌 Key Information")
            
            info_col1, info_col2, info_col3 = st.columns(3)
            
            with info_col1:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("#### 📅 Important Dates")
                if important_info["dates"]:
                    for date in important_info["dates"]:
                        st.markdown(f"- {html.escape(date)}")
                else:
                    st.write("No important dates detected.")
                st.markdown('</div>', unsafe_allow_html=True)
                    
            with info_col2:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("#### 📋 Requirements")
                if important_info["requirements"]:
                    for req in important_info["requirements"]:
                        st.markdown(f"- {html.escape(req)}")
                else:
                    st.write("No requirements detected.")
                st.markdown('</div>', unsafe_allow_html=True)
                    
            with info_col3:
                st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                st.markdown("#### ⚡ Important Actions")
                if important_info["actions"]:
                    for action in important_info["actions"]:
                        st.markdown(f"- {html.escape(action)}")
                else:
                    st.write("No specific actions detected.")
                st.markdown('</div>', unsafe_allow_html=True)
                
    else:
        # Empty State
        if not input_text.strip():
            st.markdown("""
            <div class="empty-state">
                <h4>How CivicLens works</h4>
                <ol>
                    <li>Add your document</li>
                    <li>Let AI summarize it</li>
                    <li>Review dates, requirements & actions</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

    # Footer Disclaimer
    st.markdown("""
    <div class="disclaimer-card">
        <div class="disclaimer-icon">ℹ️</div>
        <div>AI-generated summaries may contain errors. Always verify important information against the original document. CivicLens AI does not provide official legal or government advice.</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
