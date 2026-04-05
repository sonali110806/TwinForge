import { useQuery } from "@tanstack/react-query";

import { CardHeader, GlassCard } from "@/components/twinforge/GlassCard";
import { api } from "@/lib/api";

export default function SettingsPage() {
  const { data } = useQuery({ queryKey: ["settings"], queryFn: api.getSettings });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-sm text-muted-foreground mt-1">Runtime configuration exposed by the backend</p>
      </div>

      <GlassCard>
        <CardHeader title="System Configuration" accent="cyan" />
        <div className="mt-4 divide-y divide-border">
          {data?.map((setting) => (
            <div key={setting.label} className="flex items-center justify-between py-4 first:pt-0 last:pb-0">
              <div>
                <div className="text-sm font-medium text-foreground/90">{setting.label}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{setting.description}</div>
              </div>
              <div className="px-3 py-1.5 rounded-lg bg-secondary/50 text-sm text-foreground/70 font-mono">
                {setting.value}
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
}
