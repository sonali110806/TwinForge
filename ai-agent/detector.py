<<<<<<< HEAD
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
=======
def detect(metrics: dict) -> str | None:
    """Detect anomalies from system metrics. Returns issue string or None."""
    cpu    = metrics.get("cpu",    0)
    memory = metrics.get("memory", 0)
    if cpu > 90:
        return "High CPU usage"
    if memory > 90:
        return "High Memory usage"
    return None
>>>>>>> f456c65 (Initial TwinForge fullstack setup)
