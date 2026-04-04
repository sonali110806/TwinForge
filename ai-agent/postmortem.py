# postmortem.py
def generate_report(issue, best_fix):
    """
    Generates a post-mortem report for the action taken.
    """
    if issue and best_fix:
        return f"Issue '{issue}' resolved using fix: '{best_fix}'."
    else:
        return "No issues detected; no report generated."
