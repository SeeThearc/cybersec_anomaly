export default function AlertTable({ alerts }) {
  const getRiskColor = (score) => {
    if (score >= 80) return "bg-[#ef4444] text-[#7f1d1d] border-[#ef4444]";
    if (score >= 60) return "bg-[#f97316] text-[#7c2d12] border-[#f97316]";
    if (score >= 30) return "bg-[#eab308] text-[#713f12] border-[#eab308]";
    return "bg-[#22c55e] text-[#14532d] border-[#22c55e]";
  };

  const getRiskLabel = (score) => {
    if (score >= 80) return "CRITICAL";
    if (score >= 60) return "HIGH";
    if (score >= 30) return "MEDIUM";
    return "LOW";
  };

  return (
    <div className="bg-[#111827] border border-[#1f2937] rounded-xl overflow-hidden shadow-sm">
      <div className="p-6 border-b border-[#1f2937] flex justify-between items-center">
        <h2 className="text-lg font-bold text-[#f9fafb]">Recent Security Alerts</h2>
        <button className="text-sm text-[#2563eb] hover:text-[#3b82f6] font-medium">View All</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#0b1220] border-b border-[#1f2937] text-xs uppercase text-[#9ca3af] tracking-wider font-semibold">
              <th className="px-6 py-4">Alert ID</th>
              <th className="px-6 py-4">User ID</th>
              <th className="px-6 py-4">Attack Type</th>
              <th className="px-6 py-4">Risk Level</th>
              <th className="px-6 py-4">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1f2937]">
            {alerts && alerts.length > 0 ? (
              alerts.slice(0, 8).map((alert) => (
                <tr key={alert.id} className="hover:bg-[#1f2937] hover:bg-opacity-50 transition-colors">
                  <td className="px-6 py-4 font-mono text-xs text-[#9ca3af]">#{alert.id}</td>
                  <td className="px-6 py-4 text-sm font-medium">{alert.user_id}</td>
                  <td className="px-6 py-4 text-sm">{alert.prediction || alert.attack_type}</td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-2.5 py-1 text-xs font-bold rounded-md border bg-opacity-20 ${getRiskColor(
                        alert.risk_score
                      )}`}
                    >
                      {getRiskLabel(alert.risk_score)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-xs text-[#9ca3af]">
                    {new Date(alert.created_at).toLocaleTimeString()}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="px-6 py-8 text-center text-[#9ca3af] text-sm">
                  No active alerts found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
