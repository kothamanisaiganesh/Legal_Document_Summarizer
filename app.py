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
set_background('background/8.jpg')
# Streamlit app title
st.title("Legal Document Summarization")

# Create a dropdown menu for options
options = ['None','Legal Document', 'Translate']

selected_option = st.selectbox('Select an option', options)

if selected_option == 'None':
    # Code for the Translate feature
    st.title('Welcome to Legal Document Page ')

elif selected_option == 'Legal Document':
    # Code for the Legal Document feature
    st.title('Legal Document')
    subprocess.run(["streamlit", "run", "app1.py"]) 

#elif selected_option == 'Doubt':
    # Code for the Doubt feature
#    st.title('Doubt Clarification')
#    st.write('If you have any doubts, please ask.')
#    subprocess.run(["streamlit", "run", "app2.py"]) 

elif selected_option == 'Translate':
    # Code for the Translate feature
    st.title('Translate')
    subprocess.run(["streamlit", "run", "app11.py"]) 


