import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Chemins relatifs pour les assets buildés : filet de sécurité si le
  // build est un jour ouvert autrement que servi par FastAPI (voir
  // desktop/main.py, qui sert normalement frontend/dist en HTTP local).
  base: './',
  server: { port: 5173, strictPort: true },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.ts',
  },
})
