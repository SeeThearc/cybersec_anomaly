import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/alerts", label: "Alerts" },
  { to: "/users", label: "Users" },
  { to: "/analytics", label: "Analytics" },
  { to: "/copilot", label: "AI Copilot" },
  { to: "/settings", label: "Settings" },
];

function Sidebar() {
  return (
    <aside className="w-64 border-r border-[var(--color-border)] bg-[var(--color-bg-card)] p-4">
      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              [
                "block rounded-lg px-4 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-[var(--color-accent)] text-white"
                  : "text-[var(--color-text-secondary)] hover:bg-[#1f2937] hover:text-white",
              ].join(" ")
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
