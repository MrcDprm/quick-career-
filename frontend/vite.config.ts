// AI Optimized by Skills Agent: Vite config keeps the frontend skeleton minimal and extensible.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// AI Optimized by Skills Agent: React plugin enables the TypeScript application shell.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
