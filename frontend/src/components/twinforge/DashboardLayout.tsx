import { Outlet } from "react-router-dom";
import { TwinForgeSidebar } from "@/components/twinforge/Sidebar";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useState, useEffect } from "react";

export default function DashboardLayout() {
  const [agentStatus] = useState<"monitoring" | "thinking" | "executing">("monitoring");
  const [currentTime, setCurrentTime] = useState(new Date());
  const [mounted, setMounted] = useState(false);

  const ws = useWebSocket({ enabled: true, interval: 2000 });
  const systemStatus = ws.metrics.status ?? "healthy";

  useEffect(() => {
    setMounted(true);
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy": return "text-tf-green";
      case "warning": return "text-tf-yellow";
      case "critical": return "text-tf-red";
      default: return "text-tf-green";
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex">
      <TwinForgeSidebar agentStatus={agentStatus} />

      <main className="flex-1 flex flex-col min-h-screen overflow-hidden">
        {/* Top Bar */}
        <header className="h-14 border-b border-border bg-sidebar backdrop-blur-sm flex items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <h2 className="text-sm font-semibold text-muted-foreground hidden sm:block">TwinForge Dashboard</h2>
          </div>
          <div className="flex items-center gap-4">
            <div className={`flex items-center gap-2 px-2.5 py-1 rounded-full border ${
              ws.connectionStatus === "connected"
                ? "bg-tf-green/10 border-tf-green/30"
                : "bg-tf-yellow/10 border-tf-yellow/30"
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${
                ws.connectionStatus === "connected" ? "bg-tf-green animate-pulse" : "bg-tf-yellow"
              }`} />
              <span className={`text-xs font-medium ${
                ws.connectionStatus === "connected" ? "text-tf-green" : "text-tf-yellow"
              }`}>
                {ws.connectionStatus === "connected" ? "WS Connected" : ws.connectionStatus}
              </span>
            </div>

            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all duration-500 ${
              systemStatus === "healthy"
                ? "border-tf-green/30 bg-tf-green/10"
                : systemStatus === "warning"
                ? "border-tf-yellow/30 bg-tf-yellow/10"
                : "border-tf-red/30 bg-tf-red/10"
            }`}>
              <span className={`w-2 h-2 rounded-full transition-colors duration-500 ${
                systemStatus === "healthy" ? "bg-tf-green" : systemStatus === "warning" ? "bg-tf-yellow" : "bg-tf-red animate-status-pulse"
              }`} />
              <span className={`text-sm font-medium capitalize transition-colors duration-500 ${getStatusColor(systemStatus)}`}>
                {systemStatus}
              </span>
            </div>

            {mounted && (
              <div className="text-xs text-muted-foreground tabular-nums hidden sm:block">
                {currentTime.toLocaleTimeString()}
              </div>
            )}
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 p-4 md:p-6 overflow-auto">
          <Outlet context={{ ws, systemStatus, agentStatus }} />
        </div>
      </main>
    </div>
  );
}
