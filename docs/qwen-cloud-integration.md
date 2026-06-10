# Qwen Cloud Integration

IncidentPilot uses Qwen Cloud as the reasoning layer for production incident response.

## Where Qwen Cloud Is Used

Qwen Cloud is used for:
- incident context analysis
- log interpretation
- root-cause hypothesis generation
- remediation planning
- postmortem generation

## Source Files

Qwen client:
- `backend/app/services/qwen_client.py`

Agent orchestration:
- `backend/app/agents/supervisor.py`

Environment configuration:
- `backend/app/core/config.py`
- `backend/.env.example`

## Environment Variables

```env
QWEN_API_KEY=your_qwen_cloud_api_key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus