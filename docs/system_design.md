# System Design for Prophet Forecasting App

## Architecture Overview

The system is composed of three primary services:
1. **FastAPI forecasting service**
   - Receives timeseries input via file upload or JSON payload
   - Performs data quality validation and missing-value handling
   - Builds and trains Prophet models with optional regressors and holiday seasonality
   - Returns forecasted values, historical preview, and data quality metrics

2. **Flask proxy service**
   - Acts as a lightweight integration layer between the frontend and FastAPI backend
   - Enables a single endpoint for the UI and simplifies deployment network topology
   - Helps isolate frontend traffic from backend model runtime behavior

3. **React + TypeScript frontend**
   - Provides an interactive UI for uploading data and selecting forecasting configuration
   - Shows quality report, recent history, and forecast results
   - Can be deployed as a static site or served via a Node-based frontend server

## Data Flow

1. User uploads a CSV/JSON file or pastes JSON payload in the UI.
2. The React app submits the data to Flask at `/api/forecast`.
3. Flask forwards the request to FastAPI at `/api/forecast`.
4. FastAPI loads and validates the data, applies fill strategies, and trains a Prophet model.
5. Forecast results and quality diagnostics are returned through Flask back to the UI.

## Fault handling and resiliency

- Input validation detects missing required columns before model training.
- Data quality report identifies missing values, duplicate rows, and date range.
- Missing-value strategy selection prevents model failure on sparse series.
- CORS is enabled for frontend compatibility.

## Scalability

- The backend can be scaled horizontally behind a load balancer.
- The Flask proxy can be replaced with API gateway routing without changing the UI.
- Static frontend deployment can be decoupled from API services.
