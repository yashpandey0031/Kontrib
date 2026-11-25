import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // Vercel serves this app at the domain root; the existing site uses a subpath.
  base: process.env.VERCEL === "1" ? "/" : "/kontrib-app/",
  plugins: [react(), tailwindcss()],
});
