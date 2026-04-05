from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    url: str
    content_type: str  # 'youtube', 'pdf', 'web'

class SummaryResponse(BaseModel):
    summary: str
    key_takeaways: List[str]
    action_items: List[str]
    document_id: str

class ChatRequest(BaseModel):
    query: str
    document_id: str

class ChatResponse(BaseModel):
    answer: str