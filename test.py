from dotenv import load_dotenv

load_dotenv()
import json

import streamlit as st;
import os;
from PIL import Image
import google.generativeai as genai
import typing_extensions as typing

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to load Gemini Pro Vision
# model=genai.GenerativeModel('gemini-1.5-flash')

# def get_gemini_response(input, image, prompt):
#     response=model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         # Read file into bytes
#         bytes_data = uploaded_file.getvalue()

#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]

#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# # Initialize streamlit app
# st.set_page_config(page_title="Invoice Extractor")

# st.header("Invoice Extractor")
# input=st.text_input("Input Prompt: ", key="input")
# uploaded_file = st.file_uploader("Choose invoice image...", type=["jpg", "jpeg", "png"])
# image=""

# if uploaded_file is not None:
#     image=Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

# submit = st.button("Tell me about invoice")

# input_prompt = """
# You are an expert in understanding invoices. We will upload a invoice image and you will have to answer any question based on the uploaded invoice image
# """
class Recipe(typing.TypedDict):
    upside: str
    target: str
    summary: str
    full_text_raw: str


model = genai.GenerativeModel("gemini-1.5-pro",  generation_config={"response_mime_type": "application/json",
                                                 "response_schema": list[Recipe]})
sample_pdf = genai.upload_file("test.pdf")
raw_response = model.generate_content(["Summarize the entire pdf in bullet points, summary should consist of target price, upside potential and other details. If there is no target or upsidePotential then use null value.", sample_pdf])
# response = model.generate_content(["From given pdf of stock recommendation, create attractive tweet using data from pdf, tweet can be more than 280 characters", sample_pdf])

response = json.loads(raw_response.text)
print(response)

print(json.dumps(response, indent=4))
