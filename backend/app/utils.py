import io
from datetime import datetime
from typing import List, Optional, Tuple, Union

import holidays
import numpy as np
import pandas as pd
from prophet import Prophet


ALLOWED_FILL_METHODS = {"interpolate", "ffill", "bfill", "median", "mean", "drop"}


def load_time_series(
    content: Union[bytes, str, pd.DataFrame],
    filename: str,
    date_column: str,
    value_column: str,
    regressors: Optional[Union[str, List[str]]] = None,
) -> pd.DataFrame:
    if isinstance(content, bytes):
        if filename.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.lower().endswith(".json"):
            df = pd.read_json(io.BytesIO(content), orient="records")
        else:
            raise ValueError("Unsupported file type. Use CSV or JSON.")
    elif isinstance(content, pd.DataFrame):
        df = content.copy()
    else:
        raise ValueError("Cannot load input data.")

    if date_column not in df.columns or value_column not in df.columns:
        raise ValueError("Date column or value column not found in uploaded data.")

    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    df = df.dropna(subset=[date_column])
    df = df.sort_values(date_column)

    if regressors:
        if isinstance(regressors, str):
            regressors = [x.strip() for x in regressors.split(",") if x.strip()]
        missing_regressors = [r for r in regressors if r not in df.columns]
        if missing_regressors:
            raise ValueError(f"Missing regressors in data: {missing_regressors}")
    else:
        regressors = []

    prophet_df = df[[date_column, value_column] + regressors].rename(columns={date_column: "ds", value_column: "y"})
    return prophet_df


def apply_fill_strategy(df: pd.DataFrame, method: str) -> pd.DataFrame:
    if method not in ALLOWED_FILL_METHODS:
        raise ValueError(f"Unsupported fill method: {method}")

    if method == "drop":
        return df.dropna()
    if method == "interpolate":
        return df.interpolate(method="time", limit_direction="both")
    if method == "ffill":
        return df.fillna(method="ffill").fillna(method="bfill")
    if method == "bfill":
        return df.fillna(method="bfill").fillna(method="ffill")
    if method == "median":
        return df.fillna(df.median(numeric_only=True))
    if method == "mean":
        return df.fillna(df.mean(numeric_only=True))

    return df


def summarize_data_quality(df: pd.DataFrame, date_column: str, value_column: str) -> dict:
    missing_values = df.isna().sum().to_dict()
    duplicate_rows = int(df.duplicated().sum())
    start_date = df["ds"].min().strftime("%Y-%m-%d") if not df.empty else ""
    end_date = df["ds"].max().strftime("%Y-%m-%d") if not df.empty else ""

    return {
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "start_date": start_date,
        "end_date": end_date,
        "frequency": None,
    }


def build_prophet_model(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
    regressors: Optional[List[str]],
    fill_method: str,
    frequency: str,
    seasonality_mode: str,
    yearly_seasonality: bool,
    weekly_seasonality: bool,
    daily_seasonality: bool,
    holiday_country: Optional[str],
    additional_holidays: Optional[List[str]],
) -> Prophet:
    df = apply_fill_strategy(df, fill_method)

    model = Prophet(
        seasonality_mode=seasonality_mode,
        yearly_seasonality=yearly_seasonality,
        weekly_seasonality=weekly_seasonality,
        daily_seasonality=daily_seasonality,
    )

    if regressors:
        for reg in regressors:
            model.add_regressor(reg)

    if holiday_country:
        try:
            holiday_calendar = holidays.CountryHoliday(holiday_country)
            holiday_df = pd.DataFrame(
                [(date, name) for date, name in holiday_calendar.items()],
                columns=["ds", "holiday"],
            )
            model.add_country_holidays(country_name=holiday_country)
        except Exception:
            holiday_df = pd.DataFrame()
    else:
        holiday_df = pd.DataFrame()

    if additional_holidays:
        extra_holidays = []
        for holiday_date in additional_holidays:
            parsed = pd.to_datetime(holiday_date, errors="coerce")
            if pd.isna(parsed):
                continue
            extra_holidays.append({"ds": parsed, "holiday": "custom_holiday"})
        if extra_holidays:
            holiday_df = pd.concat([holiday_df, pd.DataFrame(extra_holidays)], ignore_index=True)

    if not holiday_df.empty:
        model.holidays = holiday_df

    model.fit(df)
    return model


def generate_forecast(
    model: Prophet,
    df: pd.DataFrame,
    periods: int,
    frequency: str,
    regressors: Optional[List[str]],
) -> pd.DataFrame:
    future = model.make_future_dataframe(periods=periods, freq=frequency)
    if regressors:
        for reg in regressors:
            if reg in df.columns:
                future[reg] = df[reg].ffill().bfill().iloc[-1]
    forecast = model.predict(future)
    columns = ["ds", "yhat", "yhat_lower", "yhat_upper", "trend", "seasonal", "weekly", "yearly"]
    result = forecast[[col for col in columns if col in forecast.columns]]
    return result
