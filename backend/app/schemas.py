from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ReadingIn(BaseModel):
    sensor_id: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    water_level_cm: float
    rainfall_mm_1h: float = 0
    rainfall_mm_3h: float = 0
    rainfall_forecast_mm_6h: float = 0
    battery_percent: float = 100
    source: str = "simulated"


class PredictionOut(BaseModel):
    sensor_id: str
    risk_level: str
    risk_probability: float
    current_water_level_cm: float
    estimated_water_level_cm_6h: float
    rate_of_rise_cm_per_hour: float
    alert_required: bool
    message: str


class RoutePointIn(BaseModel):
    latitude: float
    longitude: float
