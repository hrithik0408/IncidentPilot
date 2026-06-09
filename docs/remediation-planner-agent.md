# Remediation Planner Agent

The Remediation Planner Agent converts root-cause analysis into a safe, executable action proposal.

## Purpose
After root cause is identified, the planner recommends safe remediation with:
- Recommended action
- Alternatives
- Safety notes
- Risk assessment
- Approval requirements

## Inputs
- Root cause analysis (from Root Cause Agent)
- Investigation context (metrics, logs, deployments)
- Retrieved runbooks
- Prior incident memory

## Outputs
- **Recommended action**: Primary remediation proposal
- **Action type**: Type of action (rollback, restart, scale, etc.)
- **Parameters**: Deterministic executor parameters
- **Risk level**: low, medium, high, critical
- **Confidence score**: 0.0 to 1.0
- **Expected impact**: What will happen after execution
- **Reversibility**: How easy to undo
- **Approval reason**: Why human approval is needed
- **Alternatives**: Other possible actions
- **Safety notes**: Important precautions

## Safety Design
- Planner proposes, does not execute
- All actions go through policy validation
- Production actions require human approval
- Executor is deterministic and auditable

## Why This Matters
This makes IncidentPilot production-ready:
- Safe: Human-in-the-loop for risky actions
- Transparent: Shows alternatives and safety notes
- Auditable: Every plan is logged
- Reliable: Deterministic execution after approval