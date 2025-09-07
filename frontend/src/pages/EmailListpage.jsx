import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchEmails, generateDraft, sendReply, syncEmails } from "../api";
import EmailCard from "../components/EmailCard";
import DraftEditor from "../components/DraftEditor";

export default function EmailListPage() {
  const { filter } = useParams();
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);

  async function load() {
    setLoading(true);
    try {
      const data = await fetchEmails(filter || "all");
      setEmails(data.emails || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [filter]);

  async function onGenerateDraft(email) {
    try {
      const resp = await generateDraft(email.message_id);
      // update local email
      setEmails((prev) =>
        prev.map((e) => (e.message_id === email.message_id ? { ...e, ai_draft: resp.ai_draft } : e))
      );
      setSelected({ ...email, ai_draft: resp.ai_draft });
    } catch (e) {
      console.error(e);
      alert("Draft generation failed");
    }
  }

  async function onQuickReply(email) {
    const text = prompt("Quick reply text:", email.ai_draft || "Thanks — received.");
    if (!text) return;
    try {
      await sendReply(email.message_id, text);
      // mark locally
      setEmails((prev) => prev.map((e) => (e.message_id === email.message_id ? { ...e, status: "replied" } : e)));
      alert("Reply sent");
    } catch (e) {
      console.error(e);
      alert("Send failed");
    }
  }

  async function onSync() {
    await syncEmails(10);
    load();
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">{(filter || "all").toUpperCase()} Emails</h2>
        <div className="flex gap-2">
          <button onClick={onSync} className="px-3 py-1 bg-white border rounded">Sync Inbox</button>
          <button onClick={load} className="px-3 py-1 bg-brand text-white rounded">Refresh</button>
        </div>
      </div>

      {loading ? (
        <div>Loading…</div>
      ) : (
        <div className="grid gap-4">
          {emails.map((email) => (
            <EmailCard
              key={email.message_id}
              email={email}
              onGenerateDraft={onGenerateDraft}
              onQuickReply={onQuickReply}
              onSelect={(e) => setSelected(e)}
            />
          ))}
        </div>
      )}

      {selected && (
        <DraftEditor
          email={selected}
          onClose={() => setSelected(null)}
          onSend={async (text) => {
            await sendReply(selected.message_id, text);
            setSelected(null);
            load();
          }}
        />
      )}
    </div>
  );
}
