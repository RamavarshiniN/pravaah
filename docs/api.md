# Pravaah API Reference

Base URL (local): `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/readings` | Ingest a sensor/simulated reading; stores it, computes risk, stores prediction, raises alert if HIGH |
| GET | `/api/sensors` | Latest status of all sensors |
| GET | `/api/sensors/{id}/history` | Historical readings + predictions for one sensor |
| POST | `/api/predict` | Stateless risk prediction for arbitrary input |
| GET | `/api/risk-map` | Sensor markers, shelters, flood-zone + blocked roads |
| GET | `/api/alerts` | Alert history (latest 50) |
| GET | `/api/shelters` | Shelters with capacity/occupancy/status |
| POST | `/api/routes/safe` | Nearest open shelter + route avoiding flood zone |
| POST | `/api/simulate/start` | Begin demo scenario (Normal) |
| POST | `/api/simulate/step` | Advance Normal → Watch → Flood Warning |
| POST | `/api/simulate/reset` | Reset simulation stage |

### Example: POST /api/readings
```json
{
  "sensor_id": "SEN-001",
  "water_level_cm": 158,
  "rainfall_mm_1h": 50,
  "rainfall_mm_3h": 90,
  "rainfall_forecast_mm_6h": 65,
  "battery_percent": 84,
  "source": "simulated"
}
```
Response:
```json
{
  "sensor_id": "SEN-001",
  "risk_level": "HIGH",
  "risk_probability": 0.78,
  "current_water_level_cm": 158,
  "estimated_water_level_cm_6h": 188,
  "rate_of_rise_cm_per_hour": 22,
  "alert_required": true,
  "message": "High flood risk predicted..."
}
```
