import React, { useEffect, useState, useCallback } from "react";
import EmailCard from "./EmailCard";
import DraftModal from "./DraftEditor";
import { fetchEmails, generateDraft, sendReply, syncEmails, analytics } from "../api";

export default function EmailListPage({ filter }) {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [activeEmail, setActiveEmail] = useState(null);
  const [draftText, setDraftText] = useState("");
  const [stats, setStats] = useState(null);

  const loadEmails = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetchEmails(filter);
      setEmails(res.emails || []);
    } catch (e) {
      console.error(e);
      alert("Failed to load emails (check backend).");
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { loadEmails(); loadStats(); }, [loadEmails]);

  async function loadStats() {
    try {
      const s = await analytics();
      setStats(s);
    } catch (e) { console.warn(e); }
  }

  async function handleGenerate(email) {
    setModalOpen(true);
    setActiveEmail(email);
    setDraftText("Generating...");
    try {
      const r = await generateDraft(email.message_id);
      setDraftText(r.ai_draft || "");
    } catch (e) {
      console.error(e);
      setDraftText("Failed to generate draft.");
    }
  }

  async function handleQuickReply(email) {
    const text = prompt("Enter quick reply:", "Thanks — received!");
    if (!text) return;
    try {
      await sendReply(email.message_id, text);
      await loadEmails();
    } catch (e) {
      console.error(e);
      alert("Failed to send reply");
    }
  }

  async function handleSend(message_id, text) {
    try {
      await sendReply(message_id, text);
      setModalOpen(false);
      await loadEmails();
    } catch (e) {
      console.error(e);
      alert("Failed to send reply");
    }
  }

  // wire sidebar quick actions if found (so sidebar buttons can call these)
  useEffect(() => {
    const rBtn = document.getElementById("refreshBtn");
    const sBtn = document.getElementById("syncBtn");
    if (rBtn) rBtn.onclick = loadEmails;
    if (sBtn) sBtn.onclick = async () => { await syncEmails(10); await loadEmails(); };
    return () => {
      if (rBtn) rBtn.onclick = null;
      if (sBtn) sBtn.onclick = null;
    };
  }, [loadEmails]);

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">{filter.toUpperCase()}</h2>
        <div className="text-sm text-slate-600">Total: {emails.length}</div>
      </div>

      <div className="grid gap-4">
        {loading && <div className="text-sm text-slate-500">Loading…</div>}
        {!loading && emails.length === 0 && <div className="text-sm text-slate-500">No emails</div>}
        {emails.map(e => (
          <EmailCard key={e.message_id} email={e} onGenerate={handleGenerate} onQuickReply={handleQuickReply} />
        ))}
      </div>

      <DraftModal open={modalOpen} email={activeEmail} text={draftText} onClose={() => setModalOpen(false)} onSend={handleSend} />
    </div>
  );
}
