@echo off
echo Setting up and starting Flask proxy...

cd flask_proxy

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Setting environment variable...
set FORECAST_API_URL=http://localhost:8000/api/forecast

echo Starting Flask proxy...
python app.py

pause