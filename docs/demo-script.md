# Pravaah — Demo Script (2–4 min)

**0:00–0:20 — Problem**
"Flood alerts today say 'heavy rainfall expected' — but residents don't know
if THEIR street floods, when, how deep, or where to go. Pravaah fixes that."

**0:20–0:45 — Architecture (show diagram)**
Sensors/simulated readings → risk engine → map + alerts → safe route to shelter.

**0:45–1:30 — Authority Dashboard**
- Show sensor cards, map with green markers (Low risk), charts.
- Click "Advance Simulation" → watch a sensor go to MEDIUM (yellow marker).
- Click again → HIGH (red marker), flood zone circle appears, alert fires
  in the Recent Alerts panel in real time.

**1:30–2:15 — Citizen Safety Page**
- Switch to Citizen page: risk badge is now HIGH, message updates.
- Tap "View Safe Route" → nearest OPEN shelter shown, route line avoids the
  flood zone, blocked road noted ("Avoid Canal Road").
- Show Emergency Contact modal.

**2:15–2:45 — Under the hood**
- Open `/docs` Swagger UI briefly, hit `/api/predict` live to show the
  transparent risk logic + optional ML probability.

**2:45–3:00 — Honesty + roadmap**
- "This MVP uses simulated data — real deployment needs field-calibrated
  sensors and municipal partnership. Architecture scales to more wards by
  adding rows, not rewriting logic."
