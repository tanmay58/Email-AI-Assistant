import React, { useEffect, useState } from "react";
import { getAnalytics } from "../api";

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getAnalytics();
        setStats(data);
      } catch (e) {
        console.error(e);
      }
    })();
  }, []);

  if (!stats) return <div>Loading analytics…</div>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Analytics</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-medium">Total emails</h3>
          <div className="text-3xl">{stats.total_emails}</div>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-medium">Categories</h3>
          <pre className="text-sm mt-2">{JSON.stringify(stats.categories, null, 2)}</pre>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-medium">Status</h3>
          <pre className="text-sm mt-2">{JSON.stringify(stats.status, null, 2)}</pre>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-medium">Sentiments</h3>
          <pre className="text-sm mt-2">{JSON.stringify(stats.sentiments, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
}
