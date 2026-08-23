from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models


COOLDOWN_MINUTES = 15  # avoid duplicate alert spam per sensor


def maybe_create_alert(db: Session, sensor: models.Sensor, risk_level: str, message: str, shelter=None, route_note=""):
    if risk_level != "HIGH":
        return None

    cutoff = datetime.utcnow() - timedelta(minutes=COOLDOWN_MINUTES)
    recent = (
        db.query(models.Alert)
        .filter(models.Alert.sensor_id == sensor.id, models.Alert.risk_level == "HIGH")
        .filter(models.Alert.timestamp >= cutoff)
        .first()
    )
    if recent:
        return recent  # dedup: don't spam

    full_msg = message
    if shelter:
        full_msg += f" Recommended shelter: {shelter.name}."
    if route_note:
        full_msg += f" {route_note}"

    alert = models.Alert(
        sensor_id=sensor.id,
        risk_level=risk_level,
        message=full_msg,
        channel="in-app+sms(sim)",
        delivery_status="sent",
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    # Simulated SMS/WhatsApp log (no external API required)
    print(f"[SIM-SMS] To residents near {sensor.location_name}: {full_msg}")
    return alert
