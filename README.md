# Prasunethon 2.0
# Pravaah — IoT-Driven, AI-Based Flood Forecasting & Evacuation Routing

Hackathon MVP for one flood-prone ward: simulated sensor data → AI risk
prediction (rules + XGBoost) → map dashboard → automated alerts → safe
evacuation route to nearest open shelter.

> **Honesty note:** uses simulated/synthetic data. No physical sensors, live
> municipal integration, or guaranteed accuracy claimed. See `docs/limitations.md`.

## Quick Start (local)

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend runs at `http://localhost:8000` (Swagger docs at `/docs`).
Sensors and shelters auto-seed on first startup.

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`.

### 3. Run the demo simulation
Either click **"Advance Simulation"** on the Dashboard (3 clicks: Normal →
Watch → Flood Warning), or run the standalone simulator:
```bash
cd backend
python data/simulate_sensor.py
```

### 4. (Optional) Train the ML model manually
```bash
cd backend
python -m app.ml.train_model
```
Model auto-trains on first `/api/readings` call if not already present.

## Test Commands
```bash
# Health check
curl http://localhost:8000/

# Ingest a HIGH-risk reading directly
curl -X POST http://localhost:8000/api/readings -H "Content-Type: application/json" \
  -d '{"sensor_id":"SEN-001","water_level_cm":165,"rainfall_mm_1h":50,"rainfall_mm_3h":90,"rainfall_forecast_mm_6h":65}'

# Check alerts were created
curl http://localhost:8000/api/alerts

# Check safe route
curl -X POST http://localhost:8000/api/routes/safe -H "Content-Type: application/json" \
  -d '{"latitude":26.1450,"longitude":91.7355}'
```

## Deployment

**Backend (Render/Railway):**
1. Push `backend/` to a repo.
2. New Web Service → build command `pip install -r requirements.txt` →
   start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3. Note the deployed URL.

**Frontend (Vercel):**
1. Push `frontend/` to a repo.
2. Import in Vercel, framework preset "Vite".
3. Set env var `VITE_API_URL` = your backend URL.
4. Deploy.

## Repository Structure
See `docs/architecture.md` for full system design and `docs/api.md` for the
complete endpoint reference.

## Evaluation Notes
- **Implementation**: full working ingestion → risk → alert → routing loop.
- **Innovation**: hyperlocal, actionable alerts (not generic broadcasts) +
  flood-zone-aware routing.
- **Scalability**: adding a ward = adding sensor/shelter rows; risk engine
  and routing logic are location-agnostic.
- **Security**: prototype has no auth (documented as future work); no
  external API keys hardcoded.
- **Real-world impact**: designed around actual disaster-response workflow
  (citizens, authorities, volunteers) validated in Round 1 research.
