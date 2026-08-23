# Pravaah — Architecture

## Flow
IoT/Simulated Sensors → FastAPI ingestion (`/api/readings`) → SQLite storage
→ Risk Engine (rules + optional XGBoost) → Prediction stored → Map/Dashboard
(`/api/risk-map`, `/api/sensors`) → Alert Service (dedup, in-app + simulated
SMS log) → Safe Routing (`/api/routes/safe`) avoiding flood-zone/blocked roads
→ Citizen Safety Page shows nearest open shelter + route.

## Components
- **Backend**: FastAPI + SQLAlchemy + SQLite. Stateless risk classification
  with a transparent threshold engine; optional XGBoost model trained on
  synthetic labeled data adds a probability signal.
- **Frontend**: React (Vite) + Tailwind + React-Leaflet + Recharts. Two
  views: Authority Dashboard (sensor grid, map, charts, alerts) and Citizen
  Safety Page (risk badge, shelter, route, emergency contact).
- **Simulation**: `/api/simulate/start` and `/api/simulate/step` walk through
  Normal → Watch → Flood Warning, feeding realistic readings through the same
  ingestion path a real sensor would use.

## Why this design
- Single ward/locality scope keeps the MVP demo-able in minutes while the
  architecture (sensor table, ward-agnostic risk engine) generalizes to
  multiple wards by adding rows, not rewriting logic.
- Rules-first risk engine keeps predictions explainable to disaster-management
  staff; ML layer is additive, not a black box replacing the rules.
