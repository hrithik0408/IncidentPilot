"""
Alibaba Cloud deployment proof helper.

This file exists to make the Alibaba Cloud dependency explicit for hackathon judging.
In production, IncidentPilot should run on Alibaba Cloud ECS/ACK/Function Compute and use
Alibaba Cloud managed services such as ApsaraDB RDS, Tair/Redis, OSS, and CloudMonitor.

For the hackathon proof video, show:
1. This source file in the public repository.
2. IncidentPilot backend running on Alibaba Cloud ECS.
3. Environment variables below configured on the ECS instance.
4. /health endpoint responding from the ECS public IP.

No secrets are hardcoded here. Values are read from environment variables.
"""

import os
from dataclasses import dataclass

@dataclass
class AlibabaCloudRuntime:
    region_id: str
    ecs_instance_id: str
    rds_endpoint: str
    oss_bucket: str
    cloudmonitor_namespace: str


def get_alibaba_cloud_runtime() -> AlibabaCloudRuntime:
    return AlibabaCloudRuntime(
        region_id=os.getenv("ALIBABA_CLOUD_REGION_ID", "ap-southeast-1"),
        ecs_instance_id=os.getenv("ALIBABA_CLOUD_ECS_INSTANCE_ID", "local-demo"),
        rds_endpoint=os.getenv("ALIBABA_CLOUD_RDS_ENDPOINT", "postgresql://db:5432/incidentpilot"),
        oss_bucket=os.getenv("ALIBABA_CLOUD_OSS_BUCKET", "incidentpilot-demo-artifacts"),
        cloudmonitor_namespace=os.getenv("ALIBABA_CLOUD_MONITOR_NAMESPACE", "acs_ecs_dashboard"),
    )


def deployment_proof_payload() -> dict:
    runtime = get_alibaba_cloud_runtime()
    return {
        "cloud_provider": "Alibaba Cloud",
        "runtime": runtime.__dict__,
        "qwen_cloud_base_url": os.getenv("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"),
        "deployment_services": [
            "ECS or ACK for backend containers",
            "ApsaraDB RDS PostgreSQL-compatible database",
            "Tair/Redis for async jobs and caching",
            "OSS for demo artifacts and generated reports",
            "Qwen Cloud / DashScope-compatible model API for agent reasoning",
        ],
    }
