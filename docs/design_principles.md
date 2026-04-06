# Design Principles

## Separation of concerns
- Keep forecasting logic inside the FastAPI backend.
- Use Flask as a proxy/integration layer rather than embedding forecasting directly into the UI.
- Keep the UI lightweight and focused on data input, configuration, and visualization.

## Configurability
- Expose missing-value handling strategies to users so the model can adapt to different data quality scenarios.
- Allow users to configure seasonality and holiday support.
- Accept both file-based and JSON-based datasets for flexible integration.

## Robustness
- Validate data schema before model training.
- Sort and normalize dates to ensure time-based forecasting accuracy.
- Provide fallback strategies for missing values.

## Production readiness
- Use virtual environments for isolation and reproducible installations.
- Provide explicit dependency manifests for backend and Flask proxy services.
- Enable CORS and proxy support for local development and cloud deployment.
- Document startup and deployment steps clearly.
