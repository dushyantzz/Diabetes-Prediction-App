# Import CSS from file
import os

def load_css(css_file):
    with open(css_file, 'r') as f:
        return f'<style>{f.read()}</style>'

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(current_dir, 'custom.css')

# Load the CSS
try:
    st_style = load_css(css_path)
except Exception as e:
    st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top:1rem;}
    </style>
    """

footer = """
    <div class="custom-footer">
        <p>Diabetes Prediction | Data Source: National Institute of Diabetes and Digestive and Kidney Diseases | © 2025 dushyantzz <a href="https://github.com/dushyantzz/Diabetes-Prediction-App.git" target="_blank">GitHub</a></p>
    </div>
    """


head = """
    <div class="app-header">
        <h1>🌟 Diabetes Prediction App 🌟</h1>
        <p>Harness the power of machine learning to predict diabetes and provide insights!</p>
    </div>
    """

mrk = """
<div class="prediction-container prediction-{}">
    <div class="prediction-result">{}</div>
    <div class="prediction-probability">Probability: {}%</div>
    <button class="custom-button {}" onclick="window.location.href='#explanation'">
        View Explanation
    </button>
</div>
"""


about_diabets = """
## What is diabetes?

**Diabetes** is a chronic health condition that affects how your body turns food into energy. It is characterized by high levels of glucose (sugar) in the blood, which occurs because the body either doesn’t produce enough insulin, doesn’t use insulin effectively, or both.

### **Types of Diabetes**:
1. **Type 1 Diabetes**:
   - An autoimmune condition where the immune system attacks and destroys insulin-producing cells in the pancreas.
   - Typically diagnosed in children and young adults.
   - Requires daily insulin injections to manage blood sugar.

2. **Type 2 Diabetes**:
   - The body becomes resistant to insulin, or the pancreas doesn’t produce enough insulin.
   - Often linked to lifestyle factors like obesity, physical inactivity, and poor diet, but genetics also play a role.
   - Managed through lifestyle changes, medications, and sometimes insulin.

3. **Gestational Diabetes**:
   - Occurs during pregnancy when the body cannot make enough insulin to support the increased demand.
   - Usually resolves after childbirth, but it increases the risk of developing type 2 diabetes later in life.

### **Symptoms of Diabetes**:
- Frequent urination
- Excessive thirst
- Extreme hunger
- Fatigue
- Blurred vision
- Slow-healing wounds
- Unexplained weight loss (especially in type 1 diabetes)

### **Complications of Untreated Diabetes**:
- Heart disease
- Kidney damage
- Vision loss (diabetic retinopathy)
- Nerve damage (diabetic neuropathy)
- Increased risk of infections

### **Management**:
- **Diet**: Eating a balanced diet, avoiding high-sugar foods.
- **Exercise**: Regular physical activity to improve insulin sensitivity.
- **Medications**: Insulin therapy or oral diabetes medications.
- **Monitoring**: Regularly checking blood glucose levels.
"""


warn = """
This project (model) was created for hackathon purposes. It has not been reviewed by medical professionals, the model may make mistakes. Please trust only qualified experts.
"""