#!/usr/bin/env bash
set -e
cp -n .env.example .env || true
cp -n backend/.env.example backend/.env || true
cp -n frontend/.env.example frontend/.env || true
docker compose up --build
