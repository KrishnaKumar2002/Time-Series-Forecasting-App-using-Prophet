# Deployment Guide

## Local development

1. Start the FastAPI forecasting backend:
   - `cd backend`
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
   - `pip install -r requirements.txt`
   - `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

2. Start the Flask proxy:
   - `cd flask_proxy`
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
   - `pip install -r requirements.txt`
   - `set FORECAST_API_URL=http://localhost:8000/api/forecast`
   - `python app.py`

3. Start the React frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Production deployment patterns

- Deploy the FastAPI service as a container or ASGI app behind an application gateway.
- Deploy the Flask proxy separately or consolidate routing into a single API gateway.
- Build the frontend with `npm run build` and serve static assets from a CDN or static web host.

## Docker deployment (optional)

- Create Docker images for `backend` and `flask_proxy`.
- Use a reverse proxy like Nginx or Traefik to route `/api` traffic to the Flask proxy and static assets to the frontend.
- Keep environment values like `FORECAST_API_URL` configurable at runtime.
