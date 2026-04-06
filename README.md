# Prophet Time Series Forecasting App

A production-ready web application for time series forecasting using Facebook Prophet. Supports univariate and multivariate data, handles missing values, and provides flexible seasonality and holiday configurations.

## Features
- **Data Input**: Upload CSV or JSON files, or paste JSON payloads
- **Data Quality**: Automatic quality checks and missing value handling (interpolation, forward/backfill, mean, median, drop)
- **Forecasting**: Prophet-based forecasting with customizable seasonality, holidays, and regressors
- **UI**: Modern React + TypeScript interface for easy configuration and visualization
- **API**: FastAPI backend with Flask proxy for scalable deployment

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KrishnaKumar2002/Time-Series-Forecasting-App-using-Prophet.git
   cd Time-Series-Forecasting-App-using-Prophet
   git checkout feature/prophet-forecasting-app
   ```

2. **Quick start with batch files** (Windows):
   - Double-click `run_backend.bat` to start the FastAPI backend
   - Double-click `run_proxy.bat` to start the Flask proxy (in a new terminal)
   - Double-click `run_frontend.bat` to start the React frontend (in a new terminal)

3. **Manual setup** (or on other platforms):

   **Start the FastAPI backend**:
   ```bash
   cd backend
   python -m venv .venv
   # On Windows: .\.venv\Scripts\activate
   # On macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   **Start the Flask proxy** (in a new terminal):
   ```bash
   cd flask_proxy
   python -m venv .venv
   # Activate venv as above
   pip install -r requirements.txt
   export FORECAST_API_URL=http://localhost:8000/api/forecast  # Windows: set FORECAST_API_URL=http://localhost:8000/api/forecast
   python app.py
   ```

   **Start the React frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Open your browser** to `http://localhost:3000` and start forecasting!

### Testing with Sample Data

Sample data files are provided in the `samples/` directory:

- `samples/sales_data.csv`: Monthly sales data with regressors
- `samples/temperature_data.json`: Daily temperature readings

#### Using the UI:
1. Go to the app in your browser
2. Upload one of the sample files or paste JSON data
3. Configure forecasting parameters (date/value columns, fill method, seasonality)
4. Click "Run forecast" to see results

#### Using the API directly:
```bash
curl -X POST "http://localhost:5000/api/forecast" \
  -F "date_column=ds" \
  -F "value_column=y" \
  -F "periods=30" \
  -F "file=@samples/sales_data.csv"
```

## Architecture

- **Backend (FastAPI)**: Handles data processing, Prophet model training, and forecasting
- **Proxy (Flask)**: Routes requests between frontend and backend
- **Frontend (React)**: User interface for data upload and result visualization

## Deployment

See `docs/deployment.md` for production deployment options, including Docker and cloud hosting.

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Test locally with sample data
4. Submit a pull request

## License

MIT License

