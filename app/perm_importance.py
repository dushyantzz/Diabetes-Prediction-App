import streamlit as st
import pandas as pd
import numpy as np
from sklearn.inspection import permutation_importance
from loader import X, y, model
import plotly.express as px
import plotly.graph_objects as go

def app():
    # Add a card container for the feature importance section
    st.markdown('<div class="card" id="importance">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Feature Importance Analysis</div>', unsafe_allow_html=True)

    # Introduction to feature importance
    st.markdown("""
    <div style="padding: 15px; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <p style="font-size: 16px; color: #333;">
            <strong>Understanding Feature Importance</strong>: This analysis shows which health parameters have the most
            significant impact on diabetes prediction. Features with higher importance scores have a stronger influence
            on the model's predictions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Calculate permutation importance
    with st.spinner("Calculating feature importance... This may take a moment."):
        perm_importance = permutation_importance(model, X, model.predict(X), n_repeats=10, random_state=42)

    # Create DataFrame with results
    perm_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': perm_importance.importances_mean,
        'Std': perm_importance.importances_std
    }).sort_values(by='Importance', ascending=False)

    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["📈 Visual Analysis", "📋 Detailed Breakdown"])

    # Tab 1: Visual representation of feature importance
    with tab1:
        # Create two columns for layout
        col1, col2 = st.columns([3, 2])

        with col1:
            # Create enhanced horizontal bar chart
            # Add color gradient based on importance
            colors = px.colors.sequential.Blues_r[:len(perm_importance_df)]

            fig = px.bar(
                perm_importance_df,
                y='Feature',
                x='Importance',
                orientation='h',
                error_x='Std',  # Add error bars
                color='Importance',  # Color by importance
                color_continuous_scale='Blues',  # Use a blue color scale
                labels={'Importance': 'Permutation Importance', 'Feature': 'Health Parameter'},
                title='Feature Importance Ranking'
            )

            # Customize layout
            fig.update_layout(
                yaxis=dict(autorange='reversed'),
                plot_bgcolor='rgba(240,240,240,0.2)',
                height=500,
                margin=dict(l=20, r=20, t=40, b=20),
                coloraxis_showscale=False,
                xaxis_title="Importance Score",
                yaxis_title="",
                font=dict(family="Poppins, sans-serif")
            )

            # Add annotations for top features
            top_feature = perm_importance_df.iloc[0]['Feature']
            top_importance = perm_importance_df.iloc[0]['Importance']

            fig.add_annotation(
                x=top_importance,
                y=top_feature,
                text="Most Important",
                showarrow=True,
                arrowhead=1,
                ax=50,
                ay=-30,
                font=dict(size=12, color="#6e8efb"),
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="#6e8efb",
                borderwidth=1,
                borderpad=4
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Add explanation of the visualization
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; height: 100%;">
                <h4 style="color: white; background: linear-gradient(to right, #1a1a2e, #16213e); padding: 8px 12px; border-radius: 5px; display: inline-block; margin-top: 0;">How to Interpret This Chart</h4>
                <p style="color: #333333;">The chart shows how much each feature contributes to the model's predictions:</p>
                <ul style="color: #333333;">
                    <li><strong style="color: #0056b3;">Longer bars</strong> indicate features with greater impact on diabetes prediction</li>
                    <li><strong style="color: #0056b3;">Error bars</strong> show the variability in importance across multiple permutations</li>
                    <li><strong style="color: #0056b3;">Top features</strong> are the most critical health parameters to monitor</li>
                </ul>
                <p style="margin-top: 20px; color: #333333;"><strong style="color: #0056b3;">Key Insight:</strong> Glucose level is typically the strongest predictor of diabetes risk, followed by BMI and age-related factors.</p>
            </div>
            """, unsafe_allow_html=True)

    # Tab 2: Detailed breakdown of feature importance
    with tab2:
        # Create a styled table for feature importance
        st.markdown("""
        <style>
        .importance-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        .importance-table th {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            color: white;
            text-align: left;
            padding: 12px 15px;
        }
        .importance-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }
        .importance-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .importance-table tr:last-child td {
            border-bottom: none;
        }
        .importance-table tr:hover {
            background-color: #f1f1f1;
        }
        .importance-bar {
            background: linear-gradient(90deg, #6e8efb, transparent);
            height: 20px;
            border-radius: 10px;
        }
        </style>

        <h3 style="color: white; background: linear-gradient(to right, #1a1a2e, #16213e); padding: 10px 15px; border-radius: 5px; display: inline-block;">Feature Importance Details</h3>
        <table class="importance-table">
            <tr>
                <th>Rank</th>
                <th>Feature</th>
                <th>Importance Score</th>
                <th>Relative Importance</th>
                <th>Medical Relevance</th>
            </tr>
        """, unsafe_allow_html=True)

        # Calculate relative importance (percentage of max)
        max_importance = perm_importance_df['Importance'].max()

        # Medical relevance descriptions
        medical_relevance = {
            'Glucose': "High blood glucose is a primary indicator of diabetes.",
            'BMI': "Higher BMI is associated with increased insulin resistance.",
            'Age': "Risk of type 2 diabetes increases with age.",
            'Insulin': "Abnormal insulin levels indicate potential metabolic issues.",
            'Pregnancies': "Multiple pregnancies can affect glucose metabolism.",
            'DiabetesPedigreeFunction': "Family history increases diabetes risk.",
            'BloodPressure': "Hypertension often co-occurs with diabetes.",
            'SkinThickness': "Can indicate subcutaneous fat distribution."
        }

        # Add rows for each feature
        for i, (index, row) in enumerate(perm_importance_df.iterrows()):
            feature = row['Feature']
            importance = row['Importance']
            relative_importance = (importance / max_importance) * 100

            # Get medical relevance or default text
            relevance = medical_relevance.get(feature, "Contributes to the overall prediction.")

            # Create visual bar representing importance
            bar_width = int(relative_importance)

            st.markdown(f"""
            <tr>
                <td>{i+1}</td>
                <td><strong>{feature}</strong></td>
                <td>{importance:.4f}</td>
                <td>
                    <div class="importance-bar" style="width: {bar_width}%;"></div>
                    <div style="text-align: right; font-size: 0.8rem;">{relative_importance:.1f}%</div>
                </td>
                <td>{relevance}</td>
            </tr>
            """, unsafe_allow_html=True)

        st.markdown("</table>", unsafe_allow_html=True)

        # Add explanation about permutation importance
        st.markdown("""
        <div style="margin-top: 30px; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            <h4 style="margin-top: 0; color: white; background: linear-gradient(to right, #1a1a2e, #16213e); padding: 8px 12px; border-radius: 5px; display: inline-block;">About Permutation Importance</h4>
            <p style="color: #333333;">Permutation importance measures how much model performance decreases when a single feature's values are randomly shuffled. This approach:</p>
            <ul style="color: #333333;">
                <li><strong style="color: #0056b3;">Is model-agnostic</strong> (works with any machine learning model)</li>
                <li><strong style="color: #0056b3;">Reflects the actual impact</strong> on prediction accuracy</li>
                <li><strong style="color: #0056b3;">Helps identify</strong> which health parameters should be prioritized for monitoring</li>
            </ul>
            <p style="color: #333333;">Features with higher importance scores have a stronger influence on diabetes prediction and should receive more attention in clinical assessment.</p>
        </div>
        """, unsafe_allow_html=True)

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Add a button to navigate to the about section
    st.markdown("""
    <div style="text-align: center; margin: 30px 0;">
        <a href="#about" class="custom-button">Learn About Diabetes</a>
    </div>
    """, unsafe_allow_html=True)