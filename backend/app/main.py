from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router

app = FastAPI(
    title="Prophet Time Series Forecasting API",
    description="A production-ready forecasting API for CSV/JSON/time-series input with Prophet and flexible data quality handling.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}
