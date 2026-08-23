import { useEffect, useState, useCallback, useRef } from "react";
import { api } from "../services/api";
import RiskCard from "../components/RiskCard";
import FloodMap from "../components/FloodMap";
import AlertPanel from "../components/AlertPanel";
import SensorChart from "../components/SensorChart";
import LocationSelector from "../components/LocationSelector";
import { SAMPLE_WARD_DATA } from "../data/locations";

const POLL_INTERVAL_MS = 4000;
const LIVE_WARD_ID = "ward12";

export default function Dashboard() {
  const [sensors, setSensors] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [riskMap, setRiskMap] = useState(null);
  const [history, setHistory] = useState({ readings: [] });
  const [simStage, setSimStage] = useState("Normal");
  const [hasStarted, setHasStarted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [lastSync, setLastSync] = useState(null);
  const [secondsAgo, setSecondsAgo] = useState(0);
  const [selectedWard, setSelectedWard] = useState({ id: "ward12", active: true, name: "Ward 12 (Demo — Live)" });
  const isFetching = useRef(false);

  const isLive = selectedWard?.id === LIVE_WARD_ID;
  const isSample = selectedWard?.active && !isLive;
  const sampleData = isSample ? SAMPLE_WARD_DATA[selectedWard.id] : null;

  const overallRisk = isLive
    ? sensors.reduce((worst, s) => {
        const order = { LOW: 0, MEDIUM: 1, HIGH: 2 };
        return order[s.risk_level] > order[worst] ? s.risk_level : worst;
      }, "LOW")
    : sampleData?.overallRisk || "LOW";

  const refresh = useCallback(async () => {
    if (isFetching.current) return;
    isFetching.current = true;
    try {
      const [s, a, r] = await Promise.all([api.getSensors(), api.getAlerts(), api.getRiskMap()]);
      setSensors(s); setAlerts(a); setRiskMap(r);
      if (s[0]) setHistory(await api.getSensorHistory(s[0].id));
      setLastSync(Date.now());
    } finally { isFetching.current = false; }
  }, []);

  useEffect(() => {
    if (!isLive) return;
    refresh();
    const id = setInterval(refresh, POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, [refresh, isLive]);

  useEffect(() => {
    const id = setInterval(() => { if (lastSync) setSecondsAgo(Math.floor((Date.now() - lastSync) / 1000)); }, 1000);
    return () => clearInterval(id);
  }, [lastSync]);

  const runStep = async () => {
    setBusy(true);
    try {
      const res = !hasStarted ? await api.simulateStart() : await api.simulateStep();
      setHasStarted(true); setSimStage(res.stage); await refresh();
    } finally { setBusy(false); }
  };

  const resetDemo = async () => {
    setBusy(true);
    try { await api.simulateReset(); setSimStage("Normal"); setHasStarted(false); await refresh(); }
    finally { setBusy(false); }
  };

  const RISK_BADGE = { LOW: "bg-green-500", MEDIUM: "bg-yellow-500", HIGH: "bg-red-500" };
  const RISK_RING = { LOW: "ring-green-200", MEDIUM: "ring-yellow-200", HIGH: "ring-red-300" };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-gray-100">
      <header className="bg-white/90 backdrop-blur sticky top-0 z-10 border-b border-gray-200 px-6 py-4 flex flex-wrap justify-between items-center gap-3">
        <div className="flex items-center gap-3 flex-wrap">
          <h1 className="text-2xl font-bold text-blue-700 tracking-tight">Pravaah</h1>
          <span className="text-xs bg-gray-100 text-gray-600 px-2.5 py-1 rounded-full border border-gray-200">Demo Mode</span>
          {isLive && (
            <span className="flex items-center gap-1.5 text-xs text-gray-500">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              Live · synced {secondsAgo}s ago
            </span>
          )}
          {isSample && (
            <span className="text-xs bg-amber-50 text-amber-700 px-2.5 py-1 rounded-full border border-amber-200">
              Sample Data · Not Live
            </span>
          )}
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          <LocationSelector onSelectWard={setSelectedWard} />
          {selectedWard?.active && (
            <span className={`text-white text-sm font-semibold px-3 py-1.5 rounded-full ring-4 ${RISK_BADGE[overallRisk]} ${RISK_RING[overallRisk]} transition-all`}>
              Overall: {overallRisk}
            </span>
          )}
          {isLive && (
            <>
              <button onClick={runStep} disabled={busy} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 active:scale-95 transition disabled:opacity-50 shadow-sm">
                {busy ? "Running…" : `Advance Simulation (${simStage})`}
              </button>
              <button onClick={resetDemo} disabled={busy} className="bg-gray-100 text-gray-700 px-3 py-2 rounded-lg text-sm border border-gray-200 hover:bg-gray-200 transition">Reset</button>
            </>
          )}
        </div>
      </header>

      {!selectedWard?.active ? (
        <main className="p-6">
          <div className="max-w-xl mx-auto mt-16 text-center bg-white rounded-2xl shadow-sm border border-gray-100 p-10">
            <div className="w-14 h-14 mx-auto rounded-full bg-blue-50 flex items-center justify-center text-blue-500 text-2xl mb-4">📡</div>
            <h2 className="text-lg font-semibold text-gray-800 mb-2">No sensors deployed yet in {selectedWard?.name}</h2>
            <p className="text-sm text-gray-500 leading-relaxed">
              This ward isn't part of the current hackathon demo scope. The same ingestion, risk-engine, and routing pipeline already running for Ward 12 would apply here the moment sensors and shelters are seeded.
            </p>
          </div>
        </main>
      ) : (
        <main className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <section className="lg:col-span-2 space-y-4">
            {isSample && (
              <div className="bg-amber-50 border border-amber-200 text-amber-800 text-sm rounded-lg px-4 py-2.5">
                Showing static sample readings for {selectedWard.name} — not connected to live sensors. Switch to Ward 12 for the live simulation.
              </div>
            )}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {(isLive ? sensors : sampleData?.sensors || []).map((s) => <RiskCard key={s.id} sensor={s} />)}
            </div>
            {isLive && (
              <>
                <div className="h-96 bg-white rounded-xl shadow-sm border border-gray-100 p-2">
                  <FloodMap riskMap={riskMap} />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <SensorChart data={history.readings} dataKey="water_level_cm" label="Water Level Over Time (cm)" color="#2563eb" />
                  <SensorChart data={history.readings} dataKey="rainfall_mm_1h" label="Rainfall Over Time (mm/1h)" color="#0891b2" />
                </div>
              </>
            )}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 text-xs text-gray-500 flex gap-4">
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-500 inline-block" /> Low</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-yellow-500 inline-block" /> Medium</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-red-500 inline-block" /> High</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-blue-600 inline-block" /> Shelter</span>
            </div>
          </section>
          <aside className="h-[600px]">
            <AlertPanel alerts={isLive ? alerts : []} />
          </aside>
        </main>
      )}
    </div>
  );
}