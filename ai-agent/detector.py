def detect(metrics):
    cpu = float(metrics.get("cpu", 0))
    memory = float(metrics.get("memory", 0))
    latency = float(metrics.get("latency", 0))

    if cpu >= 90:
        return {"type": "cpu_percent", "label": "High CPU usage", "value": cpu}
    if memory >= 90:
        return {"type": "memory_percent", "label": "High Memory usage", "value": memory}
    if latency >= 250:
        return {"type": "response_time", "label": "High latency", "value": latency}

    return None
