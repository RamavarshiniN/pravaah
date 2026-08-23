# Limitations (Honest Disclosure)

- This is a hackathon prototype using **simulated/synthetic sensor data**, not
  physically deployed hardware or verified live feeds.
- Risk thresholds (100cm warning / 150cm danger / 20cm/h rise) are
  **illustrative defaults** — real deployment needs field calibration per
  ward/drain geometry.
- The XGBoost model is trained on a **clearly synthetic, labeled dataset**
  for demonstration only. No field-validated accuracy is claimed.
- Rainfall forecast values are simulated; no live meteorological API is
  integrated in this MVP.
- Routing uses simplified straight-line/waypoint logic, not a full road-graph
  routing engine — sufficient for demo, not for production navigation.
- Shelter/road-closure data is manually seeded, not sourced from a live
  municipal system.
- Official emergency deployment would require: municipal/NDMA partnership,
  physical sensor installation + field testing, security/privacy review,
  verified real-time shelter and road-status feeds, and multilingual/SMS
  gateway integration.
