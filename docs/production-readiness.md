# Production Readiness

IncidentPilot is designed for production incident response with safety-first architecture.

## Safety Model

1. **LLM proposes** - Qwen Cloud analyzes evidence and suggests actions
2. **Policy validates** - Policy Engine checks risk level
3. **Human approves** - Production actions require human approval
4. **Deterministic executor acts** - Approved actions execute through typed tools

## Production-Ready Features

- **Full audit trail**: Every step logged in timeline
- **Human-in-the-loop**: No blind execution of risky actions
- **Evidence-grounded reasoning**: Root cause based on metrics, logs, deployments
- **Deterministic execution**: Rollback, restart, scale through typed tools
- **Verification**: System verifies recovery after execution
- **Postmortem generation**: Automatic documentation after resolution

## Safety Boundaries

- LLM cannot execute arbitrary shell commands
- Production actions require policy validation + human approval
- All tool calls are logged with input/output/status
- Rollback is reversible and low-risk

## Current MVP Limitations

- Simulated tools (not connected to real infrastructure)
- Single team/tenant
- No real-time alert ingestion (demo trigger only)

These are intentional for hackathon demo and can be extended for production use.