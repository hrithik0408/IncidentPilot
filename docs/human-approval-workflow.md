# Human-in-the-Loop Approval
For production changes, IncidentPilot enforces a human-in-the-loop checkpoint.

## Flow
1. Remediation Planner proposes a rollback.
2. Policy Engine flags it as `requires_approval: true`.
3. Frontend displays an Approval Card with Risk Level and Expected Impact.
4. SRE clicks "Approve Remediation".
5. Action Executor runs the deterministic rollback tool.