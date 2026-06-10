# Evaluation Metrics

## Manual Incident Response vs IncidentPilot

| Metric | Manual Baseline | IncidentPilot MVP |
|---|---:|---:|
| Time to triage | 10 min | 60-90 sec |
| Manual steps | ~12 | ~4 |
| Postmortem draft | 30 min | <30 sec |
| Audit coverage | Incomplete notes | Full event timeline |
| Root cause confidence | Subjective | 0.86 with evidence |
| Human approval required | Ad-hoc | Policy-enforced |

## Key Improvements

1. **Faster triage**: Agent classifies alert in seconds vs minutes.
2. **Automated investigation**: Tools collect metrics, logs, deployments automatically.
3. **Evidence-grounded RCA**: Root cause based on data, not guesswork.
4. **Audit trail**: Every step logged for compliance.
5. **Safety**: Human approval for production actions.
6. **Postmortem automation**: Saves hours of manual documentation.

## Demo Talking Points

- "Manual incident response requires checking metrics, logs, deployments, runbooks, approvals, remediation, verification, and postmortem writing manually."
- "IncidentPilot converts that into one auditable agent workflow."
- "The demo reduces triage from around 10 minutes to around 60-90 seconds and postmortem drafting from around 30 minutes to under 30 seconds."