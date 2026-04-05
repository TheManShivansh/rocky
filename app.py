import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

if url:
    if "youtu.be" in url:
        video_id = url.split("/")[-1]
    else:
        video_id = url.split("v=")[-1]


    YouTubeTranscriptApi().get_transcript(video_id)
    text = " ".join([i['text'] for i in transcript])

    st.write("Transcript (short):")
    st.write(text[:1000])

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Summarize in 5 key points and action items:\n{text[:4000]}"}],
        model="llama3-70b-8192"
    )

    st.write(response.choices[0].message.content)
