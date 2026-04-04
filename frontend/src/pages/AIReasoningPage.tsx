import { GlassCard, CardHeader } from "@/components/twinforge/GlassCard";

export default function AIReasoningPage() {
  const reasoningSteps = [
    { id: 1, step: "Data Collection", detail: "Aggregating metrics from 12 endpoints", status: "complete" },
    { id: 2, step: "Pattern Recognition", detail: "Analyzing 48-hour trend windows", status: "complete" },
    { id: 3, step: "Anomaly Classification", detail: "Running ML classification pipeline", status: "active" },
    { id: 4, step: "Root Cause Analysis", detail: "Correlating service dependencies", status: "pending" },
    { id: 5, step: "Fix Generation", detail: "Generating candidate solutions", status: "pending" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">AI Reasoning Engine</h1>
        <p className="text-sm text-muted-foreground mt-1">Monitor AI decision-making pipeline and reasoning steps</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <GlassCard>
          <CardHeader title="Reasoning Pipeline" accent="purple" />
          <div className="mt-4 space-y-3">
            {reasoningSteps.map((step) => (
              <div key={step.id} className="flex items-start gap-3 p-3 rounded-lg bg-secondary/30">
                <span className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${
                  step.status === "complete" ? "bg-tf-green" :
                  step.status === "active" ? "bg-tf-cyan animate-pulse" : "bg-muted-foreground/30"
                }`} />
                <div>
                  <div className={`text-sm font-medium ${step.status === "pending" ? "text-muted-foreground/50" : "text-foreground/90"}`}>
                    {step.step}
                  </div>
                  <div className="text-xs text-muted-foreground mt-0.5">{step.detail}</div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Model Confidence" accent="cyan" />
          <div className="mt-4 space-y-4">
            <div className="text-center py-8">
              <div className="text-5xl font-bold text-tf-cyan tabular-nums">87%</div>
              <div className="text-sm text-muted-foreground mt-2">Overall confidence score</div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-lg bg-secondary/30 text-center">
                <div className="text-lg font-bold text-tf-green">94%</div>
                <div className="text-xs text-muted-foreground">Detection Accuracy</div>
              </div>
              <div className="p-3 rounded-lg bg-secondary/30 text-center">
                <div className="text-lg font-bold text-tf-purple">81%</div>
                <div className="text-xs text-muted-foreground">Fix Success Rate</div>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
