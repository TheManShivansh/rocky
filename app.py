import streamlit as st
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

if url:
    try:
        prompt = f"Summarize this YouTube video in 5 key points:\n{url}"

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant"
        )

        st.subheader("Summary")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error("Error occurred")
        st.write(str(e))
