import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  root: './', // Agora a raiz é a raiz do repositório
  base: "/2026-2-VeritasIA/",
  plugins: [react()],
  // ... resto da configuração
})
