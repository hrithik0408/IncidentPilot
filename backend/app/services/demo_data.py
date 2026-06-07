from sqlalchemy.orm import Session
from app.models.models import Team, User, Service, Runbook, MemoryItem
from app.core.security import hash_password

DEMO_TEAM_ID = "00000000-0000-0000-0000-000000000001"
DEMO_USER_ID = "00000000-0000-0000-0000-000000000002"
DEMO_SERVICE_ID = "00000000-0000-0000-0000-000000000003"

def ensure_demo_data(db: Session):
    team = db.get(Team, DEMO_TEAM_ID)
    if not team:
        team = Team(id=DEMO_TEAM_ID, name="Acme Cloud Platform", slug="acme")
        db.add(team)
    user = db.get(User, DEMO_USER_ID)
    if not user:
        user = User(id=DEMO_USER_ID, team_id=DEMO_TEAM_ID, email="sre@acme.dev", name="Demo SRE", role="admin", password_hash=hash_password("password"))
        db.add(user)
    service = db.get(Service, DEMO_SERVICE_ID)
    if not service:
        service = Service(
            id=DEMO_SERVICE_ID,
            team_id=DEMO_TEAM_ID,
            name="payments-api",
            environment="production",
            description="Handles checkout payment authorization and capture.",
            repository_url="https://github.com/acme/payments-api",
            healthcheck_url="https://payments.acme.dev/health",
            metadata_json={"owner": "platform-team", "current_version": "v42"},
        )
        db.add(service)
    db.commit()

    if db.query(Runbook).count() == 0:
        db.add(Runbook(
            team_id=DEMO_TEAM_ID,
            service_id=DEMO_SERVICE_ID,
            title="Payments API rollback procedure",
            description="Use when 5xx errors spike after deployment.",
            content="If 5xx errors spike within 10 minutes of a deployment and logs show DatabaseConnectionTimeout, rollback to previous stable version. Verify error rate drops below 1% and healthcheck passes. Production rollback requires human approval.",
            tags=["payments-api", "rollback", "5xx", "database-timeout"],
        ))
        db.add(Runbook(
            team_id=DEMO_TEAM_ID,
            service_id=DEMO_SERVICE_ID,
            title="Queue backlog remediation",
            description="Use when queue lag grows rapidly.",
            content="Check worker health, queue depth, and recent worker deployments. Restart workers if they are unhealthy. Scale workers by 2x if CPU is below 70% and backlog is growing.",
            tags=["queue", "workers", "scale"],
        ))
    if db.query(MemoryItem).count() == 0:
        db.add(MemoryItem(
            team_id=DEMO_TEAM_ID,
            service_id=DEMO_SERVICE_ID,
            memory_type="known_fix",
            title="Previous v39 timeout incident",
            content="A previous payments-api deployment introduced DatabaseConnectionTimeout and was resolved by rollback within 4 minutes.",
            importance_score=0.9,
            confidence_score=0.88,
            metadata_json={"incident": "INC-19"},
        ))
    db.commit()
