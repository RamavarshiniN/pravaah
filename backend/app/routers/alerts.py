from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(tags=["alerts"])


@router.get("/api/alerts")
def list_alerts(db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).order_by(models.Alert.timestamp.desc()).limit(50).all()
    out = []
    for a in alerts:
        sensor = db.query(models.Sensor).get(a.sensor_id)
        out.append({
            "id": a.id,
            "timestamp": a.timestamp.isoformat(),
            "location_name": sensor.location_name if sensor else "Unknown",
            "risk_level": a.risk_level,
            "message": a.message,
            "channel": a.channel,
            "delivery_status": a.delivery_status,
        })
    return out
