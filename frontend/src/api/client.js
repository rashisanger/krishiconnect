const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');
const ACCESS_KEY = 'kc_access_token';
const REFRESH_KEY = 'kc_refresh_token';

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: ({ access, refresh }) => {
    if (access) localStorage.setItem(ACCESS_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear: () => { localStorage.removeItem(ACCESS_KEY); localStorage.removeItem(REFRESH_KEY); },
};

function readableError(payload, status) {
  if (payload && typeof payload === 'object') {
    if (payload.detail) return payload.detail;
    if (payload.error) return payload.error;
    const first = Object.entries(payload)[0];
    if (first) return `${first[0].replaceAll('_', ' ')}: ${Array.isArray(first[1]) ? first[1][0] : first[1]}`;
  }
  return `The request could not be completed (${status}).`;
}

async function refreshAccessToken() {
  const refresh = tokenStore.getRefresh();
  if (!refresh) return null;
  const response = await fetch(`${API_BASE_URL}/accounts/token/refresh/`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh }),
  });
  if (!response.ok) { tokenStore.clear(); return null; }
  const tokens = await response.json();
  tokenStore.set(tokens); // Refresh tokens rotate in this project's SimpleJWT settings.
  return tokens.access;
}

export async function apiRequest(path, { method = 'GET', body, query, auth = true, retry = true } = {}) {
  const suffix = `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;
  const url = API_BASE_URL.startsWith('/') ? new URL(suffix, window.location.origin) : new URL(suffix);
  const requestUrl = API_BASE_URL.startsWith('/') ? `${url.pathname}${url.search}` : url.toString();
  if (query) Object.entries(query).forEach(([key, value]) => value !== '' && value != null && url.searchParams.set(key, value));
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  const access = auth ? tokenStore.getAccess() : null;
  if (access) headers.Authorization = `Bearer ${access}`;
  const response = await fetch(requestUrl, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  if (response.status === 401 && auth && retry) {
    const renewed = await refreshAccessToken();
    if (renewed) return apiRequest(path, { method, body, query, auth, retry: false });
    tokenStore.clear();
    window.dispatchEvent(new CustomEvent('kc:session-expired'));
  }
  if (response.status === 204) return null;
  const payload = await response.json().catch(() => null);
  if (!response.ok) throw new Error(readableError(payload, response.status));
  return payload;
}

export function unwrapPage(payload) { return Array.isArray(payload) ? payload : payload?.results || []; }
