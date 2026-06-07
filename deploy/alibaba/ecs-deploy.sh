#!/usr/bin/env bash
set -euo pipefail

# Alibaba Cloud ECS deployment helper.
# Run on an ECS instance with Docker and Docker Compose installed.

APP_DIR=${APP_DIR:-/opt/incidentpilot}
REPO_URL=${REPO_URL:-https://github.com/your-org/incidentpilot.git}

sudo mkdir -p "$APP_DIR"
sudo chown "$USER":"$USER" "$APP_DIR"

if [ ! -d "$APP_DIR/.git" ]; then
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"
git pull
cp .env.example .env || true
cp backend/.env.example backend/.env || true
cp frontend/.env.example frontend/.env || true

docker compose up -d --build

echo "IncidentPilot deployed. Backend: http://$(curl -s ifconfig.me):8000/health"
