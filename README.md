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


## Remediation Planner Agent

IncidentPilot includes a Remediation Planner Agent that converts root-cause analysis into a safe action proposal.

The planner returns:
- Recommended action with parameters
- Risk level and confidence score
- Expected impact and reversibility
- Alternative actions
- Safety notes

The planner does not execute actions. Production actions are passed through the policy engine and human approval workflow before execution.


## Triage Agent

When an alert arrives, the Triage Agent classifies it before investigation begins.

The Triage Agent produces:
- Incident title
- Severity (critical, high, medium, low)
- Affected service
- Alert category
- Business impact
- Recommended next step
- Triage confidence score

The triage result is recorded in the timeline as a `triage_completed` event.


## Policy and Risk Engine

IncidentPilot does not blindly execute AI recommendations. Every action passes through a deterministic Policy Engine.

### Safety Rules
- Production rollbacks are classified as `medium` risk
- Any `medium`, `high`, or `critical` risk action in production requires human approval
- The LLM cannot bypass the policy engine

This ensures "controlled autonomy" and prevents AI hallucinations from breaking production systems.


## Human Approval Workflow

For production changes, IncidentPilot enforces a human-in-the-loop checkpoint.

### Flow
1. Remediation Planner proposes a rollback
2. Policy Engine flags it as `requires_approval: true`
3. Frontend displays an Approval Card with Risk Level and Expected Impact
4. SRE clicks "Approve Remediation"
5. Action Executor runs the deterministic rollback tool


## Postmortem Agent

Once an incident is resolved and verified, the Postmortem Agent automatically drafts a report.

### Contents
- Impact summary
- Root cause (from RCA Agent)
- Resolution steps (from Execution logs)
- Prevention items (to avoid future incidents)

This saves SREs hours of manual documentation after every incident.


## Evaluation Metrics

| Metric | Manual Baseline | IncidentPilot |
|---|---:|---:|
| Time to triage | 10 min | 60-90 sec |
| Manual steps | ~12 | ~4 |
| Postmortem draft | 30 min | <30 sec |
| Audit coverage | Incomplete notes | Full event timeline |
| Root cause confidence | Subjective | 0.86 with evidence |


## Demo Line

> "IncidentPilot uses controlled autonomy: Qwen Cloud and agents propose a remediation, the policy engine checks risk, a human approves production changes, deterministic tools execute the rollback, verification confirms recovery, and the postmortem agent documents the incident."


## License

MIT