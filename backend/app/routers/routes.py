from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..services import route_service

router = APIRouter(tags=["routes"])


@router.post("/api/routes/safe")
def safe_route(payload: schemas.RoutePointIn, db: Session = Depends(get_db)):
    shelters = db.query(models.Shelter).all()
    any_high = db.query(models.Prediction).filter(models.Prediction.risk_level == "HIGH").order_by(
        models.Prediction.timestamp.desc()
    ).first() is not None
    return route_service.find_safe_route(payload.latitude, payload.longitude, shelters, any_high_risk=any_high)


@router.get("/api/risk-map")
def risk_map(db: Session = Depends(get_db)):
    sensors = db.query(models.Sensor).all()
    markers = []
    any_high = False
    for s in sensors:
        pred = (
            db.query(models.Prediction)
            .filter(models.Prediction.sensor_id == s.id)
            .order_by(models.Prediction.timestamp.desc())
            .first()
        )
        risk = pred.risk_level if pred else "LOW"
        if risk == "HIGH":
            any_high = True
        markers.append({
            "id": s.id, "location_name": s.location_name,
            "latitude": s.latitude, "longitude": s.longitude, "risk_level": risk,
        })
    shelters = db.query(models.Shelter).all()
    return {
        "sensors": markers,
        "shelters": [
            {"id": sh.id, "name": sh.name, "latitude": sh.latitude, "longitude": sh.longitude,
             "status": sh.status, "capacity": sh.capacity, "current_occupancy": sh.current_occupancy}
            for sh in shelters
        ],
        "flood_zone_active": any_high,
        "flood_zone_center": [26.1445, 91.7362],
        "flood_zone_radius_km": 0.6,
        "blocked_roads": ["Canal Road"] if any_high else [],
    }
