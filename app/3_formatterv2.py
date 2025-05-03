import streamlit as st
import re
from pydantic import BaseModel, Field, HttpUrl, conint, confloat
from typing import List
from openai import OpenAI

# Variables
client = OpenAI(api_key=st.secrets.openai.api_key)
sys_prompt = """
    You are USA Wrestling curriculum assistant. 
    Return the session data as JSON that matches the provided schema. 
    You will be provided with the following:
    - Raw transcript (You must clean this up - (a) you must determine complete sentences, (b) determine their respective start and end times, and (c) create the reformatted clean transcript)
    - Summary bullets (You can use as is or enhance if necessary)
    - Week (use value provided)
    - Session (use value provided)
    - Title (You must use the title provided and concatenate it with the week and session i.e. 'Title [Week, Session]')
    You will not be provided with tags - you must review the title, transcript, and summary bullets and determine that tags to return (overtagging is encouraged / better than undertagging)

    """
model = "gpt-4.1"

# Classes
class TranscriptSegment(BaseModel):
    """
    A single caption span within a YouTube transcript.
    Times are in seconds.
    """
    start: float = Field(..., description="Start time of the segment (in seconds)")
    end:   float = Field(..., description="End time of the segment (in seconds)")
    text:  str = Field(..., description="Verbatim caption text for the time span")

class CurriculumSession(BaseModel):
    """
    Schema for a single training plan session used in structured OpenAI outputs.
    """
    week:            int = Field(..., description="Week number in the curriculum")
    session:         int = Field(..., description="Session number within the week")
    title:           str = Field(..., description="Descriptive session title")
    tags:            List[str] = Field(..., description="Topical tags for quick filtering")
    summary_bullets: List[str] = Field(..., description="Key coaching points and variations")
    #video_url:       HttpUrl = Field(..., description="Public or signed URL to the demo video")
    transcript:      List[TranscriptSegment] = Field(..., description="Full, timestamp aligned transcript")


# Functions
def get_user_message(transcript: str, week: int, session: int, title: int, summary_bullets: str):
    user_message = f"""
    Week: {week}
    Session: {session}
    Title: {title}
    Raw Transcript: {transcript}
    Summary Bullets: {summary_bullets}
    """
    return user_message

def get_response(user_message: str):
    sys_message = {"role": "system", "content": f"{sys_prompt}"}
    user_message = {"role": "user", "content": f"{user_message}"}
    input = [sys_message, user_message]
    response = client.responses.parse(
        model=model,
        input=input,
        text_format=CurriculumSession
    )
    response_output = response.output_parsed
    return response_output


# Display

### Header Section
st.title("🧹 YouTube Transcript Cleaner")
st.caption("Paste raw transcript from YouTube and clean it by removing timestamps.")
st.divider()

### Input Section
st.subheader("Provide Inputs")
week = st.number_input(label="Enter Week Number", min_value=1, max_value=25)
session = st.number_input(label="Enter Session Number", min_value=1, max_value=45)
title = st.text_input(label="Enter Session Title")
raw_transcript = st.text_area(label="Enter Raw Transcript", height=200)
summary_bullets = st.text_area(label="Enter Summary Bullets", height=200)
btn_submit = st.button(label="Submit")
st.divider()

### Output Section
st.subheader("Output")
if btn_submit:
    if week and session and title and raw_transcript and summary_bullets:
        user_message = get_user_message(transcript=raw_transcript, week=week, session=session, title=title, summary_bullets=summary_bullets)
        response_output = get_response(user_message=user_message)
        st.success("✅ Response provided successfully")
        st.download_button(label="💾 Download Transcript as .txt",data=response_output.model_dump_json(indent=2),file_name="cleaned_transcript.txt",mime="text/plain")
        st.text_area(label="Output", value=response_output, height=400)
        st.json(response_output.model_dump_json(indent=2))

        
    else:
        st.warning("⚠️ Please complete all necessary fields")
