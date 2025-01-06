import streamlit as st
import requests

import google.generativeai as genai

# Hugging Face API Setup
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gouthamchoudary/CricketRulesModel"
HUGGING_FACE_HEADERS = {"Authorization": "Bearer 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"}

# Google Generative AI Setup
genai.configure(api_key="AIzaSyBv5IyF5DMovl_T9ryDWLnGFuEhhRrtamc")
google_model = genai.GenerativeModel("gemini-1.5-flash")

# Function to query the Hugging Face Cricket Rulesss Model
def query_cricket_rules_with_hf(input_text):
    payload = {
        "inputs": f"Input: {input_text}\nResponse:"
    }
    response = requests.post(HUGGING_FACE_API_URL, headers=HUGGING_FACE_HEADERS, json=payload)
    return response.json()

# Function to generate content with Google Generative AI
def query_cricket_rules_with_google_ai(input_text):
    # Prompt to let Google decide if input is sports-related
    prompt = (
    f"Analyze the following input and decide if it is related to sports, particularly cricket: {input_text}\n"
    "If the input is related to cricket or sports:\n"
    "- Include an explanation to enhance understanding of the topic clearly.\n"
    "If the input is not related to sports, respond with:\n"
    "\"Stick to sports, folks. I'm not your personal encyclopedia for random trivia. "
    "Got a sports question? Fire away. Otherwise, move along.\""
)

    response = google_model.generate_content(prompt)
    return response.text

# Streamlit App Layout
st.title("Cricket LLM")
st.header("Ask the model about cricket")

# User input for cricket scenario
input_text = st.text_area("Input:", "The bowler steps beyond the crease line.")

# Query button
if st.button("Get Response"):
    if input_text:
        try:
            # Try querying Hugging Face API first
            response = query_cricket_rules_with_hf(input_text)
            if "error" in response:
                raise Exception("loading...")
            else:
                st.success(f"Response: {response['choices'][0]['text'].strip()}")
        except Exception:
            # Fallback to Google Generative AI
            google_ai_response = query_cricket_rules_with_google_ai(input_text)
            st.success(f"Response: {google_ai_response}")
    else:
        st.warning("Please fill out the input field!")

# Sidebar with information about the model
st.sidebar.header("About the Model")
st.sidebar.write("""
This model is fine-tuned on cricket and can answer questions like:
- What is a no-ball in cricket?
- What are the rules for a run out?
- Why RCB is the best team in ipl?
- Etc.
""")
