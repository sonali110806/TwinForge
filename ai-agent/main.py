from detector import detect
from decision import analyze
from tournament import run_tournament
from confidence import evaluate_confidence
from postmortem import generate_report


def run_ai_agent(metrics=None):
    metrics = metrics or {"cpu": 35, "memory": 40, "latency": 95}
    issue = detect(metrics)

    if not issue:
        return {
            "issue": "No anomaly detected",
            "metrics": metrics,
            "decision": {"root_cause": "System healthy", "fixes": []},
            "results": [],
            "winner": None,
            "confidence": {"score": 0, "decision": {"action": "observe", "label": "HEALTHY", "message": "No action needed."}},
            "steps": [
                {"id": 1, "step": "Metrics captured", "detail": "Current telemetry sampled from backend summary.", "status": "complete"},
                {"id": 2, "step": "Anomaly scan", "detail": "No critical thresholds were crossed.", "status": "complete"},
            ],
            "report": generate_report(None, None, 0),
        }

    decision = analyze(issue)
    tournament = run_tournament(decision)
    confidence = evaluate_confidence(tournament)
    winner = tournament["winner"]
    report = generate_report(issue, winner, confidence["score"])

    steps = [
        {"id": 1, "step": "Metrics captured", "detail": f"CPU {metrics['cpu']}%, memory {metrics['memory']}%, latency {metrics['latency']}ms.", "status": "complete"},
        {"id": 2, "step": "Anomaly detected", "detail": issue["label"], "status": "complete"},
        {"id": 3, "step": "Root cause analysis", "detail": decision["root_cause"], "status": "complete"},
        {"id": 4, "step": "Fix tournament", "detail": f"Ranked {len(tournament['results'])} candidate remediations.", "status": "complete"},
        {"id": 5, "step": "Confidence gate", "detail": confidence["decision"]["message"], "status": "active"},
    ]

    return {
        "issue": issue["label"],
        "issueType": issue["type"],
        "metrics": metrics,
        "decision": decision,
        "results": tournament["results"],
        "winner": winner,
        "confidence": confidence,
        "steps": steps,
        "report": report,
    }
