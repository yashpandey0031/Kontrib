export default function Navbar() {
  return (
    <nav
      style={{ backgroundColor: "#171717", borderBottom: "1px solid #2e2e2e" }}
      className="flex items-center justify-between px-6 py-4"
    >
      <div className="flex items-center gap-2">
        <span className="text-xl font-bold text-white">Kontrib</span>
        <span className="text-sm text-neutral-400">
          | Compare your GitHub style
        </span>
      </div>
      <div className="flex items-center gap-4">
        <a
          href="https://github.com/yashpandey0031/kontrib"
          target="_blank"
          className="text-sm text-neutral-400 hover:text-white transition-colors"
        >
          GitHub
        </a>

        <a
          href="https://buymeacoffee.com/yashpandey"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Buy me a coffee"
          title="Buy me a coffee"
          style={{
            width: 36,
            height: 36,
            borderRadius: 9999,
            background: "#ffffff",
            border: "1px solid #2e2e2e",
            boxShadow: "0 6px 16px rgba(0,0,0,0.35)",
            animation: "coffeeJump 1.7s ease-in-out infinite",
          }}
          className="coffee-jump flex flex-none items-center justify-center"
        >
          <img
            src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg"
            alt=""
            style={{ width: 20, height: 20 }}
          />
        </a>
      </div>

      <style>{`
        @keyframes coffeeJump {
          0%, 100% { transform: translateY(0); }
          35% { transform: translateY(-4px); }
          60% { transform: translateY(0); }
        }
        .coffee-jump:hover { animation-play-state: paused; }
      `}</style>
    </nav>
  );
}
