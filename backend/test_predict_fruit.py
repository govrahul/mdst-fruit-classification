import requests
import os
from PIL import Image
import io

# Define the URL of the Flask endpoint
url = "http://127.0.0.1:8000/predict"

def test_valid_image():
    # Test with a valid fruit image
    image_path = "backend/apple.jpg"  # You'll need to create this directory and add test images
    
    with open(image_path, 'rb') as img:
        files = {'image': ('apple.jpg', img, 'image/jpeg')}
        response = requests.post(url, files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Check if response contains expected fields
    result = response.json()
    assert 'fruit' in result
    assert 'confidence' in result
    assert 'class_id' in result

def test_invalid_image():
    # Test with invalid image data
    files = {'image': ('test.jpg', b'invalid data', 'image/jpeg')}
    response = requests.post(url, files=files)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 400

def test_no_image():
    # Test without sending any image
    response = requests.post(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 400
    assert response.json()['error'] == 'No image provided'

if __name__ == "__main__":
    print("Testing valid image upload...")
    test_valid_image()
    
    print("\nTesting invalid image data...")
    test_invalid_image()
    
    print("\nTesting no image...")
    test_no_image()