import { useState } from "react";
import Navbar from "./components/Navbar";
import AnalysisForm from "./components/AnalysisForm";
import ResultsPanel from "./components/ResultsPanel";
import { analyzeRepo } from "./api/kontrib";
import type { AnalysisResponse } from "./types";

export default function App() {
  const [data, setData] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (
    username: string,
    userRepo: string,
    benchmarkRepo: string,
  ) => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const result = await analyzeRepo(username, userRepo, benchmarkRepo);
      setData(result);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong. Check your inputs and try again.");
      }
    } finally {
      setLoading(false);
    }
  };

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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <p className="text-xs text-neutral-500 uppercase tracking-widest mb-4">
              Your Details
            </p>
            <AnalysisForm onSubmit={handleAnalyze} loading={loading} />
          </div>
          <div>
            <p className="text-xs text-neutral-500 uppercase tracking-widest mb-4">
              Analysis
            </p>
            <ResultsPanel data={data} loading={loading} error={error} />
          </div>
        </div>
      </div>
    </div>
  );
}
