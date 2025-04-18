import streamlit as st
import pandas as pd
from PIL import Image
from function.gemini_vision import analyze_food_image, find_closest_food
from function.food_recognition_utils import estimate_portion_size, calculate_nutrition
from data.food_database import FOOD_DATABASE, GI_DESCRIPTIONS, DIABETES_TIPS

def app():
    # Initialize session state for meal history if not exists
    if 'meal_history' not in st.session_state:
        st.session_state.meal_history = [
            {"date": "2023-04-14", "time": "08:30", "food": "Oatmeal with banana", "carbs": 45, "calories": 320},
            {"date": "2023-04-14", "time": "12:15", "food": "Chicken salad", "carbs": 15, "calories": 350},
            {"date": "2023-04-14", "time": "19:00", "food": "Grilled salmon with vegetables", "carbs": 20, "calories": 420},
        ]

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
        st.markdown("### Upload or Capture a Food Image")
        st.markdown("Take a photo of your meal or upload an existing image to analyze its nutritional content.")

        # Create tabs for different image input methods
        img_tab1, img_tab2 = st.tabs(["📁 Upload Image", "📸 Use Camera"])

        with img_tab1:
            # File uploader for images
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        with img_tab2:
            # Initialize session states for camera functionality
            if 'camera_image' not in st.session_state:
                st.session_state.camera_image = None
            if 'camera_on' not in st.session_state:
                st.session_state.camera_on = False
            if 'last_camera_input' not in st.session_state:
                st.session_state.last_camera_input = None

            # Camera controls in a row
            camera_controls_col1, camera_controls_col2 = st.columns([1, 1])

            with camera_controls_col1:
                if st.button("🎥 Start/Stop Camera", key="toggle_camera"):
                    st.session_state.camera_on = not st.session_state.camera_on
                    st.rerun()

            with camera_controls_col2:
                if st.session_state.camera_image is not None:
                    if st.button("🔄 Reset", key="reset_camera"):
                        st.session_state.camera_image = None
                        st.session_state.last_camera_input = None
                        st.rerun()

            # Camera container that will show/hide based on state
            camera_container = st.empty()

            # Display camera or captured image based on state
            if st.session_state.camera_on:
                with camera_container.container():
                    # Show camera input when camera is on
                    camera_input = st.camera_input("Take a photo of your food", key="live_camera")

                    # Check if we have a new camera input (photo was just taken)
                    if camera_input is not None and camera_input != st.session_state.last_camera_input:
                        # Store the current input to avoid reprocessing the same image
                        st.session_state.last_camera_input = camera_input
                        st.session_state.camera_image = camera_input

                        # Success message
                        st.success("Image captured! Analyzing now...")

                        # Automatically analyze the image
                        try:
                            # Process the image
                            image = Image.open(camera_input)
                            # Use Gemini API to analyze the food image
                            with st.spinner("Analyzing your food with AI..."):
                                food_analysis = analyze_food_image(image)

                                # Store analysis results in session state for display
                                st.session_state.food_analysis = food_analysis
                                st.session_state.analyzed_image = image
                                st.session_state.image_source = "captured"

                                # Rerun to show results
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error analyzing image: {str(e)}")
            else:
                # If camera is off but we have a captured image, display it
                if st.session_state.camera_image:
                    with camera_container.container():
                        st.image(Image.open(st.session_state.camera_image), caption="Captured Image", use_column_width=True)
                        st.info("Camera is off. Turn on the camera to take a new photo.")

        # Add a reset button to clear all images
        if 'reset_images' not in st.session_state:
            st.session_state.reset_images = False

        # Camera status indicator in sidebar
        st.sidebar.markdown("### Camera Status")
        if 'camera_image' in st.session_state and st.session_state.camera_image is not None:
            if 'food_analysis' in st.session_state:
                st.sidebar.success("📸 Image analyzed successfully")
            else:
                st.sidebar.success("📸 Image captured and ready for analysis")
        elif st.session_state.get('camera_on', False):
            st.sidebar.warning("📹 Camera is active - take a photo to analyze food")
        else:
            st.sidebar.info("📴 Camera is off - click 'Start/Stop Camera' to begin")

        # Clear button in the sidebar
        if st.sidebar.button("🗑️ Clear All Images", key="clear_images"):
            st.session_state.camera_image = None
            st.session_state.last_camera_input = None
            st.session_state.reset_images = True
            st.rerun()

        # Reset the file uploader by toggling the session state
        if st.session_state.reset_images:
            st.session_state.reset_images = False
            uploaded_file = None

        # Get the image from either upload or camera capture
        image_file = None
        image_source = None

        if uploaded_file is not None:
            image_file = uploaded_file
            image_source = "uploaded"
        elif st.session_state.camera_image is not None:
            image_file = st.session_state.camera_image
            image_source = "captured"

        # Check if we have analysis results in session state from camera capture
        if 'food_analysis' in st.session_state and 'analyzed_image' in st.session_state:
            # Use the stored analysis results
            food_analysis = st.session_state.food_analysis
            image = st.session_state.analyzed_image
            image_source = st.session_state.image_source

            # Clear the analysis results from session state to prevent showing them again
            # after a page refresh unless explicitly requested
            del st.session_state.food_analysis
            del st.session_state.analyzed_image

            # Skip to displaying results
            show_analysis_results = True
        else:
            # Process the image if available but not yet analyzed
            show_analysis_results = False
            if image_file is not None:
                try:
                    image = Image.open(image_file)
                    if image_source == "uploaded":
                        st.image(image, caption="Uploaded Image", use_column_width=True)
                    # Note: We don't need to display the captured image again as it's already shown
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
                        show_analysis_results = True

        # If we have analysis results to show (either from button click or camera capture)
        if 'food_analysis' in locals() and show_analysis_results:
            # Extract food name and confidence
            identified_food = food_analysis.get('food_name', 'unknown food')
            confidence_level = food_analysis.get('confidence', 'medium')
            is_meal = food_analysis.get('is_meal', False)
            components = food_analysis.get('components', [])
            carb_content = food_analysis.get('carb_content', 'medium')

            # Map confidence level to numeric value for display
            confidence_map = {'high': 0.9, 'medium': 0.7, 'low': 0.5}
            ai_confidence = confidence_map.get(confidence_level, 0.7)

            # Add AI confidence to the session state for potential future use
            st.session_state.ai_confidence = ai_confidence

            # Store the AI-estimated carb content for display
            st.session_state.carb_estimate = carb_content

            # Find the closest match in our food database
            food, match_score = find_closest_food(identified_food, FOOD_DATABASE)

            # If it's a meal with components, show the components
            meal_components = ", ".join(components) if is_meal and components else None

            # Estimate portion size
            portion_size = estimate_portion_size(image, food)

            # Calculate nutritional information
            nutrition = calculate_nutrition(food, portion_size)

            # Use the AI-estimated carb content to determine glycemic index if confidence is low
            if match_score < 0.7 and carb_content:
                # Override the glycemic index based on carb content from Gemini AI
                if carb_content.lower() == 'high':
                    nutrition['gi'] = 'high'
                elif carb_content.lower() == 'medium':
                    nutrition['gi'] = 'medium'
                elif carb_content.lower() == 'low':
                    nutrition['gi'] = 'low'

            # Display results with source information
            st.success(f"Food identified: **{identified_food}**")

            # Show match confidence with color coding based on match quality
            match_color = '#4CAF50' if match_score > 0.8 else '#FFC107' if match_score > 0.6 else '#F44336'
            st.markdown(f"""
            <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; border-left: 5px solid {match_color};">
                Matched to database entry: <strong>{food.title()}</strong> (Confidence: {match_score:.2f})
            </div>
            """, unsafe_allow_html=True)

            st.caption(f"Image source: {image_source.capitalize()} image")

            # If it's a meal with components, show them
            if meal_components:
                st.info(f"This appears to be a meal containing: {meal_components}")

            # Display AI-estimated carb content
            carb_colors = {
                'high': '#E74C3C',  # Red for high carbs
                'medium': '#F39C12',  # Orange for medium carbs
                'low': '#27AE60'  # Green for low carbs
            }
            carb_color = carb_colors.get(carb_content, '#3498DB')  # Default blue

            st.markdown(f"""
            <div style="background-color: {carb_color}20; padding: 10px; border-radius: 5px; border-left: 5px solid {carb_color}; margin-bottom: 15px;">
                <strong>AI-Estimated Carb Content:</strong> <span style="color: {carb_color}; font-weight: bold;">{carb_content.upper()}</span>
            </div>
            """, unsafe_allow_html=True)

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

                # Determine if GI was derived from database or AI estimate
                gi_source = "Database" if match_score > 0.7 else "AI Estimate"

                st.markdown(f"""
                <div style="background-color: {gi_color[gi_level]}20; padding: 15px; border-radius: 10px; border-left: 5px solid {gi_color[gi_level]};">
                    <h4 style="color: {gi_color[gi_level]}; margin-top: 0;">{gi_level.title()} GI</h4>
                    <p style="margin-bottom: 5px;">{GI_DESCRIPTIONS[gi_level]}</p>
                    <small style="color: #666;">Source: {gi_source}</small>
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
                # Get current date and time
                import datetime
                now = datetime.datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M")

                # Create a new meal entry
                new_meal = {
                    "date": date_str,
                    "time": time_str,
                    "food": identified_food,
                    "carbs": nutrition['carbs'],
                    "calories": nutrition['calories']
                }

                # Add to session state
                st.session_state.meal_history.append(new_meal)

                # Show success message
                st.success(f"Meal '{identified_food}' saved to history!")
                st.info(f"Added {nutrition['carbs']}g of carbs and {nutrition['calories']} calories to your daily total.")

    with tab2:
        st.markdown("### Your Meal History")
        st.markdown("Track your food intake and monitor carbohydrate consumption over time.")

        # Get meal history from session state

        # Add a button to clear meal history
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear History", key="clear_history"):
                # Keep only the first 3 sample entries
                st.session_state.meal_history = st.session_state.meal_history[:3]
                st.success("Meal history cleared!")
                st.rerun()

        # Convert to DataFrame
        meal_df = pd.DataFrame(st.session_state.meal_history)

        # Sort by date and time (most recent first)
        if not meal_df.empty:
            meal_df['datetime'] = pd.to_datetime(meal_df['date'] + ' ' + meal_df['time'])
            meal_df = meal_df.sort_values('datetime', ascending=False)
            meal_df = meal_df.drop('datetime', axis=1)  # Remove the helper column

        # Display meal history
        st.dataframe(meal_df, use_container_width=True)

        # Display total carbs per day
        st.markdown("### Daily Carbohydrate Intake")

        if not meal_df.empty:
            # Calculate daily totals
            daily_carbs = meal_df.groupby("date").agg({
                "carbs": "sum",
                "calories": "sum"
            }).reset_index()

            # Get today's date
            import datetime
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            # Check if we have data for today
            today_data = daily_carbs[daily_carbs['date'] == today]

            # Display today's totals if available
            if not today_data.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Today's Carbs", f"{today_data.iloc[0]['carbs']:.0f}g",
                              delta=f"{today_data.iloc[0]['carbs'] - 130:.0f}g from min. recommended")
                with col2:
                    st.metric("Today's Calories", f"{today_data.iloc[0]['calories']:.0f} kcal")

            # Create a bar chart for daily carbs
            st.bar_chart(daily_carbs.set_index("date")["carbs"])

            # Add a line for recommended minimum carbs
            st.markdown("<div style='text-align: center; color: #777;'>Recommended daily minimum: 130g carbs</div>", unsafe_allow_html=True)
        else:
            st.info("No meal data available yet. Add meals using the food recognition feature.")

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
