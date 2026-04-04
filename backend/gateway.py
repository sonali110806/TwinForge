# backend/gateway.py

def sanitize_data(raw_data):
    """
    Removes any sensitive info (for demo we assume raw_data is metrics)
    """
    safe_data = {}

    # Only allow safe metrics
    allowed_keys = ["cpu", "memory", "response_time"]

    for key in allowed_keys:
        if key in raw_data:
            safe_data[key] = raw_data[key]

    return safe_data


def enforce_policy(data):
    """
    Blocks unsafe data (simple rule-based)
    """
    # Example rule: block if unexpected keys appear
    if len(data.keys()) == 0:
        return None

    return data


def gateway_process(raw_data):
    """
    Full pipeline: filter → validate
    """
    data = sanitize_data(raw_data)
    data = enforce_policy(data)

    return data
