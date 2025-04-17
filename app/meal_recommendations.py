import streamlit as st
import pandas as pd
import json
import datetime
import requests
import base64
from PIL import Image
import io
import time
import random

# Gemini API configuration - using the same key as food recognition
from function.gemini_vision import GEMINI_API_KEY

# Gemini API URL for text generation
GEMINI_TEXT_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def get_meal_recommendations(user_data, preferences):
    """
    Get personalized meal recommendations using Google Gemini API
    
    Args:
        user_data: Dictionary containing user health data
        preferences: Dictionary containing user food preferences
        
    Returns:
        dict: Contains meal recommendations and alternatives
    """
    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        # Create the prompt for meal recommendations
        prompt = f"""
        You are a diabetes nutrition specialist AI. Create personalized meal recommendations for a user with the following health profile and preferences:
        
        HEALTH PROFILE:
        - Diabetes Risk: {user_data.get('diabetes_risk', 'Unknown')}
        - Blood Glucose Level: {user_data.get('glucose', 'Unknown')} mg/dL
        - BMI: {user_data.get('bmi', 'Unknown')}
        - Age: {user_data.get('age', 'Unknown')}
        - Insulin Level: {user_data.get('insulin', 'Unknown')}
        
        USER PREFERENCES:
        - Dietary Restrictions: {preferences.get('dietary_restrictions', 'None')}
        - Cuisine Preferences: {preferences.get('cuisine_preferences', 'Any')}
        - Disliked Foods: {preferences.get('disliked_foods', 'None')}
        - Cooking Skill Level: {preferences.get('cooking_skill', 'Intermediate')}
        - Meal Prep Time: {preferences.get('prep_time', 'Medium')}
        
        Please provide the following in JSON format:
        1. Three meal plans (breakfast, lunch, dinner) with low glycemic index options
        2. For each meal, provide a healthier alternative to a common high-carb dish
        3. Include estimated carbohydrate content and glycemic load for each meal
        4. Add specific tips for managing blood sugar with these meals
        
        Format your response as valid JSON with these keys:
        {{
            "meal_plans": [
                {{
                    "meal_type": "Breakfast/Lunch/Dinner",
                    "name": "meal name",
                    "description": "brief description",
                    "ingredients": ["ingredient1", "ingredient2"],
                    "preparation": "brief preparation steps",
                    "carbs": "estimated carbs in grams",
                    "glycemic_load": "low/medium/high",
                    "diabetes_friendly_tips": "specific tip for this meal"
                }}
            ],
            "alternatives": [
                {{
                    "high_carb_dish": "common high carb dish",
                    "healthy_alternative": "healthier alternative",
                    "benefit": "why it's better for diabetes management"
                }}
            ],
            "general_tips": ["tip1", "tip2", "tip3"]
        }}
        
        IMPORTANT: Ensure all recommendations are evidence-based and appropriate for diabetes management.
        Focus on low glycemic index foods, balanced macronutrients, and portion control.
        Consider the user's specific preferences and restrictions.
        """
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 4096
            }
        }
        
        # Make the API request
        response = requests.post(
            GEMINI_TEXT_URL,
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
                        recommendations = json.loads(json_str)
                    else:
                        # If no JSON found, return an error
                        return {
                            "error": "Could not parse recommendations from API response"
                        }
                    
                    return recommendations
                except json.JSONDecodeError:
                    # If JSON parsing fails, return an error
                    return {
                        "error": "Failed to parse JSON from API response"
                    }
            except (KeyError, IndexError) as e:
                return {
                    "error": f"Error parsing API response: {str(e)}"
                }
        else:
            return {
                "error": f"API Error: {response.status_code} - {response.text[:200]}"
            }
            
    except Exception as e:
        return {
            "error": f"Error generating recommendations: {str(e)}"
        }

def get_feedback_improvement(meal_name, user_feedback):
    """
    Get improved meal recommendations based on user feedback
    
    Args:
        meal_name: Name of the meal to improve
        user_feedback: User's feedback about the meal
        
    Returns:
        dict: Contains improved meal recommendation
    """
    try:
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        # Create the prompt for meal improvement
        prompt = f"""
        You are a diabetes nutrition specialist AI. A user has provided feedback on a meal recommendation.
        Please improve the meal based on their feedback.
        
        ORIGINAL MEAL: {meal_name}
        
        USER FEEDBACK: {user_feedback}
        
        Please provide an improved meal recommendation in JSON format:
        {{
            "improved_meal": {{
                "name": "improved meal name",
                "description": "brief description",
                "ingredients": ["ingredient1", "ingredient2"],
                "preparation": "brief preparation steps",
                "carbs": "estimated carbs in grams",
                "glycemic_load": "low/medium/high",
                "diabetes_friendly_tips": "specific tip for this meal"
            }},
            "explanation": "explanation of how the meal was improved based on feedback"
        }}
        
        IMPORTANT: Ensure all recommendations are evidence-based and appropriate for diabetes management.
        Focus on addressing the specific feedback while maintaining nutritional quality.
        """
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 2048
            }
        }
        
        # Make the API request
        response = requests.post(
            GEMINI_TEXT_URL,
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
                        improvement = json.loads(json_str)
                    else:
                        # If no JSON found, return an error
                        return {
                            "error": "Could not parse improvement from API response"
                        }
                    
                    return improvement
                except json.JSONDecodeError:
                    # If JSON parsing fails, return an error
                    return {
                        "error": "Failed to parse JSON from API response"
                    }
            except (KeyError, IndexError) as e:
                return {
                    "error": f"Error parsing API response: {str(e)}"
                }
        else:
            return {
                "error": f"API Error: {response.status_code} - {response.text[:200]}"
            }
            
    except Exception as e:
        return {
            "error": f"Error generating improvement: {str(e)}"
        }

def app():
    # Add a card container for the meal recommendations section
    st.markdown('<div class="card" id="meal-recommendations">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Personalized Meal Recommendations</div>', unsafe_allow_html=True)
    
    # Introduction to meal recommendations
    st.markdown("""
    <div style="padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <h4>AI-Powered Meal Planning for Diabetes Management</h4>
        <p>Get personalized meal recommendations based on your health profile and food preferences. 
        Our AI system uses the Google Gemini API to create tailored meal plans that help manage blood sugar levels.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["🍽️ Get Recommendations", "📝 Saved Recommendations"])
    
    with tab1:
        # Initialize session state for user data if not exists
        if 'user_health_data' not in st.session_state:
            st.session_state.user_health_data = {
                'diabetes_risk': 'Medium',
                'glucose': 120,
                'bmi': 25.0,
                'age': 45,
                'insulin': 80
            }
        
        # Initialize session state for recommendations if not exists
        if 'meal_recommendations' not in st.session_state:
            st.session_state.meal_recommendations = None
            
        # Initialize session state for saved recommendations if not exists
        if 'saved_recommendations' not in st.session_state:
            st.session_state.saved_recommendations = []
        
        # Create two columns for health data and preferences
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Health Profile")
            
            # Health data inputs
            diabetes_risk = st.selectbox(
                "Diabetes Risk Level",
                options=["Low", "Medium", "High"],
                index=1,
                key="diabetes_risk"
            )
            
            glucose = st.slider(
                "Blood Glucose Level (mg/dL)",
                min_value=70,
                max_value=200,
                value=st.session_state.user_health_data['glucose'],
                step=1,
                key="glucose"
            )
            
            bmi = st.slider(
                "BMI",
                min_value=15.0,
                max_value=45.0,
                value=st.session_state.user_health_data['bmi'],
                step=0.1,
                key="bmi"
            )
            
            age = st.slider(
                "Age",
                min_value=18,
                max_value=90,
                value=st.session_state.user_health_data['age'],
                step=1,
                key="age"
            )
            
            insulin = st.slider(
                "Insulin Level",
                min_value=10,
                max_value=200,
                value=st.session_state.user_health_data['insulin'],
                step=1,
                key="insulin"
            )
            
            # Update user health data in session state
            st.session_state.user_health_data = {
                'diabetes_risk': diabetes_risk,
                'glucose': glucose,
                'bmi': bmi,
                'age': age,
                'insulin': insulin
            }
        
        with col2:
            st.markdown("### Food Preferences")
            
            # Food preference inputs
            dietary_restrictions = st.multiselect(
                "Dietary Restrictions",
                options=["None", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low-Sodium"],
                default=["None"],
                key="dietary_restrictions"
            )
            
            cuisine_preferences = st.multiselect(
                "Cuisine Preferences",
                options=["Any", "Mediterranean", "Asian", "Mexican", "Indian", "Italian", "American", "Middle Eastern"],
                default=["Any"],
                key="cuisine_preferences"
            )
            
            disliked_foods = st.text_input(
                "Foods You Dislike (comma separated)",
                value="",
                key="disliked_foods"
            )
            
            cooking_skill = st.select_slider(
                "Cooking Skill Level",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Intermediate",
                key="cooking_skill"
            )
            
            prep_time = st.select_slider(
                "Preferred Meal Prep Time",
                options=["Quick (15 min)", "Medium (30 min)", "Longer (45+ min)"],
                value="Medium (30 min)",
                key="prep_time"
            )
            
            # Collect preferences
            user_preferences = {
                'dietary_restrictions': ", ".join(dietary_restrictions),
                'cuisine_preferences': ", ".join(cuisine_preferences),
                'disliked_foods': disliked_foods,
                'cooking_skill': cooking_skill,
                'prep_time': prep_time
            }
        
        # Button to generate recommendations
        if st.button("Generate Meal Recommendations", key="generate_recommendations"):
            with st.spinner("Generating personalized meal recommendations with AI..."):
                # Get recommendations from Gemini API
                recommendations = get_meal_recommendations(
                    st.session_state.user_health_data,
                    user_preferences
                )
                
                # Store recommendations in session state
                st.session_state.meal_recommendations = recommendations
        
        # Display recommendations if available
        if st.session_state.meal_recommendations:
            recommendations = st.session_state.meal_recommendations
            
            # Check if there was an error
            if 'error' in recommendations:
                st.error(f"Error: {recommendations['error']}")
            else:
                st.success("✅ Personalized meal recommendations generated successfully!")
                
                # Display meal plans
                st.markdown("### 🍽️ Recommended Meal Plans")
                
                # Create tabs for breakfast, lunch, dinner
                meal_tabs = st.tabs(["🌅 Breakfast", "🌮 Lunch", "🍲 Dinner"])
                
                # Get meal plans
                meal_plans = recommendations.get('meal_plans', [])
                
                # Group meals by type
                breakfast_meals = [meal for meal in meal_plans if meal.get('meal_type', '').lower() == 'breakfast']
                lunch_meals = [meal for meal in meal_plans if meal.get('meal_type', '').lower() == 'lunch']
                dinner_meals = [meal for meal in meal_plans if meal.get('meal_type', '').lower() == 'dinner']
                
                # Display breakfast meals
                with meal_tabs[0]:
                    if breakfast_meals:
                        for i, meal in enumerate(breakfast_meals):
                            display_meal(meal, i, "breakfast")
                    else:
                        st.info("No breakfast recommendations available.")
                
                # Display lunch meals
                with meal_tabs[1]:
                    if lunch_meals:
                        for i, meal in enumerate(lunch_meals):
                            display_meal(meal, i, "lunch")
                    else:
                        st.info("No lunch recommendations available.")
                
                # Display dinner meals
                with meal_tabs[2]:
                    if dinner_meals:
                        for i, meal in enumerate(dinner_meals):
                            display_meal(meal, i, "dinner")
                    else:
                        st.info("No dinner recommendations available.")
                
                # Display alternatives
                st.markdown("### 🔄 Healthier Alternatives")
                
                alternatives = recommendations.get('alternatives', [])
                
                if alternatives:
                    for i, alt in enumerate(alternatives):
                        with st.expander(f"Alternative {i+1}: {alt.get('high_carb_dish', 'High-Carb Dish')} → {alt.get('healthy_alternative', 'Healthy Alternative')}"):
                            st.markdown(f"""
                            **Instead of:** {alt.get('high_carb_dish', 'High-Carb Dish')}
                            
                            **Try:** {alt.get('healthy_alternative', 'Healthy Alternative')}
                            
                            **Benefit:** {alt.get('benefit', 'Better for blood sugar management')}
                            """)
                else:
                    st.info("No alternatives available.")
                
                # Display general tips
                st.markdown("### 💡 General Tips for Diabetes Management")
                
                tips = recommendations.get('general_tips', [])
                
                if tips:
                    for i, tip in enumerate(tips):
                        st.markdown(f"**{i+1}.** {tip}")
                else:
                    st.info("No general tips available.")
                
                # Button to save recommendations
                if st.button("Save These Recommendations", key="save_recommendations"):
                    # Add timestamp
                    recommendations['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    # Add to saved recommendations
                    st.session_state.saved_recommendations.append(recommendations)
                    
                    st.success("Recommendations saved successfully!")
    
    with tab2:
        st.markdown("### Your Saved Meal Recommendations")
        
        # Display saved recommendations
        if st.session_state.saved_recommendations:
            # Sort by timestamp (most recent first)
            sorted_recommendations = sorted(
                st.session_state.saved_recommendations,
                key=lambda x: datetime.datetime.strptime(x.get('timestamp', '2000-01-01 00:00'), "%Y-%m-%d %H:%M"),
                reverse=True
            )
            
            for i, rec in enumerate(sorted_recommendations):
                with st.expander(f"Recommendation Set {i+1} - {rec.get('timestamp', 'Unknown date')}"):
                    # Display a sample of meals
                    meal_plans = rec.get('meal_plans', [])
                    
                    if meal_plans:
                        # Display a random meal from this recommendation set
                        sample_meal = random.choice(meal_plans)
                        display_meal(sample_meal, 0, sample_meal.get('meal_type', 'meal').lower())
                        
                        st.markdown(f"**This recommendation set includes {len(meal_plans)} meals and {len(rec.get('alternatives', []))} alternatives.**")
                    
                    # Button to delete this recommendation
                    if st.button("Delete This Recommendation", key=f"delete_rec_{i}"):
                        st.session_state.saved_recommendations.remove(rec)
                        st.experimental_rerun()
        else:
            st.info("You haven't saved any recommendations yet. Generate and save recommendations to see them here.")
            
        # Button to clear all saved recommendations
        if st.session_state.saved_recommendations:
            if st.button("Clear All Saved Recommendations", key="clear_recommendations"):
                st.session_state.saved_recommendations = []
                st.success("All saved recommendations cleared!")
                st.experimental_rerun()

def display_meal(meal, index, meal_type):
    """Helper function to display a meal recommendation"""
    
    # Get meal details
    name = meal.get('name', f'Recommended {meal_type.capitalize()}')
    description = meal.get('description', 'No description available')
    ingredients = meal.get('ingredients', [])
    preparation = meal.get('preparation', 'No preparation steps available')
    carbs = meal.get('carbs', 'Unknown')
    glycemic_load = meal.get('glycemic_load', 'Unknown')
    tips = meal.get('diabetes_friendly_tips', 'No specific tips available')
    
    # Determine color based on glycemic load
    if glycemic_load.lower() == 'low':
        gl_color = '#27AE60'  # Green
    elif glycemic_load.lower() == 'medium':
        gl_color = '#F39C12'  # Orange
    else:
        gl_color = '#E74C3C'  # Red
    
    # Display meal card
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid {gl_color};">
        <h4>{name}</h4>
        <p><em>{description}</em></p>
        
        <div style="display: flex; margin-bottom: 10px;">
            <div style="background-color: {gl_color}20; padding: 5px 10px; border-radius: 5px; margin-right: 10px;">
                <strong>Carbs:</strong> {carbs}
            </div>
            <div style="background-color: {gl_color}20; padding: 5px 10px; border-radius: 5px;">
                <strong>Glycemic Load:</strong> <span style="color: {gl_color}; font-weight: bold;">{glycemic_load.upper()}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for ingredients, preparation, and tips
    ingredient_tab, prep_tab, tips_tab = st.tabs(["🥕 Ingredients", "👨‍🍳 Preparation", "💡 Diabetes Tips"])
    
    with ingredient_tab:
        if ingredients:
            for ingredient in ingredients:
                st.markdown(f"• {ingredient}")
        else:
            st.info("No ingredients listed.")
    
    with prep_tab:
        st.markdown(preparation)
    
    with tips_tab:
        st.markdown(f"""
        <div style="background-color: #E8F4F8; padding: 10px; border-radius: 5px;">
            {tips}
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback and improvement section
    with st.expander("Provide Feedback to Improve This Recommendation"):
        feedback = st.text_area(
            "What would you like to change about this meal?",
            placeholder="e.g., 'I don't like spinach' or 'I need a quicker preparation method'",
            key=f"feedback_{meal_type}_{index}"
        )
        
        if st.button("Get Improved Recommendation", key=f"improve_{meal_type}_{index}"):
            with st.spinner("Generating improved recommendation..."):
                # Get improved recommendation
                improvement = get_feedback_improvement(name, feedback)
                
                if 'error' in improvement:
                    st.error(f"Error: {improvement['error']}")
                else:
                    st.success("Recommendation improved based on your feedback!")
                    
                    # Display improved meal
                    improved_meal = improvement.get('improved_meal', {})
                    
                    st.markdown("### Improved Recommendation")
                    display_meal(improved_meal, index+100, meal_type)  # Use a different index to avoid key conflicts
                    
                    # Display explanation
                    st.markdown(f"""
                    <div style="background-color: #F0F8FF; padding: 15px; border-radius: 5px; margin-top: 10px;">
                        <strong>How we improved it:</strong> {improvement.get('explanation', 'No explanation provided')}
                    </div>
                    """, unsafe_allow_html=True)
