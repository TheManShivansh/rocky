from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from backend.models import IngestRequest, SummaryResponse, ChatRequest, ChatResponse
from backend.ingestion import ingest_content
from backend.rag import RAGPipeline
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="QuickSense AI Backend", version="1.0.0")

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_pipeline = RAGPipeline()

@app.post("/ingest", response_model=SummaryResponse)
async def ingest_document(request: IngestRequest):
    """Ingest a document and return summary."""
    try:
        # Generate unique document ID
        document_id = str(uuid.uuid4())

        # Extract text
        text = ingest_content(request.url, request.content_type)

        # Store in vector DB
        rag_pipeline.store_document(document_id, text)

        # Generate summary
        summary_data = rag_pipeline.generate_summary(text)

        # Add document_id to response for chat functionality
        summary_data["document_id"] = document_id

        return SummaryResponse(**summary_data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """Chat with an ingested document."""
    try:
        answer = rag_pipeline.chat_with_document(request.document_id, request.query)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "QuickSense AI Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)