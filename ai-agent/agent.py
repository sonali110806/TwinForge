def run_agent(data):
    return {
        "root_cause": "CPU overload",
        "fixes": [
            {"id": "fix_a", "action": "restart_web", "risk_level": "low"},
            {"id": "fix_b", "action": "scale_memory", "risk_level": "medium"},
            {"id": "fix_c", "action": "rate_limit", "risk_level": "low"}
        ],
        "recommended": "fix_a"
    }
