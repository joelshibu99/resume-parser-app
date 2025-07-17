import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
import os
import time
import re
import json
import streamlit as st

# Load key (from .env or Streamlit secrets)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ Gemini API Key not found! Please set it in .env or Streamlit secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.0-flash"

def parse_resume_with_gemini(text, retries=3, delay=30, model_name=MODEL_NAME):
    prompt = f"""
    Extract the following details from this resume in clean JSON format:
    - Full Name
    - Email
    - Phone
    - Skills
    - Education
    - Experience

    Resume:
    {text}
    """

    gen_model = genai.GenerativeModel(model_name)

    for attempt in range(1, retries + 1):
        try:
            response = gen_model.generate_content(prompt)
            result_text = response.text.strip()

            # Clean markdown-style code block
            cleaned = re.sub(r"```json|```", "", result_text).strip()
            return json.loads(cleaned)

        except ResourceExhausted:
            time.sleep(delay)
        except json.JSONDecodeError:
            return {"error": "Gemini returned invalid JSON. Try rephrasing or cleaning the resume."}
        except Exception as e:
            return {"error": f"Unexpected error occurred: {str(e)}"}

    return {"error": "Quota exceeded or unknown error occurred."}
