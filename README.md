# IncidentPilot — Production Incident Autopilot Agent on Qwen Cloud

IncidentPilot is a production-style incident response autopilot agent. It receives alerts, creates incidents, investigates logs/metrics/deployments/runbooks, uses Qwen Cloud for reasoning, proposes safe remediations, requests human approval, executes approved actions, verifies recovery, and generates postmortems.

## Stack

- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: Vite + React + TypeScript
- Agent: Supervisor workflow with Qwen Cloud-compatible client and deterministic tools
- DB: PostgreSQL schema + seed data
- Deployment: Docker Compose, Alibaba Cloud ECS helper files

## Quick Start

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Demo Flow

1. Open dashboard.
2. Click **Trigger Demo Alert**.
3. Open the created incident.
4. Watch IncidentPilot investigate.
5. Approve rollback.
6. See remediation, verification, and postmortem.

## Qwen Cloud

Set these in `backend/.env`:

```env
QWEN_API_KEY=your_key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus
```

If no key is configured, IncidentPilot uses a deterministic local demo fallback so the product remains runnable.


## Investigation Agent

IncidentPilot includes an Investigation Agent that gathers evidence before root-cause analysis.

The agent calls read-only diagnostic tools:
- `get_service_metrics`
- `get_error_logs`
- `get_recent_deployments`
- `get_service_health`

Every tool call is stored in the database and shown in the incident timeline/dashboard. This makes the system auditable and prevents unsupported root-cause guesses.


## Runbook and Memory Retrieval

Before generating root cause, IncidentPilot retrieves relevant operational knowledge:
- **Runbooks**: Standard operating procedures (e.g., rollback procedures)
- **Prior Incident Memory**: Known fixes from previous incidents

This retrieval is logged in the timeline as `context_retrieved` event, making the reasoning process transparent and grounded in operational knowledge.

## Root Cause Agent

IncidentPilot includes a Root Cause Agent that analyzes evidence after investigation and context retrieval.

The agent receives metrics, logs, deployment history, service health, retrieved runbooks, and prior incident memory.

It produces:
- Root cause with confidence score
- Ranked hypotheses with evidence and counter-evidence
- Recommended safe remediation

This makes IncidentPilot's RCA explainable and auditable instead of a black-box LLM answer.