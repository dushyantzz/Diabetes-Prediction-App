import requests
import base64
import json
import streamlit as st
from PIL import Image
import io

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyAk_8fBZ0Mcmp3LnBtgjd-UtF3_ibhSrZo"
GEMINI_VISION_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"

def encode_image(image):
    """Convert PIL Image to base64 encoded string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def analyze_food_image(image):
    """
    Analyze a food image using Google Gemini Vision API
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: Contains food_name, confidence, and additional_info
    """
    try:
        # Encode image to base64
        base64_image = encode_image(image)
        
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        # Create the prompt for food identification
        prompt = """
        Analyze this image and identify the food item shown.
        
        Please provide the following information in JSON format:
        1. The name of the food (be specific)
        2. Confidence level (high, medium, or low)
        3. Whether it's a single food item or a meal with multiple components
        4. If it's a meal, list the main components
        
        Format your response as valid JSON with these keys:
        {
            "food_name": "specific food name",
            "confidence": "high/medium/low",
            "is_meal": true/false,
            "components": ["component1", "component2"] (if applicable)
        }
        
        Only respond with the JSON, nothing else.
        """
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 4096
            }
        }
        
        # Make the API request
        response = requests.post(
            GEMINI_VISION_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Process the response
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract the text response
            text_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
            
            # Try to parse the JSON from the response
            try:
                # Find JSON in the response (in case there's additional text)
                json_start = text_response.find('{')
                json_end = text_response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = text_response[json_start:json_end]
                    food_data = json.loads(json_str)
                else:
                    # If no JSON found, create a basic response
                    food_data = {
                        "food_name": text_response.strip(),
                        "confidence": "medium",
                        "is_meal": False,
                        "components": []
                    }
                
                return food_data
            except json.JSONDecodeError:
                # If JSON parsing fails, extract the food name from text
                return {
                    "food_name": text_response.strip(),
                    "confidence": "medium",
                    "is_meal": False,
                    "components": []
                }
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return {
                "food_name": "unknown",
                "confidence": "low",
                "is_meal": False,
                "components": []
            }
            
    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        return {
            "food_name": "error",
            "confidence": "low",
            "is_meal": False,
            "components": []
        }

def find_closest_food(food_name, food_database):
    """
    Find the closest matching food in our database
    
    Args:
        food_name: Name of the food identified by the API
        food_database: Dictionary of food items and their nutritional info
        
    Returns:
        tuple: (food_key, similarity_score)
    """
    # Convert to lowercase for comparison
    food_name_lower = food_name.lower()
    
    # First try direct match
    if food_name_lower in food_database:
        return food_name_lower, 1.0
    
    # Check if any database key is contained in the food name
    for key in food_database.keys():
        if key in food_name_lower:
            return key, 0.9
        if food_name_lower in key:
            return key, 0.8
    
    # Simple word matching for basic similarity
    best_match = None
    best_score = 0
    
    for key in food_database.keys():
        # Split both strings into words
        key_words = set(key.split())
        food_words = set(food_name_lower.split())
        
        # Calculate intersection
        common_words = key_words.intersection(food_words)
        
        # Calculate simple similarity score
        if len(key_words) > 0 and len(food_words) > 0:
            score = len(common_words) / max(len(key_words), len(food_words))
            
            if score > best_score:
                best_score = score
                best_match = key
    
    # If we found a match with some similarity
    if best_match and best_score > 0.3:
        return best_match, best_score
    
    # Default to a generic food category if available
    for generic in ['salad', 'pasta', 'rice', 'bread', 'chicken', 'fish', 'meat', 'fruit', 'vegetable']:
        if generic in food_database:
            return generic, 0.5
    
    # If all else fails, return the first item in the database
    return list(food_database.keys())[0], 0.1
