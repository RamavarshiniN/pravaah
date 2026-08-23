"""
Transparent threshold-based flood risk engine.
Demo thresholds (documented, tunable):
  WARNING_LEVEL_CM = 100
  DANGER_LEVEL_CM  = 150
  HIGH_RISE_RATE   = 20 cm/hour
"""

WARNING_LEVEL_CM = 100
DANGER_LEVEL_CM = 150
HIGH_RISE_RATE = 20


def compute_rise_rate(prev_level, curr_level, hours=1.0):
    if prev_level is None:
        return 0.0
    return round((curr_level - prev_level) / hours, 2)


def estimate_6h_level(curr_level, rise_rate):
    # simple linear projection, clamped to non-negative
    est = curr_level + rise_rate * 6
    return round(max(est, 0), 1)


def classify_risk(water_level_cm, rainfall_1h, rainfall_3h, rainfall_6h_fcst, rise_rate, ml_probability=None):
    """
    Returns (risk_level, risk_probability, message)
    """
    high = (
        water_level_cm >= DANGER_LEVEL_CM
        or (rise_rate >= HIGH_RISE_RATE and rainfall_6h_fcst >= 50)
        or (ml_probability is not None and ml_probability >= 0.70)
    )
    medium = (
        not high
        and (
            water_level_cm >= WARNING_LEVEL_CM
            or rainfall_1h >= 20
            or rise_rate >= 8
        )
    )

    if high:
        risk = "HIGH"
        prob = max(ml_probability or 0.75, 0.70)
        msg = ("High flood risk predicted. Avoid low-lying roads and proceed "
               "to the nearest designated shelter immediately.")
    elif medium:
        risk = "MEDIUM"
        prob = ml_probability or 0.45
        msg = ("Water levels rising. Monitor updates closely and prepare "
               "to move to higher ground if conditions worsen.")
    else:
        risk = "LOW"
        prob = ml_probability or 0.10
        msg = "Conditions normal. No immediate action required."

    return risk, round(prob, 2), msg


def run_risk_engine(water_level_cm, rainfall_1h, rainfall_3h, rainfall_6h_fcst, prev_level=None, ml_probability=None):
    rise_rate = compute_rise_rate(prev_level, water_level_cm)
    risk, prob, msg = classify_risk(
        water_level_cm, rainfall_1h, rainfall_3h, rainfall_6h_fcst, rise_rate, ml_probability
    )
    est_6h = estimate_6h_level(water_level_cm, rise_rate)
    return {
        "risk_level": risk,
        "risk_probability": prob,
        "current_water_level_cm": water_level_cm,
        "estimated_water_level_cm_6h": est_6h,
        "rate_of_rise_cm_per_hour": rise_rate,
        "alert_required": risk == "HIGH",
        "message": msg,
    }
