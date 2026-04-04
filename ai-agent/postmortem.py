def generate_report(issue, winner, confidence_score):
    if not issue or not winner:
        return {
            "title": "Healthy system snapshot",
            "summary": "No incident detected, so no remediation was required.",
            "downtime_prevented": "0 minutes",
        }

    return {
        "title": f"{issue['label']} incident",
        "summary": (
            f"Detected {issue['label'].lower()} at {issue['value']}. "
            f"Selected '{winner['name']}' as the safest remediation with {confidence_score}% confidence."
        ),
        "downtime_prevented": "20-45 minutes",
    }
