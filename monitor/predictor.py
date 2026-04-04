from pathlib import Path
import csv


def predict_cpu_trend(history_path="monitor/history.csv"):
    path = Path(history_path)
    if not path.exists():
        return "Collecting data..."

    values = []
    with path.open(newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            try:
                values.append(float(row[1]))
            except ValueError:
                continue

    if len(values) < 5:
        return "Collecting data..."

    recent = values[-10:]
    slope = (recent[-1] - recent[0]) / max(1, len(recent) - 1)

    if slope > 1.2:
        return f"CPU rising fast, estimated instability in ~{int(100 / slope)} sec"
    if slope > 0.4:
        return "CPU gradually increasing"
    return "CPU stable"
