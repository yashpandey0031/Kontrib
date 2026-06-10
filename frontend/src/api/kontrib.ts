import axios from "axios";
import type { AnalysisResponse, BattleResponse } from "../types";

const BASE_URL = "http://localhost:8000";

export const analyzeRepo = async (
  username: string,
  userRepo: string,
  benchmarkRepo: string,
): Promise<AnalysisResponse> => {
  const response = await axios.post(`${BASE_URL}/api/analyze`, {
    username,
    user_repo: userRepo,
    benchmark_repo: benchmarkRepo,
  });
  return response.data;
};

export const battleRepos = async (
  p1Username: string,
  p1Repo: string,
  p2Username: string,
  p2Repo: string,
  benchmarkRepo: string,
): Promise<BattleResponse> => {
  const response = await axios.post(`${BASE_URL}/api/battle`, {
    player1_username: p1Username,
    player1_repo: p1Repo,
    player2_username: p2Username,
    player2_repo: p2Repo,
    benchmark_repo: benchmarkRepo,
  });
  return response.data;
};
