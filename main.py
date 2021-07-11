
import streamlit as st
from app_pages import AppPage
from pages import introduction, house_prices, face_detection

# Create an instance of the app
app = AppPage()

# Title of the main page
st.title("Objectivity playground")

# Register each page that you want to build.
app.define_page("Introduction", introduction.build_page)
app.define_page("Predicting house prices", house_prices.build_page)
app.define_page("Face detection", face_detection.build_page)


# The main application.
app.build_page()



