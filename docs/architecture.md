# IncidentPilot Architecture

```mermaid
flowchart TD
    A[Monitoring Alert] --> B[FastAPI Alert Webhook]
    B --> C[Incident Service]
    C --> D[IncidentPilot Supervisor Agent]
    D --> E[Qwen Cloud API]
    D --> F[Tool Registry]
    D --> G[Runbook & Memory Retrieval]
    D --> H[Policy Engine]
    H --> I[Human Approval]
    I --> J[Deterministic Action Executor]
    J --> K[Verification Tool]
    K --> L[Postmortem Generator]
    C --> M[(PostgreSQL)]
    F --> M
    L --> M
    N[React Dashboard] --> B
```

## Safety Model

- LLM proposes actions.
- Deterministic executor performs actions.
- Production remediation requires approval.
- Tool calls and actions are audited.
- Dangerous/destructive actions are forbidden.
