import { useState, useEffect } from "react";
import { getAlerts } from "../services/api";
import AlertTable from "../components/AlertTable";
import { AlertCircle } from "lucide-react";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const data = await getAlerts(100);
        setAlerts(data);
      } catch (err) {
        console.error("Failed to fetch alerts:", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 15000); // refresh every 15s
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-[#9ca3af]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#ef4444] mr-3"></div>
        Loading Threat Intelligence...
      </div>
    );
  }

  const criticalCount = alerts.filter(a => a.risk_score >= 80).length;

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-[#f9fafb]">Active Security Alerts</h1>
          <p className="text-[#9ca3af] mt-1">Review and manage anomalous user activity</p>
        </div>
        <div className="flex items-center space-x-2 bg-[#ef4444] bg-opacity-10 px-4 py-2 rounded-lg border border-[#ef4444] border-opacity-20">
          <AlertCircle className="w-5 h-5 text-[#ef4444]" />
          <span className="text-[#ef4444] font-semibold">{criticalCount} Critical Alerts</span>
        </div>
      </div>

      <AlertTable alerts={alerts} />
    </div>
  );
}
