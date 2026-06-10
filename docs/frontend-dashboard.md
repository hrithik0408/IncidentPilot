# Frontend Dashboard

## Purpose
The frontend provides a visual interface for SREs to monitor incidents, review AI recommendations, and approve actions.

## Key Features

### 1. Incident List
- Shows all incidents with status pills
- Displays title, severity, and timestamp
- Click to view incident details

### 2. Incident Detail View
- **Root Cause**: AI-generated hypothesis with confidence score
- **Recommendation**: Proposed action with risk level
- **Timeline**: Full audit trail from alert to resolution
- **Tool Calls**: Evidence collected during investigation
- **Approval Card**: Approve/Reject buttons for production actions

### 3. Trigger Demo Alert
Button to simulate production incident for demo/testing

## UI Components
- Sidebar navigation
- Dashboard metrics (open/resolved incidents)
- Status pills (open, investigating, awaiting_approval, resolved)
- Timeline visualization
- Tool call expandable cards
- Postmortem viewer

## Why This Matters
- Makes AI reasoning transparent and explainable
- Human-in-the-loop approval interface
- Visual audit trail for compliance
- Production-ready dashboard design