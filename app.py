import streamlit as st
import numpy as np
import cv2
from PIL import Image
from colorize_image import colorize_image

st.title("🎨 Image Colorizer with OpenCV + Streamlit")
uploaded_file = st.file_uploader("Upload a grayscale image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = np.array(Image.open(uploaded_file).convert("RGB"))
    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("Colorize"):
        result = colorize_image(image)
        st.image(result, caption="Colorized Image", use_container_width=True)
from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running in the main thread!"

# ✅ This ensures Flask runs only when this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

import os
print("Current working directory:", os.getcwd())






