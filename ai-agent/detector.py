# detector.py
def detect(metrics):
    """
    Detects anomalies based on system metrics.
    Returns an issue string if anomaly is detected, else None.
    """
    if metrics["cpu"] > 90:
        return "High CPU usage"
    elif metrics["memory"] > 90:
        return "High Memory usage"
    else:
        return None
