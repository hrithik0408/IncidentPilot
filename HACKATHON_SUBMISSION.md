# IncidentPilot Hackathon Submission Notes

## Track

Track 4: Autopilot Agent

## What IncidentPilot Demonstrates

- End-to-end business workflow automation for production incident response.
- Qwen Cloud-powered investigation, RCA, remediation planning, and postmortem generation.
- Human-in-the-loop approval for production remediation.
- Deterministic tool execution instead of unsafe arbitrary LLM actions.
- Full audit timeline of tool calls, decisions, approval, execution, and verification.

## Required Submission Links

- Public repository: https://github.com/hrithik0408/IncidentPilot .
- Demo video: add YouTube/Vimeo URL.
- Alibaba Cloud deployment proof video: show ECS console, running containers, `/health`, `/deployment-proof`.
- Architecture diagram: `docs/architecture.md`.
- Qwen Cloud code: `backend/app/services/qwen_client.py`.
- Alibaba Cloud proof code: `backend/app/services/alibaba_cloud_proof.py`.

## Demo Metrics to Show

| Metric | Manual Baseline | IncidentPilot Demo |
|---|---:|---:|
| Time to triage | 10 minutes | ~60-90 seconds |
| Manual steps | 12 | 4 |
| Time to postmortem draft | 30 minutes | <30 seconds |
| Action audit coverage | Manual notes | Full timeline |

## Safety Claims

- Qwen proposes and explains; deterministic code executes.
- Production rollback requires human approval.
- Destructive actions are forbidden by policy.
- Every tool call is recorded.
