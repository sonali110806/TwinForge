import time

from snapshot_sync import sync_twins


def run_worker(interval_seconds=10):
    print("TwinForge worker started")
    while True:
        sync_twins()
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_worker()
