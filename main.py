from function.function import *
import streamlit as st
from loader import page_icon
from data.base import st_style, footer

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction with AI",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dushyantzz/Diabetes-Prediction-App',
        'Report a bug': 'https://github.com/dushyantzz/Diabetes-Prediction-App/issues',
        'About': 'Diabetes Prediction App using Machine Learning and Explainable AI'
    }
)

# Apply custom CSS
st.markdown(st_style, unsafe_allow_html=True)

# Header
from app.header import app as header_app
header_app()

# Sidebar inputs
from app.input import app as input_app
input_data = input_app()

# Main content container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Prediction section
from app.predict import app as predict_app
predict_app(input_data)

# Explanation section
from app.explainer import app as explain_app
explain_app(input_data)

# Model performance section
from app.performance import app as performance_app
performance_app()

# Feature importance section
from app.perm_importance import app as importance_app
importance_app()

# About section
from app.about import app as about_app
about_app()

# Close main content container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(footer, unsafe_allow_html=True)
