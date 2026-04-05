from pathlib import Path
import csv
import time

import requests

from predictor import predict_cpu_trend


BACKEND_URL = "http://127.0.0.1:5000"
HISTORY_FILE = Path(__file__).resolve().parent / "history.csv"


def fetch_summary():
    response = requests.get(f"{BACKEND_URL}/api/summary", timeout=5)
    response.raise_for_status()
    return response.json()


def log_metrics(cpu, memory, latency):
    with HISTORY_FILE.open("a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["system", cpu, memory, latency])


def run_monitor(interval_seconds=5):
    while True:
        summary = fetch_summary()
        metrics = summary["system"]
        log_metrics(metrics["cpu"], metrics["memory"], metrics["latency"])
        print("SYSTEM METRICS", metrics)
        print("PREDICTION", predict_cpu_trend(str(HISTORY_FILE)))
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_monitor()
