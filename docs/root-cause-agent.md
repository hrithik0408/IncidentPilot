# Root Cause Agent

The Root Cause Agent analyzes investigation evidence and operational context to generate evidence-grounded root cause hypotheses.

## Inputs

The agent receives:
- Service metrics (error rate, latency, CPU, connections)
- Error logs and dominant error signatures
- Recent deployment history
- Service health status
- Retrieved runbooks
- Prior incident memory

## Outputs

The agent produces:
- **Root cause**: Primary hypothesis
- **Confidence score**: 0.0 to 1.0
- **Ranked hypotheses**: Multiple hypotheses ranked by confidence
- **Evidence**: Supporting signals for each hypothesis
- **Counter-evidence**: Signals that contradict each hypothesis
- **Recommended action**: Safe remediation proposal

## Why This Matters

This makes IncidentPilot's RCA:
- **Explainable**: Shows evidence and counter-evidence
- **Auditable**: Every hypothesis is logged
- **Production-grade**: Considers multiple possibilities
- **Safe**: Includes counter-evidence to avoid overconfidence

## Example Output

```json
{
  "root_cause": "Deployment v42 introduced database timeout regression",
  "confidence_score": 0.86,
  "ranked_hypotheses": [
    {
      "rank": 1,
      "cause": "Deployment v42 regression",
      "confidence": 0.86,
      "evidence": ["5xx rate 18%", "DatabaseConnectionTimeout", "v42 deployed 2 min before alert"],
      "counter_evidence": ["DB CPU not critical", "No dependency outage"]
    }
  ]
}