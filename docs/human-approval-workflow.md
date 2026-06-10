# Human-in-the-Loop Approval Workflow

For production changes, IncidentPilot enforces a strict human-in-the-loop checkpoint. The AI agent can investigate, reason, and propose, but it cannot execute high-risk production actions without explicit human approval.

## The Approval Flow

1. **Remediation Proposal:** The Remediation Planner Agent analyzes the root cause and proposes a safe rollback or fix.
2. **Policy Evaluation:** The Policy Engine evaluates the proposed action. Since it is a production rollback, it flags it as `requires_approval: true` with a `medium` risk level.
3. **UI Notification:** The Frontend displays an Approval Card to the SRE, showing the Risk Level, Expected Impact, and Reversibility.
4. **Human Decision:** The SRE reviews the evidence and clicks "Approve Remediation" (or "Reject").
5. **Deterministic Execution:** Only after approval, the Action Executor runs the deterministic rollback tool.

## Why Human Approval is Critical

- **Safety:** Prevents AI hallucinations or incorrect reasoning from blindly breaking production systems.
- **Accountability:** Creates a clear, auditable record of who approved what action and when.
- **Compliance:** Meets enterprise requirements for production change management and audit trails.
- **Controlled Autonomy:** The AI agent proposes, but the human retains ultimate control.

## API Endpoints

### Get Pending Actions
```http
GET /api/v1/incidents/{incident_id}/actions