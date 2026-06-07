import { useEffect, useState } from 'react';
import { Activity, AlertTriangle, CheckCircle2, Clock, Database, Play, ShieldCheck, TerminalSquare } from 'lucide-react';
import { IncidentPilotAPI } from './api/client';
import './styles/global.css';

type Incident = { id: string; title: string; status: string; severity: string; summary: string; root_cause: string; confidence_score: number; created_at: string; resolved_at?: string };
type Event = { id: string; event_type: string; title: string; description: string; actor_type: string; data: any; created_at: string };
type Action = { id: string; title: string; description: string; action_type: string; parameters: any; risk_level: string; confidence_score: number; status: string; requires_approval: boolean };
type ToolCall = { id: string; tool_name: string; input: any; output: any; status: string; latency_ms: number; created_at: string };

function statusClass(status: string) {
  if (status === 'resolved') return 'pill green';
  if (status === 'awaiting_approval') return 'pill amber';
  if (status === 'remediating') return 'pill blue';
  return 'pill red';
}

export default function App() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [selected, setSelected] = useState<string>('');
  const [detail, setDetail] = useState<any>(null);
  const [events, setEvents] = useState<Event[]>([]);
  const [actions, setActions] = useState<Action[]>([]);
  const [tools, setTools] = useState<ToolCall[]>([]);
  const [postmortem, setPostmortem] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function refreshList() {
    const data = await IncidentPilotAPI.incidents();
    setIncidents(data);
    if (!selected && data.length) setSelected(data[0].id);
  }

  async function refreshDetail(id = selected) {
    if (!id) return;
    const [d, ev, ac, tc, pm] = await Promise.all([
      IncidentPilotAPI.incident(id), IncidentPilotAPI.events(id), IncidentPilotAPI.actions(id), IncidentPilotAPI.toolCalls(id), IncidentPilotAPI.postmortem(id).catch(() => null)
    ]);
    setDetail(d);
    setEvents(ev);
    setActions(ac);
    setTools(tc);
    setPostmortem(pm);
  }

  async function triggerDemo() {
    setLoading(true);
    try {
      const res = await IncidentPilotAPI.triggerDemo();
      await refreshList();
      setSelected(res.incident_id);
      await refreshDetail(res.incident_id);
    } finally { setLoading(false); }
  }

  async function approve(actionId: string) {
    setLoading(true);
    try {
      await IncidentPilotAPI.approve(actionId);
      await refreshList();
      await refreshDetail();
    } finally { setLoading(false); }
  }

  useEffect(() => { refreshList(); }, []);
  useEffect(() => { if (selected) refreshDetail(selected); }, [selected]);

  const incident: Incident | undefined = detail?.incident;
  const recommendation: Action | undefined = detail?.current_recommendation || actions[0];

  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><ShieldCheck size={28}/><div><b>IncidentPilot</b><span>Qwen Cloud Incident Autopilot</span></div></div>
      <button className="primary" disabled={loading} onClick={triggerDemo}><Play size={16}/> {loading ? 'Running Agent...' : 'Trigger Demo Alert'}</button>
      <button className="secondary" onClick={async () => { await IncidentPilotAPI.resetDemo(); await refreshList(); }}>Reset Demo State</button>
      <div className="metric"><span>Open Incidents</span><b>{incidents.filter(i => i.status !== 'resolved').length}</b></div>
      <div className="metric"><span>Resolved</span><b>{incidents.filter(i => i.status === 'resolved').length}</b></div>
      <div className="metric"><span>Agent Mode</span><b>Assist</b></div>
    </aside>

    <main>
      <header className="topbar">
        <div>
          <h1>Production Incident Autopilot</h1>
          <p>Investigate alerts, retrieve runbooks, propose remediation, request approval, verify recovery.</p>
        </div>
      </header>

      <section className="grid">
        <div className="card incident-list">
          <h2><AlertTriangle size={18}/> Incidents</h2>
          {incidents.length === 0 && <p className="muted">No incidents yet. Trigger the demo alert.</p>}
          {incidents.map(i => <button key={i.id} className={`incident-row ${selected === i.id ? 'active' : ''}`} onClick={() => setSelected(i.id)}>
            <span className={statusClass(i.status)}>{i.status}</span>
            <b>{i.title}</b>
            <small>{i.severity} · confidence {Math.round((i.confidence_score || 0) * 100)}%</small>
          </button>)}
        </div>

        <div className="card hero-card">
          {!incident ? <div className="empty"><Activity size={44}/><h2>Ready for Incident Autopilot</h2><p>Click Trigger Demo Alert to start an end-to-end IncidentPilot workflow.</p></div> : <>
            <div className="hero-header">
              <div><span className={statusClass(incident.status)}>{incident.status}</span><h2>{incident.title}</h2><p>{incident.summary}</p></div>
              <div className="confidence"><b>{Math.round((incident.confidence_score || 0) * 100)}%</b><span>RCA confidence</span></div>
            </div>
            <div className="rca"><b>Root cause hypothesis</b><p>{incident.root_cause || 'Investigation in progress...'}</p></div>
            {recommendation && <div className="approval-card">
              <div><h3>{recommendation.title}</h3><p>{recommendation.description}</p>
                <div className="kv"><span>Action</span><b>{recommendation.action_type}</b></div>
                <div className="kv"><span>Risk</span><b>{recommendation.risk_level}</b></div>
                <div className="kv"><span>Approval</span><b>{recommendation.requires_approval ? 'Required' : 'Automatic'}</b></div>
              </div>
              {recommendation.status === 'pending_approval' && <button className="approve" disabled={loading} onClick={() => approve(recommendation.id)}><CheckCircle2 size={18}/> Approve Remediation</button>}
              {recommendation.status !== 'pending_approval' && <span className="pill green">{recommendation.status}</span>}
            </div>}
          </>}
        </div>
      </section>

      {incident && <section className="details-grid">
        <div className="card">
          <h2><Clock size={18}/> Incident Timeline</h2>
          <div className="timeline">{events.map(e => <div className="timeline-item" key={e.id}><span></span><div><b>{e.title}</b><p>{e.description}</p><small>{e.actor_type} · {new Date(e.created_at).toLocaleTimeString()}</small></div></div>)}</div>
        </div>
        <div className="card">
          <h2><TerminalSquare size={18}/> Tool Calls</h2>
          {tools.map(t => <details className="tool" key={t.id}><summary>{t.tool_name} <span>{t.latency_ms}ms</span></summary><pre>{JSON.stringify(t.output, null, 2)}</pre></details>)}
        </div>
        <div className="card postmortem">
          <h2><Database size={18}/> Postmortem</h2>
          {!postmortem ? <p className="muted">Generated after remediation is verified.</p> : <>
            <h3>{postmortem.title}</h3><p>{postmortem.summary}</p>
            <b>Impact</b><p>{postmortem.impact}</p>
            <b>Resolution</b><p>{postmortem.resolution}</p>
            <b>Prevention Items</b><ul>{(postmortem.prevention_items || []).map((x: string, idx: number) => <li key={idx}>{x}</li>)}</ul>
          </>}
        </div>
      </section>}
    </main>
  </div>
}
