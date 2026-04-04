from __future__ import annotations

from datetime import datetime, timedelta
import random
from typing import Any

from sqlalchemy import desc

from database import SessionLocal
from models import ActivityLog, DeploymentEvent, IncidentReport, Twin


STATUS_PRIORITY = {"healthy": "healthy", "warning": "warning", "critical": "critical"}


def _base_config(index: int) -> dict[str, Any]:
    return {
        "cpu": 28 + index * 7,
        "memory": 40 + index * 6,
        "latency": 95 + index * 12,
        "version": f"1.0.{index}",
        "last_fix": "None",
    }


def _log(db, message: str, level: str = "info", source: str = "backend") -> ActivityLog:
    entry = ActivityLog(level=level, source=source, message=message)
    db.add(entry)
    db.flush()
    return entry


def ensure_seed_data() -> None:
    db = SessionLocal()
    try:
        if db.query(Twin).count() == 0:
            for index in range(3):
                twin = Twin(name=f"Twin-{index + 1}", status="healthy", config=_base_config(index))
                twin.created_at = datetime.utcnow() - timedelta(hours=6 - index)
                twin.updated_at = twin.created_at
                db.add(twin)

            _log(db, "TwinForge initialized with 3 digital twins", source="bootstrap")
            db.add(
                DeploymentEvent(
                    version="v1.0.0",
                    action="bootstrap",
                    status="success",
                    details="Initial TwinForge environment provisioned.",
                )
            )
            db.commit()
    finally:
        db.close()


def serialize_twin(twin: Twin) -> dict[str, Any]:
    config = twin.config or {}
    uptime_seconds = max(0, int((datetime.utcnow() - twin.created_at).total_seconds()))
    return {
        "id": twin.id,
        "name": twin.name,
        "status": twin.status,
        "cpu": round(float(config.get("cpu", 0)), 2),
        "memory": round(float(config.get("memory", 0)), 2),
        "latency": round(float(config.get("latency", 0)), 2),
        "version": config.get("version", "1.0.0"),
        "lastFix": config.get("last_fix", "None"),
        "uptimeSeconds": uptime_seconds,
        "updatedAt": twin.updated_at.isoformat(),
        "createdAt": twin.created_at.isoformat(),
    }


def list_twins() -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        twins = db.query(Twin).order_by(Twin.id.asc()).all()
        return [serialize_twin(twin) for twin in twins]
    finally:
        db.close()


def spawn_twin(name: str | None = None) -> dict[str, Any]:
    db = SessionLocal()
    try:
        next_number = db.query(Twin).count() + 1
        twin_name = name or f"Twin-{next_number}"
        twin = Twin(name=twin_name, status="healthy", config=_base_config(next_number))
        db.add(twin)
        db.flush()
        _log(db, f"{twin_name} created and attached to the fleet", source="deploy")
        db.commit()
        db.refresh(twin)
        return serialize_twin(twin)
    finally:
        db.close()


def _derive_status(cpu: float, memory: float, latency: float) -> str:
    if cpu >= 85 or memory >= 88 or latency >= 250:
        return "critical"
    if cpu >= 70 or memory >= 75 or latency >= 180:
        return "warning"
    return "healthy"


def simulate_snapshot() -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        twins = db.query(Twin).order_by(Twin.id.asc()).all()
        for twin in twins:
            config = dict(twin.config or {})
            drift = 12 if twin.status in {"cpu_spike", "memory_leak", "crashed", "critical"} else 5

            if twin.status == "crashed":
                config["cpu"] = 0
                config["memory"] = max(5, float(config.get("memory", 0)) - 4)
                config["latency"] = 500
            else:
                config["cpu"] = max(1, min(99, float(config.get("cpu", 0)) + random.uniform(-drift, drift)))
                config["memory"] = max(1, min(99, float(config.get("memory", 0)) + random.uniform(-drift / 2, drift / 2)))
                config["latency"] = max(40, min(600, float(config.get("latency", 100)) + random.uniform(-25, 25)))

            twin.status = _derive_status(config["cpu"], config["memory"], config["latency"])
            twin.config = config
            twin.updated_at = datetime.utcnow()

        db.commit()
        return [serialize_twin(twin) for twin in twins]
    finally:
        db.close()


def get_system_metrics(twins: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    data = twins or list_twins()
    if not data:
        return {"cpu": 0, "memory": 0, "latency": 0, "status": "healthy", "twinCount": 0}

    cpu = round(sum(twin["cpu"] for twin in data) / len(data), 2)
    memory = round(sum(twin["memory"] for twin in data) / len(data), 2)
    latency = round(sum(twin["latency"] for twin in data) / len(data), 2)
    status = _derive_status(cpu, memory, latency)
    return {"cpu": cpu, "memory": memory, "latency": latency, "status": status, "twinCount": len(data)}


def inject_failure(kind: str) -> dict[str, Any]:
    db = SessionLocal()
    try:
        twins = db.query(Twin).order_by(Twin.id.asc()).all()
        if kind == "cpu":
            for twin in twins:
                config = dict(twin.config or {})
                config["cpu"] = random.randint(91, 99)
                config["latency"] = max(220, config.get("latency", 200))
                twin.config = config
                twin.status = "critical"
            _log(db, "CPU spike injected across digital twins", level="warning", source="failure")
        elif kind == "memory":
            for twin in twins:
                config = dict(twin.config or {})
                config["memory"] = random.randint(92, 99)
                config["latency"] = max(200, config.get("latency", 180))
                twin.config = config
                twin.status = "critical"
            _log(db, "Memory leak injected across digital twins", level="warning", source="failure")
        elif kind == "crash":
            for twin in twins:
                config = dict(twin.config or {})
                config["cpu"] = 0
                config["latency"] = 500
                twin.config = config
                twin.status = "crashed"
            _log(db, "Crash scenario injected across digital twins", level="error", source="failure")
        else:
            raise ValueError(f"Unsupported failure kind: {kind}")

        for twin in twins:
            twin.updated_at = datetime.utcnow()

        db.commit()
        return get_system_metrics([serialize_twin(twin) for twin in twins])
    finally:
        db.close()


def rollback_twins() -> dict[str, Any]:
    db = SessionLocal()
    try:
        twins = db.query(Twin).order_by(Twin.id.asc()).all()
        for index, twin in enumerate(twins):
            twin.status = "healthy"
            twin.config = _base_config(index)
            twin.updated_at = datetime.utcnow()

        _log(db, "System rollback completed and all twins restored", level="success", source="deploy")
        db.add(
            DeploymentEvent(
                version=f"v1.0.{db.query(DeploymentEvent).count() + 1}",
                action="rollback",
                status="success",
                details="Restored the fleet to a healthy baseline configuration.",
            )
        )
        db.commit()
        return get_system_metrics([serialize_twin(twin) for twin in twins])
    finally:
        db.close()


def deploy_fix(fix_name: str, confidence: int) -> dict[str, Any]:
    db = SessionLocal()
    try:
        twins = db.query(Twin).order_by(Twin.id.asc()).all()
        for twin in twins:
            config = dict(twin.config or {})
            config["cpu"] = max(18, config.get("cpu", 30) - random.randint(18, 30))
            config["memory"] = max(22, config.get("memory", 40) - random.randint(12, 20))
            config["latency"] = max(60, config.get("latency", 100) - random.randint(40, 90))
            config["last_fix"] = fix_name
            twin.config = config
            twin.status = "healthy"
            twin.updated_at = datetime.utcnow()

        _log(db, f"Winning fix deployed: {fix_name}", level="success", source="deploy")
        db.add(
            DeploymentEvent(
                version=f"v1.1.{db.query(DeploymentEvent).count() + 1}",
                action="deploy",
                status="success",
                details=f"Applied '{fix_name}' with {confidence}% confidence.",
            )
        )
        db.commit()
        return get_system_metrics([serialize_twin(twin) for twin in twins])
    finally:
        db.close()


def record_report(title: str, issue: str, root_cause: str, fix_applied: str, downtime_prevented: str, confidence: int, summary: str) -> dict[str, Any]:
    db = SessionLocal()
    try:
        report = IncidentReport(
            title=title,
            issue=issue,
            root_cause=root_cause,
            fix_applied=fix_applied,
            downtime_prevented=downtime_prevented,
            confidence=confidence,
            summary=summary,
        )
        db.add(report)
        _log(db, f"Post-mortem generated for '{issue}'", level="info", source="ai-agent")
        db.commit()
        db.refresh(report)
        return serialize_report_obj(report)
    finally:
        db.close()


def serialize_report_obj(report: IncidentReport) -> dict[str, Any]:
    return {
        "id": report.id,
        "title": report.title,
        "issue": report.issue,
        "rootCause": report.root_cause,
        "fixApplied": report.fix_applied,
        "downtimePrevented": report.downtime_prevented,
        "confidence": report.confidence,
        "summary": report.summary,
        "createdAt": report.created_at.isoformat(),
    }


def list_reports(limit: int = 10) -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        reports = db.query(IncidentReport).order_by(desc(IncidentReport.created_at)).limit(limit).all()
        return [serialize_report_obj(report) for report in reports]
    finally:
        db.close()


def list_logs(limit: int = 50) -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        logs = db.query(ActivityLog).order_by(desc(ActivityLog.created_at)).limit(limit).all()
        return [
            {
                "id": entry.id,
                "type": entry.level,
                "source": entry.source,
                "message": entry.message,
                "timestamp": entry.created_at.isoformat(),
            }
            for entry in logs
        ]
    finally:
        db.close()


def list_deployments(limit: int = 10) -> list[dict[str, Any]]:
    db = SessionLocal()
    try:
        deployments = db.query(DeploymentEvent).order_by(desc(DeploymentEvent.created_at)).limit(limit).all()
        return [
            {
                "id": event.id,
                "version": event.version,
                "action": event.action,
                "status": event.status,
                "details": event.details,
                "createdAt": event.created_at.isoformat(),
            }
            for event in deployments
        ]
    finally:
        db.close()


def append_log(message: str, level: str = "info", source: str = "backend") -> dict[str, Any]:
    db = SessionLocal()
    try:
        entry = _log(db, message, level=level, source=source)
        db.commit()
        return {
            "id": entry.id,
            "type": entry.level,
            "source": entry.source,
            "message": entry.message,
            "timestamp": entry.created_at.isoformat(),
        }
    finally:
        db.close()
