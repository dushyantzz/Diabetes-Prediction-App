import streamlit as st

def app():
    """Navigation bar component for the Diabetes Prediction App"""

    # Create a container for the navigation bar
    with st.container():
        # Apply custom styling to the navigation bar
        st.markdown("""
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .navbar-brand {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
            margin-right: 1rem;
        }

        .navbar-links {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                padding: 0.8rem;
            }

            .navbar-brand {
                margin-bottom: 0.8rem;
            }

            .navbar-links {
                justify-content: center;
            }

            .navbar-title {
                font-size: 1.5rem;
            }
        }

        .navbar-link {
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
            background-color: rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        .navbar-link:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .navbar-link-icon {
            font-size: 1.1rem;
        }

        .navbar-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: white;
            margin: 0;
            text-shadow: 0 1px 1px rgba(0,0,0,0.2);
        }
        </style>

        <div class="navbar">
            <div class="navbar-brand">
                <h1 class="navbar-title">🌟 Diabetes Prediction App</h1>
            </div>
            <div class="navbar-links">
                <a href="#prediction" class="navbar-link"><span class="navbar-link-icon">📊</span> Prediction</a>
                <a href="#explanation" class="navbar-link"><span class="navbar-link-icon">🔍</span> Explanation</a>
                <a href="#food-recognition" class="navbar-link"><span class="navbar-link-icon">📷</span> Food Recognition</a>
                <a href="#meal-recommendations" class="navbar-link"><span class="navbar-link-icon">🍽️</span> Meal Plans</a>
                <a href="#about" class="navbar-link"><span class="navbar-link-icon">ℹ️</span> About</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Add a brief introduction below the navbar
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.1rem; color: #555;">
            Harness the power of machine learning to predict diabetes risk and get personalized insights!
        </p>
    </div>
    """, unsafe_allow_html=True)
