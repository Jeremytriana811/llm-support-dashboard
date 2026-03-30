import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Proxy API calls to the backend during development
    // This means fetch("/tickets") in React will go to http://localhost:8000/tickets
    proxy: {
      "/tickets": "http://localhost:8000",
      "/metrics": "http://localhost:8000",
    },
  },
});
