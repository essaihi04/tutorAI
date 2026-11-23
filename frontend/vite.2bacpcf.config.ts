// Construction à part du lien libre des révisions de 2ᵉ Bac PC (https://moalim.online/2bacpcf/).
// Usage : python -I scripts/publier_2bacpcf.py [--sans-envoi]
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: '/2bacpcf/',
  plugins: [react(), tailwindcss()],
  publicDir: false,
  server: { proxy: { '/api': { target: 'https://moalim.online', changeOrigin: true } } },
  build: { emptyOutDir: true, rollupOptions: { input: '2bacpcf.html' } },
})
