// Lightweight wrapper around backend endpoints. Update BASE if needed.
import axios from "axios";

const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function fetchEmails(filter = "all") {
  const resp = await axios.get(`${BASE}/emails`, { params: { filter } });
  return resp.data;
}

export async function syncEmails(maxResults = 10) {
  const resp = await axios.post(`${BASE}/emails/sync`, null, { params: { maxResults } });
  return resp.data;
}

export async function generateDraft(message_id) {
  const resp = await axios.post(`${BASE}/drafts/generate`, { message_id });
  return resp.data;
}

export async function sendReply(message_id, reply_text) {
  const resp = await axios.post(`${BASE}/reply/`, { message_id, reply_text });
  return resp.data;
}

export async function getAnalytics() {
  const resp = await axios.get(`${BASE}/analytics/stats`);
  return resp.data;
}
