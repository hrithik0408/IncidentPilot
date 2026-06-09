# IncidentPilot Investigation Agent

The Investigation Agent gathers operational evidence before root-cause reasoning begins.

## Purpose

IncidentPilot does not guess root cause from the alert alone. It first investigates the affected service using typed tools.

## Investigation Tools

### 1. get_service_metrics
Collects current service metrics: error rate, latency, CPU, database connections.

### 2. get_error_logs
Retrieves recent service error logs and dominant error signatures.

### 3. get_recent_deployments
Checks recent deployments and stable previous versions.

### 4. get_service_health
Checks current service health and deployed version.

## Agent Flow

```text
alert received
→ triage completed
→ investigation started
→ metrics queried
→ logs queried
→ deployments queried
→ health checked
→ evidence passed to Qwen Cloud reasoning layer


## Auditability

Every tool call is stored in the `tool_calls` table with:
- tool name
- input
- output
- status
- latency
- timestamp

This makes the agent's investigation transparent and debuggable.

## Safety

The Investigation Agent only uses read-only tools. It cannot modify production systems.