# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import pathlib

# Load environment variables
load_dotenv()

# --- THIS IS THE FIX ---
# We now check for the correct Anthropic API key instead of the old OpenAI key.
if "ANTHROPIC_API_KEY" not in os.environ:
    raise RuntimeError("ANTHROPIC_API_KEY not found in .env file.")
# --------------------

# Ensure the vector store directory exists
VECTOR_STORE_PATH = pathlib.Path("vector_stores")
VECTOR_STORE_PATH.mkdir(exist_ok=True)


from .api import router # Import the router from api.py

app = FastAPI(title="AskPDF Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "Backend is running with a professional structure"}