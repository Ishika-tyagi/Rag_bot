# backend/app/services.py

import os
import tempfile
import uuid
import pathlib
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# ======================================
# Environment Setup
# ======================================
load_dotenv()  # Load .env file

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
COHERE_KEY = os.getenv("COHERE_API_KEY")

if not ANTHROPIC_KEY:
    raise RuntimeError("❌ ANTHROPIC_API_KEY missing in .env file.")
if not COHERE_KEY:
    raise RuntimeError("❌ COHERE_API_KEY missing in .env file.")

VECTOR_STORE_PATH = pathlib.Path("vector_stores")
VECTOR_STORE_PATH.mkdir(exist_ok=True)

# ======================================
# PDF Processing and Embedding
# ======================================
def process_and_save_pdf(file: UploadFile):
    """Processes a PDF, creates embeddings, and saves FAISS vector store."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = file.file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Load and split PDF
        loader = PyPDFLoader(tmp_file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(docs)

        # Create embeddings using Cohere
        embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=COHERE_KEY)
        vector_db = FAISS.from_documents(documents=split_docs, embedding=embeddings)

        # Save FAISS index
        session_id = str(uuid.uuid4())
        session_path = VECTOR_STORE_PATH / session_id
        vector_db.save_local(session_path)

        # Clean up temp file
        os.remove(tmp_file_path)
        return session_id, split_docs

    except Exception as e:
        print(f"Error in process_and_save_pdf: {e}")
        raise HTTPException(status_code=500, detail="Failed to process and save PDF.")

# ======================================
# Generate Summary
# ======================================
async def generate_summary(docs: list[Document]):
    """Generates a one-paragraph summary from the first few document chunks."""
    try:
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0.2,
            api_key=ANTHROPIC_KEY,
        )

        summary_context = "\n".join(doc.page_content for doc in docs[:3])

        prompt_template = (
            "Based on the following initial text from a document, "
            "please provide a concise, one-paragraph summary of what this document is likely about.\n\n"
            "Initial Text:\n{context}"
        )
        prompt = ChatPromptTemplate.from_template(prompt_template)

        chain = prompt | llm
        summary = await chain.ainvoke({"context": summary_context})
        return summary.content

    except Exception as e:
        print(f"Error in generate_summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate summary.")

# ======================================
# Query RAG Chain
# ======================================
async def query_rag_chain(session_id: str, query: str):
    """Loads a vector store from disk and queries it using Anthropic Claude."""
    session_path = VECTOR_STORE_PATH / session_id
    if not session_path.exists():
        raise HTTPException(status_code=404, detail="Session not found.")

    try:
        # Reload FAISS and embeddings
        embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=COHERE_KEY)
        vector_db = FAISS.load_local(
            session_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )

        # Initialize Claude model
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0.5,
            api_key=ANTHROPIC_KEY,
        )

        # Build prompt and RAG chain
        prompt_template = (
            "Answer the user's question based only on the provided context.\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{input}"
        )
        prompt = ChatPromptTemplate.from_template(prompt_template)

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector_db.as_retriever()
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = await rag_chain.ainvoke({"input": query})
        return response["answer"]

    except Exception as e:
        print(f"Error in query_rag_chain: {e}")
        raise HTTPException(status_code=500, detail="Failed to process query.")
