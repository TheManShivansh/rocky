import streamlit as st
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

if url:
    try:
        prompt = f"You are given a YouTube video link.

Do NOT say you can't access it.

Instead:
- Assume the topic from title/URL
- Generate a realistic summary

Give output STRICTLY in this format:

1. Key Point 1
2. Key Point 2
3. Key Point 3
4. Key Point 4
5. Key Point 5

Also add:
Action Steps:
- Step 1
- Step 2
- Step 3

Video URL:
{url}
"""

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
