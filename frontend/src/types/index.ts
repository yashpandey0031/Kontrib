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
