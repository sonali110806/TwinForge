<<<<<<< HEAD
# tournament.py
def run_tournament(decision):
    """
    Selects the best fix from the list of fixes.
    Currently selects the first one for simplicity.
    """
    fixes = decision.get("fixes", [])
    if fixes:
        return fixes[0]  # Best fix
    else:
        return "No fix available"
=======
import random
import time


def _simulate_fix_on_twin(fix: str) -> dict:
    """Simulate applying fix on a shadow twin. Returns result dict."""
    start      = time.time()
    time.sleep(random.uniform(0.3, 1.5))
    elapsed    = round(time.time() - start, 2)
    base_prob  = 0.85 if "restart" in fix.lower() else 0.72
    passed     = random.random() < base_prob
    return {
        "fix":              fix,
        "passed":           passed,
        "execution_time":   elapsed,
        "success_prob":     round(base_prob * 100),
        "performance_gain": random.randint(10, 35),
        "risk":             "low" if base_prob > 0.80 else "medium",
    }


def run_tournament(decision: dict) -> dict:
    """
    Run every candidate fix against a simulated twin.
    Returns the best (fastest passing) fix with full results.
    """
    fixes   = decision.get("fixes", [])
    results = []

    for fix in fixes:
        result = _simulate_fix_on_twin(fix)
        results.append(result)
        status = "PASSED" if result["passed"] else "FAILED"
        print(f"  Twin sim — {fix[:45]}: {status} ({result['execution_time']}s)")

    passing = [r for r in results if r["passed"]]
    winner  = min(passing, key=lambda r: r["execution_time"]) if passing else results[0]

    return {
        "winner":      winner["fix"],
        "all_results": results,
        "twin_passed": winner["passed"],
    }
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
