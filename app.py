import streamlit as st
import tempfile
from resume_loader import get_pdf_text
from job_description_loader import get_desc_text
from cover_letter_generator import generate_cover_letter

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📄 AI Cover Letter Generator")

# Resume Upload
st.subheader("1. Upload your resume (PDF)")
resume_file = st.file_uploader("Upload Resume", type=["pdf"])

# Job Description Inputs
st.subheader("2. Paste the Job Description")
job_description = get_desc_text()

# Button to generate
if st.button("Generate Cover Letter"):
    if not resume_file or not job_description.strip():
        st.error("Please upload a resume and enter a job description.")
    else:
        with st.spinner("Processing..."):
            # Load and parse resume
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(resume_file.read())
                tmp_path = tmp_file.name

            resume_text = get_pdf_text(tmp_path)

            # Run the LangChain
            result = generate_cover_letter(resume_text, job_description)

        st.subheader("✉️ Generated Cover Letter")
        st.text_area("Cover Letter", result, height=400)

        st.success("Done! You can now copy your personalized letter.")