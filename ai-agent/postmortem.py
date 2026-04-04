<<<<<<< HEAD
# postmortem.py
def generate_report(issue, best_fix):
    """
    Generates a post-mortem report for the action taken.
    """
    if issue and best_fix:
        return f"Issue '{issue}' resolved using fix: '{best_fix}'."
    else:
        return "No issues detected; no report generated."
=======
from datetime import datetime


def generate_report(issue: str, best_fix: str, confidence: dict, tournament: dict) -> dict:
    """Generate a structured post-mortem report."""
    if not issue or not best_fix:
        return {"summary": "No incidents detected — no report generated."}
    return {
        "timestamp":          datetime.utcnow().isoformat() + "Z",
        "issue":              issue,
        "fix_applied":        best_fix,
        "twin_validated":     tournament.get("twin_passed", False),
        "confidence_score":   confidence.get("score", 0),
        "confidence_label":   confidence.get("label", ""),
        "all_fixes_tested":   [r["fix"] for r in tournament.get("all_results", [])],
        "downtime_prevented": "Estimated ~45 minutes",
        "summary": (
            f"Issue '{issue}' detected and resolved using '{best_fix}'. "
            f"Fix was {'validated on digital twin' if tournament.get('twin_passed') else 'applied (twin failed — review advised)'}. "
            f"Confidence: {round(confidence.get('score', 0) * 100)}%."
        ),
    }
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
