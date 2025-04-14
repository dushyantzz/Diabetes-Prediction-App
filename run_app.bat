@echo off
echo Starting Diabetes Prediction Application...

REM Activate the virtual environment
call diabetes_env\Scripts\activate.bat

REM Check if requirements are installed, if not install them
pip freeze | findstr /C:"streamlit" > nul
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed.
)

REM Run the Streamlit application
echo Starting Streamlit application...
streamlit run main.py

REM Deactivate the virtual environment when done
call deactivate
