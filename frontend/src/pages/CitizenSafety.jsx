import { useEffect, useState } from "react";
import { api } from "../services/api";
import FloodMap from "../components/FloodMap";
import ShelterRoute from "../components/ShelterRoute";

const RISK_BG = { LOW: "bg-green-500", MEDIUM: "bg-yellow-500", HIGH: "bg-red-500" };
const USER_POINT = [26.1520, 91.7280]; // fixed demo user location within Ward 12, outside flood zone
export default function CitizenSafety() {
  const [sensors, setSensors] = useState([]);
  const [riskMap, setRiskMap] = useState(null);
  const [route, setRoute] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showContact, setShowContact] = useState(false);

  const primary = sensors[0];
  const risk = primary?.risk_level || "LOW";

  useEffect(() => {
    (async () => {
      const [s, r] = await Promise.all([api.getSensors(), api.getRiskMap()]);
      setSensors(s);
      setRiskMap(r);
    })();
  }, []);

  const viewRoute = async () => {
    setLoading(true);
    try {
      const r = await api.safeRoute(USER_POINT[0], USER_POINT[1]);
      setRoute(r);
    } finally {
      setLoading(false);
    }
  };

  const trend = primary?.risk_level === "HIGH" ? "Rising rapidly" : primary?.risk_level === "MEDIUM" ? "Rising" : "Stable";

  return (
    <div className="min-h-screen bg-gray-50 max-w-lg mx-auto pb-10">
      <header className="px-5 py-4">
        <h1 className="text-xl font-bold text-blue-700">Pravaah — Citizen Safety</h1>
        <select className="mt-2 w-full border rounded-lg p-2 text-sm">
          <option>Ward 12 — Demo Locality</option>
        </select>
      </header>

      <div className={`mx-5 rounded-2xl p-6 text-white text-center ${RISK_BG[risk]}`}>
        <p className="text-sm opacity-80">Current Flood Risk</p>
        <p className="text-4xl font-extrabold">{risk}</p>
        <p className="mt-2 text-sm opacity-90">
          {risk === "HIGH" && "Flooding possible within the next few hours. Move to a shelter now."}
          {risk === "MEDIUM" && "Monitor conditions closely. Be ready to evacuate."}
          {risk === "LOW" && "Conditions are normal. No action needed."}
        </p>
      </div>

      <div className="mx-5 mt-4 grid grid-cols-2 gap-3">
        <div className="bg-white rounded-xl p-3 shadow-sm">
          <p className="text-xs text-gray-400">Water Level</p>
          <p className="font-bold text-lg">{primary?.water_level_cm ?? "—"} cm</p>
          <p className="text-xs text-gray-500">{trend}</p>
        </div>
        <div className="bg-white rounded-xl p-3 shadow-sm">
          <p className="text-xs text-gray-400">Est. in 6h</p>
          <p className="font-bold text-lg">{risk === "HIGH" ? "~188 cm" : risk === "MEDIUM" ? "~130 cm" : "~55 cm"}</p>
          <p className="text-xs text-gray-500">Model estimate</p>
        </div>
      </div>

      <div className="mx-5 mt-4">
        <ShelterRoute route={route} onViewRoute={viewRoute} loading={loading} />
      </div>

      <div className="mx-5 mt-4 h-72 rounded-xl overflow-hidden shadow-sm">
        <FloodMap riskMap={riskMap} route={route} userPoint={USER_POINT} />
      </div>

      <div className="mx-5 mt-4">
        <button
          onClick={() => setShowContact(true)}
          className="w-full bg-red-600 text-white rounded-lg py-3 font-semibold hover:bg-red-700"
        >
          Emergency Contact
        </button>
      </div>

      <div className="mx-5 mt-4 bg-white rounded-xl p-4 shadow-sm text-sm">
        <p className="font-semibold text-gray-700 mb-1">Alert (English)</p>
        <p className="text-gray-600">
          {risk === "HIGH"
            ? "HIGH FLOOD RISK. Water level near Ward 12 is rising rapidly. Move to Community Hall Shelter. Avoid Canal Road."
            : "No high-risk alert currently active for this ward."}
        </p>
        <p className="font-semibold text-gray-700 mt-3 mb-1">स्थानीय भाषा में अलर्ट (Placeholder)</p>
        <p className="text-gray-400 italic">Local-language alert will appear here in production.</p>
      </div>

      {showContact && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-6" onClick={() => setShowContact(false)}>
          <div className="bg-white rounded-xl p-6 max-w-sm w-full" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-bold text-lg mb-2">Emergency Contact (Prototype)</h3>
            <p className="text-sm text-gray-600 mb-4">In production this would dial local disaster-management helpline / NDRF control room.</p>
            <p className="text-sm font-mono bg-gray-100 rounded p-2">Demo Helpline: 1078 (NDMA, India)</p>
            <button onClick={() => setShowContact(false)} className="mt-4 w-full bg-gray-200 rounded-lg py-2 text-sm">Close</button>
          </div>
        </div>
      )}
    </div>
  );
}
