import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { CardHeader, ControlButton, GlassCard } from "@/components/twinforge/GlassCard";
import { api, formatRelativeDate } from "@/lib/api";

export default function DeployPage() {
  const queryClient = useQueryClient();
  const { data: deployments } = useQuery({ queryKey: ["deployments"], queryFn: api.getDeployments, refetchInterval: 5000 });

  const refresh = async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ["summary"] }),
      queryClient.invalidateQueries({ queryKey: ["latest-ai"] }),
      queryClient.invalidateQueries({ queryKey: ["deployments"] }),
      queryClient.invalidateQueries({ queryKey: ["logs"] }),
    ]);
  };

  const createTwin = useMutation({ mutationFn: () => api.createTwin(), onSuccess: refresh });
  const injectCrash = useMutation({ mutationFn: () => api.injectFailure("crash"), onSuccess: refresh });
  const runAI = useMutation({ mutationFn: api.analyzeAI, onSuccess: refresh });
  const deployFix = useMutation({ mutationFn: api.deployFix, onSuccess: refresh });
  const rollback = useMutation({ mutationFn: api.rollback, onSuccess: refresh });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Deployment</h1>
        <p className="text-sm text-muted-foreground mt-1">Operational controls tied to the integrated backend actions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <GlassCard>
          <CardHeader title="Deploy Controls" accent="green" />
          <div className="mt-4 space-y-2">
            <ControlButton onClick={() => createTwin.mutate()} color="cyan" icon="◇">Create Digital Twin</ControlButton>
            <ControlButton onClick={() => injectCrash.mutate()} color="red" icon="⚡">Inject Crash</ControlButton>
            <ControlButton onClick={() => runAI.mutate()} color="purple" icon="◈">Run AI Simulation</ControlButton>
            <ControlButton onClick={() => deployFix.mutate()} color="green" icon="▲">Deploy Fix</ControlButton>
            <ControlButton onClick={() => rollback.mutate()} color="zinc" icon="↺">Rollback System</ControlButton>
          </div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Deployment History" accent="cyan" />
          <div className="mt-4 space-y-2">
            {deployments?.map((deployment) => (
              <div key={deployment.id} className="rounded-lg bg-secondary/30 p-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="font-mono">{deployment.version}</span>
                  <span className="capitalize">{deployment.action}</span>
                </div>
                <div className="text-xs text-muted-foreground mt-1">{deployment.details}</div>
                <div className="text-xs text-muted-foreground mt-2">{formatRelativeDate(deployment.createdAt)}</div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
