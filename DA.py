import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()  # Load environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_code):
    model = genai.GenerativeModel(r'gemini-pro'.replace("'", "\\'"))
    response = model.generate_content(input_code)

    if response and response.candidates:
        if response.candidates[0].content:
            content_parts = response.candidates[0].content.parts
            if content_parts:
                text_parts = [part.text.replace('"', '\\"') for part in content_parts if part.text]
                return " ".join(text_parts)

            else:
                st.warning("No text parts found in Gemini Pro response.")
        else:
            st.warning("Missing content in Gemini Pro response.")
    else:
        st.warning("Invalid response structure from Gemini Pro.")

    return ""


# Streamlit app
st.title("Data Analysis Tool with Gemini Pro")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type="csv", help="Please upload a CSV file")

if uploaded_file is not None:
    # Check if the file is empty before attempting to read it
    if uploaded_file.size == 0:
        st.warning("The uploaded file is empty. Please upload a file with data.")
    else:
        # Load data
        try:
            df = pd.read_csv(uploaded_file)

            # Display basic information about the loaded data
            st.write("### Data Overview")
            st.write(df.head())
        except pd.errors.EmptyDataError:
            st.warning("The uploaded file does not contain any data.")

    # User prompt input
    analysis_prompt = st.text_area("Enter your analysis prompt")

    # Button to trigger analysis
    submit_analysis = st.button("Submit Analysis")

    if submit_analysis:
        # Get Gemini Pro response for custom analysis code
        analysis_code = get_gemini_response(analysis_prompt)

        # Display generated analysis code
        st.write("### Generated Analysis Code")
        st.code(analysis_code, language="python")

        # Print the generated code for debugging
        print("Generated Analysis Code:")
        print(analysis_code)

        # Execute the generated analysis code line by line
        try:
            exec(analysis_code, globals())
        except Exception as e:
            st.error(f"Error during execution: {e}")
