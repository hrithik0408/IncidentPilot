"""Runbook and prior incident memory retrieval service."""

from typing import List, Dict, Any


def build_retrieval_terms(alert_payload: dict, service_name: str) -> List[str]:
    """Build search terms for retrieval."""
    terms = [
        service_name,
        alert_payload.get("severity", ""),
        alert_payload.get("title", ""),
    ]
    
    metrics = alert_payload.get("metrics", {})
    if metrics.get("error_rate", 0) > 0.1:
        terms.extend(["5xx", "error", "rollback"])
    
    if "deployment" in alert_payload.get("description", "").lower():
        terms.extend(["deployment", "v42", "v41"])
    
    if "timeout" in alert_payload.get("description", "").lower():
        terms.extend(["timeout", "database", "connection"])
    
    return [t for t in terms if t]


def retrieve_incident_context(db, service_name: str, alert_payload: dict) -> dict:
    """
    Retrieve relevant runbooks and prior incident memory.
    
    Returns:
        dict with query_terms, runbooks, memories
    """
    from app.models.models import Runbook, MemoryItem
    
    query_terms = build_retrieval_terms(alert_payload, service_name)
    
    # Retrieve runbooks (simple relevance check)
    runbooks = db.query(Runbook).all()
    relevant_runbooks = []
    
    for runbook in runbooks:
        score = 0
        runbook_text = f"{runbook.title} {runbook.description}".lower()
        
        for term in query_terms:
            if term.lower() in runbook_text:
                score += 1
        
        if score > 0:
            relevant_runbooks.append({
                "id": str(runbook.id),
                "title": runbook.title,
                "description": runbook.description,
                "relevance_score": score / len(query_terms) if query_terms else 0
            })
    
    # Sort by relevance
    relevant_runbooks.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Retrieve memory items
    memories = db.query(MemoryItem).all()
    relevant_memories = []
    
    for memory in memories:
        score = 0
        memory_text = f"{memory.title} {memory.content}".lower()
        
        for term in query_terms:
            if term.lower() in memory_text:
                score += 1
        
        if score > 0:
            relevant_memories.append({
                "id": str(memory.id),
                "title": memory.title,
                "memory_type": memory.memory_type,
                "content": memory.content,
                "relevance_score": score / len(query_terms) if query_terms else 0
            })
    
    relevant_memories.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {
        "query_terms": query_terms,
        "runbooks": relevant_runbooks[:3],  # Top 3
        "memories": relevant_memories[:3],  # Top 3
    }