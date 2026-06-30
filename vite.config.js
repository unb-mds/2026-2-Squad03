import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: "/2026-2-VeritasIA/",
  root: './', // O Vite olha para a pasta raiz
  build: {
    rollupOptions: {
      input: '/index.html' // Aponta explicitamente para o arquivo na raiz
    }
  },
  resolve: {
    alias: {
      // Isso permite que você importe arquivos da pasta Frontend/src usando '@'
      '@': '/Frontend/src',
    },
  },
})