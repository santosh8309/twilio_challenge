import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

from personalize import personalize

# Load environment variables
load_dotenv()

# Configure Google GenerativeAI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Prompt for summarization
prompt = """Welcome, Summarizer! Your task is to distill the essence of a given meeting transcript into a concise summary. Your summary should capture the key points and tasks assigned if any in a json format, within a 250-word limit. Let's dive into the provided transcript and extract the vital details for our audience in a json format."""

summary = None
# Streamlit UI
st.title("Get Personalized tasks extracted, sent to you, from your meeting room!")


# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    # This function will be called when the button is clicked

    if transcript_text:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        # Display summary
        st.markdown("## Detailed Notes:")
        # st.write(response.text)
        personalize(response.text)
        return response.text
    else:
        return ""


# Create a text input box
meeting_transcript = st.text_area(
    "Enter the meeting transcript",
    placeholder="Copy and paste your meeting transcripts",
)

# Create a button
if st.button("Get Detailed Tasks", type="primary"):
    generate_gemini_content(meeting_transcript, prompt)
