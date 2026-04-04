<<<<<<< HEAD
# confidence.py
def evaluate_confidence(best_fix):
    """
    Evaluates the confidence of the chosen fix.
    Returns a final action string.
    """
    # Example confidence logic (static for now)
    confidence_score = 0.85

    if confidence_score >= 0.8:
        return f"Execute fix: {best_fix}"
    elif confidence_score >= 0.5:
        return f"Review before executing: {best_fix}"
    else:
        return f"Do not execute automatically: {best_fix}"
=======
def evaluate_confidence(best_fix: str, simulation_passed: bool = True) -> dict:
    """Return a confidence score and recommended action for the chosen fix."""
    score = 0.92 if simulation_passed else 0.45

    if score >= 0.80:
        action = f"AUTO-DEPLOY: {best_fix}"
        label  = "high"
    elif score >= 0.50:
        action = f"REVIEW BEFORE DEPLOY: {best_fix}"
        label  = "medium"
    else:
        action = f"DO NOT DEPLOY (low confidence): {best_fix}"
        label  = "low"

    return {
        "score":             round(score, 2),
        "label":             label,
        "action":            action,
        "simulation_passed": simulation_passed,
    }
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
