from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..services import simulation_service
from .sensors import ingest_reading
from ..schemas import ReadingIn

router = APIRouter(tags=["simulation"])


def _apply_scenario(db: Session, scenario: dict):
    sensor = db.query(models.Sensor).first()
    payload = ReadingIn(
        sensor_id=sensor.sensor_code,
        water_level_cm=scenario["water_level_cm"],
        rainfall_mm_1h=scenario["rainfall_mm_1h"],
        rainfall_mm_3h=scenario["rainfall_mm_3h"],
        rainfall_forecast_mm_6h=scenario["rainfall_forecast_mm_6h"],
        source="simulated",
    )
    return ingest_reading(payload, db)


@router.post("/api/simulate/start")
def simulate_start(db: Session = Depends(get_db)):
    scenario = simulation_service.start_simulation()
    result = _apply_scenario(db, scenario)
    return {"stage": "Normal", "prediction": result}


@router.post("/api/simulate/step")
def simulate_step(db: Session = Depends(get_db)):
    scenario = simulation_service.next_step()
    result = _apply_scenario(db, scenario)
    stage_names = ["Normal", "Watch", "Flood Warning"]
    idx = simulation_service._state["step"]
    return {"stage": stage_names[idx], "prediction": result}


@router.post("/api/simulate/reset")
def simulate_reset():
    simulation_service.reset()
    return {"status": "reset"}
