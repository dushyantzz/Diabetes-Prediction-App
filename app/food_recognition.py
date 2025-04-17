import streamlit as st
import pandas as pd
from PIL import Image
import io
import time
from function.gemini_vision import analyze_food_image, find_closest_food
from function.food_recognition_utils import estimate_portion_size, calculate_nutrition
from data.food_database import FOOD_DATABASE, GI_DESCRIPTIONS, DIABETES_TIPS

def app():
    # Add a card container for the food recognition section
    st.markdown('<div class="card" id="food-recognition">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Food Recognition & Nutritional Analysis</div>', unsafe_allow_html=True)

    # Introduction to food recognition
    st.markdown("""
    <div style="padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <p style="font-size: 16px; color: #333;">
            <strong>Track Your Diet with AI</strong>: Take a photo of your meal to identify food items and get nutritional information,
            especially carbohydrate content which is critical for diabetes management.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["📸 Analyze Food", "📊 Meal History"])

    with tab1:
        # Image upload section
        st.markdown("### Upload a Food Image")
        st.markdown("Take a photo of your meal or upload an existing image to analyze its nutritional content.")

        # File uploader for images
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        # Camera input option
        camera_input = st.camera_input("Or take a photo")

        # Process the image if uploaded or taken
        if uploaded_file is not None or camera_input is not None:
            # Use the uploaded file or camera input
            image_file = uploaded_file if uploaded_file is not None else camera_input

            # Display the image
            try:
                image = Image.open(image_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
            except Exception as e:
                st.error(f"Error opening image: {str(e)}")
                st.info("Please try a different image format (JPG, PNG recommended)")
                return

            # Add a button to analyze the image
            if st.button("Analyze Food", key="analyze_food"):
                # Show loading spinner
                with st.spinner("Analyzing your food with AI..."):
                    # Use Gemini API to analyze the food image
                    food_analysis = analyze_food_image(image)

                    # Extract food name and confidence
                    identified_food = food_analysis.get('food_name', 'unknown food')
                    confidence_level = food_analysis.get('confidence', 'medium')
                    is_meal = food_analysis.get('is_meal', False)
                    components = food_analysis.get('components', [])

                    # Map confidence level to numeric value
                    confidence_map = {'high': 0.9, 'medium': 0.7, 'low': 0.5}
                    confidence = confidence_map.get(confidence_level, 0.7)

                    # Find the closest match in our food database
                    food, match_score = find_closest_food(identified_food, FOOD_DATABASE)

                    # If it's a meal with components, show the components
                    meal_components = ", ".join(components) if is_meal and components else None

                    # Estimate portion size
                    portion_size = estimate_portion_size(image, food)

                    # Calculate nutritional information
                    nutrition = calculate_nutrition(food, portion_size)

                    # Display results
                    st.success(f"Food identified: **{identified_food}**")
                    st.info(f"Matched to database entry: **{food.title()}** (Confidence: {confidence:.2f})")

                    # If it's a meal with components, show them
                    if meal_components:
                        st.info(f"This appears to be a meal containing: {meal_components}")

                    # Display portion size
                    st.markdown(f"**Estimated portion size:** {portion_size:.0f}g")

                    # Create two columns for nutritional information
                    col1, col2 = st.columns(2)

                    with col1:
                        # Display nutritional information
                        st.markdown("### Nutritional Information")
                        st.markdown(f"""
                        <div style="background-color: #f0f2f5; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                            <table style="width: 100%;">
                                <tr>
                                    <td><strong>Calories:</strong></td>
                                    <td style="text-align: right;">{nutrition['calories']} kcal</td>
                                </tr>
                                <tr>
                                    <td><strong>Carbohydrates:</strong></td>
                                    <td style="text-align: right; color: #e74c3c; font-weight: bold;">{nutrition['carbs']}g</td>
                                </tr>
                                <tr>
                                    <td><strong>Protein:</strong></td>
                                    <td style="text-align: right;">{nutrition['protein']}g</td>
                                </tr>
                                <tr>
                                    <td><strong>Fat:</strong></td>
                                    <td style="text-align: right;">{nutrition['fat']}g</td>
                                </tr>
                                <tr>
                                    <td><strong>Fiber:</strong></td>
                                    <td style="text-align: right;">{nutrition['fiber']}g</td>
                                </tr>
                            </table>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        # Display glycemic index information
                        st.markdown("### Glycemic Index")
                        gi_level = nutrition['gi']
                        gi_color = {
                            'low': '#27AE60',  # Green for low GI
                            'medium': '#F39C12',  # Orange for medium GI
                            'high': '#E74C3C'  # Red for high GI
                        }

                        st.markdown(f"""
                        <div style="background-color: {gi_color[gi_level]}20; padding: 15px; border-radius: 10px; border-left: 5px solid {gi_color[gi_level]};">
                            <h4 style="color: {gi_color[gi_level]}; margin-top: 0;">{gi_level.title()} GI</h4>
                            <p>{GI_DESCRIPTIONS[gi_level]}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Diabetes impact
                        st.markdown("### Impact on Blood Sugar")
                        impact_text = DIABETES_TIPS

                        st.markdown(f"""
                        <div style="background-color: #f0f2f5; padding: 15px; border-radius: 10px; margin-top: 10px;">
                            <p>{impact_text[gi_level]}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Add a button to save the meal to history
                    if st.button("Save to Meal History"):
                        st.success("Meal saved to history!")
                        # In a real implementation, you would save this to a database

    with tab2:
        st.markdown("### Your Meal History")
        st.markdown("Track your food intake and monitor carbohydrate consumption over time.")

        # In a real implementation, you would load meal history from a database
        # For this demo, we'll show a sample meal history

        # Sample meal history data
        sample_meals = [
            {"date": "2023-04-14", "time": "08:30", "food": "Oatmeal with banana", "carbs": 45, "calories": 320},
            {"date": "2023-04-14", "time": "12:15", "food": "Chicken salad", "carbs": 15, "calories": 350},
            {"date": "2023-04-14", "time": "19:00", "food": "Grilled salmon with vegetables", "carbs": 20, "calories": 420},
            {"date": "2023-04-13", "time": "08:00", "food": "Whole grain toast with eggs", "carbs": 30, "calories": 380},
            {"date": "2023-04-13", "time": "13:00", "food": "Turkey sandwich", "carbs": 35, "calories": 450},
            {"date": "2023-04-13", "time": "18:30", "food": "Pasta with tomato sauce", "carbs": 65, "calories": 520},
        ]

        # Convert to DataFrame
        meal_df = pd.DataFrame(sample_meals)

        # Display meal history
        st.dataframe(meal_df, use_container_width=True)

        # Display total carbs per day
        st.markdown("### Daily Carbohydrate Intake")
        daily_carbs = meal_df.groupby("date")["carbs"].sum().reset_index()

        # Create a bar chart for daily carbs
        st.bar_chart(daily_carbs.set_index("date"))

        # Add a note about carbohydrate intake
        st.markdown("""
        <div style="background-color: #f0f2f5; padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h4 style="margin-top: 0; color: #2c3e50;">Carbohydrate Management Tips</h4>
            <ul>
                <li><strong>Recommended daily intake:</strong> 130-225g of carbohydrates per day (varies by individual)</li>
                <li><strong>Distribute carbs throughout the day</strong> to avoid blood sugar spikes</li>
                <li><strong>Focus on complex carbohydrates</strong> with lower glycemic index</li>
                <li><strong>Pair carbohydrates with protein and healthy fats</strong> to slow absorption</li>
                <li><strong>Monitor blood glucose</strong> before and after meals to understand your body's response</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Add a button to navigate to the next section
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <a href="#about" class="custom-button">Learn About Diabetes</a>
    </div>
    """, unsafe_allow_html=True)
