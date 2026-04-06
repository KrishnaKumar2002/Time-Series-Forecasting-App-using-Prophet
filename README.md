# Prophet Time Series Forecasting App

This repository contains a production-ready forecasting solution using:
- **FastAPI** backend for Prophet-based forecasting
- **Flask** proxy service for frontend integration
- **React + TypeScript + Vite** frontend UI
- Support for **CSV / JSON / single-series data**, **data quality checks**, and **missing value filling strategies**

## Features
- Load CSV or JSON timeseries data
- Handle missing values using interpolation, forward/backfill, mean, median, and drop strategies
- Configure Prophet seasonality, holidays, and regressors
- Forecast univariate and multivariate time series data
- Proxy requests through Flask to FastAPI for flexible deployment

## Getting started

### Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Flask proxy
```powershell
cd flask_proxy
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
set FORECAST_API_URL=http://localhost:8000/api/forecast
python app.py
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

The UI will proxy requests to `http://localhost:5000/api/forecast`.

## Branch
This work is created on branch `feature/prophet-forecasting-app`.

## Documentation
- `docs/system_design.md`
- `docs/design_principles.md`
- `docs/deployment.md`
