import streamlit as st
from utils.styling import get_containerstyle

st.title("Welcome to AetherAI")
st.caption("AetherAI brings revolutionary technology to the sport of Wrestling. Use the left navigation to explore the features.")
st.divider()
container = get_containerstyle(border=False)
with container:
    st.image(image=st.secrets.app.icon)
