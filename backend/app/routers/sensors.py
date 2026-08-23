from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .. import models, schemas
from ..database import get_db
from ..services import risk_engine, ml_predictor, alert_service, route_service

router = APIRouter(tags=["sensors"])


@router.get("/api/sensors")
def list_sensors(db: Session = Depends(get_db)):
    sensors = db.query(models.Sensor).all()
    out = []
    for s in sensors:
        last_reading = (
            db.query(models.Reading)
            .filter(models.Reading.sensor_id == s.id)
            .order_by(models.Reading.timestamp.desc())
            .first()
        )
        last_pred = (
            db.query(models.Prediction)
            .filter(models.Prediction.sensor_id == s.id)
            .order_by(models.Prediction.timestamp.desc())
            .first()
        )
        out.append({
            "id": s.id,
            "sensor_code": s.sensor_code,
            "location_name": s.location_name,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "status": s.status,
            "water_level_cm": last_reading.water_level_cm if last_reading else None,
            "rainfall_mm_1h": last_reading.rainfall_mm_1h if last_reading else None,
            "battery_percent": last_reading.battery_percent if last_reading else None,
            "last_updated": last_reading.timestamp.isoformat() if last_reading else None,
            "risk_level": last_pred.risk_level if last_pred else "LOW",
        })
    return out


@router.get("/api/sensors/{sensor_id}/history")
def sensor_history(sensor_id: int, db: Session = Depends(get_db)):
    readings = (
        db.query(models.Reading)
        .filter(models.Reading.sensor_id == sensor_id)
        .order_by(models.Reading.timestamp.asc())
        .all()
    )
    predictions = (
        db.query(models.Prediction)
        .filter(models.Prediction.sensor_id == sensor_id)
        .order_by(models.Prediction.timestamp.asc())
        .all()
    )
    return {
        "readings": [
            {
                "timestamp": r.timestamp.isoformat(),
                "water_level_cm": r.water_level_cm,
                "rainfall_mm_1h": r.rainfall_mm_1h,
            } for r in readings
        ],
        "predictions": [
            {
                "timestamp": p.timestamp.isoformat(),
                "risk_level": p.risk_level,
                "risk_probability": p.risk_probability,
            } for p in predictions
        ],
    }


@router.post("/api/readings", response_model=schemas.PredictionOut)
def ingest_reading(payload: schemas.ReadingIn, db: Session = Depends(get_db)):
    sensor = None
    if payload.sensor_id:
        sensor = db.query(models.Sensor).filter(models.Sensor.sensor_code == payload.sensor_id).first()
    if not sensor:
        sensor = db.query(models.Sensor).first()
    if not sensor:
        raise HTTPException(404, "No sensor found. Seed data first.")

    prev = (
        db.query(models.Reading)
        .filter(models.Reading.sensor_id == sensor.id)
        .order_by(models.Reading.timestamp.desc())
        .first()
    )
    prev_level = prev.water_level_cm if prev else None

    reading = models.Reading(
        sensor_id=sensor.id,
        water_level_cm=payload.water_level_cm,
        rainfall_mm_1h=payload.rainfall_mm_1h,
        rainfall_mm_3h=payload.rainfall_mm_3h,
        rainfall_forecast_mm_6h=payload.rainfall_forecast_mm_6h,
        battery_percent=payload.battery_percent,
        source=payload.source,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

    rise_rate = risk_engine.compute_rise_rate(prev_level, payload.water_level_cm)
    ml_prob = ml_predictor.ml_probability(
        payload.water_level_cm, payload.rainfall_mm_1h, payload.rainfall_mm_3h,
        payload.rainfall_forecast_mm_6h, rise_rate, hour=datetime.utcnow().hour
    )
    result = risk_engine.run_risk_engine(
        payload.water_level_cm, payload.rainfall_mm_1h, payload.rainfall_mm_3h,
        payload.rainfall_forecast_mm_6h, prev_level, ml_prob
    )

    pred = models.Prediction(
        sensor_id=sensor.id,
        risk_level=result["risk_level"],
        risk_probability=result["risk_probability"],
        estimated_water_level_cm_6h=result["estimated_water_level_cm_6h"],
        rate_of_rise_cm_per_hour=result["rate_of_rise_cm_per_hour"],
        model_version="rules+xgb-v1" if ml_prob is not None else "rules-v1",
    )
    db.add(pred)
    db.commit()

    if result["alert_required"]:
        shelters = db.query(models.Shelter).all()
        route = route_service.find_safe_route(sensor.latitude, sensor.longitude, shelters, any_high_risk=True)
        shelter_obj = None
        note = ""
        if route["status"] == "ok":
            shelter_obj = db.query(models.Shelter).get(route["shelter"]["id"])
            note = route.get("route_note", "")
        alert_service.maybe_create_alert(db, sensor, result["risk_level"], result["message"], shelter_obj, note)

    return schemas.PredictionOut(
        sensor_id=sensor.sensor_code,
        **result
    )
