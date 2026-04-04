def evaluate_confidence(tournament_result):
    winner = tournament_result.get("winner")
    results = tournament_result.get("results", [])

    if not winner:
        return {"score": 0, "decision": get_decision(0)}

    score = 0
    if winner["success"]:
        score += 40

    if winner["estimated_seconds"] <= 5:
        score += 20
    elif winner["estimated_seconds"] <= 15:
        score += 15
    else:
        score += 10

    if len(winner["side_effects"]) == 0:
        score += 20
    elif len(winner["side_effects"]) == 1:
        score += 10

    score += {"low": 15, "medium": 8, "high": 0}.get(winner["risk_level"], 0)

    other_successes = sum(1 for result in results if result["fix_id"] != winner["fix_id"] and result["success"])
    if other_successes:
        score += 5

    score = min(score, 100)

    if score >= 85:
        decision = {
            "action": "auto_apply",
            "label": "AUTO APPLYING",
            "color": "green",
            "message": f"Confidence {score}% — safe to deploy automatically.",
        }
    elif score >= 60:
        decision = {
            "action": "request_human_approval",
            "label": "AWAITING APPROVAL",
            "color": "amber",
            "message": f"Confidence {score}% — review recommended before deployment.",
        }
    else:
        decision = {
            "action": "escalate",
            "label": "ESCALATED",
            "color": "red",
            "message": f"Confidence {score}% — too uncertain for automatic deployment.",
        }

    return {"score": score, "decision": decision}
