import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import io
import base64

# Initialize translator
translator = Translator()

# Title of the app
st.title("🌍 Language Translation Tool")

# User input
text = st.text_area("Enter text to translate:")

# Language selection
col1, col2 = st.columns(2)

with col1:
    src_lang = st.selectbox("Source Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"))

with col2:
    dest_lang = st.selectbox("Target Language", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("spanish"))

# Translate button
if st.button("Translate"):
    if text.strip():
        # Get language codes
        src_code = [k for k, v in LANGUAGES.items() if v == src_lang][0]
        dest_code = [k for k, v in LANGUAGES.items() if v == dest_lang][0]

        # Perform translation
        translated = translator.translate(text, src=src_code, dest=dest_code)

        # Display translated text
        st.success("Translated Text:")
        st.write(translated.text)
        
        # Store translated text in session state for TTS
        st.session_state.translated_text = translated.text
        st.session_state.dest_code = dest_code

    else:
        st.warning("Please enter some text to translate.")

# Text-to-Speech button (only show if translation exists)
if 'translated_text' in st.session_state and st.session_state.translated_text:
    if st.button("🔊 Speak Translation"):
        try:
            # Create text-to-speech
            tts = gTTS(text=st.session_state.translated_text, lang=st.session_state.dest_code, slow=False)
            
            # Save to bytes buffer
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Display audio player
            st.audio(audio_bytes, format="audio/mp3")
            st.success("Audio generated successfully! Click play to listen.")
            
        except Exception as e:
            st.error(f"Text-to-speech failed: {str(e)}")
            st.info("Try using a shorter text or check your internet connection.")