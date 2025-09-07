import React from "react";

export default function Header() {
  return (
    <header className="w-full bg-white shadow p-4 sticky top-0 z-20">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-md bg-brand flex items-center justify-center text-white font-bold">AI</div>
          <div>
            <h1 className="text-xl font-semibold">Email AI Assistant</h1>
            <p className="text-sm text-gray-500">Filter, draft and reply with AI help.</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button id="syncBtn" className="px-3 py-1 border rounded bg-white hover:bg-gray-50">Refresh</button>
        </div>
      </div>
    </header>
  );
}
