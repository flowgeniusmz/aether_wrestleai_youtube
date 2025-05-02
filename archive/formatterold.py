import streamlit as st
import re
from pydantic import BaseModel
from openai import OpenAI

# Variables
client = OpenAI(api_key=st.secrets.openai.api_key)
sys_prompt = """
    You will be given a raw YouTube video transcript that has been copied and pasted by a user. This raw transcript does not have correct punctuation, complete sentences, and needs to be formatted in a way effective to be used.
    
    Your job is to provide a single, clean, effective transcript to the user. Each transcript you return must meet **ALL** of these requirements:
    - You will review and evaluate the transcript to determine where each sentence starts and stops
    - You will determine the starting time and ending time of each individual sentence using the timestamps provided in the raw transcript
    - You will create a new transcript in which each individual sentence is a new line containing the starting time, ending time, and actual sentence
    - **EACH LINE WILL FOLLOW THIS FORMAT**: [SentenceStartTime - SentenceEndTime] Sentence
    - **EXAMPLE**: [0:25 - 0:29] First, someone's taking me down in a single leg and when they shoot they shoot right.
    """
model = "gpt-4.1"

# Classes
class Transcript(BaseModel):
    transcript: str

# Functions
def get_transcript(raw_transcript: str):
    input = [{"role": "system", "content": f"{sys_prompt}"}, {"role": "user", "content": f"{raw_transcript}"}]
    response = client.responses.parse(
        model=model,
        input=input,
        text_format=Transcript
    )
    clean_transcript = response.output_parsed
    return clean_transcript

# --- Page Setup ---
st.title("🧹 YouTube Transcript Cleaner")
st.caption("Paste raw transcript from YouTube and clean it by removing timestamps.")
st.divider()


# --- UI: Input Area ---
raw_text = st.text_area("📋 Paste Raw YouTube Transcript Here:", height=400, placeholder="Paste full YouTube transcript text...")

# --- Submit Button ---
if st.button("🧼 Clean Transcript"):
    if raw_text.strip():
        #cleaned_transcript = format_youtube_transcript(raw_text)
        cleaned_transcript = get_transcript(raw_transcript=raw_text)
        cleaned_transcript_display = cleaned_transcript.transcript
        st.success("✅ Transcript cleaned successfully.")
        st.text_area("📝 Cleaned Transcript", cleaned_transcript_display, height=400)
    else:
        st.warning("⚠️ Please paste some transcript text before cleaning.")







# --- Transcript Formatter ---
def format_youtube_transcript(raw_text: str) -> str:
    """
    Cleans a raw transcript copied from the YouTube UI. 
    Removes timestamps and returns a single clean transcript paragraph.
    """
    text = raw_text.strip()
    if text.lower().startswith("transcript"):
        text = text[len("transcript"):].strip()

    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()
        # Skip lines that are just timestamps
        if re.fullmatch(r'\d{1,2}:\d{2}(?::\d{2})?', line):
            continue
        # Remove timestamps at the beginning of lines
        line = re.sub(r'^\d{1,2}:\d{2}(?::\d{2})?\s+', '', line)
        if line:
            cleaned_lines.append(line)

    return " ".join(cleaned_lines)
