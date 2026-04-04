import { useQuery } from "@tanstack/react-query";

import { CardHeader, GlassCard, MetricBar } from "@/components/twinforge/GlassCard";
import { api, formatUptime } from "@/lib/api";

export default function TwinsPage() {
  const { data } = useQuery({ queryKey: ["twins"], queryFn: api.getTwins, refetchInterval: 4000 });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Digital Twins</h1>
        <p className="text-sm text-muted-foreground mt-1">Live fleet state from the integrated backend</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {data?.map((twin) => (
          <GlassCard key={twin.id}>
            <CardHeader title={twin.name} accent="purple" />
            <div className="mt-4 space-y-3">
              <MetricBar label="CPU" value={twin.cpu} />
              <MetricBar label="Memory" value={twin.memory} />
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Latency</span>
                <span>{twin.latency}ms</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Version</span>
                <span>{twin.version}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Last Fix</span>
                <span>{twin.lastFix}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Uptime</span>
                <span>{formatUptime(twin.uptimeSeconds)}</span>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
