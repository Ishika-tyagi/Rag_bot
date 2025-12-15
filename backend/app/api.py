# backend/app/api.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from . import services
from .models import QueryModel

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    session_id, split_docs = services.process_and_save_pdf(file)
    summary = await services.generate_summary(split_docs)
    return {"session_id": session_id, "filename": file.filename, "summary": summary}


@router.post("/query")
async def handle_query(query_data: QueryModel):
    # This function now correctly awaits the async function from services
    answer = await services.query_rag_chain(query_data.session_id, query_data.query)
    return {"answer": answer}