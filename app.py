import streamlit as st
import requests

# FastAPI server URL
API_URL = "http://127.0.0.1:8000/translate/"

# Define the list of supported languages (Hindi and Korean)
languages = ["hindi","Korean"]

st.title("🌐Language Translation")

# Input text area and target language dropdown
source_text = st.text_area("Enter text to translate:", height=150)
target_language = st.selectbox("Select target language:", languages)

# Action button to trigger translation
if st.button("Translate"):
    if source_text:
        payload = {"text": source_text, "source_lang": "en_XX", "target_lang": target_language}

        with st.spinner("Translating..."):
            try:
                # Make the HTTP request to the FastAPI server
                response = requests.post(API_URL, json=payload)

                # Check if the response status is OK (200)
                if response.status_code == 200:
                    response_data = response.json()
                    translated_text = response_data.get("translated_text")
                    if translated_text:
                        st.text_area("Translated text:", translated_text, height=150)
                    else:
                        st.warning("Translation failed or result is empty.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Network error: Please try again later. ({e})")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Please enter some text to translate.")


