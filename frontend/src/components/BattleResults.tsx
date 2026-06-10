import type { BattleResponse } from "../types";
import LLMFeedback from "./LLMFeedback";

interface Props {
  data: BattleResponse | null;
  loading: boolean;
  error: string | null;
}

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

      {/* Score comparison */}
      <div className="grid grid-cols-2 gap-4">
        {[data.player1, data.player2].map((player) => (
          <div
            key={player.username}
            className="p-4 rounded-lg"
            style={{
              backgroundColor: "#1f1f1f",
              border: `1px solid ${player.username === data.winner ? "#22c55e" : "#2e2e2e"}`,
            }}
          >
            <p className="text-xs text-neutral-400 mb-1">{player.username}</p>
            <p className="text-xs text-neutral-500 mb-3">{player.repo}</p>
            <p
              className="text-4xl font-bold"
              style={{
                color: player.username === data.winner ? "#22c55e" : "#ffffff",
              }}
            >
              {player.score}
            </p>
            <p className="text-xs text-neutral-500 mt-1">/ 100</p>
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
