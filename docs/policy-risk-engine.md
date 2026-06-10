# Policy and Risk Engine

IncidentPilot does not blindly execute AI recommendations. Every action passes through a deterministic Policy Engine.

## Core Principle

**LLM proposes. Policy validates. Human approves. Deterministic executor acts.**

## Policy Rules

### Risk Classification
- `low`: Read-only operations, monitoring
- `medium`: Production rollbacks, restarts
- `high`: Scaling, configuration changes
- `critical`: Database operations, infrastructure changes

### Approval Requirements
```python
if environment == "production" and risk_level in {"medium", "high", "critical"}:
    requires_approval = True