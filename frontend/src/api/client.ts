const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

export const IncidentPilotAPI = {
  incidents: () => api<any[]>('/incidents'),
  incident: (id: string) => api<any>(`/incidents/${id}`),
  events: (id: string) => api<any[]>(`/incidents/${id}/events`),
  actions: (id: string) => api<any[]>(`/incidents/${id}/actions`),
  toolCalls: (id: string) => api<any[]>(`/incidents/${id}/tool-calls`),
  postmortem: (id: string) => api<any>(`/incidents/${id}/postmortem`),
  triggerDemo: () => api<any>('/demo/trigger-alert', { method: 'POST' }),
  resetDemo: () => api<any>('/demo/reset', { method: 'POST' }),
  approve: (id: string) => api<any>(`/actions/${id}/approve`, { method: 'POST', body: JSON.stringify({ decision_note: 'Approved from IncidentPilot dashboard.' }) }),
  reject: (id: string) => api<any>(`/actions/${id}/reject`, { method: 'POST', body: JSON.stringify({ decision_note: 'Rejected from IncidentPilot dashboard.' }) })
};
