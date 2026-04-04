<<<<<<< HEAD
# decision.py
def analyze(issue):
    """
    Analyzes the issue and provides possible fixes.
    Returns a dictionary with root cause and list of fixes.
    """
    if issue == "High CPU usage":
        return {
            "root_cause": "CPU overload due to heavy process",
            "fixes": ["Restart service", "Kill heavy process", "Optimize code"]
        }
    elif issue == "High Memory usage":
        return {
            "root_cause": "Memory leak or high memory process",
            "fixes": ["Restart app", "Clear cache", "Increase memory allocation"]
        }
    else:
        return {"root_cause": "Unknown", "fixes": []}

    
    
    
    
    
    
    
    
    
    
    
    
=======
def analyze(issue: str) -> dict:
    """Return root cause and candidate fixes for a detected issue."""
    fixes_map = {
        "High CPU usage": {
            "root_cause": "CPU overload due to heavy or runaway process",
            "fixes": [
                "Rolling restart with new memory limit",
                "Kill the heaviest process and restart gracefully",
                "Horizontal scale-out — add one more replica",
            ],
        },
        "High Memory usage": {
            "root_cause": "Memory leak or unbounded cache growth",
            "fixes": [
                "Restart app with increased memory limit",
                "Clear in-memory cache and run GC",
                "Rolling restart — preserve traffic, drain old pod",
            ],
        },
    }
    return fixes_map.get(issue, {"root_cause": "Unknown issue", "fixes": []})
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
