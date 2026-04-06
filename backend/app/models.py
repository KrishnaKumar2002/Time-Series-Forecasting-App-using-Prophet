from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class QualityReport(BaseModel):
    missing_values: Dict[str, int]
    duplicate_rows: int
    start_date: str
    end_date: str
    frequency: Optional[str] = None


class ForecastResponse(BaseModel):
    forecast: List[Dict[str, Any]]
    history: List[Dict[str, Any]]
    quality_report: QualityReport
    metadata: Dict[str, Any]
