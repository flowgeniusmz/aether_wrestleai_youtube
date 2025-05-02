import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

# VARIABLES
initial_text = "Please enter a YouTube URL and press submit."
no_url_text = "No URL was entered. Please enter a URL and press submit again."

# FUNCTIONS
#### Extract Video ID
def extract_video_id(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['youtu.be']:
            return parsed_url.path[1:]
        elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            return parse_qs(parsed_url.query)['v'][0]
    except Exception:
        return None
    
#### Get Transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = "\n".join([item['text'] for item in transcript])
        st.success("✅ Transcript Extracted Successfully:")
        return full_text
    except TranscriptsDisabled:
        full_text = "Error: Transcripts are disabled for this video."
        st.error("🚫 Transcripts are disabled for this video.")
        return full_text
    except NoTranscriptFound:
        full_text = "Error: Transcripts are not available for this video."
        st.error("🚫 No transcript available for this video.")
        return full_text
    except Exception as e:
        full_text = f"Error: {str(e)}"
        st.error(f"❌ Error: {str(e)}")
        return full_text

# SESSION STATE INIT
if "transcript_output" not in st.session_state:
    st.session_state.transcript_output = initial_text

# DISPLAY
#### Page Title
st.title("Video Transcript Generator")
st.caption("Generate or get transcripts from YouTube videos by providing the URL.")
st.divider()

#### URL Input
st.subheader("Provide a YouTube URL")
url = st.text_input("Paste YouTube video URL:", placeholder="https://www.youtube.com/watch?v=VIDEO_ID")
btn_submit = st.button(label="Submit")
st.divider()

#### Get Transcript
st.subheader("View Generated Transcript")

if btn_submit:
    if url:
        video_id = extract_video_id(url)
        if video_id:
            st.session_state.transcript_output = get_transcript(video_id)
        else:
            st.session_state.transcript_output = "Error: Could not extract video ID. Please check the URL."
            st.error("❌ Invalid YouTube URL format.")
    else:
        st.session_state.transcript_output = no_url_text

display_text = st.text_area("Transcript", st.session_state.transcript_output, height=400)
