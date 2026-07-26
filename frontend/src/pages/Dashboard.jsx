import { useState, useEffect } from "react";
import { getStatistics, getAlerts, getEvents } from "../services/api";

import MetricCard from "../components/MetricCard";
import AlertTable from "../components/AlertTable";
import RiskGauge from "../components/RiskGauge";
import Timeline from "../components/Timeline";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const [statsData, alertsData, eventsData] = await Promise.all([
        getStatistics(),
        getAlerts(8),
        getEvents(5),
      ]);
      setStats(statsData);
      setAlerts(alertsData);
      setEvents(eventsData);
      setError(null);
    } catch (err) {
      console.error("Failed to fetch dashboard data:", err);
      setError("Unable to connect to the backend server. Is it running on port 8000?");
    } finally {
      setLoading(false);
    }
  };

  // Poll every 15 seconds
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full text-[#9ca3af]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2563eb] mr-3"></div>
        Initializing SOC Telemetry...
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-[#ef4444] bg-opacity-10 border border-[#ef4444] text-[#ef4444] p-4 rounded-lg m-6">
        {error}
      </div>
    );
  }

  return (
    <div className="p-8 max-w-[1600px] mx-auto space-y-8">
      {/* Header */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-[#f9fafb]">Overview</h1>
          <p className="text-[#9ca3af] text-sm mt-1">Real-time enterprise threat monitoring</p>
        </div>
        <div className="text-xs text-[#9ca3af] flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#2563eb] animate-pulse"></span>
          Live Sync Active
        </div>
      </div>

      {/* Top Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Active Users"
          value={stats?.total_users.toLocaleString()}
          color="blue"
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          }
        />
        <MetricCard
          title="Events Analyzed"
          value={stats?.total_events.toLocaleString()}
          color="green"
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          }
        />
        <MetricCard
          title="High Risk Users"
          value={stats?.high_risk_users}
          trend="up"
          trendValue="2"
          color="yellow"
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          }
        />
        <MetricCard
          title="Critical Alerts"
          value={stats?.critical_alerts}
          trend="down"
          trendValue="1"
          color="red"
          icon={
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          }
        />
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column (Wider) */}
        <div className="lg:col-span-2 space-y-8">
          <AlertTable alerts={alerts} />
        </div>

        {/* Right Column (Narrower) */}
        <div className="space-y-8">
          <RiskGauge score={stats?.average_risk} />
          <Timeline events={events} />
        </div>
      </div>
    </div>
  );
}
