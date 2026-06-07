from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.demo_data import ensure_demo_data
from app.schemas import AlertWebhook
from app.api.routes.alerts import alert_webhook
from app.tools.simulated import SYSTEM_STATE

router = APIRouter()

@router.post("/reset")
def reset_demo(db: Session = Depends(get_db)):
    ensure_demo_data(db)
    SYSTEM_STATE["payments-api"].update({"version": "v42", "error_rate": 0.18, "latency_p95_ms": 1250, "health": "degraded", "rollback_done": False})
    return {"status": "reset", "system_state": SYSTEM_STATE}

@router.post("/trigger-alert")
async def trigger_demo_alert(db: Session = Depends(get_db)):
    ensure_demo_data(db)
    SYSTEM_STATE["payments-api"].update({"version": "v42", "error_rate": 0.18, "latency_p95_ms": 1250, "health": "degraded", "rollback_done": False})
    payload = AlertWebhook(
        source="demo-prometheus",
        external_alert_id="demo-high-5xx",
        service="payments-api",
        title="High 5xx Error Rate on payments-api",
        description="5xx error rate above 10% for 5 minutes after deployment v42.",
        severity="critical",
        labels={"env": "production", "region": "ap-south-1"},
        metrics={"error_rate": 0.18, "latency_p95_ms": 1250},
    )
    return await alert_webhook(payload, db)
