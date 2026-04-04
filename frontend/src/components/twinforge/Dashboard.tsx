import { useState, useEffect, useCallback } from "react";
import { GlassCard, CardHeader, MetricBar, ControlButton } from "@/components/twinforge/GlassCard";
import { useWebSocket } from "@/hooks/useWebSocket";

type SystemStatus = "healthy" | "critical" | "warning";
type FixStatus = "idle" | "running" | "success" | "failed";
type AgentStatus = "monitoring" | "thinking" | "executing";

interface SystemMetrics {
  cpu: number;
  memory: number;
  latency: number;
  status: SystemStatus;
}

interface TwinInstance {
  id: string;
  name: string;
  status: "active" | "simulating" | "destroyed";
  cpu: number;
  memory: number;
  destroyTimer: number;
}

interface FixOption {
  id: string;
  name: string;
  status: FixStatus;
  successProbability: number;
  performanceGain: number;
  riskLevel: "low" | "medium" | "high";
  executionTime: number;
  isWinner: boolean;
}

interface LogEntry {
  id: number;
  message: string;
  timestamp: string;
  type: "info" | "warning" | "success" | "error";
}

interface AIStep {
  id: number;
  message: string;
  complete: boolean;
}

interface PostMortem {
  rootCause: string;
  fixApplied: string;
  downtimePrevented: string;
  confidence: number;
}

export default function CommandCenter() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>("healthy");
  const [agentStatus, setAgentStatus] = useState<AgentStatus>("monitoring");
  const [realSystem, setRealSystem] = useState<SystemMetrics>({ cpu: 45, memory: 62, latency: 120, status: "healthy" });
  const [digitalTwinHealth, setDigitalTwinHealth] = useState<SystemMetrics>({ cpu: 45, memory: 62, latency: 120, status: "healthy" });
  const [confidenceScore, setConfidenceScore] = useState(0);
  const [countdown, setCountdown] = useState(120);
  const [isCountdownActive, setIsCountdownActive] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [mounted, setMounted] = useState(false);

  const ws = useWebSocket({ enabled: true, interval: 2000, baseMetrics: realSystem });

  useEffect(() => {
    if (ws.metrics && systemStatus === "healthy" && !isCountdownActive) {
      setRealSystem((prev) => ({ ...prev, cpu: ws.metrics.cpu, memory: ws.metrics.memory, latency: ws.metrics.latency }));
    }
  }, [ws.metrics, systemStatus, isCountdownActive]);

  const [twins, setTwins] = useState<TwinInstance[]>([
    { id: "a", name: "Twin A", status: "active", cpu: 45, memory: 62, destroyTimer: 300 },
    { id: "b", name: "Twin B", status: "active", cpu: 45, memory: 62, destroyTimer: 300 },
    { id: "c", name: "Twin C", status: "active", cpu: 45, memory: 62, destroyTimer: 300 },
  ]);

  const [aiSteps, setAiSteps] = useState<AIStep[]>([
    { id: 1, message: "Metrics captured", complete: false },
    { id: 2, message: "Anomaly detected", complete: false },
    { id: 3, message: "Root cause analyzed", complete: false },
    { id: 4, message: "Generated fixes", complete: false },
    { id: 5, message: "Running simulations", complete: false },
  ]);

  const [fixes, setFixes] = useState<FixOption[]>([
    { id: "a", name: "Fix A", status: "idle", successProbability: 0, performanceGain: 0, riskLevel: "low", executionTime: 0, isWinner: false },
    { id: "b", name: "Fix B", status: "idle", successProbability: 0, performanceGain: 0, riskLevel: "medium", executionTime: 0, isWinner: false },
    { id: "c", name: "Fix C", status: "idle", successProbability: 0, performanceGain: 0, riskLevel: "high", executionTime: 0, isWinner: false },
  ]);

  const [postMortem, setPostMortem] = useState<PostMortem | null>(null);

  useEffect(() => {
    setMounted(true);
    setLogs([{ id: 1, message: "System initialized", timestamp: new Date().toISOString(), type: "info" }]);
  }, []);

  const addLog = useCallback((message: string, type: LogEntry["type"] = "info") => {
    setLogs((prev) => [{ id: Date.now(), message, timestamp: new Date().toISOString(), type }, ...prev.slice(0, 19)]);
  }, []);

  useEffect(() => {
    if (!isCountdownActive || countdown <= 0) return;
    const timer = setInterval(() => setCountdown((prev) => prev - 1), 1000);
    return () => clearInterval(timer);
  }, [isCountdownActive, countdown]);

  const runAISequence = async () => {
    setAgentStatus("thinking");
    setAiSteps((prev) => prev.map((s) => ({ ...s, complete: false })));
    for (let i = 0; i < 5; i++) {
      await new Promise((r) => setTimeout(r, 600));
      setAiSteps((prev) => prev.map((s, idx) => (idx === i ? { ...s, complete: true } : s)));
    }
    setAgentStatus("monitoring");
  };

  const createTwin = () => {
    setDigitalTwinHealth({ ...realSystem });
    setTwins((prev) => prev.map((t) => ({ ...t, status: "active" as const, cpu: realSystem.cpu, memory: realSystem.memory })));
    addLog("Digital Twins created successfully", "success");
    setConfidenceScore(85);
  };

  const injectFailure = async () => {
    const crisisMetrics = { cpu: 95, memory: 88, latency: 450, status: "critical" as const };
    setRealSystem(crisisMetrics);
    ws.updateBaseMetrics(crisisMetrics);
    setSystemStatus("critical");
    setIsCountdownActive(true);
    setCountdown(120);
    addLog("Failure injected - CPU spike detected!", "error");
    setConfidenceScore(25);
    await runAISequence();
  };

  const runSimulation = async () => {
    setAgentStatus("executing");
    addLog("AI generating fixes...", "info");
    setFixes((prev) =>
      prev.map((f) => ({
        ...f, status: "idle" as const, executionTime: 0, isWinner: false,
        successProbability: Math.floor(Math.random() * 40) + 60,
        performanceGain: Math.floor(Math.random() * 30) + 10,
      }))
    );
    setTwins((prev) => prev.map((t) => ({ ...t, status: "simulating" as const })));
    await new Promise((r) => setTimeout(r, 500));
    addLog("Tournament started", "warning");

    for (let i = 0; i < 3; i++) {
      setFixes((prev) => prev.map((f, idx) => (idx === i ? { ...f, status: "running" as const } : f)));
      const execTime = Math.random() * 2000 + 500;
      await new Promise((r) => setTimeout(r, execTime));
      const success = Math.random() > 0.3;
      setFixes((prev) =>
        prev.map((f, idx) =>
          idx === i
            ? { ...f, status: (success ? "success" : "failed") as FixStatus, executionTime: execTime / 1000, successProbability: success ? prev[idx].successProbability + 10 : prev[idx].successProbability - 20 }
            : f
        )
      );
    }

    setFixes((prev) => {
      const successFixes = prev.filter((f) => f.status === "success");
      if (successFixes.length > 0) {
        const fastest = successFixes.reduce((a, b) => (a.executionTime < b.executionTime ? a : b));
        return prev.map((f) => ({ ...f, isWinner: f.id === fastest.id }));
      }
      return prev;
    });

    setTwins((prev) => prev.map((t) => ({ ...t, status: "active" as const })));
    setAgentStatus("monitoring");
    addLog("Simulation complete - Winner selected", "success");
    setConfidenceScore(92);
  };

  const deployFix = () => {
    const winner = fixes.find((f) => f.isWinner);
    if (winner) {
      const healthyMetrics = { cpu: 42, memory: 58, latency: 95, status: "healthy" as const };
      setRealSystem(healthyMetrics);
      setDigitalTwinHealth(healthyMetrics);
      ws.updateBaseMetrics(healthyMetrics);
      setSystemStatus("healthy");
      setIsCountdownActive(false);
      addLog(`${winner.name} deployed successfully`, "success");
      setConfidenceScore(98);
      setPostMortem({ rootCause: "Memory leak in request handler causing CPU cascade failure", fixApplied: winner.name, downtimePrevented: "~45 minutes", confidence: 98 });
    } else {
      addLog("No winning fix to deploy", "warning");
    }
  };

  const rollback = () => {
    const defaultMetrics = { cpu: 45, memory: 62, latency: 120, status: "healthy" as const };
    setRealSystem(defaultMetrics);
    setDigitalTwinHealth(defaultMetrics);
    ws.updateBaseMetrics(defaultMetrics);
    setSystemStatus("healthy");
    setIsCountdownActive(false);
    setCountdown(120);
    setFixes((prev) => prev.map((f) => ({ ...f, status: "idle" as const, executionTime: 0, isWinner: false, successProbability: 0, performanceGain: 0 })));
    setAiSteps((prev) => prev.map((s) => ({ ...s, complete: false })));
    setPostMortem(null);
    addLog("System rolled back to stable state", "info");
    setConfidenceScore(0);
    setAgentStatus("monitoring");
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="grid grid-cols-12 gap-4">
      {/* System Overview */}
      <div className="col-span-12 lg:col-span-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <GlassCard className="col-span-2">
            <CardHeader title="Real System Health" accent="cyan" />
            <div className="space-y-3 mt-3">
              <MetricBar label="CPU" value={realSystem.cpu} />
              <MetricBar label="Memory" value={realSystem.memory} />
              <MetricBar label="Latency" value={Math.min(100, realSystem.latency / 5)} suffix={`${realSystem.latency}ms`} />
            </div>
          </GlassCard>

          <GlassCard className="col-span-2">
            <CardHeader title="Digital Twin Health" accent="purple" />
            <div className="space-y-3 mt-3">
              <MetricBar label="CPU" value={digitalTwinHealth.cpu} />
              <MetricBar label="Memory" value={digitalTwinHealth.memory} />
              <MetricBar label="Latency" value={Math.min(100, digitalTwinHealth.latency / 5)} suffix={`${digitalTwinHealth.latency}ms`} />
            </div>
          </GlassCard>

          <GlassCard highlight={systemStatus === "critical"}>
            <CardHeader title="Anomaly Status" accent={systemStatus === "critical" ? "red" : "green"} />
            <div className="mt-3">
              <div className={`text-2xl font-bold transition-colors duration-500 ${systemStatus === "critical" ? "text-tf-red" : "text-tf-green"}`}>
                {systemStatus === "critical" ? "DETECTED" : "NONE"}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {systemStatus === "critical" ? "Active anomaly in progress" : "All systems nominal"}
              </p>
            </div>
          </GlassCard>

          <GlassCard>
            <CardHeader title="Confidence Score" accent="purple" />
            <div className="mt-3 flex items-end gap-3">
              <span className={`text-3xl font-bold tabular-nums transition-all duration-700 ${confidenceScore >= 70 ? "text-tf-green" : confidenceScore >= 40 ? "text-tf-yellow" : "text-tf-red"}`}>
                {confidenceScore}%
              </span>
            </div>
            <div className="mt-2 h-2 bg-secondary rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-700 ease-out ${confidenceScore >= 70 ? "bg-gradient-to-r from-tf-green to-emerald-400" : confidenceScore >= 40 ? "bg-gradient-to-r from-tf-yellow to-tf-orange" : "bg-gradient-to-r from-tf-red to-tf-pink"}`}
                style={{ width: `${confidenceScore}%` }}
              />
            </div>
          </GlassCard>

          <GlassCard className={isCountdownActive ? "border-tf-red/30" : ""}>
            <CardHeader title="Predicted Failure" accent={isCountdownActive ? "red" : "zinc"} />
            <div className={`mt-3 text-3xl font-mono font-bold tabular-nums transition-all duration-500 ${isCountdownActive ? "text-tf-red" : "text-muted-foreground/30"}`}>
              {formatTime(countdown)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {isCountdownActive ? "Time until system crash" : "No active threat"}
            </p>
          </GlassCard>
        </div>
      </div>

      {/* AI Reasoning Panel */}
      <div className="col-span-12 lg:col-span-4">
        <GlassCard className="h-full">
          <CardHeader title="AI Reasoning" accent="purple" />
          <div className="mt-3 bg-background/50 rounded-lg p-3 font-mono text-sm">
            <div className="text-tf-cyan mb-2">AI Agent:</div>
            <div className="space-y-2">
              {aiSteps.map((step) => (
                <div key={step.id} className={`flex items-center gap-2 transition-all duration-300 ${step.complete ? "text-tf-green" : "text-muted-foreground/40"}`}>
                  <span className={`transition-transform duration-300 ${step.complete ? "scale-100" : "scale-75"}`}>
                    {step.complete ? "✓" : "○"}
                  </span>
                  <span>{step.message}</span>
                  {!step.complete && agentStatus === "thinking" && (
                    <span className="inline-block w-1.5 h-4 bg-tf-cyan animate-pulse ml-1" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Digital Twin Visualization */}
      <div className="col-span-12">
        <GlassCard>
          <CardHeader title="Digital Twin Visualization" accent="cyan" />
          <div className="mt-4 flex items-center justify-center gap-4 flex-wrap">
            <div className={`px-6 py-4 rounded-xl border-2 transition-all duration-500 ${realSystem.status === "critical" ? "border-tf-red bg-tf-red/10" : "border-tf-cyan bg-tf-cyan/10"}`}>
              <div className="text-xs text-muted-foreground mb-1">REAL SYSTEM</div>
              <div className={`text-lg font-bold ${realSystem.status === "critical" ? "text-tf-red" : "text-tf-cyan"}`}>Production</div>
            </div>
            {twins.map((twin) => (
              <div key={twin.id} className="flex items-center gap-4">
                <div className={`w-12 h-0.5 transition-all duration-500 ${twin.status === "simulating" ? "bg-gradient-to-r from-tf-cyan to-tf-purple animate-pulse" : "bg-border"}`} />
                <div className={`px-4 py-3 rounded-xl border transition-all duration-500 ${twin.status === "simulating" ? "border-tf-purple bg-tf-purple/10 scale-105" : "border-border bg-secondary/50"}`}>
                  <div className="text-xs text-muted-foreground mb-1">{twin.name.toUpperCase()}</div>
                  <div className={`text-sm font-medium capitalize ${twin.status === "simulating" ? "text-tf-purple" : "text-muted-foreground"}`}>{twin.status}</div>
                  <div className="text-[10px] text-muted-foreground/60 mt-1">CPU: {twin.cpu}% | Mem: {twin.memory}%</div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Fix Tournament */}
      <div className="col-span-12 lg:col-span-8">
        <GlassCard>
          <CardHeader title="Fix Tournament" accent="cyan" />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
            {fixes.map((fix) => (
              <div key={fix.id} className={`relative rounded-xl border p-4 transition-all duration-500 ${fix.isWinner ? "border-tf-green bg-tf-green/10 animate-winner-glow" : fix.status === "running" ? "border-tf-cyan/50 bg-tf-cyan/5" : "border-border bg-secondary/30"}`}>
                {fix.isWinner && <div className="absolute -top-2 -right-2 px-2 py-0.5 bg-tf-green rounded text-[10px] font-bold text-background">WINNER</div>}
                <div className="text-base font-semibold text-foreground/90 mb-3">{fix.name}</div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between"><span className="text-muted-foreground">Success Rate</span><span className="text-foreground/70 tabular-nums">{fix.successProbability}%</span></div>
                  <div className="h-1.5 bg-secondary rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-tf-cyan to-tf-purple rounded-full transition-all duration-700" style={{ width: `${fix.successProbability}%` }} /></div>
                  <div className="flex justify-between mt-2"><span className="text-muted-foreground">Performance</span><span className="text-tf-green tabular-nums">+{fix.performanceGain}%</span></div>
                  <div className="flex justify-between"><span className="text-muted-foreground">Risk Level</span><span className={`capitalize ${fix.riskLevel === "low" ? "text-tf-green" : fix.riskLevel === "medium" ? "text-tf-yellow" : "text-tf-red"}`}>{fix.riskLevel}</span></div>
                </div>
                <div className={`mt-3 inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium transition-all duration-300 ${fix.status === "idle" ? "text-muted-foreground bg-secondary/50" : fix.status === "running" ? "text-tf-cyan bg-tf-cyan/10" : fix.status === "success" ? "text-tf-green bg-tf-green/10" : "text-tf-red bg-tf-red/10"}`}>
                  {fix.status === "running" && <span className="w-1 h-1 rounded-full bg-current animate-ping" />}
                  <span className="capitalize">{fix.status}</span>
                </div>
                {fix.executionTime > 0 && <div className="mt-2 text-xs text-muted-foreground">Time: <span className="text-foreground/70 tabular-nums">{fix.executionTime.toFixed(2)}s</span></div>}
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Control Panel */}
      <div className="col-span-12 lg:col-span-4">
        <GlassCard className="h-full">
          <CardHeader title="Safe Deploy Control" accent="green" />
          <div className="mt-4 space-y-2">
            <ControlButton onClick={createTwin} color="cyan" icon="◇">Create Digital Twin</ControlButton>
            <ControlButton onClick={injectFailure} color="red" icon="⚡">Inject Failure</ControlButton>
            <ControlButton onClick={runSimulation} color="purple" icon="◈">Run AI Simulation</ControlButton>
            <ControlButton onClick={deployFix} color="green" icon="▲">Deploy Fix</ControlButton>
            <ControlButton onClick={rollback} color="zinc" icon="↺">Rollback System</ControlButton>
          </div>
        </GlassCard>
      </div>

      {/* Incident Log */}
      <div className="col-span-12 lg:col-span-6">
        <GlassCard>
          <CardHeader title="Incident Log Stream" accent="orange" />
          <div className="mt-3 space-y-1 max-h-48 overflow-y-auto">
            {mounted && logs.map((log) => (
              <div key={log.id} className="flex items-center gap-3 text-sm py-2 px-3 rounded-lg bg-secondary/30 animate-slide-in">
                <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${log.type === "success" ? "bg-tf-green" : log.type === "error" ? "bg-tf-red" : log.type === "warning" ? "bg-tf-yellow" : "bg-muted-foreground"}`} />
                <span className="text-foreground/70 flex-1">{log.message}</span>
                <span className="text-xs text-muted-foreground/60 tabular-nums">{new Date(log.timestamp).toLocaleTimeString()}</span>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Post-Mortem Report */}
      <div className="col-span-12 lg:col-span-6">
        <GlassCard>
          <CardHeader title="Post-Mortem Report" accent="purple" />
          {postMortem ? (
            <div className="mt-3 space-y-3">
              <div className="p-3 rounded-lg bg-secondary/30">
                <div className="text-xs text-muted-foreground mb-1">Root Cause</div>
                <div className="text-sm text-foreground/90">{postMortem.rootCause}</div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-lg bg-secondary/30">
                  <div className="text-xs text-muted-foreground mb-1">Fix Applied</div>
                  <div className="text-sm text-tf-green font-medium">{postMortem.fixApplied}</div>
                </div>
                <div className="p-3 rounded-lg bg-secondary/30">
                  <div className="text-xs text-muted-foreground mb-1">Downtime Prevented</div>
                  <div className="text-sm text-tf-cyan font-medium">{postMortem.downtimePrevented}</div>
                </div>
                <div className="p-3 rounded-lg bg-secondary/30">
                  <div className="text-xs text-muted-foreground mb-1">Confidence</div>
                  <div className="text-sm text-tf-purple font-medium">{postMortem.confidence}%</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="mt-3 text-center py-8 text-muted-foreground/40">
              <div className="text-2xl mb-2">◉</div>
              <div className="text-sm">No incidents resolved yet</div>
            </div>
          )}
        </GlassCard>
      </div>
    </div>
  );
}
