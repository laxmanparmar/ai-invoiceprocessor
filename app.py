from dotenv import load_dotenv

load_dotenv()

import streamlit as st;
import os;
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to load Gemini Pro Vision
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize streamlit app
st.set_page_config(page_title="Invoice Extractor")

st.header("Invoice Extractor")
input=st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose invoice image...", type=["jpg", "jpeg", "png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload a invoice image and you will have to answer any question based on the uploaded invoice image
"""

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt, image_data, input)
    st.subheader("Response is")
    st.write(response)
