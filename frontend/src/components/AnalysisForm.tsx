import { useState } from "react";

interface Props {
  onSubmit: (username: string, userRepo: string, benchmarkRepo: string) => void;
  loading: boolean;
}

export default function AnalysisForm({ onSubmit, loading }: Props) {
  const [username, setUsername] = useState("");
  const [userRepo, setUserRepo] = useState("");
  const [benchmarkRepo, setBenchmarkRepo] = useState("");

  const handleSubmit = () => {
    if (username && userRepo && benchmarkRepo) {
      onSubmit(username, userRepo, benchmarkRepo);
    }
  };

  const inputStyle = {
    backgroundColor: "#1f1f1f",
    border: "1px solid #2e2e2e",
    borderRadius: "8px",
    padding: "10px 14px",
    color: "#ffffff",
    width: "100%",
    outline: "none",
    fontSize: "14px",
  };

  return (
    <div className="flex flex-col gap-4">
      <div>
        <label className="text-xs text-neutral-400 mb-1 block">
          GitHub Username
        </label>
        <input
          style={inputStyle}
          placeholder="e.g. yashpandey0031"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label className="text-xs text-neutral-400 mb-1 block">
          Your Repository
        </label>
        <input
          style={inputStyle}
          placeholder="e.g. yashpandey0031/coral-reefs-nlp"
          value={userRepo}
          onChange={(e) => setUserRepo(e.target.value)}
        />
      </div>
      <div>
        <label className="text-xs text-neutral-400 mb-1 block">
          Benchmark Repository
        </label>
        <input
          style={inputStyle}
          placeholder="e.g. microsoft/vscode"
          value={benchmarkRepo}
          onChange={(e) => setBenchmarkRepo(e.target.value)}
        />
        <p className="text-xs text-neutral-600 mt-1">
          Your commits will be compared against the top contributor of this repo
        </p>
      </div>
      <button
        onClick={handleSubmit}
        disabled={loading || !username || !userRepo || !benchmarkRepo}
        className="w-full py-3 rounded-lg font-medium text-sm transition-all"
        style={{
          backgroundColor: loading ? "#1a3a2a" : "#22c55e",
          color: loading ? "#22c55e" : "#000000",
          cursor: loading ? "not-allowed" : "pointer",
          border: "none",
        }}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
}
