const RISK_STYLES = {
  LOW: "bg-green-50 text-green-700 border border-green-200",
  MEDIUM: "bg-yellow-50 text-yellow-700 border border-yellow-200",
  HIGH: "bg-red-50 text-red-700 border border-red-200",
};

const BORDER_ACCENT = {
  LOW: "border-l-green-500",
  MEDIUM: "border-l-yellow-500",
  HIGH: "border-l-red-500",
};

export default function RiskCard({ sensor }) {
  const badge = RISK_STYLES[sensor.risk_level] || RISK_STYLES.LOW;
  const accent = BORDER_ACCENT[sensor.risk_level] || BORDER_ACCENT.LOW;
  const isHigh = sensor.risk_level === "HIGH";

  return (
    <div
      className={`rounded-xl border-l-4 ${accent} p-4 bg-white shadow-sm hover:shadow-md transition-shadow duration-200 ${
        isHigh ? "ring-2 ring-red-100 animate-[pulse_2.5s_ease-in-out_infinite]" : ""
      }`}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-semibold text-gray-800">{sensor.location_name}</h3>
          <p className="text-xs text-gray-400 font-mono">{sensor.sensor_code}</p>
        </div>
        <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${badge}`}>
          {sensor.risk_level}
        </span>
      </div>
      <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-gray-400 text-xs uppercase tracking-wide">Water Level</p>
          <p className="font-semibold text-gray-800">{sensor.water_level_cm ?? "—"} <span className="text-xs font-normal text-gray-400">cm</span></p>
        </div>
        <div>
          <p className="text-gray-400 text-xs uppercase tracking-wide">Rainfall (1h)</p>
          <p className="font-semibold text-gray-800">{sensor.rainfall_mm_1h ?? "—"} <span className="text-xs font-normal text-gray-400">mm</span></p>
        </div>
        <div>
          <p className="text-gray-400 text-xs uppercase tracking-wide">Battery</p>
          <p className="font-semibold text-gray-800">{sensor.battery_percent ?? "—"}%</p>
        </div>
        <div>
          <p className="text-gray-400 text-xs uppercase tracking-wide">Updated</p>
          <p className="font-semibold text-gray-800 text-xs">
            {sensor.last_updated ? new Date(sensor.last_updated).toLocaleTimeString() : "—"}
          </p>
        </div>
      </div>
    </div>
  );
}