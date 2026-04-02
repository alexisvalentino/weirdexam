import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
KB_DIR = BASE_DIR / "kb"
CHROMA_PATH = BASE_DIR / "app" / "data" / "chroma"

# We use a lightweight local model standard in simple RAG
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_store():
    """Reads markdown files from kb/ and builds the Chroma database."""
    print(f"Loading documents from {KB_DIR}...")
    loader = DirectoryLoader(str(KB_DIR), glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    print(f"Loaded {len(documents)} documents. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print(f"Split into {len(chunks)} chunks. Building Chroma DB at {CHROMA_PATH}...")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=str(CHROMA_PATH))
    print("Vector store built successfully.")
    return db

def get_retriever():
    """Returns the Chroma retriever."""
    if not os.path.exists(CHROMA_PATH):
        print("Chroma DB not found. Building it now...")
        db = build_vector_store()
    else:
        db = Chroma(persist_directory=str(CHROMA_PATH), embedding_function=embeddings)
    
    return db.as_retriever(search_kwargs={"k": 3})

if __name__ == "__main__":
    build_vector_store()
