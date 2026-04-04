import { GlassCard, CardHeader } from "@/components/twinforge/GlassCard";

export default function TournamentPage() {
  const fixes = [
    { id: "a", name: "Fix A — Cache Flush", probability: 92, perf: 18, risk: "low", time: "1.24s", winner: true },
    { id: "b", name: "Fix B — Service Restart", probability: 78, perf: 25, risk: "medium", time: "2.31s", winner: false },
    { id: "c", name: "Fix C — Config Rollback", probability: 65, perf: 12, risk: "high", time: "0.89s", winner: false },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Fix Tournament</h1>
        <p className="text-sm text-muted-foreground mt-1">Compare and evaluate AI-generated fix candidates</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {fixes.map((fix) => (
          <GlassCard key={fix.id} className={fix.winner ? "border-tf-green/50 animate-winner-glow" : ""}>
            {fix.winner && (
              <div className="inline-block px-2 py-0.5 bg-tf-green rounded text-[10px] font-bold text-background mb-3">
                WINNER
              </div>
            )}
            <CardHeader title={fix.name} accent={fix.winner ? "green" : "cyan"} />
            <div className="mt-4 space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Success Rate</span>
                <span className="text-foreground/80 tabular-nums">{fix.probability}%</span>
              </div>
              <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-tf-cyan to-tf-purple rounded-full" style={{ width: `${fix.probability}%` }} />
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Performance Gain</span>
                <span className="text-tf-green tabular-nums">+{fix.perf}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Risk</span>
                <span className={`capitalize ${fix.risk === "low" ? "text-tf-green" : fix.risk === "medium" ? "text-tf-yellow" : "text-tf-red"}`}>
                  {fix.risk}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Exec Time</span>
                <span className="text-foreground/70 tabular-nums">{fix.time}</span>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
