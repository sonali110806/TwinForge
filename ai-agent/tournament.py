import random

def _score_fix(fix, issue_type):
    base = 55 + (25 if issue_type in fix.get("good_for", []) else 0)
    risk_bonus = {"low": 10, "medium": 2, "high": -8}.get(fix.get("risk_level", "high"), 0)
    side_effect_penalty = len(fix.get("side_effects", [])) * 5
    speed_bonus = max(0, 18 - int(fix.get("estimated_seconds", 20)) // 2)
    return max(0, min(99, base + risk_bonus + speed_bonus - side_effect_penalty + random.randint(-4, 4)))

def run_tournament(decision):
    fixes = decision.get("fixes", [])
    issue_type = decision.get("anomaly_type", "")
    results = []
    for fix in fixes:
        p = _score_fix(fix, issue_type)
        results.append({
            "fix_id": fix["id"],
            "name": fix["name"],
            "risk_level": fix["risk_level"],
            "success_probability": p,
            "performance_gain": max(5, min(35, p // 3)),
            "estimated_seconds": fix["estimated_seconds"],
            "side_effects": fix.get("side_effects", []),
            "success": p >= 60,
        })
    winner = max(results, key=lambda x: (x["success_probability"], -len(x["side_effects"]), -x["estimated_seconds"]), default=None)
    return {"results": results, "winner": winner}
