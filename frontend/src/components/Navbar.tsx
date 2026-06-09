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
      <a
        href="https://github.com/yashpandey0031/kontrib"
        target="_blank"
        className="text-sm text-neutral-400 hover:text-white transition-colors"
      >
        GitHub
      </a>
    </nav>
  );
}
