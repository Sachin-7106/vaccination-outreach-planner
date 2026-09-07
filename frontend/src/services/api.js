const API_BASE = '/api';

export async function fetchAreas() {
  const res = await fetch(`${API_BASE}/areas`);
  if (!res.ok) throw new Error('Failed to fetch city areas');
  return res.json();
}

export async function generatePlan(planParams) {
  const res = await fetch(`${API_BASE}/planner/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(planParams)
  });
  if (!res.ok) throw new Error('Failed to generate outreach plan');
  return res.json();
}

export async function comparePlan(planParams) {
  const res = await fetch(`${API_BASE}/planner/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(planParams)
  });
  if (!res.ok) throw new Error('Failed to compare plan objectives');
  return res.json();
}

export async function submitReview(reviewData) {
  const res = await fetch(`${API_BASE}/reviews/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reviewData)
  });
  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    throw new Error(errorJson.detail || 'Failed to submit human review');
  }
  return res.json();
}

export async function fetchAuditTrail() {
  const res = await fetch(`${API_BASE}/reviews/audit-trail`);
  if (!res.ok) throw new Error('Failed to fetch audit trail');
  return res.json();
}

export async function fetchRecommendations(status = null) {
  const url = status ? `${API_BASE}/reviews/recommendations?status=${status}` : `${API_BASE}/reviews/recommendations`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
}

export async function fetchEvaluationMetrics(num_sessions = 5, capacity = 300, max_dist = 12.0) {
  const res = await fetch(`${API_BASE}/eval/metrics?num_sessions=${num_sessions}&capacity=${capacity}&max_dist=${max_dist}`);
  if (!res.ok) throw new Error('Failed to fetch evaluation metrics');
  return res.json();
}

export async function fetchErrorAnalysis() {
  const res = await fetch(`${API_BASE}/eval/error-analysis`);
  if (!res.ok) throw new Error('Failed to fetch error analysis scenarios');
  return res.json();
}
