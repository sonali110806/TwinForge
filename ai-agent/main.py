<<<<<<< HEAD
# main.py

from detector import detect
from decision import analyze
from tournament import run_tournament
from confidence import evaluate_confidence
from postmortem import generate_report

def run_ai_agent(metrics=None):
    # Step 1: Simulated system metrics if none provided
    if metrics is None:
        metrics = {"cpu": 95, "memory": 85}

    print("\n🔄 Monitoring system...")

    # Step 2: Detect anomaly
    issue = detect(metrics)
    print("Issue Detected:", issue)

    if issue:
        # Step 3: AI Decision (root cause + fixes)
        decision = analyze(issue)
        print("Decision:", decision)

        # Step 4: Run fix tournament
        best_fix = run_tournament(decision)
        print("Best Fix Selected:", best_fix)

        # Step 5: Confidence-based action
        action = evaluate_confidence(best_fix)
        print("Final Action:", action)

        # Step 6: Generate post-mortem report
        report = generate_report(issue, best_fix)
        print("Post-Mortem Report:", report)

        return {
            "issue": issue,
            "decision": decision,
            "fix": best_fix,
            "action": action,
            "report": report
        }

    else:
        print("✅ System is running normally")
        return {
            "issue": "No anomaly detected",
            "decision": "",
            "fix": "",
            "action": "No action needed",
            "report": ""
        }


# Run directly for testing
if __name__ == "__main__":
    run_ai_agent()
=======
from detector   import detect
from decision   import analyze
from tournament import run_tournament
from confidence import evaluate_confidence
from postmortem import generate_report
from agent      import build_prompt


def run_ai_agent(metrics: dict | None = None) -> dict:
    """
    Full Digital-Twin agent pipeline:
    1. Detect anomaly  2. Analyze  3. Tournament on shadow twin
    4. Confidence eval  5. Post-mortem report
    """
    if metrics is None:
        metrics = {"cpu": 95, "memory": 85}

    print("\n🔄 AI Agent — monitoring system…")

    issue = detect(metrics)
    print(f"  Issue: {issue}")

    if not issue:
        print("  ✅ System healthy.")
        return {
            "issue":      None,
            "decision":   {},
            "tournament": {},
            "confidence": {},
            "report":     {"summary": "System healthy — no action needed."},
            "prompt":     "",
        }

    decision   = analyze(issue)
    prompt     = build_prompt(issue, metrics)
    print(f"  Root cause: {decision['root_cause']}")

    print("  Running fix tournament on digital twin…")
    tournament = run_tournament(decision)
    print(f"  Winner: {tournament['winner']}")

    confidence = evaluate_confidence(
        tournament["winner"],
        simulation_passed=tournament["twin_passed"],
    )
    print(f"  Confidence: {confidence['label']} ({confidence['score']})")

    report = generate_report(issue, tournament["winner"], confidence, tournament)
    print(f"  {report['summary']}")

    return {
        "issue":      issue,
        "decision":   decision,
        "tournament": tournament,
        "confidence": confidence,
        "report":     report,
        "prompt":     prompt,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_ai_agent(), indent=2))
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
