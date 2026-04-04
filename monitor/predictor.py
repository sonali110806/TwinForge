import os
import pandas as pd
import numpy as np

_HERE        = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(_HERE, "history.csv")
COLUMNS      = ["timestamp", "cpu", "memory", "network"]


def _load_history() -> pd.DataFrame:
    if not os.path.exists(HISTORY_PATH):
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(HISTORY_PATH, names=COLUMNS, header=None)


def predict_cpu_trend() -> str:
    try:
        df = _load_history()
        if len(df) < 5:
            return "⏳ Collecting data…"

        cpu_values = pd.to_numeric(df["cpu"], errors="coerce").dropna().tail(10).values
        if len(cpu_values) < 3:
            return "⏳ Insufficient numeric data…"

        x     = np.arange(len(cpu_values))
        slope = np.polyfit(x, cpu_values, 1)[0]

        if slope > 0.5:
            seconds = max(1, int((100 - cpu_values[-1]) / slope))
            return f"⚠️ CPU rising fast → possible crash in ~{seconds}s"
        if slope > 0.2:
            return "⚠️ CPU gradually increasing"
        return "✅ CPU stable"
    except Exception as e:
        return f"Prediction error: {e}"
