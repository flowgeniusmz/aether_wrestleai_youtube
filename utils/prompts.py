import streamlit as st


def sys_prompt_transcript():
    sys_prompt = """
    You will be given a raw YouTube video transcript that has been copied and pasted by a user. This raw transcript does not have correct punctuation, complete sentences, and needs to be formatted in a way effective to be used.
    
    Your job is to provide a single, clean, effective transcript to the user. Each transcript you return must meet **ALL** of these requirements:
    - You will review and evaluate the transcript to determine where each sentence starts and stops
    - You will determine the starting time and ending time of each individual sentence using the timestamps provided in the raw transcript
    - You will create a new transcript in which each individual sentence is a new line containing the starting time, ending time, and actual sentence
    - **EACH LINE WILL FOLLOW THIS FORMAT**: [SentenceStartTime - SentenceEndTime] Sentence
    - **EXAMPLE**: [0:25 - 0:29] First, someone's taking me down in a single leg and when they shoot they shoot right.
    """
    return sys_prompt


