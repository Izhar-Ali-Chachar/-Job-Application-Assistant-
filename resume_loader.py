from langchain_community.document_loaders import PyPDFLoader

file_path = "data/resume.pdf"

def get_pdf_text(file_path):
    loader = PyPDFLoader(file_path)

    documents = loader.load()

    all_text = ""

    for doc in documents:
        all_text += doc.page_content + '\n'

    return all_text