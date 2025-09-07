import React from "react";

export default function EmailCard({ email, onGenerateDraft, onQuickReply, onSelect }) {
  return (
    <div className="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition">
      <div className="flex justify-between items-start">
        <div>
          <div className="text-sm text-gray-600">{email.sender}</div>
          <div className="font-semibold">{email.subject || "(no subject)"}</div>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-500">{(new Date(email.received_at)).toLocaleString()}</div>
          <div className="mt-2">
            <span className="text-xs px-2 py-1 rounded-full bg-gray-100">{email.category}</span>
          </div>
        </div>
      </div>

      <p className="mt-3 text-sm text-gray-600 line-clamp-3">{email.body}</p>

      <div className="mt-4 flex gap-2">
        <button onClick={() => onGenerateDraft?.(email)} className="px-3 py-1 rounded bg-brand text-white text-sm">Generate Draft</button>
        <button onClick={() => onQuickReply?.(email)} className="px-3 py-1 rounded border text-sm">Quick Reply</button>
        <button onClick={() => onSelect?.(email)} className="ml-auto text-sm text-gray-500">Open</button>
      </div>
    </div>
  );
}
