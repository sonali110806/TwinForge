from models import SessionLocal, Twin
import random


def cpu_spike():
    db = SessionLocal()
    try:
        for t in db.query(Twin).all():
            t.cpu    = 99.0
            t.status = "cpu_spike"
            t.config = {**(t.config or {}), "cpu": 99}
        db.commit()
    finally:
        db.close()


def crash():
    db = SessionLocal()
    try:
        for t in db.query(Twin).all():
            t.status = "crashed"
        db.commit()
    finally:
        db.close()


def memory_leak():
    db = SessionLocal()
    try:
        for t in db.query(Twin).all():
            t.memory = float(random.randint(95, 100))
            t.status = "memory_leak"
            t.config = {**(t.config or {}), "memory": round(t.memory, 1)}
        db.commit()
    finally:
        db.close()


def heal_all():
    db = SessionLocal()
    try:
        for t in db.query(Twin).all():
            t.status = "healthy"
            t.cpu    = float(random.randint(20, 45))
            t.memory = float(random.randint(30, 60))
            t.config = {**(t.config or {}), "cpu": round(t.cpu, 1), "memory": round(t.memory, 1)}
        db.commit()
    finally:
        db.close()
