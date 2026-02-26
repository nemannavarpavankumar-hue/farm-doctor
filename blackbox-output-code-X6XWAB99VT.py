import os
import random
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

treatment_db = {
    "Tomato___Late_Blight": {
        "disease": "Late Blight",
        "pesticide": "Mancozeb or Copper Fungicide",
        "instruction": "Apply immediately. Remove infected leaves. Do not spray if rain is expected."
    },
    "Tomato___Healthy": {
        "disease": "Healthy",
        "pesticide": "None",
        "instruction": "Plant looks good! Keep monitoring."
    },
    "Potato___Early_Blight": {
        "disease": "Early Blight",
        "pesticide": "Chlorothalonil",
        "instruction": "Apply every 7-10 days. Ensure good air circulation."
    },
    "Apple___Black_Rot": {
        "disease": "Black Rot",
        "pesticide": "Myclobutanil",
        "instruction": "Prune infected branches. Apply fungicide in early spring."
    },
    "Grape___Leaf_Blight": {
        "disease": "Leaf Blight",
        "pesticide": "Bordeaux Mixture",
        "instruction": "Remove leaf debris. Spray on dry days."
    },
    "Corn___Common_Rust": {
        "disease": "Common Rust",
        "pesticide": "Mancozeb or Chlorothalonil",
        "instruction": "Apply fungicide when humidity is high."
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Simulating AI (Random Selection for Demo)
        keys = list(treatment_db.keys())
        simulated_prediction_key = random.choice(keys)
        result = treatment_db[simulated_prediction_key]

        return jsonify({
            'disease': result['disease'],
            'pesticide': result['pesticide'],
            'instruction': result['instruction'],
            'image_url': filepath
        })

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)