# 📄 RAG-Based PDF Question Answering System

A **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions based on their content.  
The system uses **Cohere embeddings**, **FAISS vector store**, and **Anthropic Claude** for accurate and contextual answers.

---

## 🚀 Features
- Upload PDF documents
- Automatic text chunking and vector embedding
- Semantic search using FAISS
- Question answering using Anthropic Claude
- FastAPI-based backend
- Modular and scalable project structure

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python
- **LLM:** Anthropic Claude
- **Embeddings:** Cohere
- **Vector Store:** FAISS
- **Framework:** LangChain

---

## 📁 Project Structure
```Rag-pdf-chatbot/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI app entry point
│ │ ├── api.py # API routes
│ │ ├── services.py # RAG logic (PDF processing, embeddings, QA)
│ │
│ ├── vector_stores/ # Stored FAISS indexes (ignored in git)
│ ├── requirements.txt
│ └── .env.example
├── frontend/
  ├── package.json
  │
  ├── tailwind.config.js
  │
  ├── postcss.config.js
  │ 
  ├── vite.config.js
  │  
  └── src/
    │
    ├── index.css
    │
    ├── main.jsx
    │
    ├── App.jsx
    │
    ├── components/
    │   │
    │   ├── ChatWindow.jsx
    │   │   # Main chat interface
    │   │
    │   ├── MessageBubble.jsx
    │   │   # Individual chat message component
    │   │
    │   ├── Sidebar.jsx
    │   │   # Sidebar navigation and controls
    │   │
    │   └── UploadBox.jsx
    │       # File upload component
    │
    └── assets/
        │
        └── logo.svg
            # Static assets such as images and icons

├── .gitignore
├── README.md
└── LICENSE
```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/rag-pdf-chatbot.git
cd rag-pdf-chatbot
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```
### 2️⃣Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
### 3️⃣ Install Dependencies
pip install -r backend/requirements.txt
### 4️⃣ Configure Environment Variables
cp backend/.env.example backend/.env
Edit backend/.env and add your API keys:
ANTHROPIC_API_KEY=your_anthropic_api_key
COHERE_API_KEY=your_cohere_api_key
### 5️⃣ Run the Backend
uvicorn backend.app.main:app --reload
### 6️⃣Run the Frontend
npm run dev
