from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import AgentRun, Incident, ActionProposal, Approval, Postmortem, Runbook, MemoryItem, ActionExecution
from app.services.events import add_event
from app.services.qwen_client import qwen_client
from app.services.policy import evaluate_action
from app.tools.registry import registry
import app.tools.simulated  # noqa

SYSTEM_PROMPT = """You are IncidentPilot, a production incident response agent. Use only provided evidence. Return valid JSON. Never claim actions executed unless a tool confirms it. Production changes require approval."""

class IncidentPilotSupervisor:
    def __init__(self, db: Session):
        self.db = db

    async def run_full_investigation(self, incident_id: str) -> dict:
        incident = self.db.get(Incident, incident_id)
        if not incident:
            raise ValueError("Incident not found")
        incident.status = "investigating"
        self.db.commit()
        add_event(self.db, incident_id, "investigation_started", "IncidentPilot started investigation", "Gathering logs, metrics, deployments, runbooks, and prior incidents.")

        run = AgentRun(incident_id=incident_id, agent_type="full_investigation", input={"incident": incident.title}, model_name="qwen-plus")
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        service_name = "payments-api"
        metrics = registry.call(self.db, incident_id, run.id, "get_service_metrics", {"service": service_name, "window": "15m"})
        logs = registry.call(self.db, incident_id, run.id, "get_error_logs", {"service": service_name, "limit": 50})
        deployments = registry.call(self.db, incident_id, run.id, "get_recent_deployments", {"service": service_name, "lookback_minutes": 60})
        health = registry.call(self.db, incident_id, run.id, "get_service_health", {"service": service_name})
        add_event(self.db, incident_id, "tool_called", "Diagnostic tools executed", "Queried metrics, logs, deployments, and health status.", data={"metrics": metrics, "logs": logs, "deployments": deployments, "health": health})

        runbooks = self.db.execute(select(Runbook).where(Runbook.team_id == incident.team_id)).scalars().all()
        memories = self.db.execute(select(MemoryItem).where(MemoryItem.team_id == incident.team_id)).scalars().all()
        context = {
            "incident": {"title": incident.title, "severity": incident.severity},
            "metrics": metrics,
            "logs": logs,
            "deployments": deployments,
            "health": health,
            "runbooks": [{"title": r.title, "content": r.content} for r in runbooks],
            "prior_incidents": [{"title": m.title, "content": m.content} for m in memories],
        }
        fallback = {
            "root_cause": "Bad deployment v42 likely introduced database timeout errors.",
            "confidence_score": 0.86,
            "evidence": [
                "5xx error rate is 18% and service health is degraded.",
                "Error logs show DatabaseConnectionTimeout in version v42.",
                "Deployment v42 completed 2 minutes before the alert.",
                "Runbook recommends rollback when 5xx spike follows deployment.",
            ],
            "recommended_action": {
                "title": "Rollback payments-api from v42 to v41",
                "description": "Deployment v42 correlates with the incident and rollback is reversible.",
                "action_type": "rollback_deployment",
                "parameters": {"service": "payments-api", "target_version": "v41"},
                "risk_level": "medium",
                "confidence_score": 0.86,
            },
        }
        analysis = await qwen_client.json_chat(SYSTEM_PROMPT, f"Analyze incident and produce root cause and remediation JSON:\n{context}", fallback)
        incident.root_cause = analysis.get("root_cause", fallback["root_cause"])
        incident.confidence_score = float(analysis.get("confidence_score", 0.86))
        incident.summary = "IncidentPilot identified a likely bad deployment causing database timeout errors."
        self.db.commit()
        add_event(self.db, incident_id, "hypothesis_generated", "Root cause hypothesis generated", incident.root_cause, data=analysis)

        action = analysis.get("recommended_action", fallback["recommended_action"])
        policy = evaluate_action(action.get("action_type"), "production", action.get("risk_level", "medium"))
        proposal = ActionProposal(
            incident_id=incident_id,
            agent_run_id=run.id,
            title=action.get("title"),
            description=action.get("description", ""),
            action_type=action.get("action_type"),
            parameters=action.get("parameters", {}),
            risk_level=action.get("risk_level", "medium"),
            confidence_score=float(action.get("confidence_score", 0.86)),
            requires_approval=policy["requires_approval"],
            status="pending_approval" if policy["requires_approval"] else "approved",
        )
        self.db.add(proposal)
        self.db.commit()
        self.db.refresh(proposal)
        add_event(self.db, incident_id, "action_proposed", proposal.title, proposal.description, data={"policy": policy, "proposal_id": proposal.id})

        if policy["requires_approval"]:
            approval = Approval(action_proposal_id=proposal.id, incident_id=incident_id, status="pending")
            incident.status = "awaiting_approval"
            self.db.add(approval)
            self.db.commit()
            add_event(self.db, incident_id, "approval_requested", "Human approval requested", policy["reason"], data={"action_id": proposal.id})
        else:
            await self.execute_action(proposal.id)

        run.status = "completed"
        run.output = analysis
        run.completed_at = datetime.utcnow()
        self.db.commit()
        return {"agent_run_id": run.id, "analysis": analysis, "action_id": proposal.id}

    async def execute_action(self, action_id: str) -> dict:
        proposal = self.db.get(ActionProposal, action_id)
        if not proposal:
            raise ValueError("Action not found")
        incident = self.db.get(Incident, proposal.incident_id)
        incident.status = "remediating"
        proposal.status = "executing"
        self.db.commit()
        add_event(self.db, incident.id, "action_executed", f"Executing: {proposal.title}", "Deterministic executor started.")
        output = registry.call(self.db, incident.id, proposal.agent_run_id, proposal.action_type, proposal.parameters)
        execution = ActionExecution(action_proposal_id=proposal.id, incident_id=incident.id, status="completed", input=proposal.parameters, output=output, completed_at=datetime.utcnow())
        self.db.add(execution)
        proposal.status = "executed"
        self.db.commit()
        verify = registry.call(self.db, incident.id, proposal.agent_run_id, "verify_error_rate_normal", {"service": proposal.parameters.get("service", "payments-api")})
        if verify.get("healthy"):
            incident.status = "resolved"
            incident.resolved_at = datetime.utcnow()
            add_event(self.db, incident.id, "verification_passed", "Recovery verified", f"Error rate is now {verify.get('error_rate')}.", data=verify)
            await self.generate_postmortem(incident.id)
        else:
            incident.status = "investigating"
            add_event(self.db, incident.id, "verification_failed", "Recovery verification failed", "Metrics did not return to normal.", data=verify)
        self.db.commit()
        return {"execution": output, "verification": verify}

    async def generate_postmortem(self, incident_id: str) -> dict:
        incident = self.db.get(Incident, incident_id)
        events = self.db.query(__import__('app.models.models', fromlist=['IncidentEvent']).IncidentEvent).filter_by(incident_id=incident_id).order_by(__import__('app.models.models', fromlist=['IncidentEvent']).IncidentEvent.created_at).all()
        timeline = [{"time": e.created_at.isoformat(), "event": e.title} for e in events]
        fallback = {
            "title": f"Postmortem: {incident.title}",
            "summary": incident.summary,
            "impact": "Payments API returned elevated 5xx errors until rollback completed.",
            "root_cause": incident.root_cause,
            "resolution": "Rolled back payments-api from v42 to v41 and verified error rate normalization.",
            "prevention_items": ["Add canary analysis before full rollout", "Add regression test for database timeout handling", "Update runbook with this incident signature"],
        }
        pm = await qwen_client.json_chat(SYSTEM_PROMPT, f"Generate a postmortem JSON for incident {incident.title} with timeline {timeline}", fallback)
        postmortem = Postmortem(
            incident_id=incident_id,
            title=pm.get("title", fallback["title"]),
            summary=pm.get("summary", fallback["summary"]),
            impact=pm.get("impact", fallback["impact"]),
            root_cause=pm.get("root_cause", fallback["root_cause"]),
            timeline=timeline,
            resolution=pm.get("resolution", fallback["resolution"]),
            prevention_items=pm.get("prevention_items", fallback["prevention_items"]),
        )
        self.db.add(postmortem)
        add_event(self.db, incident_id, "postmortem_generated", "Postmortem generated", postmortem.summary)
        self.db.commit()
        return pm
