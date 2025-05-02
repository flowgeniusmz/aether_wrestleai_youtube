import streamlit as st
import base64


def set_background():
    path = st.secrets.app.icon
    style = '<style>.stApp {{background: url("data:image/png;base64,{0}"), rgba(255, 255, 255, 0.5); background-size: cover; background-blend-mode: lighten; background-position: center; background-repeat: no-repeat;}}</style>'
    with open(file=path, mode="rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
        background = style.format(encoded_string)
        st.markdown(body=background, unsafe_allow_html=True)