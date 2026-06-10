# Execution and Verification

## Deterministic Action Executor

After human approval, IncidentPilot executes actions through typed, deterministic tools.

## Execution Flow
1. Action approved by human
2. Policy validation passed
3. Deterministic executor calls appropriate tool
4. Tool executes (rollback, restart, scale)
5. Verification tool checks recovery
6. Incident marked resolved if verification passes

## Verification Tools

### verify_error_rate_normal
- Checks if error rate dropped below threshold
- Confirms service health is restored
- Returns healthy: true/false with current error_rate

## Safety Guarantees
- Only approved actions execute
- Execution is deterministic (no LLM involved)
- Every execution is logged with input/output
- Verification confirms success before marking resolved
- Failed verification reopens incident for investigation

## Audit Trail
Events logged:
- `action_approved`
- `action_executed`
- `verification_passed` or `verification_failed`