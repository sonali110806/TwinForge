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

    
    
    
    
    
    
    
    
    
    
    
    
