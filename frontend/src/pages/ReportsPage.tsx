import { GlassCard, CardHeader } from "@/components/twinforge/GlassCard";

export default function ReportsPage() {
  const reports = [
    {
      id: 1,
      title: "CPU Cascade Failure — Node Cluster East",
      date: "2 hours ago",
      rootCause: "Memory leak in request handler causing CPU cascade failure",
      fixApplied: "Fix A — Cache Flush",
      downtimePrevented: "~45 minutes",
      confidence: 98,
    },
    {
      id: 2,
      title: "Latency Spike — API Gateway",
      date: "1 day ago",
      rootCause: "DNS resolution timeout in upstream service",
      fixApplied: "Fix B — DNS Cache Refresh",
      downtimePrevented: "~20 minutes",
      confidence: 91,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Post-Mortem Reports</h1>
        <p className="text-sm text-muted-foreground mt-1">Detailed analysis of resolved incidents</p>
      </div>

      <div className="space-y-4">
        {reports.map((report) => (
          <GlassCard key={report.id}>
            <div className="flex items-start justify-between">
              <CardHeader title={report.title} accent="purple" />
              <span className="text-xs text-muted-foreground">{report.date}</span>
            </div>
            <div className="mt-4 space-y-3">
              <div className="p-3 rounded-lg bg-secondary/30">
                <div className="text-xs text-muted-foreground mb-1">Root Cause</div>
                <div className="text-sm text-foreground/90">{report.rootCause}</div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 rounded-lg bg-secondary/30">
                  <div className="text-xs text-muted-foreground mb-1">Fix Applied</div>
                  <div className="text-sm text-tf-green font-medium">{report.fixApplied}</div>
                </div>
                <div className="p-3 rounded-lg bg-secondary/30">
                  <div className="text-xs text-muted-foreground mb-1">Downtime Prevented</div>
                  <div className="text-sm text-tf-cyan font-medium">{report.downtimePrevented}</div>
                </div>
                <div className="p-3 rounded-lg bg-secondary/30">
                  <div className="text-xs text-muted-foreground mb-1">Confidence</div>
                  <div className="text-sm text-tf-purple font-medium">{report.confidence}%</div>
                </div>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
