# Policy and Risk Engine
IncidentPilot does not blindly execute AI recommendations. Every action passes through a deterministic Policy Engine.

## Rules
- Production rollbacks are classified as `medium` risk.
- Any `medium`, `high`, or `critical` risk action in production requires human approval.
- The LLM cannot bypass the policy engine.

## Why This Matters
This ensures "controlled autonomy" and prevents AI hallucinations from breaking production systems.