@echo off
echo Setting up and starting FastAPI backend...

cd backend

if not exist .venv (
    echo Creating virtual environment...
    python -m venv --clear .venv --without-pip
    if errorlevel 1 (
        echo Failed to create venv with python, trying python3...
        python3 -m venv --clear .venv --without-pip
        if errorlevel 1 (
            echo Failed to create virtual environment. Please check Python installation.
            pause
            exit /b 1
        )
    )
    echo Installing pip in venv...
    .venv\Scripts\python -m ensurepip --upgrade
    if errorlevel 1 (
        echo Failed to install pip. Trying alternative method...
        curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        .venv\Scripts\python get-pip.py
        del get-pip.py
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