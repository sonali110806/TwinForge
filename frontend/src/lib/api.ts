export type SystemStatus = "healthy" | "warning" | "critical";

export interface Twin {
  id: number;
  name: string;
  status: string;
  cpu: number;
  memory: number;
  latency: number;
  version: string;
  lastFix: string;
  uptimeSeconds: number;
  updatedAt: string;
  createdAt: string;
}

export interface SystemMetrics {
  cpu: number;
  memory: number;
  latency: number;
  status: SystemStatus;
  twinCount: number;
}

export interface LogEntry {
  id: number;
  type: "info" | "warning" | "success" | "error";
  source: string;
  message: string;
  timestamp: string;
}

export interface Report {
  id: number;
  title: string;
  issue: string;
  rootCause: string;
  fixApplied: string;
  downtimePrevented: string;
  confidence: number;
  summary: string;
  createdAt: string;
}

export interface Deployment {
  id: number;
  version: string;
  action: string;
  status: string;
  details: string;
  createdAt: string;
}

export interface AIResult {
  issue: string;
  issueType?: string;
  decision: {
    root_cause: string;
    fixes: Array<{
      id: string;
      name: string;
      action: string;
      risk_level: string;
      estimated_seconds: number;
      side_effects: string[];
    }>;
  };
  results: Array<{
    fix_id: string;
    name: string;
    risk_level: string;
    success_probability: number;
    performance_gain: number;
    estimated_seconds: number;
    side_effects: string[];
    success: boolean;
  }>;
  winner: {
    fix_id: string;
    name: string;
    risk_level: string;
    success_probability: number;
    performance_gain: number;
    estimated_seconds: number;
    side_effects: string[];
    success: boolean;
  } | null;
  confidence: {
    score: number;
    decision: {
      action: string;
      label: string;
      color: string;
      message: string;
    };
  };
  steps: Array<{
    id: number;
    step: string;
    detail: string;
    status: string;
  }>;
  report: {
    title: string;
    summary: string;
    downtime_prevented: string;
  };
}

export interface IncidentFormInput {
  appName: string;
  issueType: string;
  cpu: number | string;
  memory: number | string;
  latency: number | string;
  issueDescription: string;
  severity: string;
  environment: string;
  errorLogs: string;
  codeSnippet: string;
}

export interface IncidentSubmissionResult {
  input: {
    appName: string;
    issueDescription: string;
    severity: string;
    environment: string;
    errorLogs: string;
    codeSnippet: string;
    metrics: {
      cpu: number;
      memory: number;
      latency: number;
    };
  };
  analysis: AIResult;
  report: {
    title: string;
    summary: string;
  };
  remediationCode: string;
}

export interface SummaryResponse {
  system: SystemMetrics;
  twins: Twin[];
  prediction: string;
  logs: LogEntry[];
  reports: Report[];
  deployments: Deployment[];
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  getSummary: () => request<SummaryResponse>("/api/summary"),
  getTwins: () => request<Twin[]>("/api/twins"),
  createTwin: (name?: string) =>
    request<{ twin: Twin; message: string }>("/api/twins", {
      method: "POST",
      body: JSON.stringify(name ? { name } : {}),
    }),
  analyzeAI: () => request<AIResult>("/api/ai/analyze"),
  getLatestAI: () => request<AIResult>("/api/ai/latest"),
  injectFailure: (kind: "cpu" | "memory" | "crash") =>
    request<{ message: string }>("/api/failure/" + kind, { method: "POST" }),
  deployFix: () => request<{ message: string }>("/api/deploy", { method: "POST" }),
  rollback: () => request<{ message: string }>("/api/rollback", { method: "POST" }),
  getReports: () => request<Report[]>("/api/reports"),
  getLogs: () => request<LogEntry[]>("/api/logs"),
  getDeployments: () => request<Deployment[]>("/api/deployments"),
  getSettings: () => request<Array<{ label: string; value: string; description: string }>>("/api/settings"),
  submitIncident: (payload: IncidentFormInput) =>
    request<IncidentSubmissionResult>("/api/code-analysis/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export function formatRelativeDate(value: string) {
  const deltaMinutes = Math.max(0, Math.round((Date.now() - new Date(value).getTime()) / 60000));
  if (deltaMinutes < 1) return "just now";
  if (deltaMinutes < 60) return `${deltaMinutes} min ago`;

  const hours = Math.round(deltaMinutes / 60);
  if (hours < 24) return `${hours} hr ago`;

  const days = Math.round(hours / 24);
  return `${days} day ago`;
}

export function formatUptime(seconds: number) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${hours}h ${minutes}m`;
}
