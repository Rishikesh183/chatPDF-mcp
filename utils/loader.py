from langchain.document_loaders import PyPDFLoader,UnstructuredPowerPointLoader,CSVLoader,UnstructuredWordDocumentLoader,TextLoader,UnstructuredMarkdownLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import List

def load_and_split_document(file_path: str):
    ext = Path(file_path).suffix.lower()
    
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".pptx":
        loader = UnstructuredPowerPointLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path)
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    elif ext == ".md":
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    return split_docs
