import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import fitz  # PyMuPDF
from urllib.parse import urlparse

def extract_youtube_transcript(url: str) -> str:
    """Extract transcript from YouTube video."""
    try:
        video_id = urlparse(url).query.split('v=')[1].split('&')[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract YouTube transcript: {str(e)}")

def extract_pdf_text(url: str) -> str:
    """Extract text from PDF URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_data = response.content

        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {str(e)}")

def extract_web_text(url: str) -> str:
    """Extract text from web article."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        raise ValueError(f"Failed to extract web text: {str(e)}")

def ingest_content(url: str, content_type: str) -> str:
    """Main ingestion function."""
    if content_type == 'youtube':
        return extract_youtube_transcript(url)
    elif content_type == 'pdf':
        return extract_pdf_text(url)
    elif content_type == 'web':
        return extract_web_text(url)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")