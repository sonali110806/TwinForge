from __future__ import annotations

from pathlib import Path
from datetime import datetime
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
ACTIVE_INCIDENT = None

init_db()
ensure_seed_data()


def _safe_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _metrics_from_incident(payload: dict) -> dict:
    severity = (payload.get("severity") or "medium").lower()
    issue_type = (payload.get("issueType") or "").lower()
    combined_text = " ".join(
        [
            str(payload.get("issueDescription") or ""),
            str(payload.get("errorLogs") or ""),
            str(payload.get("codeSnippet") or ""),
            issue_type,
        ]
    ).lower()

    default_cpu = {"low": 55, "medium": 78, "high": 95}.get(severity, 78)
    default_memory = {"low": 48, "medium": 72, "high": 91}.get(severity, 72)
    default_latency = {"low": 110, "medium": 220, "high": 360}.get(severity, 220)

    if any(keyword in combined_text for keyword in ["memory", "heap", "leak", "outofmemory", "out of memory"]):
        default_memory = max(default_memory, 94)
        default_latency = max(default_latency, 260)
    if any(keyword in combined_text for keyword in ["timeout", "latency", "slow", "503", "gateway", "response"]):
        default_latency = max(default_latency, 320)
        default_cpu = max(default_cpu, 74)
    if any(keyword in combined_text for keyword in ["cpu", "loop", "recursion", "100%", "spike", "traffic"]):
        default_cpu = max(default_cpu, 95)
    if any(keyword in combined_text for keyword in ["crash", "panic", "fatal", "segmentation", "exception"]):
        default_cpu = max(default_cpu, 92)
        default_memory = max(default_memory, 88)
        default_latency = max(default_latency, 380)

    return {
        "cpu": _safe_float(payload.get("cpu"), default_cpu),
        "memory": _safe_float(payload.get("memory"), default_memory),
        "latency": _safe_float(payload.get("latency"), default_latency),
    }


def _generate_fix_snippet(winner: dict | None) -> str:
    if not winner:
        return "# No remediation code required."

    snippets = {
        "rate_limit": """# Example remediation\nfrom flask_limiter import Limiter\nlimiter.limit('100/minute')(checkout_handler)""",
        "scale_up": """# Example deployment change\nreplicas:\n  web:\n    count: 3""",
        "restart_service": """# Example operational fix\nsudo systemctl restart twinforge-web\n# or restart the affected deployment""",
        "scale_memory": """# Example container resource update\nservices:\n  web:\n    deploy:\n      resources:\n        limits:\n          memory: 512M""",
        "clear_cache": """# Example application fix\ncache.clear()\n# rebuild stale objects on next request""",
    }
    return snippets.get(winner.get("fix_id"), "# Remediation snippet unavailable for this fix.")


def _status_from_metrics(metrics: dict) -> str:
    cpu = float(metrics.get("cpu", 0))
    memory = float(metrics.get("memory", 0))
    latency = float(metrics.get("latency", 0))
    if cpu >= 85 or memory >= 88 or latency >= 250:
        return "critical"
    if cpu >= 70 or memory >= 75 or latency >= 180:
        return "warning"
    return "healthy"


def _build_incident_twins(metrics: dict, app_name: str, issue: str, winner_name: str) -> list[dict]:
    cpu = float(metrics.get("cpu", 0))
    memory = float(metrics.get("memory", 0))
    latency = float(metrics.get("latency", 0))
    base_names = [f"{app_name} Primary", f"{app_name} Shadow", f"{app_name} Recovery"]
    adjustments = [(0, 0, 0), (-8, -5, -30), (+6, +4, +45)]
    now = Path(HISTORY_FILE).stat().st_mtime if HISTORY_FILE.exists() else None

    twins = []
    for index, (name, (cpu_delta, mem_delta, lat_delta)) in enumerate(zip(base_names, adjustments), start=1):
        twin_cpu = max(1, min(99, round(cpu + cpu_delta, 2)))
        twin_memory = max(1, min(99, round(memory + mem_delta, 2)))
        twin_latency = max(40, min(600, round(latency + lat_delta, 2)))
        twin_status = _status_from_metrics(
            {"cpu": twin_cpu, "memory": twin_memory, "latency": twin_latency}
        )
        twins.append(
            {
                "id": index,
                "name": name,
                "status": twin_status,
                "cpu": twin_cpu,
                "memory": twin_memory,
                "latency": twin_latency,
                "version": f"incident-{index}",
                "lastFix": winner_name,
                "uptimeSeconds": 1800 + index * 320,
                "updatedAt": datetime.utcnow().isoformat(),
                "createdAt": datetime.utcnow().isoformat(),
                "issue": issue,
            }
        )

    return twins


def _set_active_incident(app_name: str, metrics: dict, analysis: dict, issue_description: str) -> None:
    global ACTIVE_INCIDENT

    winner_name = analysis.get("winner", {}).get("name", "No fix needed")
    ACTIVE_INCIDENT = {
        "appName": app_name,
        "system": {
            "cpu": round(float(metrics.get("cpu", 0)), 2),
            "memory": round(float(metrics.get("memory", 0)), 2),
            "latency": round(float(metrics.get("latency", 0)), 2),
            "status": _status_from_metrics(metrics),
            "twinCount": 3,
        },
        "twins": _build_incident_twins(metrics, app_name, analysis.get("issue", "No anomaly detected"), winner_name),
        "prediction": f"Active incident for {app_name}: {issue_description[:100]}",
    }


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
    if ACTIVE_INCIDENT is not None:
        twins = ACTIVE_INCIDENT["twins"]
        metrics = ACTIVE_INCIDENT["system"]
        prediction = ACTIVE_INCIDENT["prediction"]
    else:
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
    global ACTIVE_INCIDENT
    metrics = inject_failure(kind)
    analysis = _generate_analysis(metrics)
    _set_active_incident("TwinForge Fleet", metrics, analysis, f"Injected {kind} failure for simulation")
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
    global LATEST_ANALYSIS, ACTIVE_INCIDENT

    if LATEST_ANALYSIS is None:
        _generate_analysis()

    winner = LATEST_ANALYSIS["winner"]
    if winner is None:
        return jsonify({"message": "No deployable fix available"}), 400

    metrics = deploy_fix(winner["name"], LATEST_ANALYSIS["confidence"]["score"])
    append_log(f"Deployment completed for {winner['name']}", level="success", source="deploy")
    ACTIVE_INCIDENT = {
        "appName": ACTIVE_INCIDENT["appName"] if ACTIVE_INCIDENT else "TwinForge Fleet",
        "system": {**metrics, "status": "healthy"},
        "twins": _build_incident_twins(metrics, ACTIVE_INCIDENT["appName"] if ACTIVE_INCIDENT else "TwinForge Fleet", "Resolved incident", winner["name"]),
        "prediction": f"Deployment applied successfully: {winner['name']}",
    }
    return jsonify({"message": "Winning fix deployed", "winner": winner, "system": metrics})


@app.route("/api/rollback", methods=["POST"])
def rollback():
    global ACTIVE_INCIDENT, LATEST_ANALYSIS
    metrics = rollback_twins()
    ACTIVE_INCIDENT = None
    LATEST_ANALYSIS = run_ai_agent(metrics)
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


@app.route("/api/incident/submit", methods=["POST"])
@app.route("/api/code-analysis/submit", methods=["POST"])
def incident_submit():
    global LATEST_ANALYSIS

    payload = request.get_json(silent=True) or {}
    metrics = _metrics_from_incident(payload)
    analysis = run_ai_agent(metrics)

    app_name = payload.get("appName") or "Unknown Application"
    issue_description = payload.get("issueDescription") or "No description provided"
    environment = payload.get("environment") or "unknown"
    severity = payload.get("severity") or "medium"
    error_logs = payload.get("errorLogs") or ""
    code_snippet = payload.get("codeSnippet") or ""
    remediation_code = _generate_fix_snippet(analysis.get("winner"))

    if analysis.get("issue") and analysis["issue"] != "No anomaly detected" and analysis.get("winner"):
        report = record_report(
            title=f"{app_name} Incident Report",
            issue=analysis["issue"],
            root_cause=analysis["decision"]["root_cause"],
            fix_applied=analysis["winner"]["name"],
            downtime_prevented=analysis["report"]["downtime_prevented"],
            confidence=analysis["confidence"]["score"],
            summary=(
                f"Application: {app_name}. Environment: {environment}. "
                f"Severity: {severity}. Incident: {issue_description}. "
                f"Logs summary: {error_logs[:180]}. "
                f"AI summary: {analysis['report']['summary']}"
            ),
        )
        append_log(
            f"Incident submitted for {app_name}: {analysis['issue']}",
            level="warning",
            source="incident-form",
        )
    else:
        report = {
            "title": f"{app_name} Healthy Report",
            "summary": f"No anomaly detected for {app_name}. Incident details: {issue_description}",
        }
        append_log(
            f"Incident form submitted for {app_name} with no anomaly detected",
            level="info",
            source="incident-form",
        )

    LATEST_ANALYSIS = analysis
    _set_active_incident(app_name, metrics, analysis, issue_description)
    return jsonify(
        {
            "input": {
                "appName": app_name,
                "issueDescription": issue_description,
                "severity": severity,
                "environment": environment,
                "errorLogs": error_logs,
                "codeSnippet": code_snippet,
                "metrics": metrics,
            },
            "analysis": analysis,
            "report": report,
            "remediationCode": remediation_code,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
