import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

export default function RiskGauge({ score }) {
  const normalizedScore = Math.min(Math.max(score || 0, 0), 100);
  const remainder = 100 - normalizedScore;

  const data = [
    { name: "Risk", value: normalizedScore },
    { name: "Safe", value: remainder },
  ];

  const getColor = (s) => {
    if (s >= 80) return "#ef4444"; // Red
    if (s >= 60) return "#f97316"; // Orange
    if (s >= 30) return "#eab308"; // Yellow
    return "#22c55e"; // Green
  };

  const riskColor = getColor(normalizedScore);
  const COLORS = [riskColor, "#1f2937"];

  return (
    <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm flex flex-col items-center justify-center">
      <h2 className="text-lg font-bold text-[#f9fafb] self-start mb-2">System Risk Level</h2>
      <div className="relative w-full h-48">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="75%"
              startAngle={180}
              endAngle={0}
              innerRadius="60%"
              outerRadius="80%"
              paddingAngle={0}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        {/* Score overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-6">
          <span className="text-4xl font-bold" style={{ color: riskColor }}>
            {normalizedScore.toFixed(1)}
          </span>
          <span className="text-xs text-[#9ca3af] uppercase tracking-wider font-semibold mt-1">
            Risk Score
          </span>
        </div>
      </div>
    </div>
  );
}
