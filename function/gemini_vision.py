import requests
import base64
import json
import streamlit as st
from PIL import Image
import io

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyAk_8fBZ0Mcmp3LnBtgjd-UtF3_ibhSrZo"
GEMINI_VISION_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def encode_image(image):
    """Convert PIL Image to base64 encoded string"""
    try:
        # Convert RGBA images to RGB to avoid JPEG encoding issues
        if image.mode == 'RGBA':
            # Create a white background image
            background = Image.new('RGB', image.size, (255, 255, 255))
            # Paste the image on the background
            background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
            image = background
        elif image.mode != 'RGB':
            # Convert any other mode to RGB
            image = image.convert('RGB')

        # Save as JPEG
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    except Exception as e:
        # If there's any error in image processing, log it and raise
        st.error(f"Error processing image: {str(e)}")
        # Create a simple solid color image as fallback
        fallback_img = Image.new('RGB', (224, 224), (200, 200, 200))
        buffered = io.BytesIO()
        fallback_img.save(buffered, format="JPEG")
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
        You are a food recognition AI specialized in identifying food items for diabetes management. Your task is to analyze food images with high accuracy.

        IMPORTANT: Examine the image carefully and identify the exact food item(s) shown.

        Please provide the following information in JSON format:
        1. The name of the food (be very specific, e.g., "chocolate brownie" not just "dessert")
        2. Confidence level (high, medium, or low) based on how clearly you can identify the food
        3. Whether it's a single food item or a meal with multiple components
        4. If it's a meal, list all visible main components
        5. Estimate the primary carbohydrate content (high, medium, low) if possible

        Format your response ONLY as valid JSON with these keys:
        {
            "food_name": "specific food name",
            "confidence": "high/medium/low",
            "is_meal": true/false,
            "components": ["component1", "component2"],
            "carb_content": "high/medium/low"
        }

        CRITICAL: Only respond with the JSON object, nothing else. No explanations, no markdown formatting.
        This is for a diabetes management application where accurate food identification is essential for health monitoring.
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
            try:
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
                            "components": [],
                            "carb_content": "medium"
                        }

                    return food_data
                except json.JSONDecodeError:
                    # If JSON parsing fails, extract the food name from text
                    return {
                        "food_name": text_response.strip(),
                        "confidence": "medium",
                        "is_meal": False,
                        "components": [],
                        "carb_content": "medium"
                    }
            except (KeyError, IndexError) as e:
                st.error(f"Error parsing API response: {str(e)}")
                st.info("API Response: " + str(response_data)[:200] + "...")
                return {
                    "food_name": "parsing error",
                    "confidence": "low",
                    "is_meal": False,
                    "components": [],
                    "carb_content": "medium"
                }
        elif response.status_code == 404:
            error_msg = "API Error: Model not found or deprecated. Using gemini-1.5-flash model."
            st.error(error_msg)
            st.info("Response: " + response.text[:200])
            return {
                "food_name": "API error - model not found",
                "confidence": "low",
                "is_meal": False,
                "components": [],
                "carb_content": "medium"
            }
        else:
            st.error(f"API Error: {response.status_code} - {response.text[:200]}")
            return {
                "food_name": "unknown",
                "confidence": "low",
                "is_meal": False,
                "components": [],
                "carb_content": "medium"
            }

    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        return {
            "food_name": "error",
            "confidence": "low",
            "is_meal": False,
            "components": [],
            "carb_content": "medium"
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
    food_name_lower = food_name.lower().strip()

    # Handle plurals by removing trailing 's' if present
    singular_food_name = food_name_lower[:-1] if food_name_lower.endswith('s') else food_name_lower

    # First try direct match
    if food_name_lower in food_database:
        return food_name_lower, 1.0

    # Try singular form if the original was plural
    if singular_food_name in food_database and singular_food_name != food_name_lower:
        return singular_food_name, 0.95

    # Check for exact word matches (to handle compound names like "vegetable salad")
    for key in food_database.keys():
        # If the food name contains the exact database key as a whole word
        if f" {key} " in f" {food_name_lower} " or food_name_lower == key:
            return key, 0.9
        # If the singular form contains the exact database key
        if f" {key} " in f" {singular_food_name} " or singular_food_name == key:
            return key, 0.85

    # Check if any database key is contained in the food name
    for key in food_database.keys():
        if key in food_name_lower:
            return key, 0.8
        if food_name_lower in key:
            return key, 0.7

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
