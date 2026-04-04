import { useQuery } from "@tanstack/react-query";

import { CardHeader, GlassCard } from "@/components/twinforge/GlassCard";
import { api } from "@/lib/api";

export default function AIReasoningPage() {
  const { data } = useQuery({ queryKey: ["latest-ai"], queryFn: api.getLatestAI, refetchInterval: 5000 });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">AI Reasoning Engine</h1>
        <p className="text-sm text-muted-foreground mt-1">Structured reasoning steps and deployment confidence</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <GlassCard>
          <CardHeader title="Reasoning Pipeline" accent="purple" />
          <div className="mt-4 space-y-3">
            {data?.steps.map((step) => (
              <div key={step.id} className="rounded-lg bg-secondary/30 p-3">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium">{step.step}</div>
                  <span className="text-xs uppercase text-muted-foreground">{step.status}</span>
                </div>
                <div className="text-xs text-muted-foreground mt-1">{step.detail}</div>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Confidence Gate" accent="cyan" />
          <div className="mt-4 space-y-4">
            <div className="text-5xl font-bold text-tf-cyan tabular-nums">{data?.confidence.score ?? 0}%</div>
            <div className="text-sm text-muted-foreground">{data?.confidence.decision.message ?? "No active remediation."}</div>
            <div className="rounded-lg bg-secondary/30 p-3">
              <div className="text-xs text-muted-foreground">Root cause</div>
              <div className="text-sm mt-1">{data?.decision.root_cause ?? "System healthy"}</div>
            </div>
            <div className="rounded-lg bg-secondary/30 p-3">
              <div className="text-xs text-muted-foreground">Suggested winner</div>
              <div className="text-sm mt-1">{data?.winner?.name ?? "No fix needed"}</div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
