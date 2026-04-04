import { GlassCard, CardHeader } from "@/components/twinforge/GlassCard";

export default function SettingsPage() {
  const settings = [
    { label: "WebSocket Interval", value: "2000ms", description: "Frequency of metric updates" },
    { label: "Auto-Recovery", value: "Enabled", description: "Automatically deploy winning fix" },
    { label: "Twin Count", value: "3", description: "Number of digital twin instances" },
    { label: "Failure Threshold", value: "85% CPU", description: "CPU usage that triggers alert" },
    { label: "Log Retention", value: "30 days", description: "How long incident logs are kept" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-sm text-muted-foreground mt-1">Configure TwinForge system parameters</p>
      </div>

      <GlassCard>
        <CardHeader title="System Configuration" accent="cyan" />
        <div className="mt-4 divide-y divide-border">
          {settings.map((s, i) => (
            <div key={i} className="flex items-center justify-between py-4 first:pt-0 last:pb-0">
              <div>
                <div className="text-sm font-medium text-foreground/90">{s.label}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{s.description}</div>
              </div>
              <div className="px-3 py-1.5 rounded-lg bg-secondary/50 text-sm text-foreground/70 font-mono">
                {s.value}
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
}
