from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    sensor_code = Column(String, unique=True, index=True)
    location_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    warning_level_cm = Column(Float, default=100)
    danger_level_cm = Column(Float, default=150)
    status = Column(String, default="active")  # active/offline


class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    water_level_cm = Column(Float)
    rainfall_mm_1h = Column(Float)
    rainfall_mm_3h = Column(Float)
    rainfall_forecast_mm_6h = Column(Float)
    battery_percent = Column(Float, default=100)
    source = Column(String, default="simulated")


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    risk_level = Column(String)
    risk_probability = Column(Float)
    estimated_water_level_cm_6h = Column(Float)
    rate_of_rise_cm_per_hour = Column(Float)
    model_version = Column(String, default="rules-v1")


class Shelter(Base):
    __tablename__ = "shelters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity = Column(Integer)
    current_occupancy = Column(Integer, default=0)
    status = Column(String, default="open")  # open/closed


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    risk_level = Column(String)
    message = Column(String)
    channel = Column(String, default="in-app")
    delivery_status = Column(String, default="sent")
