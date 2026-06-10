export interface MetricDetail {
  your_value: number;
  benchmark_value: number;
  gap: number;
  rating: "good" | "needs improvement" | "below benchmark";
}

export interface Analysis {
  total_commits: MetricDetail;
  avg_message_length: MetricDetail;
  conventional_commit_rate: MetricDetail;
  multiline_rate: MetricDetail;
}

export interface AnalysisResponse {
  user: string;
  user_repo: string;
  benchmark_repo: string;
  benchmark_contributor: string;
  analysis: Analysis;
  result: string;
}

export interface BreakdownItem {
  your_value: number;
  benchmark_value: number;
  score: number;
}

export interface PlayerResult {
  username: string;
  repo: string;
  score: number;
  breakdown: Record<string, BreakdownItem>;
  metrics: Record<string, number>;
  feedback: string;
}

export interface BattleResponse {
  winner: string;
  loser: string;
  benchmark_repo: string;
  player1: PlayerResult;
  player2: PlayerResult;
  composite_benchmark: Record<string, number>;
}
