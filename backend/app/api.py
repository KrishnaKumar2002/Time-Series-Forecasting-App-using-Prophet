import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, PositiveInt

from .models import ForecastInput, ForecastResponse, QualityReport
from .utils import (
    build_prophet_model,
    generate_forecast,
    load_time_series,
    summarize_data_quality,
)

router = APIRouter()

class JsonPayload(BaseModel):
    data: List[Dict[str, Any]]
    date_column: str
    value_column: str
    regressors: Optional[List[str]] = None
    fill_method: Optional[str] = "interpolate"
    frequency: Optional[str] = "D"
    periods: PositiveInt = 30
    seasonality_mode: Optional[str] = "additive"
    yearly_seasonality: Optional[bool] = True
    weekly_seasonality: Optional[bool] = True
    daily_seasonality: Optional[bool] = False
    holiday_country: Optional[str] = None
    additional_holidays: Optional[List[str]] = None

@router.post("/forecast", response_model=ForecastResponse)
async def forecast(
    date_column: str = Form(...),
    value_column: str = Form(...),
    frequency: str = Form("D"),
    periods: PositiveInt = Form(30),
    fill_method: str = Form("interpolate"),
    seasonality_mode: str = Form("additive"),
    yearly_seasonality: bool = Form(True),
    weekly_seasonality: bool = Form(True),
    daily_seasonality: bool = Form(False),
    holiday_country: Optional[str] = Form(None),
    regressors: Optional[str] = Form(None),
    additional_holidays: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    json_payload: Optional[str] = Form(None),
) -> ForecastResponse:
    if not file and not json_payload:
        raise HTTPException(status_code=400, detail="A CSV/JSON file or JSON payload is required.")

    if file:
        contents = await file.read()
        df = load_time_series(contents, file.filename, date_column, value_column, regressors)
    else:
        try:
            payload = JsonPayload.parse_raw(json_payload)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {exc}")
        df = pd.DataFrame(payload.data)
        if payload.regressors:
            regressors = payload.regressors
        else:
            regressors = None
        df = load_time_series(df, payload.date_column, payload.value_column, regressors)
        date_column = payload.date_column
        value_column = payload.value_column
        fill_method = payload.fill_method
        frequency = payload.frequency
        periods = payload.periods
        seasonality_mode = payload.seasonality_mode
        yearly_seasonality = payload.yearly_seasonality
        weekly_seasonality = payload.weekly_seasonality
        daily_seasonality = payload.daily_seasonality
        holiday_country = payload.holiday_country
        additional_holidays = payload.additional_holidays

    quality_report = summarize_data_quality(df, date_column, value_column)

    model = build_prophet_model(
        df,
        date_column=date_column,
        value_column=value_column,
        regressors=regressors,
        fill_method=fill_method,
        frequency=frequency,
        seasonality_mode=seasonality_mode,
        yearly_seasonality=yearly_seasonality,
        weekly_seasonality=weekly_seasonality,
        daily_seasonality=daily_seasonality,
        holiday_country=holiday_country,
        additional_holidays=additional_holidays,
    )

    forecast_df = generate_forecast(model, df, periods, frequency, regressors)
    forecast_records = forecast_df.to_dict(orient="records")
    history_records = df.tail(100).to_dict(orient="records")

    return ForecastResponse(
        forecast=forecast_records,
        history=history_records,
        quality_report=quality_report,
        metadata={
            "rows": len(df),
            "columns": list(df.columns),
            "forecast_periods": periods,
        },
    )
