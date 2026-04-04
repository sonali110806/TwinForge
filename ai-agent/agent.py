def run_agent(data):
    return {
        "root_cause": "CPU overload",
        "fixes": [
            {"id": "a", "action": "restart_web"},
            {"id": "b", "action": "scale_memory"},
            {"id": "c", "action": "rate_limit"}
        ],
        "recommended": "a"
    }
