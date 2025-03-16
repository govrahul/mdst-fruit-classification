from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import ast
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if image is provided
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Read and decode image
    file = request.files['image']
    image_bytes = file.read()
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({'error': 'Could not read the image file'}), 400

    # Preprocess image
    resize = tf.image.resize(img, (100, 100))
    resize_rgb = tf.reverse(resize, axis=[-1])  # Convert BGR to RGB
    normalized_image = resize_rgb/255.0
    
    # Load model
    try:
        model = tf.keras.models.load_model('model/fruitclassifier.keras')
    except Exception as e:
        print(f"Error loading model: {e}")
        return jsonify({'error': 'Model loading failed'}), 500

    # Make prediction
    try:
        yhat = model.predict(np.expand_dims(normalized_image, 0))
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500
    
    # Get top 5 predictions
    top_indices = np.argsort(yhat[0])[-5:][::-1]
    top_probabilities = yhat[0][top_indices]
    
    # Load fruits dictionary
    with open("Backend/directories.txt", 'r') as file:
        content = file.read()
        fruits_dict = ast.literal_eval(content)
    
    # Return prediction
    for pred_class, confidence in zip(top_indices, top_probabilities):
        pred_class = int(pred_class)
        if pred_class in fruits_dict:
            whole_fruit = fruits_dict[pred_class]
            fruit = whole_fruit.split()[0]
            return jsonify({
                'fruit': fruit,
                'confidence': float(confidence),
                'class_id': pred_class
            })
    
    return jsonify({
        'error': 'Could not classify image with confidence',
        'attempted_classes': [int(i) for i in top_indices],
        'probabilities': [float(p) for p in top_probabilities],
        'available_classes': list(fruits_dict.keys())
    }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)