# Alibaba Cloud Deployment

## ECS Deployment

1. Create Alibaba Cloud ECS instance.
2. Install Docker and Docker Compose.
3. Clone this repository.
4. Configure `.env` and `backend/.env`.
5. Run:

```bash
bash deploy/alibaba/ecs-deploy.sh
```

## Required Hackathon Proof

Record a short video showing:

- ECS instance console.
- Docker containers running.
- Backend `/health` endpoint responding.
- Code file showing Qwen Cloud API usage: `backend/app/services/qwen_client.py`.
- Architecture diagram: `docs/architecture.md`.
