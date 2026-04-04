# TwinForge — Digital Twin IT

> Zero-risk autonomous IT: test every fix on a shadow twin before touching production.

## Quick Start

### Option A — Docker (recommended)
```bash
docker compose up --build
```
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000
- Prometheus: http://localhost:9090

### Option B — Local development

**Backend**
```bash
cd backend
pip install -r requirements.txt
# Requires Postgres running locally
DATABASE_URL=postgresql://twin:twin@localhost:5432/digitwin python app.py
# In a second terminal:
DATABASE_URL=postgresql://twin:twin@localhost:5432/digitwin python worker.py
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:8080
```

**AI Agent (standalone test)**
```bash
cd ai-agent
python main.py
```

## Project Structure
```
DigiTwin/
├── backend/          # Flask API + WebSocket broadcaster
│   ├── app.py        # Main server (CORS, WS, REST)
│   ├── models.py     # SQLAlchemy models (single source of truth)
│   ├── twin_manager.py
│   ├── failure_injector.py
│   ├── worker.py     # Background sync loop
│   └── requirements.txt
├── ai-agent/         # Autonomous fix pipeline
│   ├── main.py       # Orchestrator
│   ├── detector.py   # Anomaly detection
│   ├── decision.py   # Root cause + fix generation
│   ├── tournament.py # Shadow twin simulation tournament
│   ├── confidence.py # Score-based deployment gating
│   └── postmortem.py # Structured incident report
├── monitor/          # Prometheus metrics + trend prediction
│   ├── monitor.py
│   ├── predictor.py
│   └── prometheus.yml
├── frontend/         # React + Tailwind dashboard (UI unchanged)
└── docker-compose.yml
```

## Fixes Applied (vs original)
| File | Fix |
|------|-----|
| `backend/database.py` | **Removed** — was an exact duplicate of models.py causing import conflicts |
| `backend/models.py` | Added `cpu` and `memory` as proper DB columns (not just in JSON) |
| `backend/app.py` | Added CORS, WebSocket endpoint, `/api/health`, `/api/agent/run`, `/api/failure/heal` |
| `backend/requirements.txt` | Added `Flask-Cors`, `flask-sock`, `APScheduler` |
| `backend/worker.py` | Added DB init retry on startup |
| `backend/snapshot_sync.py` | Fixed to use unified `twin_manager.snapshot_sync()` |
| `backend/failure_injector.py` | Fixed to use top-level `cpu`/`memory` columns |
| `ai-agent/tournament.py` | Now actually runs all fixes and picks fastest passing one |
| `ai-agent/confidence.py` | Score is now dynamic (based on simulation result, not hardcoded) |
| `ai-agent/postmortem.py` | Returns structured dict instead of plain string |
| `ai-agent/agent.py` | `build_prompt()` now called from `main.py` |
| `monitor/predictor.py` | Fixed relative path bug (was breaking on any CWD) |
| `monitor/monitor.py` | Fixed path + added column headers for CSV |
| `frontend/vite.config.ts` | Removed `lovable-tagger`, added `/api` + `/ws` proxy |
| `frontend/package.json` | Removed `lovable-tagger` dev dependency |
| `frontend/index.html` | Updated title from "Lovable App" to "TwinForge" |
| `docker-compose.yml` | Mounted `ai-agent/` into backend container, added Prometheus service |
