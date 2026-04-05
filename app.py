import streamlit as st
from pytube import YouTube
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

if url:
    try:
        yt = YouTube(url)

        # Get captions
        caption = yt.captions.get_by_language_code('en')

        if caption is None:
            st.error("No captions available for this video")
            st.stop()

        text = caption.generate_srt_captions()

    except Exception as e:
        st.error(f"Error fetching video: {str(e)}")
        st.stop()

    st.subheader("Transcript (short)")
    st.write(text[:1000])

    # AI Summary
    try:
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Summarize in 5 key points and action items:\n{text[:4000]}"
            }],
            model="llama3-70b-8192"
        )

        st.subheader("Summary")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"AI Error: {str(e)}")
