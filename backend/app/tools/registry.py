import time
from typing import Callable
from sqlalchemy.orm import Session
from app.models.models import ToolCall

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, Callable] = {}

    def register(self, name: str, fn: Callable):
        self.tools[name] = fn

    def call(self, db: Session, incident_id: str, agent_run_id: str | None, name: str, payload: dict):
        start = time.time()
        status = "success"
        error = ""
        try:
            if name not in self.tools:
                raise ValueError(f"Tool not registered: {name}")
            output = self.tools[name](payload)
        except Exception as exc:
            output = {}
            status = "error"
            error = str(exc)
        latency_ms = int((time.time() - start) * 1000)
        call = ToolCall(
            agent_run_id=agent_run_id,
            incident_id=incident_id,
            tool_name=name,
            input=payload,
            output=output,
            status=status,
            latency_ms=latency_ms,
            error_message=error,
        )
        db.add(call)
        db.commit()
        return output

registry = ToolRegistry()
