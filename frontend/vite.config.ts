import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // Served from tinkeryard.xyz/kontrib, so assets must resolve under that path.
  base: "/kontrib-app/",
  plugins: [react(), tailwindcss()],
});
