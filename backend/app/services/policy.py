def evaluate_action(action_type: str, environment: str, risk_level: str) -> dict:
    forbidden = {"delete_database", "delete_resource", "drop_table"}
    if action_type in forbidden:
        return {"allowed": False, "requires_approval": True, "reason": "Destructive action is forbidden."}
    if environment == "production" and risk_level in {"medium", "high", "critical"}:
        return {"allowed": True, "requires_approval": True, "reason": "Production change requires approval."}
    return {"allowed": True, "requires_approval": False, "reason": "Low-risk action can be executed automatically."}
