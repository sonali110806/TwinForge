import { useEffect, useRef, useState } from "react";

type SystemMetrics = {
  cpu: number;
  memory: number;
  latency: number;
  status: "healthy" | "critical" | "warning";
};

type ConnectionStatus = "connecting" | "connected" | "disconnected";

interface UseWebSocketOptions {
  enabled?: boolean;
  interval?: number;
  baseMetrics?: SystemMetrics;
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const { enabled = true, interval = 2000, baseMetrics } = options;
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>("connecting");
  const [metrics, setMetrics] = useState<SystemMetrics>(
    baseMetrics ?? { cpu: 0, memory: 0, latency: 0, status: "healthy" }
  );
  const timerRef = useRef<number>();

  useEffect(() => {
    if (!enabled) {
      setConnectionStatus("disconnected");
      return;
    }

    const load = async () => {
      try {
        const response = await fetch("/api/summary");
        if (!response.ok) {
          throw new Error("Summary request failed");
        }

        const data = await response.json();
        setMetrics(data.system);
        setConnectionStatus("connected");
      } catch {
        setConnectionStatus("disconnected");
      }
    };

    load();
    timerRef.current = window.setInterval(load, interval);
    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
    };
  }, [enabled, interval]);

  return {
    connectionStatus,
    metrics,
    lastMessage: null,
    connect: () => setConnectionStatus("connecting"),
    disconnect: () => setConnectionStatus("disconnected"),
    updateBaseMetrics: (newBase: SystemMetrics) => setMetrics(newBase),
  };
}
