import { useState, useEffect } from "react";
import { GlassCard, CardHeader } from "@/components/twinforge/GlassCard";

interface LogEntry {
  id: number;
  message: string;
  timestamp: string;
  type: "info" | "warning" | "success" | "error";
}

const initialLogs: LogEntry[] = [
  { id: 1, message: "System initialized", timestamp: new Date().toISOString(), type: "info" },
  { id: 2, message: "WebSocket connection established", timestamp: new Date().toISOString(), type: "success" },
  { id: 3, message: "Metrics collection started", timestamp: new Date().toISOString(), type: "info" },
  { id: 4, message: "CPU usage spike detected on node-3", timestamp: new Date(Date.now() - 60000).toISOString(), type: "warning" },
  { id: 5, message: "Auto-scaling triggered for cluster-east", timestamp: new Date(Date.now() - 120000).toISOString(), type: "info" },
  { id: 6, message: "Memory leak resolved in handler-pool", timestamp: new Date(Date.now() - 180000).toISOString(), type: "success" },
  { id: 7, message: "Latency threshold exceeded (>400ms)", timestamp: new Date(Date.now() - 300000).toISOString(), type: "error" },
];

export default function LogsPage() {
  const [logs, setLogs] = useState<LogEntry[]>(initialLogs);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    const interval = setInterval(() => {
      const types: LogEntry["type"][] = ["info", "warning", "success", "error"];
      const messages = [
        "Health check passed",
        "Metrics snapshot captured",
        "Connection pool recycled",
        "Certificate renewal scheduled",
        "Rate limit approaching threshold",
      ];
      setLogs((prev) => [
        {
          id: Date.now(),
          message: messages[Math.floor(Math.random() * messages.length)],
          timestamp: new Date().toISOString(),
          type: types[Math.floor(Math.random() * types.length)],
        },
        ...prev.slice(0, 49),
      ]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const filtered = filter === "all" ? logs : logs.filter((l) => l.type === filter);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Incident Logs</h1>
        <p className="text-sm text-muted-foreground mt-1">Real-time incident and event log stream</p>
      </div>

      <div className="flex gap-2">
        {["all", "info", "warning", "success", "error"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-all border ${
              filter === f
                ? "bg-tf-cyan/20 text-tf-cyan border-tf-cyan/30"
                : "text-muted-foreground border-transparent hover:bg-secondary"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      <GlassCard>
        <CardHeader title="Log Stream" accent="orange" />
        <div className="mt-3 space-y-1 max-h-[60vh] overflow-y-auto">
          {filtered.map((log) => (
            <div
              key={log.id}
              className="flex items-center gap-3 text-sm py-2 px-3 rounded-lg bg-secondary/30 animate-slide-in"
            >
              <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
                log.type === "success" ? "bg-tf-green" :
                log.type === "error" ? "bg-tf-red" :
                log.type === "warning" ? "bg-tf-yellow" : "bg-muted-foreground"
              }`} />
              <span className="text-foreground/70 flex-1">{log.message}</span>
              <span className="text-xs text-muted-foreground/60 tabular-nums flex-shrink-0">
                {new Date(log.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
}
