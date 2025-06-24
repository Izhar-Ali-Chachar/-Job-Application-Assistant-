from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

def extract_job_search_query(text: str) -> str:
    prompt = PromptTemplate(
        template="""
        Based on the following user text (which may be a resume or a cover letter),
        extract the most relevant job search keyword or short phrase.
        This should be something you'd type into a job board (like "Python developer", "React engineer", "AI researcher", etc.)

        Text:
        {text}

        Return only the keyword or phrase, nothing else.
        """,
        input_variables=["text"]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite-preview-06-17")
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"text": text})
