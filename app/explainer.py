import streamlit as st
import shap
import numpy as np
from loader import model
import matplotlib.pyplot as plt
import pandas as pd


def app(input_data):
    # Add a card container for the explanation section
    st.markdown('<div class="card" id="explanation">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Understanding Your Prediction</div>', unsafe_allow_html=True)

    # Introduction to SHAP explanations
    st.markdown("""
    <div style="padding: 10px; margin-bottom: 20px; background-color: #f8f9fa; border-radius: 5px;">
        <p style="font-size: 16px; color: #333;">
            <strong>What are SHAP explanations?</strong> SHAP (SHapley Additive exPlanations) values help us understand
            how each feature in your data contributes to the prediction. This makes our AI model transparent and interpretable.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Process data for SHAP
    sample_transformed = model.named_steps['feature_engineering'].transform(input_data)
    explainer = shap.TreeExplainer(model.named_steps['model'])
    shap_values_single = explainer.shap_values(sample_transformed)

    # Print the shape of shap_values_single to debug
    print(f"SHAP values shape: {np.array(shap_values_single).shape}")

    # Handle expected_value based on its type
    if isinstance(explainer.expected_value, list):
        base_value = explainer.expected_value[1]  # Use the positive class (class 1)
    else:
        base_value = explainer.expected_value

    # Extract SHAP values for the positive class (class 1)
    # For this specific model, we know it's a binary classifier
    # The shape is likely (1, n_features, 2) where 2 is for the two classes
    # We want the values for class 1 (positive class)
    if isinstance(shap_values_single, list) and len(shap_values_single) > 1:
        # If it's a list of arrays (one per class)
        shap_values_class_1 = shap_values_single[1][0]  # Class 1, first sample
    elif isinstance(shap_values_single, np.ndarray):
        if shap_values_single.ndim == 3:
            # If it's a 3D array (samples, features, classes)
            shap_values_class_1 = shap_values_single[0, :, 1]  # First sample, all features, class 1
        else:
            # If it's a 2D array (samples, features)
            shap_values_class_1 = shap_values_single[0]  # First sample
    else:
        # Fallback
        shap_values_class_1 = shap_values_single[0]

    # Create tabs for different explanations
    tab1, tab2, tab3 = st.tabs(["🔍 Your Inputs", "📊 Waterfall Plot", "⚖️ Force Plot"])

    # Tab 1: Your Inputs with beautiful formatting
    with tab1:
        st.markdown('<div style="padding: 15px;">', unsafe_allow_html=True)

        # Get the input data values for display
        # These values will be used in the formatted HTML table

        # Create a styled table for inputs
        # Create a formatted HTML table for the input data
        pregnancies = input_data.iloc[0]['Pregnancies']
        glucose = input_data.iloc[0]['Glucose']
        insulin = input_data.iloc[0]['Insulin']
        bmi = input_data.iloc[0]['BMI']
        age = input_data.iloc[0]['Age']

        st.markdown(f"""
        <style>
        .input-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        .input-table th {{
            background: linear-gradient(to right, #1a1a2e, #16213e);
            color: white;
            text-align: left;
            padding: 12px 15px;
            font-weight: 600;
        }}
        .input-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
            color: #333333;
        }}
        .input-table tr {{
            background-color: #ffffff;
        }}
        .input-table tr:nth-child(even) {{
            background-color: #f0f2f5;
        }}
        .input-table tr:last-child td {{
            border-bottom: none;
        }}
        .input-table tr:hover {{
            background-color: #e6f7ff;
        }}
        </style>

        <h3 style="color: #1a1a2e; font-weight: 600; background: linear-gradient(to right, #1a1a2e, #16213e); color: white; padding: 10px 15px; border-radius: 5px; display: inline-block;">Your Health Parameters</h3>
        <table class="input-table">
            <tr>
                <th>Parameter</th>
                <th>Your Value</th>
                <th>Normal Range</th>
            </tr>
            <tr>
                <td>Pregnancies</td>
                <td>{pregnancies}</td>
                <td>N/A</td>
            </tr>
            <tr>
                <td>Glucose</td>
                <td>{glucose} mg/dL</td>
                <td>70-99 mg/dL (fasting)</td>
            </tr>
            <tr>
                <td>Insulin</td>
                <td>{insulin} μU/mL</td>
                <td>2-25 μU/mL (fasting)</td>
            </tr>
            <tr>
                <td>BMI</td>
                <td>{bmi}</td>
                <td>18.5-24.9</td>
            </tr>
            <tr>
                <td>Age</td>
                <td>{age} years</td>
                <td>N/A</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

        # Add a note about the parameters
        st.info("""
        **Note**: These are the values you entered that were used to make the prediction. The normal ranges are general
        guidelines and may vary based on individual factors and specific medical contexts.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

    # Tab 2: SHAP Waterfall Plot with explanation
    with tab2:
        st.markdown('<div style="padding: 15px;">', unsafe_allow_html=True)

        # Create two columns
        wcol1, wcol2 = st.columns([3, 2])

        with wcol1:
            # Create a more attractive feature importance plot instead of waterfall plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Get feature importance values
            feature_importance = pd.DataFrame({
                'Feature': sample_transformed.columns.tolist(),
                'Importance': np.abs(shap_values_class_1)
            }).sort_values('Importance', ascending=False)

            # Create a colorful gradient for the bars
            colors = plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, len(feature_importance)))

            # Plot feature importance with improved styling
            bars = ax.barh(feature_importance['Feature'], feature_importance['Importance'], color=colors)

            # Add value labels to the bars
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                        f'{width:.3f}', ha='left', va='center', fontweight='bold')

            # Style the plot
            ax.set_title('Feature Impact on Prediction', fontsize=16, fontweight='bold', color='#2c3e50')
            ax.set_xlabel('Absolute SHAP Value (Impact on Prediction)', fontsize=12, fontweight='bold')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis='y', labelsize=12, labelcolor='#2c3e50')
            ax.tick_params(axis='x', labelsize=10)

            # Add a grid for better readability
            ax.grid(axis='x', linestyle='--', alpha=0.6)

            # Style the plot
            fig.patch.set_facecolor("#f8f9fa")
            fig.patch.set_alpha(0.8)
            ax.set_title("Feature Impact on Prediction", fontsize=14, fontweight='bold')
            ax.set_facecolor("#ffffff")

            # Display the plot
            st.pyplot(fig)

        with wcol2:
            st.markdown("""
            <div style="background-color: #f0f2f5; padding: 20px; border-radius: 10px; height: 100%; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); border-left: 4px solid #6e8efb;">
            <h4 style="color: #2c3e50; margin-top: 0; font-size: 1.2rem; font-weight: 600;">How to Read This Plot</h4>
            <ul style="padding-left: 20px; line-height: 1.6; color: #333333;">
                <li><strong style="color: #0056b3;">Longer Bars</strong>: Features with greater impact on your prediction.</li>
                <li><strong style="color: #0056b3;">Top Features</strong>: The most important factors for your specific case.</li>
                <li><strong style="color: #0056b3;">Color Gradient</strong>: Helps visualize the relative importance of each feature.</li>
                <li><strong style="color: #0056b3;">Values</strong>: The numbers show the exact impact magnitude of each feature.</li>
            </ul>
            <p style="margin-top: 15px; font-style: italic; color: #333333;">This personalized analysis shows which health factors are most relevant to your diabetes risk assessment.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Tab 3: SHAP Force Plot with explanation
    with tab3:
        st.markdown('<div style="padding: 15px;">', unsafe_allow_html=True)

        # Create the force plot
        try:
            # Try to create the force plot with the processed SHAP values
            force_plot_html = shap.force_plot(
                base_value=base_value,
                shap_values=shap_values_class_1,
                features=sample_transformed.iloc[0].values,
                feature_names=sample_transformed.columns.tolist(),
                link="logit"
            )
        except Exception as e:
            # If there's an error, try an alternative approach
            st.error(f"Error creating force plot: {str(e)}")
            # Create a simple text explanation instead
            st.write("Feature importance values:")
            feature_importance = pd.DataFrame({
                'Feature': sample_transformed.columns.tolist(),
                'Importance': np.abs(shap_values_class_1)
            }).sort_values('Importance', ascending=False)
            st.dataframe(feature_importance)
            # Create a dummy force plot object to avoid errors
            force_plot_html = None

        # Add explanation before the plot
        st.markdown("""
        <div style="background-color: #f0f2f5; padding: 20px; border-radius: 10px; margin-bottom: 25px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); border-left: 4px solid #6e8efb;">
            <h4 style="color: #2c3e50; margin-top: 0; font-size: 1.2rem; font-weight: 600;">Feature Interaction Visualization</h4>
            <p style="line-height: 1.6; color: #333333;">This interactive visualization shows how your health parameters work together to influence the prediction:</p>
            <ul style="padding-left: 20px; line-height: 1.6; color: #333333;">
                <li><strong style="color: #d9534f;">Red Features</strong>: Push your prediction toward higher diabetes risk</li>
                <li><strong style="color: #0275d8;">Blue Features</strong>: Push your prediction toward lower diabetes risk</li>
                <li><strong style="color: #333333;">Feature Width</strong>: Indicates the strength of each feature's influence</li>
            </ul>
            <p style="margin-top: 10px; font-style: italic; color: #333333;">The visualization helps you understand how different factors combine to produce your final risk assessment.</p>
        </div>
        """, unsafe_allow_html=True)

        # Add SHAP JS visualization with improved styling if force_plot_html is not None
        if force_plot_html is not None:
            try:
                # Add custom CSS to improve force plot visibility
                custom_css = """
                <style>
                .force-bar-labels text {
                    fill: #333333 !important;
                    font-weight: 600 !important;
                    font-size: 12px !important;
                }
                .force-bar-axis text {
                    fill: #333333 !important;
                    font-weight: 600 !important;
                    font-size: 12px !important;
                }
                </style>
                """
                force_plot_html = f"<head>{shap.getjs()}{custom_css}</head><body style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); border: 1px solid #e0e0e0;'>{force_plot_html.html()}</body>"
                st.components.v1.html(force_plot_html, height=220)
            except Exception as e:
                st.error(f"Error displaying force plot: {str(e)}")

        # Add feature importance explanation
        st.markdown("""
        <div style="margin-top: 25px; background-color: #f0f2f5; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); border-left: 4px solid #20bf6b;">
            <h4 style="color: #2c3e50; margin-top: 0; font-size: 1.2rem; font-weight: 600;">What This Means For You</h4>
            <p style="line-height: 1.6; color: #333333;">The features with the largest impact are the most significant for your specific diabetes risk assessment:</p>
            <ul style="padding-left: 20px; line-height: 1.6; color: #333333;">
                <li><strong style="color: #198754;">Focus Areas</strong>: Consider discussing the top factors with your healthcare provider</li>
                <li><strong style="color: #198754;">Personalized Insights</strong>: These factors may differ from general diabetes risk factors</li>
                <li><strong style="color: #198754;">Actionable Information</strong>: Some factors (like glucose levels) can be modified through lifestyle changes</li>
            </ul>
            <p style="margin-top: 10px; font-style: italic; color: #333333;">Remember that this analysis is based on your specific data and may provide valuable insights for your health journey.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Close the card container
    st.markdown('</div>', unsafe_allow_html=True)

    # Add a button to navigate to the next section
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <a href="#performance" class="custom-button" style="padding: 0.9rem 1.8rem; font-size: 1.1rem; box-shadow: 0 6px 12px rgba(110, 142, 251, 0.3);">View Model Performance <span style="margin-left: 5px;">➡️</span></a>
    </div>
    """, unsafe_allow_html=True)