from typing import List, Dict


WEEK_1_TEMPLATE = [
    {"treeni": 1, "sets": 6,  "reps": 4, "base_pct": 0.65},
    {"treeni": 2, "sets": 7,  "reps": 5, "base_pct": 0.60},
    {"treeni": 3, "sets": 8,  "reps": 3, "base_pct": 0.70},
    {"treeni": 4, "sets": 10, "reps": 2, "base_pct": 0.75},
]

WEEK_4_SESSIONS = [
    {"treeni": 1, "sets": 4, "reps": 3, "pct": 0.60, "type": "deload"},
    {"treeni": 2, "sets": 3, "reps": 2, "pct": 0.70, "type": "deload"},
    {"treeni": 3, "type": "rest"},
    {"treeni": 4, "type": "test"},
]


def _intensity_tier(pct: float) -> str:
    if pct < 0.68:
        return "low"
    elif pct < 0.78:
        return "mid"
    else:
        return "high"


def fi_kg(value: float) -> str:
    if value % 0.5 < 0.001:
        return f"{value:.1f}".replace(".", ",") + " kg"
    return f"{value:.2f}".replace(".", ",") + " kg"


def fi_pct(value: float) -> str:
    return f"{round(value * 100)} %"


def calculate_program(max_added: float, weekly_increase: float) -> List[Dict]:
    weeks = []

    for week_num in range(1, 4):
        sessions = []
        for t in WEEK_1_TEMPLATE:
            adjusted_pct = t["base_pct"] + (week_num - 1) * (weekly_increase / 100)
            weight = round(max_added * adjusted_pct / 1.25) * 1.25
            sessions.append({
                "treeni": t["treeni"],
                "sets": t["sets"],
                "reps": t["reps"],
                "pct": adjusted_pct,
                "weight": weight,
                "type": "normal",
                "intensity_tier": _intensity_tier(adjusted_pct),
            })
        weeks.append({
            "week_number": week_num,
            "week_type": "kuormitus",
            "sessions": sessions,
        })

    week4_sessions = []
    for s in WEEK_4_SESSIONS:
        if s["type"] == "deload":
            weight = round(max_added * s["pct"] / 1.25) * 1.25
            week4_sessions.append({
                "treeni": s["treeni"],
                "sets": s["sets"],
                "reps": s["reps"],
                "pct": s["pct"],
                "weight": weight,
                "type": "deload",
                "intensity_tier": "deload",
            })
        elif s["type"] == "rest":
            week4_sessions.append({
                "treeni": s["treeni"],
                "type": "rest",
                "intensity_tier": "deload",
            })
        else:
            week4_sessions.append({
                "treeni": s["treeni"],
                "type": "test",
                "intensity_tier": "test",
            })

    weeks.append({
        "week_number": 4,
        "week_type": "deload",
        "sessions": week4_sessions,
    })

    return weeks
