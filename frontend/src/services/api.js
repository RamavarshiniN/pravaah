const BASE_URL = import.meta.env.VITE_API_URL || "";

async function req(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

export const api = {
  getSensors: () => req("/api/sensors"),
  getSensorHistory: (id) => req(`/api/sensors/${id}/history`),
  getAlerts: () => req("/api/alerts"),
  getShelters: () => req("/api/shelters"),
  getRiskMap: () => req("/api/risk-map"),
  predict: (payload) => req("/api/predict", { method: "POST", body: JSON.stringify(payload) }),
  safeRoute: (lat, lon) => req("/api/routes/safe", { method: "POST", body: JSON.stringify({ latitude: lat, longitude: lon }) }),
  simulateStart: () => req("/api/simulate/start", { method: "POST" }),
  simulateStep: () => req("/api/simulate/step", { method: "POST" }),
  simulateReset: () => req("/api/simulate/reset", { method: "POST" }),
};
