import { useState } from "react";

const BENCHMARK_REPOS = [
  { value: "microsoft/vscode", label: "VS Code — Microsoft" },
  { value: "facebook/react", label: "React — Meta" },
  { value: "torvalds/linux", label: "Linux Kernel" },
  { value: "django/django", label: "Django — Python" },
  { value: "expressjs/express", label: "Express — Node.js" },
  { value: "golang/go", label: "Go Language" },
];

interface Props {
  onSubmit: (
    p1Username: string,
    p1Repo: string,
    p2Username: string,
    p2Repo: string,
    benchmarkRepo: string,
  ) => void;
  loading: boolean;
}

export default function BattleForm({ onSubmit, loading }: Props) {
  const [p1Username, setP1Username] = useState("");
  const [p1Repo, setP1Repo] = useState("");
  const [p2Username, setP2Username] = useState("");
  const [p2Repo, setP2Repo] = useState("");
  const [benchmarkRepo, setBenchmarkRepo] = useState(BENCHMARK_REPOS[0].value);

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

  const handleSubmit = () => {
    if (p1Username && p1Repo && p2Username && p2Repo) {
      onSubmit(p1Username, p1Repo, p2Username, p2Repo, benchmarkRepo);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-6">
        {/* Player 1 */}
        <div
          className="flex flex-col gap-3 p-4 rounded-lg"
          style={{ backgroundColor: "#1f1f1f", border: "1px solid #2e2e2e" }}
        >
          <p className="text-xs text-neutral-400 uppercase tracking-widest">
            Player 1
          </p>
          <div>
            <label className="text-xs text-neutral-500 mb-1 block">
              Username
            </label>
            <input
              style={inputStyle}
              placeholder="e.g. yashpandey0031"
              value={p1Username}
              onChange={(e) => setP1Username(e.target.value)}
            />
          </div>
          <div>
            <label className="text-xs text-neutral-500 mb-1 block">
              Repository
            </label>
            <input
              style={inputStyle}
              placeholder="e.g. yashpandey0031/coral-reefs-nlp"
              value={p1Repo}
              onChange={(e) => setP1Repo(e.target.value)}
            />
          </div>
        </div>

        {/* Player 2 */}
        <div
          className="flex flex-col gap-3 p-4 rounded-lg"
          style={{ backgroundColor: "#1f1f1f", border: "1px solid #2e2e2e" }}
        >
          <p className="text-xs text-neutral-400 uppercase tracking-widest">
            Player 2
          </p>
          <div>
            <label className="text-xs text-neutral-500 mb-1 block">
              Username
            </label>
            <input
              style={inputStyle}
              placeholder="e.g. jewels86"
              value={p2Username}
              onChange={(e) => setP2Username(e.target.value)}
            />
          </div>
          <div>
            <label className="text-xs text-neutral-500 mb-1 block">
              Repository
            </label>
            <input
              style={inputStyle}
              placeholder="e.g. jewels86/Lazulite"
              value={p2Repo}
              onChange={(e) => setP2Repo(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Benchmark selector */}
      <div>
        <label className="text-xs text-neutral-400 mb-1 block">
          Compare against contributors from
        </label>
        <select
          value={benchmarkRepo}
          onChange={(e) => setBenchmarkRepo(e.target.value)}
          style={{ ...inputStyle, cursor: "pointer" }}
        >
          {BENCHMARK_REPOS.map((r) => (
            <option
              key={r.value}
              value={r.value}
              style={{ backgroundColor: "#1f1f1f" }}
            >
              {r.label}
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading || !p1Username || !p1Repo || !p2Username || !p2Repo}
        className="w-full py-3 rounded-lg font-medium text-sm transition-all"
        style={{
          backgroundColor: loading ? "#1a3a2a" : "#22c55e",
          color: loading ? "#22c55e" : "#000000",
          cursor: loading ? "not-allowed" : "pointer",
          border: "none",
        }}
      >
        {loading ? "Battling..." : "Start Battle"}
      </button>
    </div>
  );
}
