# Triage Agent

The Triage Agent classifies incoming alerts before full investigation begins.

## Purpose
Not all alerts are equal. The Triage Agent intelligently categorizes alerts to prioritize response and route to appropriate investigation.

## Output Fields
- **incident_title**: Generated from alert analysis
- **severity**: critical, high, medium, low
- **affected_service**: Detected service name
- **alert_category**: availability, performance, operational
- **business_impact**: Customer-facing impact assessment
- **recommended_next_step**: start_investigation or monitor
- **triage_confidence**: 0.0 to 1.0

## Why This Matters
- Prevents alert fatigue
- Ensures critical incidents get immediate attention
- Provides structured classification for audit trail
- Records triage decision in timeline as `triage_completed` event