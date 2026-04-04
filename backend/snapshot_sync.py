# snapshot_sync.py
# All sync logic lives in twin_manager.snapshot_sync().
# This module exposes a scheduler wrapper for optional use.

from twin_manager import snapshot_sync
from apscheduler.schedulers.background import BackgroundScheduler


def start_sync():
    scheduler = BackgroundScheduler()
    scheduler.add_job(snapshot_sync, "interval", seconds=10)
    scheduler.start()
    return scheduler
