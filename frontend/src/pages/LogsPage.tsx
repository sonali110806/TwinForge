import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { CardHeader, GlassCard } from "@/components/twinforge/GlassCard";
import { api } from "@/lib/api";

export default function LogsPage() {
  const [filter, setFilter] = useState<string>("all");
  const { data } = useQuery({ queryKey: ["logs"], queryFn: api.getLogs, refetchInterval: 3000 });

  const filtered = filter === "all" ? data ?? [] : (data ?? []).filter((log) => log.type === filter);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Incident Logs</h1>
        <p className="text-sm text-muted-foreground mt-1">Backend activity stream across deployment, failures, and AI analysis</p>
      </div>

      <div className="flex gap-2">
        {["all", "info", "warning", "success", "error"].map((entry) => (
          <button
            key={entry}
            onClick={() => setFilter(entry)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-all border ${
              filter === entry
                ? "bg-tf-cyan/20 text-tf-cyan border-tf-cyan/30"
                : "text-muted-foreground border-transparent hover:bg-secondary"
            }`}
          >
            {entry}
          </button>
        ))}
      </div>

      <GlassCard>
        <CardHeader title="Log Stream" accent="orange" />
        <div className="mt-3 space-y-2 max-h-[60vh] overflow-y-auto">
          {filtered.map((log) => (
            <div key={log.id} className="rounded-lg bg-secondary/30 p-3 text-sm">
              <div className="flex items-center justify-between gap-3">
                <span>{log.message}</span>
                <span className="text-xs uppercase text-muted-foreground">{log.type}</span>
              </div>
              <div className="text-xs text-muted-foreground mt-1">
                {new Date(log.timestamp).toLocaleString()} · {log.source}
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
}
