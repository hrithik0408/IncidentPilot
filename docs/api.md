# API Reference

Base URL: `/api/v1`

## Demo

- `POST /demo/trigger-alert`
- `POST /demo/reset`

## Incidents

- `GET /incidents`
- `GET /incidents/{incident_id}`
- `GET /incidents/{incident_id}/events`
- `GET /incidents/{incident_id}/actions`
- `GET /incidents/{incident_id}/tool-calls`
- `POST /incidents/{incident_id}/agent/run`

## Actions

- `GET /actions/{action_id}`
- `POST /actions/{action_id}/approve`
- `POST /actions/{action_id}/reject`

## Alerts

- `POST /alerts/webhook`
