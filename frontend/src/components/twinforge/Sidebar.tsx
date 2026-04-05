import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X } from "lucide-react";

type AgentStatus = "monitoring" | "thinking" | "executing";

const navItems = [
  { id: "command", path: "/", label: "Command Center", icon: "⌘" },
  { id: "twins", path: "/twins", label: "Digital Twins", icon: "◇" },
  { id: "reasoning", path: "/ai", label: "AI Reasoning", icon: "◈" },
  { id: "tournament", path: "/tournament", label: "Fix Tournament", icon: "▣" },
  { id: "deploy", path: "/deploy", label: "Deployment", icon: "▲" },
  { id: "incident-intake", path: "/incident-intake", label: "Incident Intake", icon: "✦" },
  { id: "logs", path: "/logs", label: "Incident Logs", icon: "≡" },
  { id: "reports", path: "/reports", label: "Post Mortem", icon: "◉" },
  { id: "settings", path: "/settings", label: "Settings", icon: "⚙" },
];

interface SidebarProps {
  agentStatus: AgentStatus;
}

export function TwinForgeSidebar({ agentStatus }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* Mobile overlay */}
      {!collapsed && (
        <div
          className="fixed inset-0 bg-background/80 z-30 lg:hidden"
          onClick={() => setCollapsed(true)}
        />
      )}

      {/* Mobile toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="fixed top-3 left-3 z-50 lg:hidden p-2 rounded-lg bg-secondary border border-border"
      >
        {collapsed ? <Menu className="w-5 h-5" /> : <X className="w-5 h-5" />}
      </button>

      <aside
        className={`fixed lg:relative z-40 h-screen border-r border-border bg-sidebar backdrop-blur-sm flex flex-col transition-all duration-300 ${
          collapsed ? "-translate-x-full lg:translate-x-0 lg:w-16" : "translate-x-0 w-64"
        }`}
      >
        <div className="p-4 border-b border-border">
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl bg-gradient-to-br from-tf-cyan via-tf-purple to-tf-pink flex items-center justify-center shadow-lg shadow-tf-cyan/20 flex-shrink-0 cursor-pointer"
              onClick={() => setCollapsed(!collapsed)}
            >
              <span className="text-lg font-bold text-foreground">T</span>
            </div>
            {!collapsed && (
              <div>
                <h1 className="text-lg font-bold tracking-tight text-foreground">TwinForge</h1>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                  Autonomous Digital Twin
                </p>
              </div>
            )}
          </div>
        </div>

        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <Link
              key={item.id}
              to={item.path}
              onClick={() => {
                if (window.innerWidth < 1024) setCollapsed(true);
              }}
              title={collapsed ? item.label : undefined}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive(item.path)
                  ? "bg-gradient-to-r from-tf-cyan/20 to-tf-purple/20 text-tf-cyan border border-tf-cyan/30"
                  : "text-muted-foreground hover:text-foreground hover:bg-secondary border border-transparent"
              }`}
            >
              <span className="text-base opacity-70 flex-shrink-0">{item.icon}</span>
              {!collapsed && item.label}
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-border">
          {!collapsed && <div className="text-xs text-muted-foreground">AI Agent</div>}
          <div
            className={`flex items-center gap-2 mt-1 ${
              agentStatus === "thinking"
                ? "text-tf-purple"
                : agentStatus === "executing"
                ? "text-tf-cyan"
                : "text-tf-green"
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full bg-current flex-shrink-0 ${
                agentStatus !== "monitoring" ? "animate-pulse" : ""
              }`}
            />
            {!collapsed && (
              <span className="text-sm font-medium capitalize">{agentStatus}</span>
            )}
          </div>
        </div>
      </aside>
    </>
  );
}
