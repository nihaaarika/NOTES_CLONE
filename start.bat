@echo off
REM Quick Start Script for Notion Clone (Windows)

echo 🚀 Notion Clone - Quick Start
echo ==============================
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)
echo ✓ Python found: 
python --version

REM Create virtual environment
echo.
echo ✓ Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo ✓ Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed successfully

REM Create data directory
echo.
echo ✓ Setting up data directory...
if not exist "data" mkdir data
echo ✓ Data directory ready

REM Run app
echo.
echo ✓ Starting Notion Clone...
echo.
echo 🌐 App will open in your browser at: http://localhost:8501
echo 📚 Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause