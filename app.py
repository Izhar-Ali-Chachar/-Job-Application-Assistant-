import streamlit as st
import tempfile
from resume_loader import get_pdf_text
from job_description_loader import get_desc_text
from cover_letter_generator import generate_cover_letter
from job_search_tool import search_remote_jobs
from extract_job_search_query import extract_job_search_query  # your LLM-based function

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📄 AI Cover Letter Generator")

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

            resume_text = get_pdf_text(tmp_path)

            # Generate cover letter
            result = generate_cover_letter(resume_text, job_description)

        st.subheader("✉️ Generated Cover Letter")
        st.text_area("Cover Letter", result, height=400)
        st.success("Done! You can now copy your personalized letter.")

        # Step 4: Job Search
        st.subheader("3. 🔎 Find Remote Jobs")

        search_from = st.selectbox("Search jobs based on:", ["Resume", "Cover Letter"])
        keyword_source = resume_text if search_from == "Resume" else result

        with st.spinner("Generating search query from your text..."):
            auto_keyword = extract_job_search_query(keyword_source)

        st.markdown(f"**💡 Suggested Job Query:** `{auto_keyword}`")

        # Manual override
        manual_query = st.text_input("🔧 Optional: Enter your own job search query", value=auto_keyword)

        if st.button("Search Jobs"):
            with st.spinner(f"Searching remote jobs for: '{manual_query}'..."):
                job_results = search_remote_jobs(manual_query)

            st.markdown("### 🧠 Matching Remote Jobs")
            if job_results.startswith("Error") or "No jobs" in job_results:
                st.warning(job_results)
            else:
                for line in job_results.split("\n"):
                    if line.startswith("- "):
                        st.markdown(line)
            st.code(f"Final search keyword: {manual_query}")
            st.code(f"Raw result: {job_results}")
