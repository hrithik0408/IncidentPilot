from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import settings

app = FastAPI(
    title="IncidentPilot API",
    description="Production Incident Autopilot Agent on Qwen Cloud",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "env": settings.app_env}

app.include_router(api_router, prefix=settings.api_v1_prefix)

@app.get("/deployment-proof")
def deployment_proof():
    from app.services.alibaba_cloud_proof import deployment_proof_payload
    return deployment_proof_payload()
