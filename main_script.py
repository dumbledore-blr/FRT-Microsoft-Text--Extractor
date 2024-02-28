# Imports
import streamlit as st
from azure_ocr import GetTextRead
from azure_translator import translate_text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set the title of the tab
st.set_page_config(page_title="Extraction Application")

# Custom CSS style
cus_css = """
body {
    background-color: #323232;
    opacity: 0.9;
    background-image:  linear-gradient(30deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(150deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(30deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(150deg, #000000 12%, transparent 12.5%, transparent 87%, #000000 87.5%, #000000), linear-gradient(60deg, #00000077 25%, transparent 25.5%, transparent 75%, #00000077 75%, #00000077), linear-gradient(60deg, #00000077 25%, transparent 25.5%, transparent 75%, #00000077 75%, #00000077);
    background-size: 80px 140px;
    background-position: 0 0, 0 0, 40px 70px, 40px 70px, 0 0, 40px 70px;
}
"""
# Apply custom CSS
st.markdown(f"<style>{cus_css}</style>", unsafe_allow_html=True)

# Streamlit app title and instructions
st.title("Extractor Application")
st.subheader("Upload your files here")

# First field for image upload
uploaded_file = st.file_uploader("OCR & Translator from Azure Cognitive Services", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    # Save the uploaded image to a temporary file
    image_path = "temp_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    # Process the image if available
    if os.path.exists(image_path):
        # Call the OCR function and get the extracted text
        extracted_text = GetTextRead(image_path)

        # Display the extracted text
        if extracted_text:
            st.subheader("Extracted Text:")
            lines = extracted_text.split("\n")
            for line in lines:
                st.write(line)

            # Dictionary mapping language codes to full names
            language_names = {
                "en": "English",
                "fr": "French",
                "zu": "Zulu",
                "es": "Spanish",
                "it": "Italian",
                "ar": "Arabic",
                "hi": "Hindi",
                "ml": "Malayalam",
                "zh-Hans": "Simplified Chinese",
                "de": "German",
                "ja": "Japanese",
                "ko": "Korean",
                "ru": "Russian",
                "pt": "Portuguese",
                "tr": "Turkish",
                "nl": "Dutch",
                "th": "Thai",
                "sv": "Swedish",
                "fi": "Finnish",
                "no": "Norwegian",
                "da": "Danish",
                "pl": "Polish",
                "id": "Indonesian",
                "uk": "Ukrainian",
                "cs": "Czech",
                "el": "Greek",
                "ro": "Romanian",
                "hu": "Hungarian",
                "he": "Hebrew",
                "bn": "Bengali",
                "ta": "Tamil",
                "te": "Telugu",
                "vi": "Vietnamese",
                "mr": "Marathi",
                "ur": "Urdu", 
                "fa": "Persian",
                "af": "Afrikaans",
                "sw": "Swahili",
                "tl": "Tagalog",
                "ne": "Nepali",
                "pa": "Punjabi",
                "gu": "Gujarati",
                "my": "Burmese",
                "sd": "Sindhi",
                "ha": "Hausa",
                "yo": "Yoruba",
                "ig": "Igbo",
                "si": "Sinhala",
                "km": "Khmer",
                "sn": "Shona",
                "so": "Somali",
                "am": "Amharic",
                "jv": "Javanese",
                "rw": "Kinyarwanda",
                "mg": "Malagasy",
                "zu": "Zulu",
            }

            # Third field for language selection
            target_language = st.selectbox("Select target language for translation", list(language_names.values()))

            for code, name in language_names.items():
                if name == target_language:
                    target_language_code = code

            # Translator API Key and Region
            trans_api_key = '46935b2ccfb044e9aeda2e1eeca7ff52'
            trans_api_region = "centralindia"

            with st.spinner("Translating..."):
                translation_response = translate_text(trans_api_key, trans_api_region, extracted_text, [target_language_code])

            if translation_response:
                # Display the translated text
                translated_text = translation_response[0]['translations'][0]['text']
                st.subheader("Translated Text:")
                lines = translated_text.split("\n")
                for line in lines:
                    st.write(line)
            else:
                st.error("Translation failed. Please try again later.")
        else:
            st.error("Text extraction failed.")
