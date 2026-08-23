from fastapi import APIRouter
from datetime import datetime
from .. import schemas
from ..services import risk_engine, ml_predictor

router = APIRouter(tags=["predictions"])


@router.post("/api/predict", response_model=schemas.PredictionOut)
def predict(payload: schemas.ReadingIn):
    rise_rate = 0.0  # no prior state in stateless predict call
    ml_prob = ml_predictor.ml_probability(
        payload.water_level_cm, payload.rainfall_mm_1h, payload.rainfall_mm_3h,
        payload.rainfall_forecast_mm_6h, rise_rate, hour=datetime.utcnow().hour
    )
    result = risk_engine.run_risk_engine(
        payload.water_level_cm, payload.rainfall_mm_1h, payload.rainfall_mm_3h,
        payload.rainfall_forecast_mm_6h, None, ml_prob
    )
    return schemas.PredictionOut(sensor_id=payload.sensor_id or "SEN-000", **result)
