export default function MetricCard({ title, value, icon, trend, trendValue, color = "blue" }) {
  const colorMap = {
    blue: "text-[#2563eb]",
    red: "text-[#ef4444]",
    green: "text-[#22c55e]",
    yellow: "text-[#eab308]",
  };

  return (
    <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-[#9ca3af] text-sm font-medium">{title}</h3>
        <div className={`p-2 rounded-lg bg-[#1f2937] bg-opacity-50 ${colorMap[color]}`}>
          {icon}
        </div>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold text-[#f9fafb]">{value}</span>
      </div>
      
      {trend && (
        <div className="mt-4 flex items-center gap-1 text-sm">
          <span className={trend === "up" ? "text-[#ef4444]" : "text-[#22c55e]"}>
            {trend === "up" ? "↑" : "↓"} {trendValue}
          </span>
          <span className="text-[#9ca3af]">vs last hour</span>
        </div>
      )}
    </div>
  );
}
