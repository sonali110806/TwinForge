import sys, os, json, threading, time

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sock import Sock

from models import init_db
from twin_manager import spawn_twin, get_twins, snapshot_sync
from failure_injector import cpu_spike, crash, memory_leak, heal_all

# Allow importing ai-agent from sibling folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ai-agent"))

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
sock = Sock(app)

_ws_clients: set = set()
_ws_lock = threading.Lock()

# ── Wait for Postgres ──────────────────────────────────────────────
for _i in range(20):
    try:
        init_db()
        print("✅ Database connected")
        break
    except Exception as _e:
        print(f"⏳ Waiting for database… ({_e})")
        time.sleep(2)

# ── Background WebSocket broadcaster ──────────────────────────────
def _broadcast():
    while True:
        try:
            payload = json.dumps({
                "type":      "metrics",
                "data":      get_twins(),
                "timestamp": time.time(),
            })
            dead = set()
            with _ws_lock:
                for ws in list(_ws_clients):
                    try:
                        ws.send(payload)
                    except Exception:
                        dead.add(ws)
            with _ws_lock:
                _ws_clients -= dead
        except Exception as e:
            print(f"Broadcast error: {e}")
        time.sleep(2)

threading.Thread(target=_broadcast, daemon=True).start()

# ── REST endpoints ─────────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "timestamp": time.time()})


@app.route("/api/twins")
def twins():
    try:
        return jsonify(get_twins())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/twins/spawn", methods=["POST"])
def spawn():
    try:
        for name in ("Twin-1", "Twin-2", "Twin-3"):
            spawn_twin(name)
        return jsonify({"message": "3 twins spawned"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/failure/cpu", methods=["POST"])
def api_cpu():
    try:
        cpu_spike()
        return jsonify({"status": "cpu spike injected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/failure/crash", methods=["POST"])
def api_crash():
    try:
        crash()
        return jsonify({"status": "crashed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/failure/memory", methods=["POST"])
def api_memory():
    try:
        memory_leak()
        return jsonify({"status": "memory leak injected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/failure/heal", methods=["POST"])
def api_heal():
    try:
        heal_all()
        return jsonify({"status": "all twins healed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/agent/run", methods=["POST"])
def api_agent():
    try:
        from main import run_ai_agent
        body   = request.get_json(silent=True) or {}
        result = run_ai_agent(body.get("metrics"))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── WebSocket endpoint ─────────────────────────────────────────────
@sock.route("/ws")
def websocket(ws):
    with _ws_lock:
        _ws_clients.add(ws)
    try:
        while True:
            if ws.receive(timeout=30) is None:
                break
    except Exception:
        pass
    finally:
        with _ws_lock:
            _ws_clients.discard(ws)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
