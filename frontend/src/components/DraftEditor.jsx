import React, { useState } from "react";

export default function DraftEditor({ email, onClose, onSend }) {
  const [text, setText] = useState(email.ai_draft || "");

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center p-4">
      <div className="bg-white max-w-2xl w-full rounded-lg p-6 shadow-lg">
        <div className="flex items-start justify-between">
          <div>
            <div className="text-sm text-gray-500">Draft reply to: <span className="font-medium">{email.sender}</span></div>
            <div className="text-sm text-gray-500">Subject: {email.subject || "(no subject)"}</div>
          </div>
          <button onClick={onClose} className="text-gray-500">Cancel</button>
        </div>

        <textarea
          className="w-full mt-4 p-3 border rounded h-40"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="mt-4 flex justify-end gap-2">
          <button onClick={onClose} className="px-3 py-1 rounded border">Close</button>
          <button onClick={() => onSend(text)} className="px-4 py-1 rounded bg-accent text-white">Send Reply</button>
        </div>
      </div>
    </div>
  );
}
