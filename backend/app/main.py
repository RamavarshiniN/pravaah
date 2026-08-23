from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, SessionLocal
from . import models
from .config import CORS_ORIGINS
from .routers import sensors, predictions, alerts, shelters, routes, simulation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pravaah API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router)
app.include_router(predictions.router)
app.include_router(alerts.router)
app.include_router(shelters.router)
app.include_router(routes.router)
app.include_router(simulation.router)


@app.on_event("startup")
def seed_if_empty():
    db = SessionLocal()
    try:
        if db.query(models.Sensor).count() == 0:
            sensors_seed = [
                models.Sensor(sensor_code="SEN-001", location_name="Ward 12 Drain", latitude=26.1445, longitude=91.7362),
                models.Sensor(sensor_code="SEN-002", location_name="Ward 12 River Point", latitude=26.1470, longitude=91.7390),
                models.Sensor(sensor_code="SEN-003", location_name="Ward 12 Bridge", latitude=26.1420, longitude=91.7340),
                models.Sensor(sensor_code="SEN-004", location_name="Ward 12 Market", latitude=26.1460, longitude=91.7320),
                models.Sensor(sensor_code="SEN-005", location_name="Ward 12 School Rd", latitude=26.1400, longitude=91.7370),
            ]
            db.add_all(sensors_seed)

            shelters_seed = [
                models.Shelter(name="Community Hall Shelter", latitude=26.1500, longitude=91.7400, capacity=200, current_occupancy=20, status="open"),
                models.Shelter(name="Govt. School Shelter", latitude=26.1380, longitude=91.7300, capacity=150, current_occupancy=140, status="open"),
                models.Shelter(name="Ward Office Shelter", latitude=26.1460, longitude=91.7450, capacity=100, current_occupancy=0, status="closed"),
            ]
            db.add_all(shelters_seed)
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {"app": "Pravaah", "status": "running", "docs": "/docs"}
