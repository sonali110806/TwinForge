import { useQuery } from "@tanstack/react-query";

import { CardHeader, GlassCard } from "@/components/twinforge/GlassCard";
import { api, formatRelativeDate } from "@/lib/api";

export default function ReportsPage() {
  const { data } = useQuery({ queryKey: ["reports"], queryFn: api.getReports, refetchInterval: 5000 });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Post-Mortem Reports</h1>
        <p className="text-sm text-muted-foreground mt-1">Incident summaries generated from the integrated AI analysis flow</p>
      </div>

      <div className="space-y-4">
        {data?.map((report) => (
          <GlassCard key={report.id}>
            <div className="flex items-start justify-between">
              <CardHeader title={report.title} accent="purple" />
              <span className="text-xs text-muted-foreground">{formatRelativeDate(report.createdAt)}</span>
            </div>
            <div className="mt-4 space-y-3">
              <div className="rounded-lg bg-secondary/30 p-3">
                <div className="text-xs text-muted-foreground mb-1">Root Cause</div>
                <div className="text-sm">{report.rootCause}</div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground mb-1">Fix Applied</div>
                  <div className="text-sm">{report.fixApplied}</div>
                </div>
                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground mb-1">Downtime Prevented</div>
                  <div className="text-sm">{report.downtimePrevented}</div>
                </div>
                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground mb-1">Confidence</div>
                  <div className="text-sm">{report.confidence}%</div>
                </div>
              </div>
              <div className="text-sm text-muted-foreground">{report.summary}</div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
