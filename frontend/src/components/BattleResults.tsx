import type { BattleResponse } from "../types";
import LLMFeedback from "./LLMFeedback";

interface Props {
  data: BattleResponse | null;
  loading: boolean;
  error: string | null;
}

const metricLabels: Record<string, string> = {
  total_commits: "Total Commits",
  avg_message_length: "Avg Message Length",
  conventional_commit_rate: "Conventional Commits",
  multiline_rate: "Multiline Rate",
};

export default function BattleResults({ data, loading, error }: Props) {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-32 gap-3">
        <div
          className="w-6 h-6 rounded-full border-2 animate-spin"
          style={{ borderColor: "#22c55e", borderTopColor: "transparent" }}
        />
        <p className="text-sm text-neutral-400">
          Fetching data and scoring both players...
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
      <div className="flex items-center justify-center h-32">
        <p className="text-neutral-500 text-sm">
          Battle results will appear here
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Winner banner */}
      <div
        className="p-4 rounded-lg text-center"
        style={{ backgroundColor: "#0f2a1a", border: "1px solid #22c55e" }}
      >
        <p className="text-xs text-neutral-400 mb-1">Winner</p>
        <p className="text-2xl font-bold" style={{ color: "#22c55e" }}>
          {data.winner}
        </p>
      </div>

      {/* Score cards with breakdown */}
      <div className="grid grid-cols-2 gap-4">
        {[data.player1, data.player2].map((player) => (
          <div
            key={player.username}
            className="p-4 rounded-lg flex flex-col gap-3"
            style={{
              backgroundColor: "#1f1f1f",
              border: `1px solid ${player.username === data.winner ? "#22c55e" : "#2e2e2e"}`,
            }}
          >
            <div>
              <p className="text-xs text-neutral-400">{player.username}</p>
              <p className="text-xs text-neutral-500">{player.repo}</p>
            </div>
            <p
              className="text-4xl font-bold"
              style={{
                color: player.username === data.winner ? "#22c55e" : "#ffffff",
              }}
            >
              {player.score}
              <span className="text-sm text-neutral-500 ml-1">/ 100</span>
            </p>

            {/* Breakdown */}
            <div
              className="flex flex-col gap-2 pt-3"
              style={{ borderTop: "1px solid #2e2e2e" }}
            >
              {Object.entries(player.breakdown).map(([key, item]) => (
                <div key={key} className="flex items-center justify-between">
                  <span className="text-xs text-neutral-500">
                    {metricLabels[key] || key}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-neutral-400">
                      {item.your_value} / {item.benchmark_value}
                    </span>
                    <span
                      className="text-xs font-medium"
                      style={{
                        color:
                          item.score >= 80
                            ? "#22c55e"
                            : item.score >= 50
                              ? "#f59e0b"
                              : "#ef4444",
                      }}
                    >
                      {item.score}pts
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Feedback */}
      <div className="flex flex-col gap-4">
        {[data.player1, data.player2].map((player) => (
          <LLMFeedback
            key={player.username}
            result={player.feedback}
            benchmarkContributor={`top contributors of ${data.benchmark_repo}`}
          />
        ))}
      </div>
    </div>
  );
}
