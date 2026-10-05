const API_BASE = '/api';

export function getAuthToken() {
  return localStorage.getItem('city_health_token') || '';
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('city_health_token', token);
  } else {
    localStorage.removeItem('city_health_token');
  }
}

export function getStoredUser() {
  const raw = localStorage.getItem('city_health_user');
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (e) {
    return null;
  }
}

export function setStoredUser(user) {
  if (user) {
    localStorage.setItem('city_health_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('city_health_user');
  }
}

function authHeaders(extra = {}) {
  const token = getAuthToken();
  const headers = { 'Content-Type': 'application/json', ...extra };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export async function loginUser(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    throw new Error(errorJson.detail || 'Login failed. Please check credentials.');
  }
  const data = await res.json();
  setAuthToken(data.access_token);
  setStoredUser({
    user_id: data.user_id,
    username: data.username,
    role: data.role,
    full_name: data.full_name
  });
  return data;
}

export async function fetchAreas() {
  const res = await fetch(`${API_BASE}/areas`, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch city areas');
  return res.json();
}

export async function fetchAreasGeoJSON() {
  const res = await fetch(`${API_BASE}/areas/geojson`, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch city zones GeoJSON');
  return res.json();
}

export async function generatePlan(planParams) {
  const res = await fetch(`${API_BASE}/planner/generate`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(planParams)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to generate outreach plan');
  }
  return res.json();
}

export async function comparePlan(planParams) {
  const res = await fetch(`${API_BASE}/planner/compare`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(planParams)
  });
  if (!res.ok) throw new Error('Failed to compare plan objectives');
  return res.json();
}

export async function submitReview(reviewData) {
  const res = await fetch(`${API_BASE}/reviews/approve`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(reviewData)
  });
  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    throw new Error(errorJson.detail || 'Failed to submit human review');
  }
  return res.json();
}

export async function fetchAuditTrail() {
  const res = await fetch(`${API_BASE}/reviews/audit-trail`, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch audit trail');
  return res.json();
}

export async function fetchRecommendations(status = null) {
  const url = status ? `${API_BASE}/reviews/recommendations?status=${status}` : `${API_BASE}/reviews/recommendations`;
  const res = await fetch(url, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch recommendations');
  return res.json();
}

export async function fetchEvaluationMetrics(num_sessions = 5, capacity = 300, max_dist = 12.0) {
  const res = await fetch(`${API_BASE}/eval/metrics?num_sessions=${num_sessions}&capacity=${capacity}&max_dist=${max_dist}`, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch evaluation metrics');
  return res.json();
}

export async function fetchErrorAnalysis() {
  const res = await fetch(`${API_BASE}/eval/error-analysis`, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch error analysis scenarios');
  return res.json();
}

export async function fetchForecasts(areaId = null) {
  const url = areaId ? `${API_BASE}/forecast?area_id=${areaId}` : `${API_BASE}/forecast`;
  const res = await fetch(url, { headers: authHeaders() });
  if (!res.ok) throw new Error('Failed to fetch forecasting data');
  return res.json();
}
