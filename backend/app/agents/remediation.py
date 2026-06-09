"""Remediation Planner Agent - converts root cause to safe action proposal."""

from typing import Dict, Any, List


def default_remediation_plan() -> dict:
    """Default fallback remediation plan."""
    return {
        "recommended_action": {
            "title": "Rollback payments-api from v42 to v41",
            "description": "Deployment v42 correlates with the incident and rollback is reversible.",
            "action_type": "rollback_deployment",
            "parameters": {"service": "payments-api", "target_version": "v41"},
            "risk_level": "medium",
            "confidence_score": 0.86,
            "expected_impact": "Reduce 5xx errors within 2-5 minutes after rollback.",
            "reversibility": "high",
            "approval_reason": "Production rollback requires human approval."
        },
        "alternatives": [
            {
                "title": "Restart payments-api service",
                "description": "Quick restart to clear transient issues",
                "risk_level": "low",
                "confidence_score": 0.3
            },
            {
                "title": "Scale workers or instances",
                "description": "Add capacity to handle load",
                "risk_level": "low",
                "confidence_score": 0.2
            }
        ],
        "safety_notes": [
            "Do not execute without policy validation.",
            "Production rollback requires human approval.",
            "Verify error rate and health checks after execution.",
            "Monitor for 15 minutes post-rollback to ensure stability."
        ]
    }


async def plan_remediation(context: dict, analysis: dict) -> dict:
    """
    Plan safe remediation based on root cause analysis.
    
    Args:
        context: Investigation context (metrics, logs, deployments, etc.)
        analysis: Root cause analysis output
    
    Returns:
        dict with recommended_action, alternatives, safety_notes
    """
    # For now, use deterministic fallback for reliable demo
    # In production, this would call Qwen Cloud with structured prompt
    plan = default_remediation_plan()
    
    # TODO: Integrate Qwen Cloud call here
    # from app.services.qwen_client import qwen_client
    # result = await qwen_client.json_chat(
    #     "You are an SRE remediation planner...",
    #     f"Plan remediation for: {analysis}",
    #     plan
    # )
    # return result
    
    return plan