ALL_FIXES = {

    "restart_service": {
        "id": "restart_service",
        "name": "Restart Web Service",
        "action": "restart_service",
        "description": "Fully restart the web container to clear memory and reset connections",
        "risk_level": "medium",   
        "estimated_seconds": 15,
        "good_for": ["crash", "memory_leak", "frozen_process"],
        "side_effects": ["brief_downtime_10s"]
    },

    "scale_memory": {
        "id": "scale_memory",
        "name": "Increase Memory Limit",
        "action": "scale_memory",
        "description": "Double the memory limit for the web container from 256MB to 512MB",
        "risk_level": "low",    
        "estimated_seconds": 5,
        "good_for": ["memory_exhaustion", "out_of_memory"],
        "side_effects": []
    },

    "rate_limit": {
        "id": "rate_limit",
        "name": "Apply Rate Limiting",
        "action": "rate_limit",
        "description": "Limit requests to the overloaded endpoint to 100/minute",
        "risk_level": "low",
        "estimated_seconds": 8,
        "good_for": ["cpu_spike", "traffic_overload", "ddos_like"],
        "side_effects": ["some_requests_rejected"]
    },

    "rollback": {
        "id": "rollback",
        "name": "Rollback to Last Stable Version",
        "action": "rollback",
        "description": "Revert the container to the previous working Docker image",
        "risk_level": "medium",
        "estimated_seconds": 30,
        "good_for": ["bad_deployment", "code_bug", "regression"],
        "side_effects": ["brief_downtime_30s", "latest_changes_lost"]
    },

    "scale_up": {
        "id": "scale_up",
        "name": "Scale Up Instances",
        "action": "scale_up",
        "description": "Spin up a second instance of the web service to share the load",
        "risk_level": "low",
        "estimated_seconds": 20,
        "good_for": ["cpu_spike", "high_traffic", "slow_response"],
        "side_effects": ["uses_more_resources"]
    },

    "clear_cache": {
        "id": "clear_cache",
        "name": "Clear Application Cache",
        "action": "clear_cache",
        "description": "Flush the application cache to free memory and resolve stale data",
        "risk_level": "low",
        "estimated_seconds": 3,
        "good_for": ["memory_leak", "stale_data", "slow_response"],
        "side_effects": ["temporary_slowdown_while_cache_rebuilds"]
    },
}


def get_fixes_for_anomaly(anomaly_type: str) -> list:
    """
    Given an anomaly type, return the 3 best fixes to test in tournament.
    This is called by the AI agent to pick which fixes to race.
    """
    fix_map = {
        "cpu_percent":       ["rate_limit",       "scale_up",      "restart_service"],
        "memory_percent":    ["scale_memory",      "clear_cache",   "restart_service"],
        "response_time":     ["rate_limit",        "scale_up",      "clear_cache"],
        "container_crash":   ["restart_service",   "rollback",      "scale_up"],
        "error_rate":        ["rollback",          "restart_service","rate_limit"],
    }

    fix_ids = fix_map.get(anomaly_type, ["restart_service", "scale_memory", "rate_limit"])
    return [ALL_FIXES[fid] for fid in fix_ids]