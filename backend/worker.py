import sys, os, time

sys.path.insert(0, os.path.dirname(__file__))

from models import init_db
from twin_manager import snapshot_sync

print("🚀 Worker started")

for _i in range(20):
    try:
        init_db()
        print("✅ Worker: database connected")
        break
    except Exception as _e:
        print(f"⏳ Worker waiting for DB… ({_e})")
        time.sleep(2)

while True:
    try:
        snapshot_sync()
        print("🔄 Twin configs synced")
    except Exception as e:
        print(f"❌ Sync error: {e}")
    time.sleep(10)
