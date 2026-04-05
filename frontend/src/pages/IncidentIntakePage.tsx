import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { CardHeader, GlassCard } from "@/components/twinforge/GlassCard";
import { api, IncidentFormInput } from "@/lib/api";


const initialForm: IncidentFormInput = {
  appName: "",
  issueType: "cpu_spike",
  cpu: 95,
  memory: 88,
  latency: 320,
  issueDescription: "",
  severity: "high",
  environment: "production",
  errorLogs: "",
  codeSnippet: "",
};


export default function IncidentIntakePage() {
  const [form, setForm] = useState<IncidentFormInput>(initialForm);
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: api.submitIncident,
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["latest-ai"] }),
        queryClient.invalidateQueries({ queryKey: ["reports"] }),
        queryClient.invalidateQueries({ queryKey: ["logs"] }),
        queryClient.invalidateQueries({ queryKey: ["summary"] }),
      ]);
    },
  });

  const updateField = (key: keyof IncidentFormInput, value: string) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Incident Intake</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Paste code, logs, or errors and generate AI analysis, winning fix, remediation code, and a report.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <GlassCard>
          <CardHeader title="Code And Error Intake" accent="cyan" />
          <form
            className="mt-4 space-y-3"
            onSubmit={(event) => {
              event.preventDefault();
              mutation.mutate(form);
            }}
          >
            <input
              className="w-full rounded-lg bg-secondary/30 p-3"
              placeholder="Application Name"
              value={form.appName}
              onChange={(e) => updateField("appName", e.target.value)}
            />

            <select
              className="w-full rounded-lg bg-secondary/30 p-3"
              value={form.issueType}
              onChange={(e) => updateField("issueType", e.target.value)}
            >
              <option value="cpu_spike">CPU Spike</option>
              <option value="memory_leak">Memory Leak</option>
              <option value="latency_issue">Latency Issue</option>
              <option value="crash">Crash</option>
            </select>

            <input
              className="w-full rounded-lg bg-secondary/30 p-3"
              type="number"
              placeholder="CPU"
              value={form.cpu}
              onChange={(e) => updateField("cpu", e.target.value)}
            />
            <input
              className="w-full rounded-lg bg-secondary/30 p-3"
              type="number"
              placeholder="Memory"
              value={form.memory}
              onChange={(e) => updateField("memory", e.target.value)}
            />
            <input
              className="w-full rounded-lg bg-secondary/30 p-3"
              type="number"
              placeholder="Latency"
              value={form.latency}
              onChange={(e) => updateField("latency", e.target.value)}
            />

            <select
              className="w-full rounded-lg bg-secondary/30 p-3"
              value={form.severity}
              onChange={(e) => updateField("severity", e.target.value)}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>

            <input
              className="w-full rounded-lg bg-secondary/30 p-3"
              placeholder="Environment"
              value={form.environment}
              onChange={(e) => updateField("environment", e.target.value)}
            />

            <textarea
              className="w-full rounded-lg bg-secondary/30 p-3 min-h-28"
              placeholder="Issue Description"
              value={form.issueDescription}
              onChange={(e) => updateField("issueDescription", e.target.value)}
            />

            <textarea
              className="w-full rounded-lg bg-secondary/30 p-3 min-h-32 font-mono text-sm"
              placeholder="Paste error logs or stack trace"
              value={form.errorLogs}
              onChange={(e) => updateField("errorLogs", e.target.value)}
            />

            <textarea
              className="w-full rounded-lg bg-secondary/30 p-3 min-h-40 font-mono text-sm"
              placeholder="Paste code snippet to analyze"
              value={form.codeSnippet}
              onChange={(e) => updateField("codeSnippet", e.target.value)}
            />

            <button
              type="submit"
              className="w-full rounded-lg bg-tf-cyan/20 border border-tf-cyan/30 p-3"
            >
              Analyze And Generate Report
            </button>
          </form>
        </GlassCard>

        <GlassCard>
          <CardHeader title="Analysis Result" accent="purple" />
          <div className="mt-4 space-y-3">
            {!mutation.data && (
              <p className="text-sm text-muted-foreground">
                Submit the form to generate AI reasoning, fixes, and a report.
              </p>
            )}

            {mutation.data && (
              <>
                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Detected Issue</div>
                  <div className="text-sm mt-1">{mutation.data.analysis.issue}</div>
                </div>

                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Root Cause</div>
                  <div className="text-sm mt-1">{mutation.data.analysis.decision.root_cause}</div>
                </div>

                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Suggested Fixes</div>
                  <div className="text-sm mt-1 space-y-1">
                    {mutation.data.analysis.results.length > 0 ? (
                      mutation.data.analysis.results.map((result) => (
                        <div key={result.fix_id}>
                          {result.name} ({result.success_probability}% success)
                        </div>
                      ))
                    ) : (
                      <div>No fixes needed</div>
                    )}
                  </div>
                </div>

                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Winning Fix</div>
                  <div className="text-sm mt-1">{mutation.data.analysis.winner?.name ?? "No fix needed"}</div>
                </div>

                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Confidence</div>
                  <div className="text-sm mt-1">{mutation.data.analysis.confidence.score}%</div>
                </div>

                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Generated Report</div>
                  <div className="text-sm mt-1">{mutation.data.report.summary}</div>
                </div>

                <div className="rounded-lg bg-secondary/30 p-3">
                  <div className="text-xs text-muted-foreground">Generated Remediation Code</div>
                  <pre className="text-xs mt-2 whitespace-pre-wrap">{mutation.data.remediationCode}</pre>
                </div>
              </>
            )}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
