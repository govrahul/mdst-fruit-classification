import requests
import os
from dotenv import load_dotenv
import pandas as pd
# Load environment variables from .env file
load_dotenv()

import predict_fruit
 
# TODO: Ensure your EDMAMAM_APP_ID AND EDAMAM_APP_KEY are properly defined
app_id = os.getenv('EDAMAM_APP_ID')
app_key = os.getenv('EDAMAM_APP_KEY')

def analyze_ingredient(ingredient):
    # Edamam API endpoint for ingredient analysis

    api_url = "https://api.edamam.com/api/nutrition-data"
    
    # Parameters for the GET request
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'ingr': ingredient
    }
    
    # Make the GET request
    response = requests.get(api_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if not data.get('totalNutrients'):
            print(f"Failed to analyze ingredient: {ingredient}")
            return None
        return data
    else:
        print(f"Failed to analyze ingredient: {response.status_code}")
        return None


def get_prediction(image_path):
    
    # TODO: Set the url to the url you used in predict_fruit.py
    url = "http://127.0.0.1:8000/predict"
    with open(image_path, 'rb') as img:
        files = {'image': (os.path.basename(image_path), img, 'image/jpeg')}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result['fruit']
    else:
        print(f"Failed to get prediction: {response.status_code}")
        return None

# Example usage
#** REPLACE INGREDIENT WITH PREDICTED LABEL/MAKE SURE TO INCLUDE QUANTITY + RIGHT FORMAT **

# Replace with the path to your test image
image_path = "backend/apple.jpg"

#TODO: Call the get_prediction function from above
predicted_fruit = get_prediction(image_path)

ingredient_info = analyze_ingredient(predicted_fruit + " 1")

# Extract total nutrients into a DataFrame
if ingredient_info:

    nutrients = ingredient_info.get('totalNutrients', {})
    nutrients_data = {
        nutrient: {
            'label': details['label'],
            'quantity': details['quantity'],
            'unit': details['unit']
        }
        for nutrient, details in nutrients.items()
    }

    # TODO: Convert to DataFrame (Hint: use pd.DataFrame.from_dict)
    nutrients_data = pd.DataFrame.from_dict(nutrients_data)

    # TODO: Display the DataFrame
    print(nutrients_data)