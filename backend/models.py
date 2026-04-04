from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

from database import Base, engine


class Twin(Base):
    __tablename__ = "twins"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, default="healthy")
    config = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False, default="info")
    source = Column(String, nullable=False, default="system")
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class IncidentReport(Base):
    __tablename__ = "incident_reports"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    issue = Column(String, nullable=False)
    root_cause = Column(Text, nullable=False)
    fix_applied = Column(String, nullable=False)
    downtime_prevented = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DeploymentEvent(Base):
    __tablename__ = "deployment_events"

    id = Column(Integer, primary_key=True)
    version = Column(String, nullable=False)
    action = Column(String, nullable=False)
    status = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


def init_db():
    Base.metadata.create_all(engine)
