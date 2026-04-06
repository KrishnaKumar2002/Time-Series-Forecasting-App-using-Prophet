@echo off
echo Setting up and starting FastAPI backend...

cd backend

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create venv with python, trying python3...
        python3 -m venv .venv
        if errorlevel 1 (
            echo Failed to create virtual environment. Please check Python installation.
            pause
            exit /b 1
        )
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Starting FastAPI server...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause