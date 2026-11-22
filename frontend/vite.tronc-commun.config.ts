// Construction à part du lien libre du Tronc Commun (https://moalim.online/tronc-commun/).
// Usage : npx vite build --config vite.tronc-commun.config.ts --outDir <dossier>  (voir scripts/publier_tronc_commun.py)
// En local : npx vite --config vite.tronc-commun.config.ts  puis /tronc-commun/tronc-commun.html
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ command }) => ({
  base: '/tronc-commun/',
  plugins: [react(), tailwindcss()],
  // en local, les médias viennent de public/ ; à la construction, le script de publication les copie un à un
  publicDir: command === 'serve' ? 'public' : false,
  // en local : la route du Tronc Commun peut aller vers un serveur de test (TC_API), le reste vers le site
  server: { proxy: {
    '/api/v1/public/tronc-commun': { target: process.env.TC_API || 'https://moalim.online', changeOrigin: true },
    '/api': { target: 'https://moalim.online', changeOrigin: true },
  } },
  build: {
    emptyOutDir: true,
    rollupOptions: { input: 'tronc-commun.html' },
  },
}))
