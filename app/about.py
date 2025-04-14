import streamlit as st

def app():
    # Add a card container for the about section
    st.markdown('<div class="card" id="about">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">About Diabetes</div>', unsafe_allow_html=True)

    # Create tabs for different aspects of diabetes information
    tab1, tab2, tab3 = st.tabs(["🔍 Overview", "🩺 Symptoms & Risk Factors", "❤️ Prevention & Management"])

    # Tab 1: Overview of diabetes
    with tab1:
        # Title
        st.markdown('<h3>What is Diabetes?</h3>', unsafe_allow_html=True)

        # Description
        st.markdown("""
        **Diabetes** is a chronic health condition that affects how your body turns food into energy.
        It is characterized by high levels of glucose (sugar) in the blood, which occurs because the body either
        doesn't produce enough insulin, doesn't use insulin effectively, or both.
        """)

        # Create two columns for Type 1 and Type 2 diabetes
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div style="padding: 15px; background-color: #e6f2ff; border-radius: 10px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #2e86c1;">Type 1 Diabetes</h4>', unsafe_allow_html=True)
            st.markdown("""
            - An autoimmune condition where the immune system attacks insulin-producing cells
            - Usually diagnosed in children and young adults
            - Requires daily insulin injections
            - Not preventable with current knowledge
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div style="padding: 15px; background-color: #fff5e6; border-radius: 10px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #e67e22;">Type 2 Diabetes</h4>', unsafe_allow_html=True)
            st.markdown("""
            - Body becomes resistant to insulin or doesn't produce enough
            - Most common form (90-95% of all diabetes cases)
            - Often linked to lifestyle factors and genetics
            - Can often be prevented or delayed with healthy lifestyle
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Gestational diabetes section
        st.markdown('<div style="padding: 15px; background-color: #f8f9fa; border-radius: 10px; margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #6e8efb;">Gestational Diabetes</h4>', unsafe_allow_html=True)
        st.markdown("""
        Occurs during pregnancy when the body cannot make enough insulin to support the increased demand.
        Usually resolves after childbirth, but increases the risk of developing type 2 diabetes later in life.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2: Symptoms and risk factors
    with tab2:
        # Create two columns for Symptoms and Risk Factors
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<h3>Common Symptoms</h3>', unsafe_allow_html=True)
            st.markdown('<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px;">', unsafe_allow_html=True)
            st.markdown("""
            - **Frequent urination**, especially at night
            - **Excessive thirst** and increased fluid intake
            - **Unexplained weight loss** (especially in type 1)
            - **Extreme hunger** despite eating
            - **Blurred vision** or vision changes
            - **Fatigue** and weakness
            - **Slow-healing wounds** or frequent infections
            - **Tingling or numbness** in hands or feet (type 2)
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<h3>Risk Factors</h3>', unsafe_allow_html=True)
            st.markdown('<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-top: 0; color: #6e8efb;">Type 1 Diabetes</h4>', unsafe_allow_html=True)
            st.markdown("""
            - Family history of type 1 diabetes
            - Certain genetic factors
            - Possible environmental triggers
            """)

            st.markdown('<h4 style="color: #6e8efb;">Type 2 Diabetes</h4>', unsafe_allow_html=True)
            st.markdown("""
            - **Overweight or obesity**
            - **Physical inactivity**
            - Family history of diabetes
            - Age (risk increases after 45)
            - History of gestational diabetes
            - Polycystic ovary syndrome
            - High blood pressure or cholesterol
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Complications section
        st.markdown('<h3>Complications of Untreated Diabetes</h3>', unsafe_allow_html=True)

        # Create a 2x2 grid for complications
        comp_col1, comp_col2 = st.columns(2)

        with comp_col1:
            st.markdown('<div style="background: linear-gradient(135deg, #ff6b6b10, #ff6b6b30); padding: 15px; border-radius: 10px; border-left: 4px solid #ff6b6b; margin-bottom: 15px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-top: 0;">Heart Disease</h4>', unsafe_allow_html=True)
            st.markdown('Increased risk of heart attack, stroke, and cardiovascular problems')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div style="background: linear-gradient(135deg, #1dd1a130, #1dd1a110); padding: 15px; border-radius: 10px; border-left: 4px solid #1dd1a1;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-top: 0;">Vision Loss</h4>', unsafe_allow_html=True)
            st.markdown('Diabetic retinopathy can cause blindness')
            st.markdown('</div>', unsafe_allow_html=True)

        with comp_col2:
            st.markdown('<div style="background: linear-gradient(135deg, #48dbfb10, #48dbfb30); padding: 15px; border-radius: 10px; border-left: 4px solid #48dbfb; margin-bottom: 15px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-top: 0;">Kidney Damage</h4>', unsafe_allow_html=True)
            st.markdown('Can lead to kidney failure and need for dialysis')
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div style="background: linear-gradient(135deg, #feca57, #feca5710); padding: 15px; border-radius: 10px; border-left: 4px solid #feca57;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-top: 0;">Nerve Damage</h4>', unsafe_allow_html=True)
            st.markdown('Diabetic neuropathy causing pain, tingling, and numbness')
            st.markdown('</div>', unsafe_allow_html=True)

    # Tab 3: Prevention and management
    with tab3:
        # Title
        st.markdown('<h3>Prevention & Management Strategies</h3>', unsafe_allow_html=True)

        # Create two columns for Healthy Diet and Regular Physical Activity
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #6e8efb; margin-top: 0;">Healthy Diet</h4>', unsafe_allow_html=True)
            st.markdown('''
            - Focus on fruits, vegetables, and whole grains
            - Choose lean proteins and healthy fats
            - Limit refined carbohydrates and added sugars
            - Control portion sizes
            - Consider working with a dietitian for personalized advice
            ''')
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #6e8efb; margin-top: 0;">Regular Physical Activity</h4>', unsafe_allow_html=True)
            st.markdown('''
            - Aim for at least 150 minutes of moderate exercise weekly
            - Include both aerobic exercise and strength training
            - Break up long periods of sitting
            - Find activities you enjoy to stay motivated
            - Start slowly and gradually increase intensity
            ''')
            st.markdown('</div>', unsafe_allow_html=True)

        # Create two more columns for Weight Management and Regular Monitoring
        col3, col4 = st.columns(2)

        with col3:
            st.markdown('<div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-top: 20px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #6e8efb; margin-top: 0;">Weight Management</h4>', unsafe_allow_html=True)
            st.markdown('''
            - Even modest weight loss (5-10%) can help prevent diabetes
            - Focus on sustainable lifestyle changes rather than crash diets
            - Set realistic goals and track progress
            - Combine diet changes with increased physical activity
            ''')
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div style="padding: 20px; background-color: #f8f9fa; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-top: 20px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color: #6e8efb; margin-top: 0;">Regular Monitoring</h4>', unsafe_allow_html=True)
            st.markdown('''
            - Check blood glucose levels as recommended by your doctor
            - Keep track of your results to identify patterns
            - Get regular check-ups and screenings
            - Monitor blood pressure and cholesterol levels
            - Pay attention to foot health and vision changes
            ''')
            st.markdown('</div>', unsafe_allow_html=True)

        # When to See a Doctor section
        st.markdown('<div style="margin-top: 30px; padding: 20px; background-color: #e8f4f8; border-radius: 10px; border-left: 5px solid #6e8efb;">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin-top: 0;">When to See a Doctor</h4>', unsafe_allow_html=True)
        st.markdown('''
        If you experience symptoms of diabetes or have risk factors, consult a healthcare provider. Early detection and treatment can prevent complications and improve outcomes.

        Regular screenings are recommended for adults over 45, especially those who are overweight or have other risk factors.
        ''')
        st.markdown('<div style="text-align: center; margin-top: 15px;">', unsafe_allow_html=True)
        st.markdown('<a href="https://www.diabetes.org/" target="_blank" class="custom-button">Learn More at American Diabetes Association</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Add disclaimer
    st.warning("""
    ⚠️ **Medical Disclaimer**: This application is for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

    This model was created for demonstration purposes and has not been reviewed by medical professionals.
    """)
