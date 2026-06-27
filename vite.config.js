import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: "/2026-2-VeritasIA/",
  resolve: {
    alias: {
      // Isso ajuda o Vite a encontrar seus arquivos dentro da pasta Frontend
      '@': '/Frontend/src',
    },
  },

})

