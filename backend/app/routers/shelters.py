from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(tags=["shelters"])


@router.get("/api/shelters")
def list_shelters(db: Session = Depends(get_db)):
    shelters = db.query(models.Shelter).all()
    return [
        {
            "id": s.id, "name": s.name, "latitude": s.latitude, "longitude": s.longitude,
            "capacity": s.capacity, "current_occupancy": s.current_occupancy, "status": s.status,
        } for s in shelters
    ]
