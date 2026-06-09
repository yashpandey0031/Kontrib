import type { AnalysisResponse } from "../types";
import MetricsCard from "./MetricsCard";
import LLMFeedback from "./LLMFeedback";

interface Props {
  data: AnalysisResponse | null;
  loading: boolean;
  error: string | null;
}

const metricLabels: Record<string, string> = {
  total_commits: "Total Commits",
  avg_message_length: "Avg Message Length",
  conventional_commit_rate: "Conventional Commits",
  multiline_rate: "Multiline Rate",
};

export default function ResultsPanel({ data, loading, error }: Props) {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-3">
        <div
          className="w-6 h-6 rounded-full border-2 border-t-transparent animate-spin"
          style={{ borderColor: "#22c55e", borderTopColor: "transparent" }}
        />
        <p className="text-sm text-neutral-400">
          Fetching GitHub data and analyzing...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="p-4 rounded-lg text-sm"
        style={{
          backgroundColor: "#2a1f1f",
          border: "1px solid #3a2020",
          color: "#ef4444",
        }}
      >
        {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-2">
        <p className="text-neutral-500 text-sm">
          Enter your details and click Analyze
        </p>
        <p className="text-neutral-600 text-xs">Results will appear here</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      <div>
        <p className="text-xs text-neutral-500 mb-1">Analyzing</p>
        <p className="text-white font-medium">{data.user_repo}</p>
        <p className="text-xs text-neutral-500 mt-1">
          vs top contributor{" "}
          <span className="text-neutral-300">{data.benchmark_contributor}</span>{" "}
          from {data.benchmark_repo}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {Object.entries(data.analysis).map(([key, metric]) => (
          <MetricsCard
            key={key}
            label={metricLabels[key] || key}
            metric={metric}
          />
        ))}
      </div>

      <LLMFeedback
        result={data.result}
        benchmarkContributor={data.benchmark_contributor}
      />
    </div>
  );
}
