import streamlit as st
import requests
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

def get_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "v=" in url:
        return url.split("v=")[-1]
    return None

def get_transcript(video_id):
    api = f"https://youtubetranscript.com/?server_vid2={video_id}"
    r = requests.get(api)
    if r.status_code != 200:
        return None
    data = r.json()
    text = " ".join([i['text'] for i in data])
    return text

if url:
    video_id = get_video_id(url)

    if not video_id:
        st.error("Invalid URL")
        st.stop()

    text = get_transcript(video_id)

    if not text:
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
