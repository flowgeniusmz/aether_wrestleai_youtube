import streamlit as st
from utils.background import set_background

# 0. Set Page Config
page_title = st.secrets.app.title
page_icon = st.secrets.app.icon
layout = st.secrets.app.layout
initial_sidebar_state = st.secrets.app.sidebar
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout, initial_sidebar_state=initial_sidebar_state)

# 1. Set Background
#set_background()

# 2. Set Logo
image = page_icon
icon_image = page_icon
size = "large"
link = st.secrets.app.link
logo = st.logo(image=image, size=size, icon_image=icon_image, link=link)

# 3. Set Pages
page_home = st.Page(page="app/0_home.py", title="Home", url_path="/home", default=True)
page_transcript = st.Page(page="app/1_transcripts.py", title="Transcripts", url_path="/transcripts")
page_formatter = st.Page(page="app/2_formatter.py", title="Formatter", url_path="/formatter")

pages = [page_home, page_transcript, page_formatter]

# 4. Set Navigation
navigation = st.navigation(pages=pages)

# 5. Run Nav
navigation.run()
