const BADGE = {
  LOW: "bg-green-100 text-green-700",
  MEDIUM: "bg-yellow-100 text-yellow-700",
  HIGH: "bg-red-100 text-red-700",
};

export default function AlertPanel({ alerts }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-4 h-full overflow-y-auto">
      <h3 className="font-semibold text-gray-800 mb-3">Recent Alerts</h3>
      {(!alerts || alerts.length === 0) && (
        <p className="text-sm text-gray-400">No alerts yet. Run the demo simulation to trigger one.</p>
      )}
      <ul className="space-y-3">
        {alerts?.map((a) => (
          <li key={a.id} className="border-l-4 border-red-400 bg-red-50 rounded p-3">
            <div className="flex justify-between items-center mb-1">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${BADGE[a.risk_level]}`}>
                {a.risk_level}
              </span>
              <span className="text-xs text-gray-400">{new Date(a.timestamp).toLocaleTimeString()}</span>
            </div>
            <p className="text-sm text-gray-700">{a.message}</p>
            <p className="text-xs text-gray-400 mt-1">{a.location_name} · via {a.channel}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
