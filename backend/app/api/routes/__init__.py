from fastapi import APIRouter
from app.api.routes import auth, services, alerts, incidents, agents, actions, runbooks, postmortems, demo

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
api_router.include_router(agents.router, prefix="/agent-runs", tags=["agents"])
api_router.include_router(actions.router, prefix="/actions", tags=["actions"])
api_router.include_router(runbooks.router, prefix="/runbooks", tags=["runbooks"])
api_router.include_router(postmortems.router, prefix="/postmortems", tags=["postmortems"])
api_router.include_router(demo.router, prefix="/demo", tags=["demo"])
