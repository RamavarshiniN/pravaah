"""
Standalone sensor simulator — sends JSON readings to the backend,
mimicking what an ESP32 + ultrasonic sensor would transmit over Wi-Fi.
Run: python simulate_sensor.py
"""
import time
import requests

API_URL = "http://localhost:8000/api/readings"

SCENARIOS = [
    {"water_level_cm": 55, "rainfall_mm_1h": 2, "rainfall_mm_3h": 5, "rainfall_forecast_mm_6h": 5},
    {"water_level_cm": 105, "rainfall_mm_1h": 22, "rainfall_mm_3h": 40, "rainfall_forecast_mm_6h": 35},
    {"water_level_cm": 165, "rainfall_mm_1h": 50, "rainfall_mm_3h": 90, "rainfall_forecast_mm_6h": 65},
]

if __name__ == "__main__":
    for i, s in enumerate(SCENARIOS):
        payload = {
            "sensor_id": "SEN-001",
            "location_name": "Ward 12 Drain",
            "latitude": 26.1445,
            "longitude": 91.7362,
            "water_level_cm": s["water_level_cm"],
            "rainfall_mm_1h": s["rainfall_mm_1h"],
            "rainfall_mm_3h": s["rainfall_mm_3h"],
            "rainfall_forecast_mm_6h": s["rainfall_forecast_mm_6h"],
            "battery_percent": 84,
            "source": "simulated",
        }
        r = requests.post(API_URL, json=payload)
        print(f"Stage {i+1}: {r.status_code} -> {r.json()}")
        time.sleep(2)
