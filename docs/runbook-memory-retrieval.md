# Runbook and Prior Incident Memory Retrieval

## Why This Matters

Real SREs don't just look at alerts. They check:
- Runbooks (standard operating procedures)
- Prior incidents (what worked before)
- Known fixes (tribal knowledge)

IncidentPilot does the same before generating root cause.

## Retrieval Sources

### 1. Runbooks
Standard operating procedures stored in the database.
Example: "Payments API rollback procedure"

### 2. Memory Items
Prior incident learnings and known fixes.
Example: "Previous v39 timeout incident - rollback fixed it"

## Retrieval Strategy

1. Extract query terms from alert (service name, error type, deployment version)
2. Search runbooks by title and content relevance
3. Search memory items by type and relevance
4. Return top matches with relevance scores

## Audit Trail

Every retrieval is logged as `context_retrieved` event with:
- query_terms used
- runbooks retrieved
- memories retrieved
- relevance scores

## Why This Helps Judges

This proves IncidentPilot is not guessing - it's using operational knowledge.

## Source Files

- Retrieval service: `backend/app/services/retrieval.py`
- Supervisor integration: `backend/app/agents/supervisor.py`
- Demo data: `backend/app/services/demo_data.py`