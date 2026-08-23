export default function ShelterRoute({ route, onViewRoute, loading }) {
  if (!route) {
    return (
      <button
        onClick={onViewRoute}
        disabled={loading}
        className="w-full bg-blue-600 text-white rounded-lg py-3 font-semibold hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Finding safe route…" : "View Safe Route"}
      </button>
    );
  }

  if (route.status === "no_route") {
    return (
      <div className="bg-red-50 border border-red-300 rounded-lg p-4 text-red-700 text-sm font-medium">
        ⚠️ {route.message}
      </div>
    );
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <p className="font-semibold text-blue-900">{route.shelter.name}</p>
      <p className="text-sm text-blue-700">
        {route.distance_km} km away · {route.shelter.current_occupancy}/{route.shelter.capacity} occupied
      </p>
      {route.route_note && <p className="text-xs text-red-600 mt-1">{route.route_note}</p>}
    </div>
  );
}
