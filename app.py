import streamlit as st
from groq import Groq

st.title("YouTube Summary")

url = st.text_input("Enter YouTube URL")

client = Groq(api_key=st.secrets["API_KEY"])

if url:
    try:
        prompt = f"""
        Summarize this YouTube video in 5 key points and give action steps:
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
        st.error(f"Error: {str(e)}")        st.error("Invalid YouTube URL")
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
