interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  highlight?: boolean;
}

export function GlassCard({ children, className = "", highlight = false }: GlassCardProps) {
  return (
    <div className={`rounded-xl border border-tf-glass-border bg-tf-glass/30 backdrop-blur-sm p-4 transition-all duration-500 ${
      highlight ? "border-tf-red/50 bg-tf-red/5" : ""
    } ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ title, accent }: { title: string; accent: string }) {
  const accentColors: Record<string, string> = {
    cyan: "bg-tf-cyan",
    purple: "bg-tf-purple",
    green: "bg-tf-green",
    red: "bg-tf-red",
    orange: "bg-tf-orange",
    zinc: "bg-muted-foreground",
  };

  return (
    <h3 className="text-sm font-semibold text-muted-foreground flex items-center gap-2">
      <span className={`w-1.5 h-1.5 rounded-full ${accentColors[accent] || "bg-muted-foreground"}`} />
      {title}
    </h3>
  );
}

export function MetricBar({ label, value, suffix }: { label: string; value: number; suffix?: string }) {
  const getColor = (v: number) => {
    if (v >= 80) return "from-tf-red to-tf-pink";
    if (v >= 60) return "from-tf-yellow to-tf-orange";
    return "from-tf-green to-emerald-400";
  };

  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-muted-foreground">{label}</span>
        <span className="text-foreground/70 tabular-nums">{suffix || `${value}%`}</span>
      </div>
      <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full bg-gradient-to-r transition-all duration-700 ease-out ${getColor(value)}`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

interface ControlButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  color: "cyan" | "red" | "purple" | "green" | "zinc";
  icon: string;
}

export function ControlButton({ children, onClick, color, icon }: ControlButtonProps) {
  const colorStyles = {
    cyan: "bg-tf-cyan/10 text-tf-cyan border-tf-cyan/30 hover:bg-tf-cyan/20 hover:border-tf-cyan/50",
    red: "bg-tf-red/10 text-tf-red border-tf-red/30 hover:bg-tf-red/20 hover:border-tf-red/50",
    purple: "bg-tf-purple/10 text-tf-purple border-tf-purple/30 hover:bg-tf-purple/20 hover:border-tf-purple/50",
    green: "bg-tf-green/10 text-tf-green border-tf-green/30 hover:bg-tf-green/20 hover:border-tf-green/50",
    zinc: "bg-muted/50 text-foreground/70 border-muted-foreground/30 hover:bg-muted hover:border-muted-foreground/50",
  };

  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-sm font-medium transition-all duration-200 active:scale-[0.98] ${colorStyles[color]}`}
    >
      <span className="text-base opacity-70">{icon}</span>
      {children}
    </button>
  );
}
