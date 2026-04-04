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
