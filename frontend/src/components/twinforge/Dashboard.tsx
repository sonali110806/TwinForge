import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { CardHeader, ControlButton, GlassCard, MetricBar } from "@/components/twinforge/GlassCard";
import { api, formatRelativeDate, formatUptime } from "@/lib/api";

export default function CommandCenter() {
  const queryClient = useQueryClient();
  const summaryQuery = useQuery({
    queryKey: ["summary"],
    queryFn: api.getSummary,
    refetchInterval: 3000,
  });

  const aiQuery = useQuery({
    queryKey: ["latest-ai"],
    queryFn: api.getLatestAI,
    refetchInterval: 5000,
  });

  const refreshAll = async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ["summary"] }),
      queryClient.invalidateQueries({ queryKey: ["latest-ai"] }),
      queryClient.invalidateQueries({ queryKey: ["twins"] }),
      queryClient.invalidateQueries({ queryKey: ["logs"] }),
      queryClient.invalidateQueries({ queryKey: ["reports"] }),
      queryClient.invalidateQueries({ queryKey: ["deployments"] }),
    ]);
  };

  const createTwin = useMutation({
    mutationFn: () => api.createTwin(),
    onSuccess: refreshAll,
  });

  const runAnalysis = useMutation({
    mutationFn: api.analyzeAI,
    onSuccess: refreshAll,
  });

  const injectCpu = useMutation({
    mutationFn: () => api.injectFailure("cpu"),
    onSuccess: refreshAll,
  });

  const injectMemory = useMutation({
    mutationFn: () => api.injectFailure("memory"),
    onSuccess: refreshAll,
  });

  const deployFix = useMutation({
    mutationFn: api.deployFix,
    onSuccess: refreshAll,
  });

  const rollback = useMutation({
    mutationFn: api.rollback,
    onSuccess: refreshAll,
  });

  const summary = summaryQuery.data;
  const ai = aiQuery.data;

  if (!summary) {
    return <div className="text-sm text-muted-foreground">Loading TwinForge command center...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <GlassCard>
          <CardHeader title="System CPU" accent="cyan" />
          <div className="mt-4">
            <MetricBar label="Average CPU" value={summary.system.cpu} />
          </div>
        </GlassCard>
        <GlassCard>
          <CardHeader title="System Memory" accent="purple" />
          <div className="mt-4">
            <MetricBar label="Average Memory" value={summary.system.memory} />
          </div>
        </GlassCard>
        <GlassCard>
          <CardHeader title="Latency" accent="orange" />
          <div className="mt-4">
            <MetricBar
              label="Average Latency"
              value={Math.min(100, Math.round(summary.system.latency / 4))}
              suffix={`${summary.system.latency}ms`}
            />
          </div>
        </GlassCard>
        <GlassCard highlight={summary.system.status === "critical"}>
          <CardHeader title="Fleet Status" accent={summary.system.status === "critical" ? "red" : "green"} />
          <div className="mt-4">
            <div className="text-2xl font-bold capitalize">{summary.system.status}</div>
            <p className="text-xs text-muted-foreground mt-1">{summary.system.twinCount} twins currently connected</p>
          </div>
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <GlassCard className="xl:col-span-2">
          <CardHeader title="Digital Twins" accent="purple" />
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3">
            {summary.twins.map((twin) => (
              <div key={twin.id} className="rounded-xl bg-secondary/30 p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="font-medium">{twin.name}</div>
                  <span className="text-xs capitalize text-muted-foreground">{twin.status}</span>
                </div>
                <MetricBar label="CPU" value={twin.cpu} />
                <MetricBar label="Memory" value={twin.memory} />
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>{twin.version}</span>
                  <span>{formatUptime(twin.uptimeSeconds)}</span>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Actions" accent="cyan" />
          <div className="mt-4 space-y-2">
            <ControlButton onClick={() => createTwin.mutate()} color="cyan" icon="◇">Create Twin</ControlButton>
            <ControlButton onClick={() => injectCpu.mutate()} color="red" icon="⚡">Inject CPU Spike</ControlButton>
            <ControlButton onClick={() => injectMemory.mutate()} color="red" icon="⚠">Inject Memory Leak</ControlButton>
            <ControlButton onClick={() => runAnalysis.mutate()} color="purple" icon="◈">Run AI Analysis</ControlButton>
            <ControlButton onClick={() => deployFix.mutate()} color="green" icon="▲">Deploy Winner</ControlButton>
            <ControlButton onClick={() => rollback.mutate()} color="zinc" icon="↺">Rollback</ControlButton>
          </div>
        </GlassCard>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <GlassCard>
          <CardHeader title="AI Recommendation" accent="green" />
          <div className="mt-4 space-y-3">
            <div className="text-sm text-muted-foreground">Current issue</div>
            <div className="text-lg font-semibold">{ai?.issue ?? "No anomaly detected"}</div>
            <div className="text-sm text-muted-foreground">{ai?.confidence.decision.message ?? "Monitoring only."}</div>
            {ai?.winner && (
              <div className="rounded-lg bg-secondary/30 p-3">
                <div className="text-xs text-muted-foreground">Winning fix</div>
                <div className="text-sm font-medium mt-1">{ai.winner.name}</div>
              </div>
            )}
          </div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Trend Prediction" accent="orange" />
          <div className="mt-4 text-sm text-foreground/85">{summary.prediction}</div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Recent Logs" accent="zinc" />
          <div className="mt-4 space-y-2">
            {summary.logs.slice(0, 4).map((log) => (
              <div key={log.id} className="rounded-lg bg-secondary/30 p-3">
                <div className="text-sm">{log.message}</div>
                <div className="text-xs text-muted-foreground mt-1">{formatRelativeDate(log.timestamp)}</div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
