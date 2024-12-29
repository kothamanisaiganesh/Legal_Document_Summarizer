# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 10:48:58 2024

@author: CMP
"""
from googletrans import Translator
import streamlit as st
import subprocess

from random import randint
import numpy as np
import pickle
import streamlit as st
import base64
import streamlit as st

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:background/background.avif;base64,%s");
    background-position: center;
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown('<style>h1 { color: White ; }</style>', unsafe_allow_html=True)

    st.markdown('<style>p { color: Black; }</style>', unsafe_allow_html=True)
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('background/1111.jpg')
import streamlit as st
from googletrans import Translator

def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text


# Set the title
st.markdown("<h1 style='color: black;'>Summary Translator</h1>", unsafe_allow_html=True)


text_to_translate = st.text_input("Enter text to translate", "Legal Document")

target_language = st.selectbox("Select Target Language", ("english", "hindi", "telugu", "tamil", "kannada","urdu","marathi","malayalam"))



# Custom CSS for the button
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: white;
        color: black;
        border: 2px solid black;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Button to trigger translation
if st.button("Translate"):
    translation = translate_text(text_to_translate, target_language)
    st.write(f"{target_language.capitalize()}: {translation}")

