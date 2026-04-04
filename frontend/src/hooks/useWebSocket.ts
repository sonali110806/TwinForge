import { useState, useEffect, useCallback, useRef } from "react";

interface SystemMetrics {
  cpu: number;
  memory: number;
  latency: number;
  status: "healthy" | "critical" | "warning";
}

interface WebSocketMessage {
  type: "metrics" | "alert" | "status";
  payload: Partial<SystemMetrics>;
  timestamp: string;
}

type ConnectionStatus = "connecting" | "connected" | "disconnected" | "reconnecting";

interface UseWebSocketOptions {
  enabled?: boolean;
  interval?: number;
  baseMetrics?: SystemMetrics;
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const { enabled = true, interval = 2000, baseMetrics } = options;
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>("disconnected");
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics>(
    baseMetrics ?? { cpu: 45, memory: 62, latency: 120, status: "healthy" }
  );
  const intervalRef = useRef<ReturnType<typeof setInterval>>();
  const reconnectRef = useRef<ReturnType<typeof setTimeout>>();

  const generateFluctuation = useCallback((base: number, range: number) => {
    return Math.max(0, Math.min(100, base + (Math.random() - 0.5) * range));
  }, []);

  const connect = useCallback(() => {
    setConnectionStatus("connecting");
    
    // Simulate connection handshake
    setTimeout(() => {
      setConnectionStatus("connected");
      
      intervalRef.current = setInterval(() => {
        const newMetrics: SystemMetrics = {
          cpu: Math.round(generateFluctuation(metrics.cpu, 8)),
          memory: Math.round(generateFluctuation(metrics.memory, 4)),
          latency: Math.round(generateFluctuation(metrics.latency > 200 ? metrics.latency : 120, 30)),
          status: metrics.status,
        };
        
        // Auto-detect warning/critical from metrics
        if (newMetrics.cpu > 85 || newMetrics.latency > 400) {
          newMetrics.status = "critical";
        } else if (newMetrics.cpu > 70 || newMetrics.latency > 250) {
          newMetrics.status = "warning";
        }
        
        const msg: WebSocketMessage = {
          type: "metrics",
          payload: newMetrics,
          timestamp: new Date().toISOString(),
        };
        
        setMetrics(newMetrics);
        setLastMessage(msg);
      }, interval);
    }, 500);
  }, [interval, generateFluctuation, metrics.cpu, metrics.memory, metrics.latency, metrics.status]);

  const disconnect = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    if (reconnectRef.current) clearTimeout(reconnectRef.current);
    setConnectionStatus("disconnected");
  }, []);

  const updateBaseMetrics = useCallback((newBase: SystemMetrics) => {
    setMetrics(newBase);
  }, []);

  useEffect(() => {
    if (enabled) {
      connect();
    }
    return () => {
      disconnect();
    };
  }, [enabled]);

  // Reconnect on disconnect
  useEffect(() => {
    if (connectionStatus === "disconnected" && enabled) {
      reconnectRef.current = setTimeout(() => {
        setConnectionStatus("reconnecting");
        setTimeout(() => connect(), 1000);
      }, 3000);
    }
    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
    };
  }, [connectionStatus, enabled]);

  return {
    connectionStatus,
    metrics,
    lastMessage,
    connect,
    disconnect,
    updateBaseMetrics,
  };
}
