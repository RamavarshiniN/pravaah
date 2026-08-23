import { useState, useEffect } from "react";
import { STATES, getDistricts, getWards } from "../data/locations";

export default function LocationSelector({ onSelectWard }) {
  const [state, setState] = useState("Assam");
  const [district, setDistrict] = useState("Kamrup Metropolitan");
  const [ward, setWard] = useState("ward12");
  const districts = getDistricts(state);
  const wards = getWards(state, district);

  useEffect(() => {
    onSelectWard?.(wards.find((w) => w.id === ward) || null);
  }, [ward, district, state]);

  const handleState = (e) => {
    const s = e.target.value; setState(s);
    const fd = getDistricts(s)[0]; setDistrict(fd);
    setWard(getWards(s, fd)[0]?.id || "");
  };
  const handleDistrict = (e) => {
    const d = e.target.value; setDistrict(d);
    setWard(getWards(state, d)[0]?.id || "");
  };
  const cls = "text-sm border border-gray-200 rounded-lg px-2.5 py-1.5 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-400 transition";

  return (
    <div className="flex items-center gap-2">
      <select value={state} onChange={handleState} className={cls}>{STATES.map((s) => <option key={s} value={s}>{s}</option>)}</select>
      <span className="text-gray-300">/</span>
      <select value={district} onChange={handleDistrict} className={cls}>{districts.map((d) => <option key={d} value={d}>{d}</option>)}</select>
      <span className="text-gray-300">/</span>
      <select value={ward} onChange={(e) => setWard(e.target.value)} className={cls}>{wards.map((w) => <option key={w.id} value={w.id}>{w.name}</option>)}</select>
    </div>
  );
}