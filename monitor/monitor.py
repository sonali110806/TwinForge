import os, time, requests
from datetime import datetime
from predictor import predict_cpu_trend, HISTORY_PATH

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")


def get_cpu_usage() -> float:
    try:
        res    = requests.get(f"{PROMETHEUS_URL}/api/v1/query",
                              params={"query": "rate(container_cpu_usage_seconds_total[1m])"},
                              timeout=5).json()
        values = res["data"]["result"]
        return round(sum(float(v["value"][1]) for v in values) * 100, 2) if values else 0.0
    except Exception as e:
        print(f"Error fetching CPU: {e}")
        return 0.0


def get_memory_usage() -> float:
    try:
        res    = requests.get(f"{PROMETHEUS_URL}/api/v1/query",
                              params={"query": "container_memory_usage_bytes"},
                              timeout=5).json()
        values = res["data"]["result"]
        return round(sum(float(v["value"][1]) for v in values) / (1024 * 1024), 2) if values else 0.0
    except Exception as e:
        print(f"Error fetching Memory: {e}")
        return 0.0


def check_alerts(cpu: float, memory: float):
    if cpu    > 80:   print("🚨 ALERT: High CPU Usage!")
    if memory > 1500: print("🚨 ALERT: High Memory Usage!")


def log_to_csv(cpu: float, memory: float):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')},{cpu},{memory},0\n")


if __name__ == "__main__":
    while True:
        cpu    = get_cpu_usage()
        memory = get_memory_usage()
        print(f"\n===== SYSTEM METRICS =====")
        print(f"CPU Usage:    {cpu}%")
        print(f"Memory Usage: {memory} MB")
        check_alerts(cpu, memory)
        print(predict_cpu_trend())
        log_to_csv(cpu, memory)
        time.sleep(5)
