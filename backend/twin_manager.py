from models import SessionLocal, Twin
import random


def spawn_twin(name: str) -> dict:
    db = SessionLocal()
    try:
        cpu    = float(random.randint(10, 40))
        memory = float(random.randint(20, 50))
        twin   = Twin(
            name=name,
            status="healthy",
            cpu=cpu,
            memory=memory,
            config={"cpu": cpu, "memory": memory, "version": "1.0"},
        )
        db.add(twin)
        db.commit()
        db.refresh(twin)
        return {"message": f"{name} spawned", "id": twin.id}
    finally:
        db.close()


def get_twins() -> list:
    db = SessionLocal()
    try:
        return [
            {
                "id":     t.id,
                "name":   t.name,
                "status": t.status,
                "cpu":    round(t.cpu,    1),
                "memory": round(t.memory, 1),
                "config": t.config or {},
            }
            for t in db.query(Twin).all()
        ]
    finally:
        db.close()


def snapshot_sync():
    """Simulate real telemetry fluctuation on all healthy twins."""
    db = SessionLocal()
    try:
        for t in db.query(Twin).all():
            if t.status == "healthy":
                t.cpu    = max(0.0, min(100.0, t.cpu    + random.uniform(-3, 3)))
                t.memory = max(0.0, min(100.0, t.memory + random.uniform(-2, 2)))
                t.config = {**(t.config or {}), "cpu": round(t.cpu, 1), "memory": round(t.memory, 1)}
        db.commit()
    finally:
        db.close()
