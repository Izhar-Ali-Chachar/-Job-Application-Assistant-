import streamlit as st
import tempfile
from resume_loader import get_pdf_text
from job_description_loader import get_desc_text
from cover_letter_generator import generate_cover_letter
from create_agent import get_jobs
from extract_job_search_query import extract_job_search_query

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📄 AI Cover Letter Generator")

# Initialize session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

if "auto_keyword" not in st.session_state:
    st.session_state.auto_keyword = ""

# Step 1: Resume Upload
st.subheader("1. Upload your resume (PDF)")
resume_file = st.file_uploader("Upload Resume", type=["pdf"])

# Step 2: Job Description Input
st.subheader("2. Paste the Job Description")
job_description = get_desc_text()

# Step 3: Generate Cover Letter
if st.button("Generate Cover Letter"):
    if not resume_file or not job_description.strip():
        st.error("Please upload a resume and enter a job description.")
    else:
        with st.spinner("Processing..."):
            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(resume_file.read())
                tmp_path = tmp_file.name

            st.session_state.resume_text = get_pdf_text(tmp_path)
            st.session_state.cover_letter = generate_cover_letter(st.session_state.resume_text, job_description)

        st.success("✅ Cover Letter Generated!")

# Display the cover letter if it exists
if st.session_state.cover_letter:
    st.subheader("✉️ Generated Cover Letter")
    st.text_area("Cover Letter", st.session_state.cover_letter, height=400)

    # Step 4: Job Search
    st.subheader("3. 🔎 Find Remote Jobs")

    search_from = st.selectbox("Search jobs based on:", ["Resume", "Cover Letter"])
    keyword_source = (
        st.session_state.resume_text if search_from == "Resume" else st.session_state.cover_letter
    )

    with st.spinner("Generating search query from your text..."):
        st.session_state.auto_keyword = extract_job_search_query(keyword_source)

    st.markdown(f"**💡 Suggested Job Query:** `{st.session_state.auto_keyword}`")

    # Manual override
    manual_query = st.text_input("🔧 Optional: Enter your own job search query", value=st.session_state.auto_keyword)

    if st.button("Search Jobs"):
        with st.spinner(f"Searching remote jobs for: '{manual_query}'..."):
            try:
                job_results = get_jobs(manual_query)
            except Exception as e:
                job_results = f"❌ Error while fetching jobs: {e}"

        st.markdown("### 🧠 Matching Remote Jobs")
        if not job_results or "Error" in job_results or "No jobs" in job_results:
            st.warning(job_results)
        else:
            st.markdown(job_results, unsafe_allow_html=True)

        st.code(f"Final search keyword: {manual_query}")
