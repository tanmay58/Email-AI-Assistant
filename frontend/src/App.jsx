import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import EmailListPage from "./pages/EmailListPage";
import DraftsPage from "./pages/DraftsPage";
import AnalyticsPage from "./pages/AnalyticsPage";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <Routes>
            <Route path="/" element={<Navigate to="/emails/all" replace />} />
            <Route path="/emails/:filter" element={<EmailListPage />} />
            <Route path="/drafts" element={<DraftsPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="*" element={<div>Not found</div>} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
