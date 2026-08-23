"""
MVP safe routing: haversine distance to filter open/available shelters,
apply penalty if straight path crosses a simulated flood zone polygon,
return a simple polyline (waypoints) as the "route".
"""
import math

# Simple simulated flood zone (ward-scale bounding box) — active only when HIGH risk exists
FLOOD_ZONE_CENTER = (26.1445, 91.7362)
FLOOD_ZONE_RADIUS_KM = 0.6

BLOCKED_ROADS = ["Canal Road"]  # illustrative for alert text


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def path_crosses_flood_zone(lat1, lon1, lat2, lon2, any_high_risk):
    if not any_high_risk:
        return False
    # check midpoint distance to flood zone center as a cheap proxy
    mid_lat, mid_lon = (lat1 + lat2) / 2, (lon1 + lon2) / 2
    d = haversine_km(mid_lat, mid_lon, *FLOOD_ZONE_CENTER)
    return d <= FLOOD_ZONE_RADIUS_KM


def find_safe_route(user_lat, user_lon, shelters, any_high_risk=False):
    candidates = [s for s in shelters if s.status == "open" and s.current_occupancy < s.capacity]
    if not candidates:
        return {
            "status": "no_route",
            "message": "No verified safe route available. Contact local emergency services.",
        }

    scored = []
    for s in candidates:
        dist = haversine_km(user_lat, user_lon, s.latitude, s.longitude)
        blocked = path_crosses_flood_zone(user_lat, user_lon, s.latitude, s.longitude, any_high_risk)
        cost = dist + (999 if blocked else 0)  # huge penalty for flood-zone crossing
        scored.append((cost, dist, blocked, s))

    scored.sort(key=lambda x: x[0])
    best_cost, best_dist, blocked, shelter = scored[0]

    if blocked:
        return {
            "status": "no_route",
            "message": "No verified safe route available. Contact local emergency services.",
        }

    route_note = f"Avoid {BLOCKED_ROADS[0]}." if any_high_risk else ""
    return {
        "status": "ok",
        "shelter": {
            "id": shelter.id,
            "name": shelter.name,
            "latitude": shelter.latitude,
            "longitude": shelter.longitude,
            "capacity": shelter.capacity,
            "current_occupancy": shelter.current_occupancy,
        },
        "distance_km": round(best_dist, 2),
        "route_coordinates": [
            [user_lat, user_lon],
            [shelter.latitude, shelter.longitude],
        ],
        "route_note": route_note,
    }
