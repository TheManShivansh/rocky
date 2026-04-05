import streamlit as st
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

if url:
    try:
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"""
                Analyze this YouTube video and give:
                1. 5 key points
                2. Actionable insights

                URL: {url}
                """
            }],
            model="llama3-70b-8192"
        )

        st.subheader("Summary")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {str(e)}")        
        st.error("Transcript not available")
        st.stop()

    st.subheader("Transcript (short)")
    st.write(text[:1000])

    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"Summarize in 5 key points and action items:\n{text[:4000]}"
        }],
        model="llama3-70b-8192"
    )

    st.subheader("Summary")
    st.write(response.choices[0].message.content)
