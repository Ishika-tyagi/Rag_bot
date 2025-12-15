# backend/app/models.py
from pydantic import BaseModel

class QueryModel(BaseModel):
    session_id: str
    query: str