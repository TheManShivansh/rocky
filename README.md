# QuickSense AI - Multimodal Research Oracle

A production-ready MVP that summarizes YouTube videos, PDFs, and Web articles using RAG (Retrieval-Augmented Generation) architecture.

## Features

- **Multimodal Ingestion**: Support for YouTube videos, PDFs, and web articles
- **Automatic Summarization**: Generate summary, 5 key takeaways, and 3 action items upon ingestion
- **Chat with Document**: Interactive Q&A interface
- **RAG Pipeline**: Uses LangChain for text chunking, ChromaDB for vector storage, and Groq Llama-3 for generation

## Technical Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Model**: Groq Llama-3-70b-8192
- **Vector Database**: ChromaDB (local)
- **Embeddings**: HuggingFace all-MiniLM-L6-v2 (local)

## Setup

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env` to `.env.local` (optional, or just set GROQ_API_KEY)
   - Add your Groq API key: `GROQ_API_KEY=your_actual_key`

4. **Run the backend**:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Run the frontend** (in a separate terminal):
   ```bash
   cd frontend
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

6. **Access the application**:
   - Frontend: http://localhost:8501
   - Backend API docs: http://localhost:8000/docs

## Usage

1. **Ingest Content**:
   - Enter a YouTube URL, PDF URL, or web article URL
   - Click "Ingest" to process and summarize

2. **View Summary**:
   - Automatic summary, key takeaways, and action items are generated

3. **Chat with Document**:
   - Ask questions about the ingested content
   - Get AI-powered responses based on the document

## Project Structure

```
/
├── backend/          # FastAPI backend
│   ├── main.py       # Main FastAPI app
│   ├── ingestion.py  # Ingestion logic
│   ├── rag.py        # RAG pipeline
│   └── models.py     # Pydantic models
├── frontend/         # Streamlit frontend
│   └── app.py        # Main Streamlit app
├── requirements.txt  # Python dependencies
├── .env              # Environment variables template
└── README.md         # This file
```