def calculate_confidence(tournament_result: dict) -> int:
    """
    Calculate confidence score for the winning fix.
    Returns integer 0-100.
    """
    winner = tournament_result.get("winner_details", {})
    all_results = tournament_result.get("all_results", [])

    score = 0
    breakdown = {}

    if winner.get("success", False):
        score += 40
        breakdown["fix_succeeded"] = 40
    else:
        breakdown["fix_succeeded"] = 0

        print(f"[Scorer] Fix did not succeed on twin → max score capped at 30")
        return min(30, score)

    recovery = winner.get("recovery_seconds", 999)
    if recovery < 10:
        points = 20
    elif recovery < 30:
        points = 15
    elif recovery < 60:
        points = 10
    elif recovery < 120:
        points = 5
    else:
        points = 0
    score += points
    breakdown["recovery_speed"] = points


    side_effects = winner.get("side_effects", [])
    if len(side_effects) == 0:
        points = 20
    elif len(side_effects) == 1:
        points = 10
    else:
        points = 0
    score += points
    breakdown["no_side_effects"] = points


    risk = winner.get("risk_level", "high")
    risk_points = {"low": 15, "medium": 8, "high": 0}
    points = risk_points.get(risk, 0)
    score += points
    breakdown["risk_level"] = points


    other_successes = sum(1 for r in all_results
                          if r.get("success") and r["fix_id"] != winner["fix_id"])
    if other_successes >= 1:
        score += 5
        breakdown["other_fixes_also_worked"] = 5
    else:
        breakdown["other_fixes_also_worked"] = 0

    # Cap at 100
    final_score = min(score, 100)

    print(f"\n[Scorer] Confidence Score Breakdown:")
    for factor, pts in breakdown.items():
        print(f"  {factor}: +{pts}")
    print(f"  TOTAL: {final_score}/100")

    return final_score


def get_decision(confidence_score: int) -> dict:
    """
    Convert confidence score to action decision.
    """
    if confidence_score >= 85:
        return {
            "action": "auto_apply",
            "label": "AUTO APPLYING",
            "color": "green",
            "message": f"Confidence {confidence_score}% — applying autonomously"
        }
    elif confidence_score >= 60:
        return {
            "action": "request_human_approval",
            "label": "AWAITING APPROVAL",
            "color": "amber",
            "message": f"Confidence {confidence_score}% — requesting human confirmation"
        }
    else:
        return {
            "action": "escalate",
            "label": "ESCALATED",
            "color": "red",
            "message": f"Confidence {confidence_score}% — too uncertain, human must decide"
        }
    

# ─── TEST ─────────────────────────────────────────────────────
if __name__ == "__main__":
    # Simulate a tournament result
    fake_result = {
        "winner": "rate_limit",
        "winner_details": {
            "fix_id": "rate_limit",
            "fix_name": "Apply Rate Limiting",
            "success": True,
            "recovery_seconds": 8,
            "side_effects": [],
            "risk_level": "low"
        },
        "all_results": [
            {"fix_id": "rate_limit",      "success": True,  "recovery_seconds": 8},
            {"fix_id": "scale_up",        "success": True,  "recovery_seconds": 20},
            {"fix_id": "restart_service", "success": False, "recovery_seconds": 15},
        ]
    }

    score = calculate_confidence(fake_result)
    decision = get_decision(score)

    print(f"\n[TEST] Final score: {score}")
    print(f"[TEST] Decision: {decision['action']}")
    print(f"[TEST] Message: {decision['message']}")
    