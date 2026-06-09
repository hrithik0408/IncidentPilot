"""Triage Agent for intelligent alert classification."""

from typing import Any


async def triage_alert(alert_payload: dict) -> dict:
    """
    Classify incoming alert and produce structured triage output.
    
    Returns:
        dict with: incident_title, severity, affected_service, 
                   initial_summary, alert_category, recommended_next_step,
                   business_impact, triage_confidence, reasoning
    """
    service = alert_payload.get("service", "unknown-service")
    title = alert_payload.get("title", "Unknown Alert")
    severity = alert_payload.get("severity", "medium")
    description = alert_payload.get("description", "")
    metrics = alert_payload.get("metrics", {})
    source = alert_payload.get("source", "unknown")
    
    # Determine alert category
    error_rate = metrics.get("error_rate", 0)
    latency = metrics.get("latency_p95_ms", 0)
    
    if error_rate > 0.1:
        alert_category = "availability"
    elif latency > 1000:
        alert_category = "performance"
    else:
        alert_category = "operational"
    
    # Determine business impact
    if severity in ["critical", "high"]:
        business_impact = "Potential customer-facing reliability degradation."
    elif severity == "medium":
        business_impact = "Degraded service quality affecting some users."
    else:
        business_impact = "Minor operational issue with limited user impact."
    
    # Determine recommended next step
    if severity in ["critical", "high"]:
        recommended_next_step = "start_investigation"
    else:
        recommended_next_step = "monitor"
    
    # Build initial summary
    initial_summary = f"Alert received from {source} for {service}: {title}. {description}"
    
    # Reasoning
    reasoning = f"Triage classified alert as {alert_category} with {severity} severity based on metrics (error_rate={error_rate}, latency={latency}ms)."
    
    # Confidence score
    triage_confidence = 0.84
    
    return {
        "incident_title": title,
        "severity": severity,
        "affected_service": service,
        "initial_summary": initial_summary,
        "alert_category": alert_category,
        "recommended_next_step": recommended_next_step,
        "business_impact": business_impact,
        "triage_confidence": triage_confidence,
        "reasoning": reasoning,
    }