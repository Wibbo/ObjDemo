import streamlit as st
from app_pages import AppPage
from pages import introduction, retail_sales

# Create an instance of the app
st.set_page_config(layout="wide")
app = AppPage()

# Title of the main page
st.title("Objectivity playground")

# Register each page that you want to build.
app.define_page("Introduction", introduction.build_page)
app.define_page("Retail sales", retail_sales.build_page)

# The main application.
app.build_page()



