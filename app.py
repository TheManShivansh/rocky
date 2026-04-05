import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

# UI
st.title("YouTube Summary")
url = st.text_input("Enter YouTube URL")

# Groq client
client = Groq(api_key=st.secrets["API_KEY"])


# ----------- FUNCTION TO GET VIDEO ID -----------
def get_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return None


# ----------- FUNCTION TO GET TRANSCRIPT -----------
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([i["text"] for i in transcript])
        return text
    except:
        return None


# ----------- MAIN LOGIC -----------
if url:
    video_id = get_video_id(url)

    if not video_id:
        st.error("Invalid YouTube URL")
    else:
        text = get_transcript(video_id)

        if text:
            # Show transcript
            st.subheader("Transcript (short)")
            st.write(text[:1000])

            # Generate summary
            try:
                response = client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": f"Summarize this transcript in 5 key points:\n{text}"
                    }],
                    model="llama-3.1-8b-instant"
                )

                st.subheader("Summary")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Summary error: {str(e)}")

        else:
            st.error("Transcript not available for this video")
