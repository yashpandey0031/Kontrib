import type { MetricDetail } from "../types";

interface Props {
  label: string;
  metric: MetricDetail;
}

const ratingColor: Record<string, string> = {
  good: "#22c55e",
  "needs improvement": "#f59e0b",
  "below benchmark": "#ef4444",
};

const ratingLabel: Record<string, string> = {
  good: "Good",
  "needs improvement": "Needs Work",
  "below benchmark": "Below Benchmark",
};

export default function MetricsCard({ label, metric }: Props) {
  const color = ratingColor[metric.rating] || "#a3a3a3";

  return (
    <div
      style={{
        backgroundColor: "#1f1f1f",
        border: "1px solid #2e2e2e",
        borderRadius: "8px",
        padding: "16px",
      }}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-neutral-400">{label}</span>
        <span
          className="text-xs px-2 py-1 rounded-full font-medium"
          style={{ backgroundColor: `${color}20`, color }}
        >
          {ratingLabel[metric.rating]}
        </span>
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold text-white">{metric.your_value}</p>
          <p className="text-xs text-neutral-500 mt-1">your value</p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-neutral-400">
            {metric.benchmark_value}
          </p>
          <p className="text-xs text-neutral-500 mt-1">benchmark</p>
        </div>
      </div>
      <div
        className="mt-3 pt-3"
        style={{ borderTop: "1px solid #2e2e2e" }}
      >
        <p className="text-xs text-neutral-500">
          Gap:{" "}
          <span style={{ color }}>{metric.gap > 0 ? `+${metric.gap}` : metric.gap}</span>
        </p>
      </div>
    </div>
  );
}