from __future__ import annotations

from pathlib import Path
import csv
import sys

from flask import Flask, jsonify, request

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
AI_AGENT_DIR = PROJECT_ROOT / "ai-agent"
MONITOR_DIR = PROJECT_ROOT / "monitor"

for path in (PROJECT_ROOT, AI_AGENT_DIR, MONITOR_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from main import run_ai_agent
from predictor import predict_cpu_trend

from models import init_db
from twin_manager import (
    append_log,
    deploy_fix,
    ensure_seed_data,
    get_system_metrics,
    inject_failure,
    list_deployments,
    list_logs,
    list_reports,
    list_twins,
    record_report,
    rollback_twins,
    simulate_snapshot,
    spawn_twin,
)


app = Flask(__name__)
LATEST_ANALYSIS = None
HISTORY_FILE = MONITOR_DIR / "history.csv"

init_db()
ensure_seed_data()


def _write_history(metrics: dict) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY_FILE.open("a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["system", metrics["cpu"], metrics["memory"], metrics["latency"]])


def _current_snapshot() -> tuple[list[dict], dict]:
    twins = simulate_snapshot()
    metrics = get_system_metrics(twins)
    _write_history(metrics)
    return twins, metrics


def _generate_analysis(metrics: dict | None = None):
    global LATEST_ANALYSIS

    effective_metrics = metrics or _current_snapshot()[1]
    analysis = run_ai_agent(effective_metrics)

    if analysis.get("issue") and analysis["issue"] != "No anomaly detected":
        record_report(
            title=f"{analysis['issue']} Incident",
            issue=analysis["issue"],
            root_cause=analysis["decision"]["root_cause"],
            fix_applied=analysis["winner"]["name"],
            downtime_prevented=analysis["report"]["downtime_prevented"],
            confidence=analysis["confidence"]["score"],
            summary=analysis["report"]["summary"],
        )

    LATEST_ANALYSIS = analysis
    return analysis


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/summary", methods=["GET"])
def summary():
    twins, metrics = _current_snapshot()
    prediction = predict_cpu_trend(str(HISTORY_FILE))
    return jsonify(
        {
            "system": metrics,
            "twins": twins,
            "prediction": prediction,
            "logs": list_logs(8),
            "reports": list_reports(3),
            "deployments": list_deployments(5),
        }
    )


@app.route("/api/twins", methods=["GET", "POST"])
def twins():
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        twin = spawn_twin(payload.get("name"))
        return jsonify({"message": "Twin created", "twin": twin}), 201

    return jsonify(list_twins())


@app.route("/api/failure/<kind>", methods=["POST"])
def failure(kind: str):
    metrics = inject_failure(kind)
    analysis = _generate_analysis(metrics)
    return jsonify({"message": f"{kind} failure injected", "system": metrics, "analysis": analysis})


@app.route("/api/ai/analyze", methods=["GET", "POST"])
def analyze():
    payload = request.get_json(silent=True) or {}
    metrics = payload.get("metrics")
    analysis = _generate_analysis(metrics)
    return jsonify(analysis)


@app.route("/api/ai/latest", methods=["GET"])
def latest_ai():
    if LATEST_ANALYSIS is None:
        _generate_analysis()
    return jsonify(LATEST_ANALYSIS)


@app.route("/api/deploy", methods=["POST"])
def deploy():
    global LATEST_ANALYSIS

    if LATEST_ANALYSIS is None:
        _generate_analysis()

    winner = LATEST_ANALYSIS["winner"]
    if winner is None:
        return jsonify({"message": "No deployable fix available"}), 400

    metrics = deploy_fix(winner["name"], LATEST_ANALYSIS["confidence"]["score"])
    append_log(f"Deployment completed for {winner['name']}", level="success", source="deploy")
    return jsonify({"message": "Winning fix deployed", "winner": winner, "system": metrics})


@app.route("/api/rollback", methods=["POST"])
def rollback():
    metrics = rollback_twins()
    return jsonify({"message": "Rollback completed", "system": metrics})


@app.route("/api/reports", methods=["GET"])
def reports():
    return jsonify(list_reports(20))


@app.route("/api/logs", methods=["GET"])
def logs():
    return jsonify(list_logs(100))


@app.route("/api/deployments", methods=["GET"])
def deployments():
    return jsonify(list_deployments(20))


@app.route("/api/settings", methods=["GET"])
def settings():
    return jsonify(
        [
            {"label": "Metrics Poll Interval", "value": "2s", "description": "Frontend refresh cadence for summary data."},
            {"label": "Auto Seed Twins", "value": "Enabled", "description": "Bootstraps 3 twins on first startup."},
            {"label": "Database", "value": "SQLite", "description": "Uses a local database unless DATABASE_URL is set."},
            {"label": "Failure Threshold", "value": "CPU > 85%", "description": "Critical threshold used by the AI detector."},
            {"label": "Prediction Source", "value": "history.csv", "description": "Trend predictor reads persisted metric history."},
        ]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
