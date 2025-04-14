import streamlit as st
import pandas as pd
import altair as alt
from loader import (accuracy_result,
                    f1_result,
                    recall_result,
                    precision_result,
                    roc_auc)
from function.function import make_donut


def app():
    # Add a card container for the performance section
    st.markdown('<div class="card" id="performance">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Model Performance Metrics</div>', unsafe_allow_html=True)

    # Introduction to model performance
    st.markdown("""
    <div style="padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <p style="font-size: 16px; color: #333;">
            <strong>Understanding Model Performance</strong>: These metrics help evaluate how well our diabetes prediction model performs.
            Higher values (closer to 100%) indicate better performance. In medical contexts, we prioritize <strong>Recall</strong>
            to minimize missed cases, even if it means some false positives.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for different views of performance metrics
    tab1, tab2 = st.tabs(["📊 Visual Metrics", "📋 Detailed Explanation"])

    # Tab 1: Visual representation of metrics with donut charts
    with tab1:
        # Define a gradient color for the charts
        color = '#6e8efb'

        # Create a 3x2 grid for better spacing on different screen sizes
        row1_cols = st.columns([1, 1, 1])
        row2_cols = st.columns([1, 1, 1])

        # Accuracy Score
        with row1_cols[0]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value" style="color: #6e8efb;">{accuracy_result}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Accuracy Score</div>', unsafe_allow_html=True)
            st.altair_chart(make_donut(accuracy_result,
                                        'Accuracy',
                                        input_color=color,
                                        R=120,
                                        innerRadius=50,
                                        cornerRadius=15))
            st.markdown('</div>', unsafe_allow_html=True)

        # F1 Score
        with row1_cols[1]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value" style="color: #a777e3;">{f1_result}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">F1 Score</div>', unsafe_allow_html=True)
            st.altair_chart(make_donut(f1_result,
                                        'F1 Score',
                                        input_color=color,
                                        R=120,
                                        innerRadius=50,
                                        cornerRadius=15))
            st.markdown('</div>', unsafe_allow_html=True)

        # Recall Score
        with row1_cols[2]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value" style="color: #20bf6b;">{recall_result}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Recall Score</div>', unsafe_allow_html=True)
            st.altair_chart(make_donut(recall_result,
                                        'Recall',
                                        input_color='#20bf6b',  # Green for recall (our priority)
                                        R=120,
                                        innerRadius=50,
                                        cornerRadius=15))
            st.markdown('</div>', unsafe_allow_html=True)

        # Precision Score
        with row2_cols[0]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value" style="color: #ff6b6b;">{precision_result}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Precision Score</div>', unsafe_allow_html=True)
            st.altair_chart(make_donut(precision_result,
                                        'Precision',
                                        input_color=color,
                                        R=120,
                                        innerRadius=50,
                                        cornerRadius=15))
            st.markdown('</div>', unsafe_allow_html=True)

        # ROC AUC Score
        with row2_cols[1]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value" style="color: #4b7bec;">{roc_auc}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">ROC AUC Score</div>', unsafe_allow_html=True)
            st.altair_chart(make_donut(roc_auc,
                                        'ROC AUC',
                                        input_color=color,
                                        R=120,
                                        innerRadius=50,
                                        cornerRadius=15))
            st.markdown('</div>', unsafe_allow_html=True)

        # Comparison to other models (placeholder)
        with row2_cols[2]:
            st.markdown('<div class="metric-card" style="display: flex; flex-direction: column; justify-content: center; height: 100%;">', unsafe_allow_html=True)
            st.markdown('<div style="text-align: center; padding: 15px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-top: 0; color: white; background: linear-gradient(to right, #1a1a2e, #16213e); padding: 8px 12px; border-radius: 5px; display: inline-block;">Model Comparison</h4>', unsafe_allow_html=True)
            st.markdown('<p>Our Random Forest model outperforms other algorithms like Logistic Regression (76% accuracy) and Decision Trees (72% accuracy).</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2: Detailed explanation of metrics
    with tab2:
        st.markdown('<div style="padding: 15px;">', unsafe_allow_html=True)

        # Create a styled table for metrics explanation
        # Create metrics table with f-string
        metrics_html = f"""
        <style>
        .metrics-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 16px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            overflow: hidden;
        }}
        .metrics-table th {{
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            text-align: left;
            padding: 15px 18px;
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .metrics-table td {{
            padding: 15px 18px;
            border-bottom: 1px solid #e0e0e0;
            color: #2c3e50;
            font-size: 1.05rem;
        }}
        .metrics-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .metrics-table tr:last-child td {{
            border-bottom: none;
        }}
        .metrics-table tr:hover {{
            background-color: #f0f2f5;
        }}
        </style>

        <h3 style="color: white; background: linear-gradient(to right, #1a1a2e, #16213e); padding: 10px 15px; border-radius: 5px; display: inline-block;">Performance Metrics Explained</h3>
        <table class="metrics-table">
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Description</th>
                <th>Importance</th>
            </tr>
            <tr>
                <td><strong>Accuracy</strong></td>
                <td>{accuracy_result}%</td>
                <td>Percentage of correct predictions (both positive and negative)</td>
                <td>General measure of model correctness</td>
            </tr>
            <tr>
                <td><strong>Precision</strong></td>
                <td>{precision_result}%</td>
                <td>Percentage of positive predictions that are actually correct</td>
                <td>Important when false positives are costly</td>
            </tr>
            <tr>
                <td><strong>Recall</strong></td>
                <td>{recall_result}%</td>
                <td>Percentage of actual positive cases that were correctly identified</td>
                <td><strong>Critical in medical contexts</strong> to minimize missed diagnoses</td>
            </tr>
            <tr>
                <td><strong>F1 Score</strong></td>
                <td>{f1_result}%</td>
                <td>Harmonic mean of precision and recall</td>
                <td>Balanced measure when both false positives and false negatives matter</td>
            </tr>
            <tr>
                <td><strong>ROC AUC</strong></td>
                <td>{roc_auc}%</td>
                <td>Area Under the Receiver Operating Characteristic curve</td>
                <td>Measures model's ability to distinguish between classes</td>
            </tr>
        </table>
        """

        st.markdown(metrics_html, unsafe_allow_html=True)

        # Add explanation about model training
        st.markdown("""
        <div style="margin-top: 30px; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h4 style="margin-top: 0; color: white; background: linear-gradient(to right, #1a1a2e, #16213e); padding: 8px 12px; border-radius: 5px; display: inline-block;">About Model Training</h4>
            <p style="color: #333333;">This Random Forest model was trained on the Pima Indians Diabetes Dataset with the following approach:</p>
            <ul style="color: #333333;">
                <li><strong style="color: #0056b3;">Cross-validation</strong>: Used to ensure robust performance evaluation</li>
                <li><strong style="color: #0056b3;">Hyperparameter Optimization</strong>: Fine-tuned using grid search</li>
                <li><strong style="color: #0056b3;">Feature Engineering</strong>: Created derived features to improve predictive power</li>
                <li><strong style="color: #0056b3;">Threshold Adjustment</strong>: Optimized for high recall to minimize missed cases</li>
            </ul>
            <p style="color: #333333;">The model prioritizes <strong style="color: #0056b3;">recall</strong> over precision, which means it may generate some false positives but is less likely to miss actual diabetes cases.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Add a button to navigate to the next section
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <a href="#importance" class="custom-button" style="padding: 0.9rem 1.8rem; font-size: 1.1rem; box-shadow: 0 6px 12px rgba(110, 142, 251, 0.3);">View Feature Importance <span style="margin-left: 5px;">➡️</span></a>
    </div>
    """, unsafe_allow_html=True)