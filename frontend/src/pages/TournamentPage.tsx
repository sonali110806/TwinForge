import { useQuery } from "@tanstack/react-query";

import { CardHeader, GlassCard } from "@/components/twinforge/GlassCard";
import { api } from "@/lib/api";

export default function TournamentPage() {
  const { data } = useQuery({ queryKey: ["latest-ai"], queryFn: api.getLatestAI, refetchInterval: 5000 });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Fix Tournament</h1>
        <p className="text-sm text-muted-foreground mt-1">Candidate remediations ranked by risk, speed, and success probability</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {data?.results.map((fix) => (
          <GlassCard key={fix.fix_id} className={data.winner?.fix_id === fix.fix_id ? "border-tf-green/50" : ""}>
            <CardHeader title={fix.name} accent={data.winner?.fix_id === fix.fix_id ? "green" : "cyan"} />
            <div className="mt-4 space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Success Rate</span>
                <span>{fix.success_probability}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Performance Gain</span>
                <span>+{fix.performance_gain}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Risk</span>
                <span className="capitalize">{fix.risk_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Runtime</span>
                <span>{fix.estimated_seconds}s</span>
              </div>
              <div className="text-xs text-muted-foreground">
                Side effects: {fix.side_effects.length ? fix.side_effects.join(", ") : "None"}
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
