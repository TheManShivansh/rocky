import streamlit as st
import requests
import json

# Backend URL
BACKEND_URL = "http://localhost:8000"

st.title("QuickSense AI - Multimodal Research Oracle")

st.markdown("""
Upload or provide URLs for YouTube videos, PDFs, or web articles to get AI-powered summaries and chat with the content.
""")

# Session state for document ID
if 'document_id' not in st.session_state:
    st.session_state.document_id = None

# Ingestion Section
st.header("Ingest Content")

content_type = st.selectbox("Content Type", ["youtube", "pdf", "web"])
url = st.text_input("URL", placeholder="Enter URL here...")

if st.button("Ingest"):
    if url:
        with st.spinner("Processing..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ingest",
                    json={"url": url, "content_type": content_type}
                )
                response.raise_for_status()
                data = response.json()

                st.session_state.document_id = data.get("document_id")

                st.success("Content ingested successfully!")

                # Display summary
                st.subheader("Summary")
                st.write(data["summary"])

                st.subheader("Key Takeaways")
                for takeaway in data["key_takeaways"]:
                    st.write(f"• {takeaway}")

                st.subheader("Action Items")
                for item in data["action_items"]:
                    st.write(f"• {item}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a URL")

# Chat Section
if st.session_state.document_id:
    st.header("Chat with Document")

    query = st.text_input("Ask a question about the document", key="chat_input")

    if st.button("Ask"):
        if query:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={"query": query, "document_id": st.session_state.document_id}
                    )
                    response.raise_for_status()
                    data = response.json()

                    st.write("**Answer:**")
                    st.write(data["answer"])

                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.error("Please enter a question")

# Footer
st.markdown("---")
st.markdown("Built with FastAPI, Streamlit, and Groq AI")