import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();

  const menuItems = [
    { name: "Dashboard", path: "/" },
    { name: "Alerts", path: "/alerts" },
    { name: "Users", path: "/users" },
    { name: "Analytics", path: "/analytics" },
    { name: "AI Copilot", path: "/copilot" },
    { name: "Settings", path: "/settings" },
  ];

  return (
    <aside className="w-64 h-screen bg-[#111827] border-r border-[#1f2937] flex flex-col fixed left-0 top-0 text-[#f9fafb]">
      {/* Logo Area */}
      <div className="h-16 flex items-center px-6 border-b border-[#1f2937]">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-[#2563eb] flex items-center justify-center font-bold">
            U
          </div>
          <span className="text-xl font-bold tracking-wider">Cyber Detect</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-6 px-4 space-y-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              className={`block px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-[#2563eb] text-white"
                  : "text-[#9ca3af] hover:bg-[#1f2937] hover:text-white"
              }`}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* Footer Profile */}
      <div className="p-4 border-t border-[#1f2937]">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[#1f2937] border border-[#374151]" />
          <div>
            <p className="text-sm font-medium">Analyst John</p>
            <p className="text-xs text-[#9ca3af]">Level 2 SOC</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
