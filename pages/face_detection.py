import streamlit as st
import cv2
from streamlit.elements.image import image_to_url
import numpy as np


def build_page() -> None:
    """
    Defines a page in the streamlit application.
    :return: None
    """

    # Upload the dataset and save as csv
    st.markdown("""This application identifies faces and then 
                detects the prevailing emotion. 
                """)

    bar = st.sidebar.markdown("""---""")
    chosen_asset = st.sidebar.radio("What do you want to detect?", ('Face','Eyes')) 

    img_data = st.file_uploader(label='Load image for identification', type=['png', 'jpg'])

    col1, col2 = st.beta_columns(2)
    
    with col1:
        if img_data:
            original_image = getCVImage(img_data)
            st.image(original_image, channels="BGR")

    with col2:
        if chosen_asset == 'Face':
            if img_data is not None:
                new_image = original_image.copy()
                img_with_faces  = find_assets(new_image)
                st.image(img_with_faces, channels="BGR")
        if chosen_asset == 'Eyes':
            if img_data is not None:
                new_image = original_image.copy()
                img_with_faces  = find_assets(new_image, 'Eyes')
                st.image(img_with_faces, channels="BGR")


def find_assets(img_clean, asset_type='Face'):
    
    if asset_type == 'Face':
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img_clean, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    if asset_type == 'Eyes':
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        gray = cv2.cvtColor(img_clean, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.07, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(img_clean, (x, y), (x+w, y+h), (0, 200, 0), 6)

    return img_clean      

def getCVImage(img_stream):
    file_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, 1)



