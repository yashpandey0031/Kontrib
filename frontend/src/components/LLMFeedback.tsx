interface Props {
  result: string;
  benchmarkContributor: string;
}

export default function LLMFeedback({ result, benchmarkContributor }: Props) {
  const lines = result.split("\n").filter((l) => l.trim() !== "");

  return (
    <div
      style={{
        backgroundColor: "#1f1f1f",
        border: "1px solid #2e2e2e",
        borderRadius: "8px",
        padding: "20px",
      }}
    >
      <div className="flex items-center gap-2 mb-4">
        <div
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: "#22c55e" }}
        />
        <span className="text-sm text-neutral-400">
          AI Analysis — compared against{" "}
          <span className="text-white font-medium">{benchmarkContributor}</span>
        </span>
      </div>
      <div className="space-y-2">
        {lines.map((line, i) => (
          <p
            key={i}
            className="text-sm leading-relaxed"
            style={{ color: line.startsWith("**") ? "#ffffff" : "#a3a3a3" }}
          >
            {line.replace(/\*\*/g, "")}
          </p>
        ))}
      </div>
    </div>
  );
}
