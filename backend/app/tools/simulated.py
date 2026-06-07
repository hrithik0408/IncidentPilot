from app.tools.registry import registry

SYSTEM_STATE = {
    "payments-api": {
        "version": "v42",
        "previous_version": "v41",
        "error_rate": 0.18,
        "latency_p95_ms": 1250,
        "health": "degraded",
        "rollback_done": False,
    }
}

def get_service_metrics(payload):
    service = payload.get("service", "payments-api")
    s = SYSTEM_STATE[service]
    return {
        "service": service,
        "error_rate": s["error_rate"],
        "latency_p95_ms": s["latency_p95_ms"],
        "cpu": 0.62,
        "db_connections": 187,
        "window": payload.get("window", "15m"),
    }

def get_error_logs(payload):
    service = payload.get("service", "payments-api")
    return {
        "service": service,
        "logs": [
            "ERROR DatabaseConnectionTimeout at PaymentRepository.authorize line=88 version=v42",
            "ERROR request failed status=500 route=/v1/payments/authorize trace=abc123",
            "WARN retry exhausted for db connection pool version=v42",
        ],
        "dominant_error": "DatabaseConnectionTimeout",
    }

def get_recent_deployments(payload):
    service = payload.get("service", "payments-api")
    return {
        "service": service,
        "deployments": [
            {"version": "v42", "time": "2 minutes before alert", "author": "deploy-bot", "status": "completed"},
            {"version": "v41", "time": "2 days before alert", "author": "deploy-bot", "status": "stable"},
        ],
    }

def get_service_health(payload):
    service = payload.get("service", "payments-api")
    s = SYSTEM_STATE[service]
    return {"service": service, "health": s["health"], "current_version": s["version"]}

def rollback_deployment(payload):
    service = payload.get("service", "payments-api")
    target = payload.get("target_version") or payload.get("to_version") or "v41"
    s = SYSTEM_STATE[service]
    s["version"] = target
    s["error_rate"] = 0.007
    s["latency_p95_ms"] = 180
    s["health"] = "healthy"
    s["rollback_done"] = True
    return {"service": service, "current_version": target, "message": "Rollback completed successfully."}

def restart_service(payload):
    service = payload.get("service", "payments-api")
    return {"service": service, "message": "Service restart simulated successfully."}

def scale_workers(payload):
    service = payload.get("service", "payments-api")
    replicas = payload.get("replicas", 4)
    return {"service": service, "replicas": replicas, "message": "Workers scaled successfully."}

def verify_error_rate_normal(payload):
    service = payload.get("service", "payments-api")
    s = SYSTEM_STATE[service]
    return {"service": service, "healthy": s["error_rate"] < 0.01, "error_rate": s["error_rate"]}

def register_simulated_tools():
    registry.register("get_service_metrics", get_service_metrics)
    registry.register("get_error_logs", get_error_logs)
    registry.register("get_recent_deployments", get_recent_deployments)
    registry.register("get_service_health", get_service_health)
    registry.register("rollback_deployment", rollback_deployment)
    registry.register("restart_service", restart_service)
    registry.register("scale_workers", scale_workers)
    registry.register("verify_error_rate_normal", verify_error_rate_normal)

register_simulated_tools()
