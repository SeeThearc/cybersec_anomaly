import { useState, useEffect } from "react";
import { getAnalytics } from "../services/api";
import {
  PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  AreaChart, Area,
  LineChart, Line
} from "recharts";

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const analyticsData = await getAnalytics();
        setData(analyticsData);
      } catch (err) {
        console.error("Failed to fetch analytics:", err);
        setError("Failed to load analytics data from backend.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-[#9ca3af]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2563eb] mr-3"></div>
        Loading Analytics...
      </div>
    );
  }

  if (error || !data) {
    return <div className="text-[#ef4444] p-6">{error || "No data available."}</div>;
  }

  const COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#2563eb", "#8b5cf6"];

  return (
    <div className="p-8 max-w-[1600px] mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-[#f9fafb]">Advanced Analytics</h1>
        <p className="text-[#9ca3af] text-sm mt-1">Deep dive into telemetry and ML model performance</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* 1. Attack Distribution */}
        <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Attack Distribution</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.attack_distribution}
                  cx="50%" cy="50%"
                  innerRadius={60} outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {data.attack_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: "#1f2937", border: "none" }} itemStyle={{ color: "#f9fafb" }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 2. Risk Distribution (Trend) */}
        <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Average Risk Trend</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.risk_trend}>
                <defs>
                  <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                <XAxis dataKey="time" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" fontSize={12} domain={[0, 100]} />
                <RechartsTooltip contentStyle={{ backgroundColor: "#1f2937", border: "none", color: "#f9fafb" }} />
                <Area type="monotone" dataKey="risk" stroke="#ef4444" fillOpacity={1} fill="url(#colorRisk)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 3. Department Chart */}
        <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Alerts by Department</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.department_distribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
                <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" fontSize={12} />
                <RechartsTooltip cursor={{fill: '#1f2937'}} contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", color: "#f9fafb" }} />
                <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 4. Monthly Events */}
        <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Monthly Telemetry Volume</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.monthly_events}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
                <XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
                <YAxis stroke="#9ca3af" fontSize={12} />
                <RechartsTooltip cursor={{fill: '#1f2937'}} contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", color: "#f9fafb" }} />
                <Bar dataKey="events" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* ML Metrics Section */}
      <div>
        <h2 className="text-xl font-bold text-[#f9fafb] mt-8 mb-4 border-b border-[#1f2937] pb-2">ML Model Performance</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* 5. ROC Curve */}
          <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-bold text-[#f9fafb] mb-4">ROC Curve</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.roc_curve}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="fpr" stroke="#9ca3af" fontSize={12} type="number" domain={[0, 1]} tickCount={6} />
                  <YAxis stroke="#9ca3af" fontSize={12} type="number" domain={[0, 1]} tickCount={6} />
                  <RechartsTooltip contentStyle={{ backgroundColor: "#1f2937", border: "none", color: "#f9fafb" }} />
                  <Line type="monotone" dataKey="tpr" stroke="#22c55e" strokeWidth={2} dot={false} />
                  {/* Random Guess Line */}
                  <Line type="linear" dataKey="fpr" stroke="#4b5563" strokeDasharray="5 5" dot={false} isAnimationActive={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-[#9ca3af] text-center mt-2">False Positive Rate vs True Positive Rate</p>
          </div>

          {/* 6. PR Curve */}
          <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Precision-Recall Curve</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.pr_curve}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="recall" stroke="#9ca3af" fontSize={12} type="number" domain={[0, 1]} tickCount={6} />
                  <YAxis stroke="#9ca3af" fontSize={12} type="number" domain={[0, 1]} tickCount={6} />
                  <RechartsTooltip contentStyle={{ backgroundColor: "#1f2937", border: "none", color: "#f9fafb" }} />
                  <Line type="monotone" dataKey="precision" stroke="#3b82f6" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-[#9ca3af] text-center mt-2">Recall vs Precision</p>
          </div>

          {/* 7. SHAP Feature Importance */}
          <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-bold text-[#f9fafb] mb-4">SHAP Feature Importance</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.shap_importance} layout="vertical" margin={{ left: 40 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" horizontal={false} />
                  <XAxis type="number" stroke="#9ca3af" fontSize={12} />
                  <YAxis dataKey="feature" type="category" stroke="#9ca3af" fontSize={12} />
                  <RechartsTooltip cursor={{fill: '#1f2937'}} contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", color: "#f9fafb" }} />
                  <Bar dataKey="importance" fill="#f59e0b" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* 8. Custom Grid Confusion Matrix */}
          <div className="bg-[#111827] border border-[#1f2937] rounded-xl p-6 shadow-sm">
            <h2 className="text-lg font-bold text-[#f9fafb] mb-4">Confusion Matrix</h2>
            <div className="w-full overflow-x-auto">
              <div className="min-w-max">
                {/* Header row */}
                <div className="flex">
                  <div className="w-24"></div>
                  {data.confusion_matrix.classes.map(cls => (
                    <div key={cls} className="w-20 text-center text-xs font-semibold text-[#9ca3af] transform -rotate-45 mb-2">
                      {cls}
                    </div>
                  ))}
                </div>
                {/* Matrix rows */}
                {data.confusion_matrix.matrix.map((row, i) => (
                  <div key={i} className="flex items-center mb-1">
                    <div className="w-24 text-xs font-semibold text-[#9ca3af] text-right pr-4">
                      {data.confusion_matrix.classes[i]}
                    </div>
                    {row.map((val, j) => {
                      // Calculate color intensity (simplified logic)
                      const isDiagonal = i === j;
                      let bgClass = "bg-[#1f2937]";
                      if (val > 0) {
                        if (isDiagonal) {
                          bgClass = val > 1000 ? "bg-[#166534]" : val > 100 ? "bg-[#22c55e]" : "bg-[#86efac] text-black";
                        } else {
                          bgClass = val > 10 ? "bg-[#ef4444]" : "bg-[#fca5a5] text-black";
                        }
                      }
                      
                      return (
                        <div 
                          key={`${i}-${j}`} 
                          className={`w-20 h-10 flex items-center justify-center mr-1 text-sm font-mono rounded ${bgClass} ${isDiagonal && val>0 ? 'text-white' : ''}`}
                        >
                          {val}
                        </div>
                      )
                    })}
                  </div>
                ))}
              </div>
            </div>
            <div className="mt-4 flex gap-4 text-xs text-[#9ca3af] justify-center">
              <span className="flex items-center gap-1"><div className="w-3 h-3 bg-[#22c55e] rounded-sm"></div> True Positives</span>
              <span className="flex items-center gap-1"><div className="w-3 h-3 bg-[#ef4444] rounded-sm"></div> False Positives/Negatives</span>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}
