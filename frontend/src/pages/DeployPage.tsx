import { GlassCard, CardHeader, ControlButton } from "@/components/twinforge/GlassCard";

export default function DeployPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Deployment</h1>
        <p className="text-sm text-muted-foreground mt-1">Safe deployment controls with rollback capability</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <GlassCard>
          <CardHeader title="Deploy Controls" accent="green" />
          <div className="mt-4 space-y-2">
            <ControlButton onClick={() => {}} color="cyan" icon="◇">Create Digital Twin</ControlButton>
            <ControlButton onClick={() => {}} color="red" icon="⚡">Inject Failure</ControlButton>
            <ControlButton onClick={() => {}} color="purple" icon="◈">Run AI Simulation</ControlButton>
            <ControlButton onClick={() => {}} color="green" icon="▲">Deploy Fix</ControlButton>
            <ControlButton onClick={() => {}} color="zinc" icon="↺">Rollback System</ControlButton>
          </div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Deployment History" accent="cyan" />
          <div className="mt-4 space-y-2">
            {[
              { version: "v2.4.1", time: "2 hours ago", status: "success" },
              { version: "v2.4.0", time: "1 day ago", status: "success" },
              { version: "v2.3.9", time: "3 days ago", status: "rolled back" },
            ].map((d, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-secondary/30 text-sm">
                <span className="text-foreground/90 font-mono">{d.version}</span>
                <span className="text-muted-foreground">{d.time}</span>
                <span className={`capitalize text-xs font-medium px-2 py-0.5 rounded ${
                  d.status === "success" ? "bg-tf-green/10 text-tf-green" : "bg-tf-yellow/10 text-tf-yellow"
                }`}>
                  {d.status}
                </span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
