from googletrans import Translator
import streamlit as st
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

text_to_translate = st.text_area('Enter the content for Summary ', height=400)


Tamil_translation = translate_text(text_to_translate, "ta")
print("Tamil :", Tamil_translation)

# Translate to English
english_translation = translate_text(text_to_translate, "en")
print("English:", english_translation)

# Translate to Hindi
hindi_translation = translate_text(text_to_translate, "hi")
print("Hindi:", hindi_translation)

# Translate to Telugu
telugu_translation = translate_text(text_to_translate, "te")
print("Telugu:", telugu_translation)

# Translate to Telugu
telugu_translation = translate_text(text_to_translate, "te")
print("Telugu:", telugu_translation)

malayalam_translation = translate_text(text_to_translate, "ml")
print("malayalam :", malayalam_translation)