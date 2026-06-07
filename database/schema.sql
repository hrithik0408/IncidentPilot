CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS teams (
    id VARCHAR PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    team_id VARCHAR REFERENCES teams(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'responder',
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS services (
    id VARCHAR PRIMARY KEY,
    team_id VARCHAR REFERENCES teams(id),
    name VARCHAR(255) NOT NULL,
    environment VARCHAR(50) DEFAULT 'production',
    description TEXT DEFAULT '',
    repository_url TEXT DEFAULT '',
    healthcheck_url TEXT DEFAULT '',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incidents (
    id VARCHAR PRIMARY KEY,
    team_id VARCHAR REFERENCES teams(id),
    service_id VARCHAR REFERENCES services(id),
    title TEXT NOT NULL,
    summary TEXT DEFAULT '',
    severity VARCHAR(50) DEFAULT 'medium',
    status VARCHAR(50) DEFAULT 'open',
    root_cause TEXT DEFAULT '',
    confidence_score FLOAT DEFAULT 0,
    detected_at TIMESTAMP DEFAULT NOW(),
    acknowledged_at TIMESTAMP NULL,
    resolved_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR PRIMARY KEY,
    team_id VARCHAR REFERENCES teams(id),
    service_id VARCHAR REFERENCES services(id),
    incident_id VARCHAR REFERENCES incidents(id),
    source VARCHAR(100) NOT NULL,
    external_alert_id VARCHAR(255) DEFAULT '',
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    severity VARCHAR(50) DEFAULT 'medium',
    status VARCHAR(50) DEFAULT 'received',
    payload JSONB DEFAULT '{}',
    received_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incident_events (
    id VARCHAR PRIMARY KEY,
    incident_id VARCHAR REFERENCES incidents(id),
    event_type VARCHAR(100) NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    actor_type VARCHAR(50) DEFAULT 'agent',
    data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id VARCHAR PRIMARY KEY,
    incident_id VARCHAR REFERENCES incidents(id),
    agent_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'running',
    input JSONB DEFAULT '{}',
    output JSONB DEFAULT '{}',
    model_name VARCHAR(100) DEFAULT 'qwen-plus',
    prompt_tokens INT DEFAULT 0,
    completion_tokens INT DEFAULT 0,
    total_cost FLOAT DEFAULT 0,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP NULL,
    error_message TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS tool_calls (
    id VARCHAR PRIMARY KEY,
    agent_run_id VARCHAR REFERENCES agent_runs(id),
    incident_id VARCHAR REFERENCES incidents(id),
    tool_name VARCHAR(100) NOT NULL,
    input JSONB DEFAULT '{}',
    output JSONB DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'success',
    latency_ms INT DEFAULT 0,
    error_message TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS runbooks (
    id VARCHAR PRIMARY KEY,
    team_id VARCHAR REFERENCES teams(id),
    service_id VARCHAR REFERENCES services(id),
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    content TEXT NOT NULL,
    tags JSONB DEFAULT '[]',
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS memory_items (
    id VARCHAR PRIMARY KEY,
    team_id VARCHAR REFERENCES teams(id),
    service_id VARCHAR REFERENCES services(id),
    incident_id VARCHAR REFERENCES incidents(id),
    memory_type VARCHAR(100) NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    importance_score FLOAT DEFAULT 0.5,
    confidence_score FLOAT DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS action_proposals (
    id VARCHAR PRIMARY KEY,
    incident_id VARCHAR REFERENCES incidents(id),
    agent_run_id VARCHAR REFERENCES agent_runs(id),
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    action_type VARCHAR(100) NOT NULL,
    parameters JSONB DEFAULT '{}',
    risk_level VARCHAR(50) DEFAULT 'medium',
    confidence_score FLOAT DEFAULT 0,
    requires_approval BOOLEAN DEFAULT true,
    status VARCHAR(50) DEFAULT 'proposed',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS approvals (
    id VARCHAR PRIMARY KEY,
    action_proposal_id VARCHAR REFERENCES action_proposals(id),
    incident_id VARCHAR REFERENCES incidents(id),
    requested_to VARCHAR REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'pending',
    decision_note TEXT DEFAULT '',
    requested_at TIMESTAMP DEFAULT NOW(),
    decided_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS action_executions (
    id VARCHAR PRIMARY KEY,
    action_proposal_id VARCHAR REFERENCES action_proposals(id),
    incident_id VARCHAR REFERENCES incidents(id),
    executor VARCHAR(100) DEFAULT 'deterministic_executor',
    status VARCHAR(50) DEFAULT 'running',
    input JSONB DEFAULT '{}',
    output JSONB DEFAULT '{}',
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP NULL,
    error_message TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS postmortems (
    id VARCHAR PRIMARY KEY,
    incident_id VARCHAR REFERENCES incidents(id),
    title TEXT NOT NULL,
    summary TEXT DEFAULT '',
    impact TEXT DEFAULT '',
    root_cause TEXT DEFAULT '',
    timeline JSONB DEFAULT '[]',
    resolution TEXT DEFAULT '',
    prevention_items JSONB DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);
