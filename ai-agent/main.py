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
  


        
           
        
    

