import axios from "axios";
import type { AnalysisResponse } from "../types";

const BASE_URL = "http://localhost:8000";

export const analyzeRepo = async (
  username: string,
  userRepo: string,
  benchmarkRepo: string,
): Promise<AnalysisResponse> => {
  const response = await axios.post(`${BASE_URL}/analyze`, {
    username,
    user_repo: userRepo,
    benchmark_repo: benchmarkRepo,
  });
  return response.data;
};
