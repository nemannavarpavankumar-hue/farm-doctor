import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(page_title="Plant Doctor AI", page_icon="🌿")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    model = MobileNetV2(weights='imagenet')
    return model

model = load_model()

# --- CLASS NAMES (Common Plant Diseases) ---
class_names = [
    'Apple - Scab', 'Apple - Black Rot', 'Apple - Cedar Rust',
    'Cherry - Powdery Mildew', 'Corn - Cercospora', 'Corn - Common Rust',
    'Grape - Black Rot', 'Orange - Citrus Greening', 'Peach - Bacterial Spot',
    'Pepper - Bacterial Spot', 'Potato - Early Blight', 'Potato - Late Blight',
    'Strawberry - Leaf Scorch', 'Tomato - Bacterial Spot', 'Tomato - Early Blight',
    'Tomato - Late Blight', 'Tomato - Leaf Mold', 'Tomato - Septoria Leaf Spot',
    'Tomato - Spider Mites', 'Tomato - Target Spot', 'Tomato - Mosaic Virus',
    'Tomato - Yellow Leaf Curl Virus', 'Healthy Leaf'
]

# --- APP UI ---
st.title("🌿 Plant Disease Detector")
st.write("Upload a leaf image to detect potential diseases.")

uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Leaf', use_container_width=True)
    st.write("🔍 Analyzing...")
    img = image.resize((224, 224))
    img_array = img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = preprocess_input(img_array)
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    top_class_index = np.argmax(score)
    result = class_names[top_class_index] if top_class_index < len(class_names) else "Unknown"
    confidence = 100 * np.max(score)
    st.subheader("📋 Diagnosis Result:")
    if "Healthy" in result:
        st.success(f"✅ {result}")
    else:
        st.error(f"⚠️ {result}")
    st.info(f"Confidence: {confidence:.2f}%")
    st.warning("Disclaimer: This is a demo using AI. For accurate diagnosis, consult an agricultural expert.")