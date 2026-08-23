SCENARIOS = [
    {  # Normal - LOW
        "water_level_cm": 55, "rainfall_mm_1h": 2, "rainfall_mm_3h": 5,
        "rainfall_forecast_mm_6h": 5, "rise_hint": 1,
    },
    {  # Watch - MEDIUM
        "water_level_cm": 105, "rainfall_mm_1h": 22, "rainfall_mm_3h": 40,
        "rainfall_forecast_mm_6h": 35, "rise_hint": 10,
    },
    {  # Flood Warning - HIGH
        "water_level_cm": 165, "rainfall_mm_1h": 50, "rainfall_mm_3h": 90,
        "rainfall_forecast_mm_6h": 65, "rise_hint": 25,
    },
]

_state = {"step": 0, "running": False}


def start_simulation():
    _state["step"] = 0
    _state["running"] = True
    return SCENARIOS[0]


def next_step():
    if not _state["running"]:
        start_simulation()
    _state["step"] = min(_state["step"] + 1, len(SCENARIOS) - 1)
    return SCENARIOS[_state["step"]]


def current_scenario():
    return SCENARIOS[_state["step"]]


def reset():
    _state["step"] = 0
    _state["running"] = False
