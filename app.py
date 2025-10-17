import streamlit as st
from google import genai 
from dotenv import load_dotenv
import os
from google.genai import types
import pathlib
import httpx
from PIL import Image
from io import BytesIO

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key = GEMINI_API_KEY)

st.title("AI Multitool with Gemini")
tab1, tab2, tab3 = st.tabs(["🖼️ Image Generator", "📄 PDF Summarizer", "🎥 YouTube Summarizer"])

with tab1:


    st.title('AI Image Generator')
    user_prompt = st.text_input('What do you want to Generatre Image for ?')

    if st.button('Generate Image'):
        if not user_prompt :
            st.warning('Please Enter the prompt!')
        else:
            with st.spinner("Generating image..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-image",
                        contents=[user_prompt],
                    )

                    st.subheader('Generated Image')

                    for part in response.candidates[0].content.parts:
                        if part.text is not None:
                            st.write(part.text)
                        elif part.inline_data is not None:
                            image = Image.open(BytesIO(part.inline_data.data))
                            st.image(image, caption="Generated Image")
                except Exception as e:
                    st.error(f"Error in generating Image: {e}")

with tab2:
    st.title('PDF Summarizer')

    uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_pdf is not None:
        pdf_bytes = uploaded_pdf.read()
        col1, col2 = st.columns(2)

        prompt="Summarize this document."
        prompt2="इस दस्तावेज़ का सारांश हिंदी में दें।" 

        with col1:
            if st.button('Summarize in English'):
                with st.spinner("Generating ...", show_time=True):
                    try:
                        response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Part.from_bytes(
                                data=pdf_bytes,
                                mime_type='application/pdf',
                            ),
                            prompt]
                        )
                        st.subheader('Document  summary')
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error in generating summary: {e}")

        with col2:
            if st.button('Summarize in Hindi'):
                with st.spinner("Generating ...", show_time=True):
                    try:
                        response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Part.from_bytes(
                                data=pdf_bytes,
                                mime_type='application/pdf',
                            ),
                            prompt2]
                        )
                        st.subheader('दस्तावेज़ सारांश (Hindi)')
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error in generating summary: {e}")

    else:
        st.info("Please upload a PDF file to summarize.")


with tab3:
    st.title("Youtube Video Summarizer")

    youtube_url = st.text_input('Paste the Youtube link here') 

    if st.button('Generate Text'):
        if not youtube_url:
            st.warning("No Youtube URL Present!")
        else:
            try:
                with st.spinner("Generating ...", show_time=True):
                    response = client.models.generate_content(
                        model='models/gemini-2.5-flash',
                        contents=types.Content(
                            parts=[
                                types.Part(
                                    file_data=types.FileData(file_uri=youtube_url)
                                ),
                                types.Part(text='Please summarize the video in 3 sentences.')
                            ]
                        )
                    )
                    st.subheader('Video summary')
                    st.write(response.text)
            except Exception as e:
                st.error("Error in generating summary") 


st.markdown("---")
st.caption("Built using Streamlit and Google Gemini API by Dhruv")
