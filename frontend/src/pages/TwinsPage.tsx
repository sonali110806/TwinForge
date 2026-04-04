import { GlassCard, CardHeader } from "@/components/twinforge/GlassCard";

export default function TwinsPage() {
  const twins = [
    { id: "a", name: "Twin Alpha", status: "active", cpu: 42, memory: 58, uptime: "12h 34m" },
    { id: "b", name: "Twin Beta", status: "active", cpu: 38, memory: 65, uptime: "8h 12m" },
    { id: "c", name: "Twin Gamma", status: "standby", cpu: 5, memory: 22, uptime: "2h 05m" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Digital Twins</h1>
        <p className="text-sm text-muted-foreground mt-1">Manage and monitor your digital twin instances</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {twins.map((twin) => (
          <GlassCard key={twin.id}>
            <CardHeader title={twin.name} accent="purple" />
            <div className="mt-4 space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Status</span>
                <span className={`font-medium capitalize ${twin.status === "active" ? "text-tf-green" : "text-tf-yellow"}`}>
                  {twin.status}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">CPU</span>
                <span className="text-foreground/70 tabular-nums">{twin.cpu}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Memory</span>
                <span className="text-foreground/70 tabular-nums">{twin.memory}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Uptime</span>
                <span className="text-foreground/70 tabular-nums">{twin.uptime}</span>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
