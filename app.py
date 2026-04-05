import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

if url:
    video_id = url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    text = " ".join([i['text'] for i in transcript])
    
    st.write("Transcript (short):")
    st.write(text[:1000])
