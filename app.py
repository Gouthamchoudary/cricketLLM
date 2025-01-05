import streamlit as st
import requests

import google.generativeai as genai

# Hugging Face API Setup
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/gouthamchoudary/CricketRulesModel"
HUGGING_FACE_HEADERS = {"Authorization": "Bearer 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"}

# Google Generative AI Setup
genai.configure(api_key="AIzaSyBv5IyF5DMovl_T9ryDWLnGFuEhhRrtamc")
google_model = genai.GenerativeModel("gemini-1.5-flash")

# Function to query the Hugging Face Cricket Rules Model
def query_cricket_rules_with_hf(instruction, input_text):
    payload = {
        "inputs": f"Instruction: {instruction}\nInput: {input_text}\nResponse:"
    }
    response = requests.post(HUGGING_FACE_API_URL, headers=HUGGING_FACE_HEADERS, json=payload)
    return response.json()

# Function to generate content with Google Generative AI
def query_cricket_rules_with_google_ai(instruction, input_text):
    prompt = f"Instruction: {instruction}\nInput: {input_text}\nResponse:"
    response = google_model.generate_content(prompt)
    return response.text

# Streamlit App Layout
st.title("Cricket LLM")
st.header("Ask the model about cricket")

# User input for instruction and cricket scenario
instruction = st.text_input("Instruction:", "Explain the rule for a no-ball.")
input_text = st.text_area("Input:", "The bowler steps beyond the crease line.")

# Query button
if st.button("Get Response"):
    if instruction and input_text:
        try:
            # Try querying Hugging Face API first
            response = query_cricket_rules_with_hf(instruction, input_text)
            
            if "error" in response:
                st.error(f"loading:")
                raise Exception("")
            else:
                st.success(f"Response: {response['choices'][0]['text'].strip()}")
        
        except Exception as e:
            # Fallback to Google Generative AI
            google_ai_response = query_cricket_rules_with_google_ai(instruction, input_text)
            st.success(f"Response: {google_ai_response}")
    else:
        st.warning("Please fill out both fields!")

# Sidebar with information about the model
st.sidebar.header("About the Model")
st.sidebar.write("""
This model is fine-tuned on cricket and can answer questions like:
- What is a no-ball in cricket?
- What are the rules for a run out?
- Why RCB is better than CSK ?
- Etc.
""")
