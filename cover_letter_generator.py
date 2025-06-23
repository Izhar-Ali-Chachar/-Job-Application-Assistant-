from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

def generate_cover_letter(resume, job_description):
    prompt = PromptTemplate(
        template = """
    You are a helpful assistant that writes personalized cover letters.
    Resume:
    {resume}

    Job Description:
    {job_description}

    Write a cover letter that matches the job and highlights the most relevant resume experience. Keep it professional and concise.
    """,
        input_variables = ['resume', 'job_description']
    )

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17')

    parser = StrOutputParser()

    chain = prompt | llm | parser

    result = chain.invoke({"resume": resume, "job_description": job_description})

    return result