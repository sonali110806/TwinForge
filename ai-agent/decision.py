def analyze(issue):
    if not issue:
        return {"root_cause": "System healthy", "fixes": []}

    anomaly_type = issue["type"]
    root_cause_map = {
        "cpu_percent": "Traffic spike or runaway compute workload overloaded the service.",
        "memory_percent": "Memory pressure suggests a leak, cache growth, or oversized workload.",
        "response_time": "Upstream dependency latency is cascading into slower responses.",
    }

    fix_map = {
        "cpu_percent": [
            {
                "id": "rate_limit",
                "name": "Apply Rate Limiting",
                "action": "rate_limit",
                "risk_level": "low",
                "estimated_seconds": 8,
                "good_for": ["cpu_percent", "response_time"],
                "side_effects": ["some_requests_rejected"],
            },
            {
                "id": "scale_up",
                "name": "Scale Up Instances",
                "action": "scale_up",
                "risk_level": "low",
                "estimated_seconds": 20,
                "good_for": ["cpu_percent", "response_time"],
                "side_effects": ["uses_more_resources"],
            },
            {
                "id": "restart_service",
                "name": "Restart Web Service",
                "action": "restart_service",
                "risk_level": "medium",
                "estimated_seconds": 15,
                "good_for": ["cpu_percent", "memory_percent"],
                "side_effects": ["brief_downtime_10s"],
            },
        ],
        "memory_percent": [
            {
                "id": "scale_memory",
                "name": "Increase Memory Limit",
                "action": "scale_memory",
                "risk_level": "low",
                "estimated_seconds": 5,
                "good_for": ["memory_percent"],
                "side_effects": [],
            },
            {
                "id": "clear_cache",
                "name": "Clear Application Cache",
                "action": "clear_cache",
                "risk_level": "low",
                "estimated_seconds": 3,
                "good_for": ["memory_percent", "response_time"],
                "side_effects": ["temporary_slowdown"],
            },
            {
                "id": "restart_service",
                "name": "Restart Web Service",
                "action": "restart_service",
                "risk_level": "medium",
                "estimated_seconds": 15,
                "good_for": ["memory_percent"],
                "side_effects": ["brief_downtime_10s"],
            },
        ],
        "response_time": [
            {
                "id": "rate_limit",
                "name": "Apply Rate Limiting",
                "action": "rate_limit",
                "risk_level": "low",
                "estimated_seconds": 8,
                "good_for": ["response_time"],
                "side_effects": ["some_requests_rejected"],
            },
            {
                "id": "scale_up",
                "name": "Scale Up Instances",
                "action": "scale_up",
                "risk_level": "low",
                "estimated_seconds": 20,
                "good_for": ["response_time"],
                "side_effects": ["uses_more_resources"],
            },
            {
                "id": "clear_cache",
                "name": "Clear Application Cache",
                "action": "clear_cache",
                "risk_level": "low",
                "estimated_seconds": 3,
                "good_for": ["response_time"],
                "side_effects": ["temporary_slowdown"],
            },
        ],
    }

    return {
        "anomaly_type": anomaly_type,
        "root_cause": root_cause_map.get(anomaly_type, "Unknown infrastructure regression."),
        "fixes": fix_map.get(anomaly_type, []),
    }
