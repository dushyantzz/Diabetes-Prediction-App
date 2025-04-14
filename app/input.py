import streamlit as st
import pandas as pd


def app():
    # Add custom sidebar header
    st.sidebar.markdown('<div class="sidebar-header">Input Parameters</div>', unsafe_allow_html=True)

    # Add description
    st.sidebar.markdown("""
    <div style="margin-bottom: 20px; font-size: 0.9rem; color: #555;">
        Enter your health parameters below to get a diabetes prediction.
    </div>
    """, unsafe_allow_html=True)

    # Create input fields with tooltips

    # Pregnancies
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>Pregnancies</span>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">Number of times pregnant</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pregnancies_value = st.sidebar.number_input(
        'Pregnancies',
        min_value=0,
        max_value=20,
        value=1,
        label_visibility="collapsed"
    )

    # Glucose
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span>Glucose</span>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">Plasma glucose concentration (mg/dL)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    glucose_value = st.sidebar.number_input(
        'Glucose',
        min_value=0,
        max_value=250,
        value=100,
        label_visibility="collapsed"
    )

    # Insulin
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span>Insulin</span>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">2-Hour serum insulin (mu U/ml)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    insulin_value = st.sidebar.number_input(
        'Insulin',
        min_value=0,
        max_value=1000,
        value=100,
        label_visibility="collapsed"
    )

    # BMI
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span>BMI</span>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">Body Mass Index (weight in kg/(height in m)²)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    bmi_value = st.sidebar.number_input(
        'BMI',
        min_value=0.0,
        max_value=100.0,
        value=37.0,
        format="%.1f",
        label_visibility="collapsed"
    )

    # Age
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span>Age</span>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">Age in years</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    age_value = st.sidebar.number_input(
        'Age',
        min_value=0,
        max_value=100,
        value=25,
        label_visibility="collapsed"
    )

    # Add predict button
    st.sidebar.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
    predict_button = st.sidebar.button('Predict', use_container_width=True)

    # Add reset button
    reset_button = st.sidebar.button('Reset Values', use_container_width=True)

    st.sidebar.markdown('---')

    # Add information section
    st.sidebar.markdown("""
    <div style="font-size: 0.8rem; color: #777; margin-top: 20px;">
        <p><strong>Data Source:</strong> National Institute of Diabetes and Digestive and Kidney Diseases</p>
        <p><strong>Model:</strong> Random Forest Classifier</p>
    </div>
    """, unsafe_allow_html=True)

    return pd.DataFrame([[pregnancies_value, glucose_value, insulin_value, bmi_value, age_value]],
                        columns=['Pregnancies', 'Glucose', 'Insulin','BMI','Age'])