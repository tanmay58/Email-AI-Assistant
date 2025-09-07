import React from "react";
import { NavLink } from "react-router-dom";

const buttons = [
  { to: "/emails/all", label: "All", color: "bg-white" },
  { to: "/emails/unread", label: "Unread", color: "bg-white" },
  { to: "/emails/support", label: "Support", color: "bg-white" },
  { to: "/emails/query", label: "Query", color: "bg-white" },
  { to: "/emails/request", label: "Request", color: "bg-white" },
  { to: "/emails/help", label: "Help", color: "bg-white" },
  { to: "/drafts", label: "Drafts", color: "bg-white" },
  { to: "/analytics", label: "Analytics", color: "bg-white" },
];

export default function Sidebar() {
  return (
    <aside className="w-60 p-6 sticky top-16 h-[calc(100vh-64px)]">
      <nav className="space-y-3">
        {buttons.map((b) => (
          <NavLink
            key={b.to}
            to={b.to}
            className={({ isActive }) =>
              `block px-3 py-2 rounded-lg flex items-center justify-between hover:shadow-sm transition ${
                isActive ? "bg-brand text-white" : "bg-white text-gray-800"
              }`
            }
          >
            <span className="font-medium">{b.label}</span>
            <span className="text-xs text-gray-500">→</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
