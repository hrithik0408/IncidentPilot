#!/usr/bin/env bash
set -e
curl -s -X POST http://localhost:8000/api/v1/demo/trigger-alert | python -m json.tool
