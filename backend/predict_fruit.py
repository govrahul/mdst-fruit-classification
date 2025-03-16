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
    """
    TODO: Implement a fruit classification endpoint that:
    1. Accepts an image file
    2. Preprocesses the image
    3. Makes a prediction using the model
    4. Returns the predicted fruit with confidence score
    """
    
    # TODO: Check if image is provided in the request
    # Return error if no image is found

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # TODO: Read and decode the image
    # Hint: Use request.files, cv2.imdecode
    image = request.files['image']
    image_bytes = image.read()
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "No image provided"}), 400

    # TODO: Preprocess the image
    # 1. Resize to 100x100
    # 2. Convert BGR to RGB
    # 3. Normalize pixel values to [0,1]
    resize = tf.image.resize(image, (100, 100))
    resize_rgb = tf.reverse(resize, axis=[-1])
    resize_rgb = resize_rgb / 255.0
    
    # TODO: Load the model
    # Hint: Use try-except for error handling
    try:
        model = tf.keras.models.load_model('backend/fruitclassifier.keras')
    except:
        return jsonify({"message": "no model found", "status_code": 501}), 501
    
    # TODO: Make prediction
    # Hint: Use model.predict() and handle exceptions
    try:
        predictions = model.predict(np.expand_dims(resize_rgb, 0))
    except:
        return jsonify({"message": "prediction not made", "status_code": 502}), 502

    # TODO: Get top 5 predictions
    # Hint: Use np.argsort()
    indices = np.argsort(predictions[0])[-5:][::-1]
    top = predictions[0][indices]
    
    # TODO: Load fruits dictionary from 'Backend/directories.txt'
    # Hint: Use ast.literal_eval()
    with open("backend/directories.txt", 'r') as file:
        content = file.read()
        fruits_dict = ast.literal_eval(content)
    
    # TODO: Return prediction
    # Format: {
    #   'fruit': fruit_name,
    #   'confidence': confidence_score,
    #   'class_id': class_id
    # }

    for pred_class, confidence in zip(indices, top):
        pred_class = int(pred_class)
        if pred_class in fruits_dict:
            whole_fruit = fruits_dict[pred_class]
            fruit = whole_fruit.split()[0]
            j = jsonify({
                'fruit': fruit,
                'confidence': float(confidence),
                'class_id': pred_class
            }), 200
            print(j)
            return j
    
    return jsonify({
        'error': 'Could not classify image with confidence',
        'attempted_classes': [int(i) for i in indices],
        'probabilities': [float(p) for p in top],
        'available_classes': list(fruits_dict.keys())
    }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


