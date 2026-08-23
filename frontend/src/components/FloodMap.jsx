import { MapContainer, TileLayer, CircleMarker, Popup, Circle, Polyline, Marker } from "react-leaflet";
import L from "leaflet";

const RISK_COLOR = { LOW: "#16a34a", MEDIUM: "#eab308", HIGH: "#dc2626" };

const shelterIcon = new L.DivIcon({
  html: `<div style="background:#2563eb;color:white;border-radius:50%;width:14px;height:14px;border:2px solid white"></div>`,
  className: "",
  iconSize: [14, 14],
});

export default function FloodMap({ riskMap, route, userPoint, center = [26.1445, 91.7362] }) {
  if (!riskMap) return <div className="h-full flex items-center justify-center text-gray-400">Loading map…</div>;

  return (
    <MapContainer center={center} zoom={14} className="h-full w-full rounded-xl">
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {riskMap.sensors.map((s) => (
        <CircleMarker
          key={s.id}
          center={[s.latitude, s.longitude]}
          radius={10}
          pathOptions={{ color: RISK_COLOR[s.risk_level], fillColor: RISK_COLOR[s.risk_level], fillOpacity: 0.8 }}
        >
          <Popup>
            <b>{s.location_name}</b><br />Risk: {s.risk_level}
          </Popup>
        </CircleMarker>
      ))}

      {riskMap.shelters.map((sh) => (
        <Marker key={sh.id} position={[sh.latitude, sh.longitude]} icon={shelterIcon}>
          <Popup>
            <b>{sh.name}</b><br />
            Status: {sh.status}<br />
            Occupancy: {sh.current_occupancy}/{sh.capacity}
          </Popup>
        </Marker>
      ))}

      {riskMap.flood_zone_active && (
        <Circle
          center={riskMap.flood_zone_center}
          radius={riskMap.flood_zone_radius_km * 1000}
          pathOptions={{ color: "#dc2626", fillColor: "#dc2626", fillOpacity: 0.15 }}
        />
      )}

      {route && route.status === "ok" && (
        <Polyline positions={route.route_coordinates} pathOptions={{ color: "#2563eb", weight: 4 }} />
      )}

      {userPoint && (
        <CircleMarker center={userPoint} radius={8} pathOptions={{ color: "#111827", fillColor: "#111827", fillOpacity: 1 }}>
          <Popup>You are here</Popup>
        </CircleMarker>
      )}
    </MapContainer>
  );
}
