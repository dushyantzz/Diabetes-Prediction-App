import streamlit as st
from loader import model, accuracy_result
from data.config import thresholds
from function.function import make_donut
from data.base import mrk


def app(input_data):
    # Add a card container for the prediction section
    st.markdown('<div class="card" id="prediction">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Prediction Results</div>', unsafe_allow_html=True)

    # Make prediction
    prediction = model.predict_proba(input_data)[:, 1]
    probability_pct = (prediction * 100).round(2)[0]
    is_diabetes = 'Diabetes' if prediction >= thresholds else 'No Diabetes'
    button_class = 'danger' if prediction >= thresholds else 'success'

    # Create columns for layout
    cols = st.columns([3, 2])

    # Column 1: Prediction text and metrics
    with cols[0]:
        # Display prediction information directly without animation
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #6e8efb;">
            <h3 style="margin-top: 0; color: #2c3e50;">Analysis Results</h3>
            <p style="font-size: 1.1rem; margin-bottom: 10px;">Model Accuracy: <strong>{accuracy_result}%</strong></p>
            <p style="font-size: 1.1rem; margin-bottom: 10px;">Prediction: <strong>{is_diabetes}</strong></p>
            <p style="font-size: 1.1rem; margin-bottom: 0;">Probability: <strong>{probability_pct}%</strong></p>
        </div>
        """, unsafe_allow_html=True)

        # Add metrics in card format
        st.markdown('<div style="display: flex; justify-content: space-between; margin-top: 20px;">', unsafe_allow_html=True)

        # Metric 1: Accuracy
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{accuracy_result}%</div>
            <div class="metric-label">Model Accuracy</div>
        </div>
        ''', unsafe_allow_html=True)

        # Metric 2: Probability
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{probability_pct}%</div>
            <div class="metric-label">Probability</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: Prediction result and donut chart
    with cols[1]:
        # Format the prediction result
        result_text = f'<strong>Warning:</strong> Diabetes Detected!' if prediction >= thresholds else 'No Diabetes Detected'
        prediction_type = 'positive' if prediction >= thresholds else 'negative'

        # Display the prediction using our custom format
        st.markdown(mrk.format(
            prediction_type,  # CSS class
            result_text,      # Result text
            probability_pct,  # Probability percentage
            button_class      # Button class
        ), unsafe_allow_html=True)

        # Add space
        st.write('\n')

        # Create and display the donut chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        donut_chart = make_donut(
            probability_pct,
            'Diabetes Risk',
            input_color='#ff6b6b' if prediction >= thresholds else '#2e86c1'
        )
        st.altair_chart(donut_chart)
        st.markdown('</div>', unsafe_allow_html=True)

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Add a note about the prediction
    if prediction >= thresholds:
        st.warning("""
        ⚠️ **Important Note**: This prediction suggests a higher risk of diabetes. Please consult with a healthcare professional for proper diagnosis and advice.
        """)
    else:
        st.success("""
        ✅ **Good News**: This prediction suggests a lower risk of diabetes. However, maintaining a healthy lifestyle is still important.
        """)

    # Add an anchor for the explanation section
    st.markdown('<div id="explanation"></div>', unsafe_allow_html=True)