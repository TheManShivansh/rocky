import chromadb
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Groq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from typing import List

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = Groq(
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def chunk_text(self, text: str) -> List[str]:
        """Chunk text into smaller pieces."""
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separator=" "
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def store_document(self, document_id: str, text: str):
        """Store document chunks in ChromaDB."""
        chunks = self.chunk_text(text)
        collection = self.client.get_or_create_collection(name=document_id)

        # Clear existing
        collection.delete()

        # Add new chunks
        for i, chunk in enumerate(chunks):
            embedding = self.embeddings.embed_query(chunk)
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[f"{document_id}_{i}"]
            )

    def retrieve_context(self, document_id: str, query: str, k: int = 5) -> str:
        """Retrieve relevant context for a query."""
        collection = self.client.get_collection(name=document_id)
        query_embedding = self.embeddings.embed_query(query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        context = " ".join(results['documents'][0]) if results['documents'] else ""
        return context

    def generate_summary(self, text: str) -> dict:
        """Generate summary, key takeaways, and action items."""
        prompt_template = """
        Based on the following text, provide:
        1. A concise summary (2-3 sentences)
        2. 5 key takeaways (bullet points)
        3. 3 action items (bullet points)

        Text: {text}

        Format your response as:
        SUMMARY: [summary]
        KEY TAKEAWAYS:
        - [takeaway 1]
        - [takeaway 2]
        ...
        ACTION ITEMS:
        - [item 1]
        - [item 2]
        ...
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = prompt | self.llm

        response = chain.invoke({"text": text[:4000]})  # Limit text length

        # Parse response
        lines = response.split('\n')
        summary = ""
        key_takeaways = []
        action_items = []

        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith('SUMMARY:'):
                summary = line.replace('SUMMARY:', '').strip()
                current_section = 'summary'
            elif line.startswith('KEY TAKEAWAYS:'):
                current_section = 'takeaways'
            elif line.startswith('ACTION ITEMS:'):
                current_section = 'actions'
            elif line.startswith('- ') and current_section == 'takeaways':
                key_takeaways.append(line[2:])
            elif line.startswith('- ') and current_section == 'actions':
                action_items.append(line[2:])

        return {
            "summary": summary,
            "key_takeaways": key_takeaways[:5],  # Limit to 5
            "action_items": action_items[:3]     # Limit to 3
        }

    def chat_with_document(self, document_id: str, query: str) -> str:
        """Chat with the document using RAG."""
        context = self.retrieve_context(document_id, query)

        if not context:
            return "No relevant information found in the document."

        prompt_template = """
        Based on the following context from the document, answer the user's question.
        If the context doesn't contain enough information, say so.

        Context: {context}

        Question: {query}

        Answer:
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])
        chain = prompt | self.llm

        response = chain.invoke({"context": context, "query": query})
        return response