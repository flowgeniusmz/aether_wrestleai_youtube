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
    response_output = response.output_parsed
    clean_transcript = response_output.transcript
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
        cleaned_transcript = get_transcript(raw_transcript=raw_text)
        st.success("✅ Transcript cleaned successfully.")
        st.text_area("📝 Cleaned Transcript", cleaned_transcript, height=400)

        st.download_button(
            label="💾 Download Transcript as .txt",
            data=cleaned_transcript,
            file_name="cleaned_transcript.txt",
            mime="text/plain"
        )

    else:
        st.warning("⚠️ Please paste some transcript text before cleaning.")




