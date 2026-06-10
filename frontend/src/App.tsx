import { useState } from "react";
import Navbar from "./components/Navbar";
import AnalysisForm from "./components/AnalysisForm";
import ResultsPanel from "./components/ResultsPanel";
import BattleForm from "./components/BattleForm";
import BattleResults from "./components/BattleResults";
import { analyzeRepo, battleRepos } from "./api/kontrib";
import type { AnalysisResponse, BattleResponse } from "./types";

type Mode = "analyze" | "battle";

export default function App() {
  const [mode, setMode] = useState<Mode>("analyze");

  // analyze state
  const [analyzeData, setAnalyzeData] = useState<AnalysisResponse | null>(null);
  const [analyzeLoading, setAnalyzeLoading] = useState(false);
  const [analyzeError, setAnalyzeError] = useState<string | null>(null);

  // battle state
  const [battleData, setBattleData] = useState<BattleResponse | null>(null);
  const [battleLoading, setBattleLoading] = useState(false);
  const [battleError, setBattleError] = useState<string | null>(null);

  const handleAnalyze = async (
    username: string,
    userRepo: string,
    benchmarkRepo: string,
  ) => {
    setAnalyzeLoading(true);
    setAnalyzeError(null);
    setAnalyzeData(null);
    try {
      const result = await analyzeRepo(username, userRepo, benchmarkRepo);
      setAnalyzeData(result);
    } catch (err: unknown) {
      setAnalyzeError(
        err instanceof Error ? err.message : "Something went wrong.",
      );
    } finally {
      setAnalyzeLoading(false);
    }
  };

  const handleBattle = async (
    p1Username: string,
    p1Repo: string,
    p2Username: string,
    p2Repo: string,
    benchmarkRepo: string,
  ) => {
    setBattleLoading(true);
    setBattleError(null);
    setBattleData(null);
    try {
      const result = await battleRepos(
        p1Username,
        p1Repo,
        p2Username,
        p2Repo,
        benchmarkRepo,
      );
      setBattleData(result);
    } catch (err: unknown) {
      setBattleError(
        err instanceof Error ? err.message : "Something went wrong.",
      );
    } finally {
      setBattleLoading(false);
    }
  };

  const tabStyle = (active: boolean) => ({
    padding: "8px 20px",
    borderRadius: "6px",
    fontSize: "14px",
    fontWeight: "500",
    cursor: "pointer",
    border: "none",
    backgroundColor: active ? "#22c55e" : "transparent",
    color: active ? "#000000" : "#a3a3a3",
    transition: "all 0.15s",
  });

  return (
    <div className="min-h-screen" style={{ backgroundColor: "#171717" }}>
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            How does your commit style compare?
          </h1>
          <p className="text-neutral-400 text-sm">
            Analyze your GitHub contribution patterns against top open source
            contributors.
          </p>
        </div>

        {/* Mode tabs */}
        <div
          className="flex gap-2 mb-8 p-1 w-fit rounded-lg"
          style={{ backgroundColor: "#1f1f1f", border: "1px solid #2e2e2e" }}
        >
          <button
            style={tabStyle(mode === "analyze")}
            onClick={() => setMode("analyze")}
          >
            Analyze
          </button>
          <button
            style={tabStyle(mode === "battle")}
            onClick={() => setMode("battle")}
          >
            1v1 Battle
          </button>
        </div>

        {/* Analyze mode */}
        {mode === "analyze" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <p className="text-xs text-neutral-500 uppercase tracking-widest mb-4">
                Your Details
              </p>
              <AnalysisForm onSubmit={handleAnalyze} loading={analyzeLoading} />
            </div>
            <div>
              <p className="text-xs text-neutral-500 uppercase tracking-widest mb-4">
                Analysis
              </p>
              <ResultsPanel
                data={analyzeData}
                loading={analyzeLoading}
                error={analyzeError}
              />
            </div>
          </div>
        )}

        {/* Battle mode */}
        {mode === "battle" && (
          <div className="flex flex-col gap-8">
            <BattleForm onSubmit={handleBattle} loading={battleLoading} />
            <div>
              <p className="text-xs text-neutral-500 uppercase tracking-widest mb-4">
                Battle Results
              </p>
              <BattleResults
                data={battleData}
                loading={battleLoading}
                error={battleError}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
