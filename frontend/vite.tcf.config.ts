// Construction à part du lien libre du Tronc Commun (https://moalim.online/TCF/).
// Usage : npx vite build --config vite.tcf.config.ts --outDir <dossier>  (voir scripts/publier_tcf.py)
// En local : npx vite --config vite.tcf.config.ts  puis /TCF/tcf.html
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ command }) => ({
  base: '/TCF/',
  plugins: [react(), tailwindcss()],
  // en local, les médias viennent de public/ ; à la construction, le script de publication les copie un à un
  publicDir: command === 'serve' ? 'public' : false,
  // en local : la route du Tronc Commun peut aller vers un serveur de test (TC_API), le reste vers le site
  server: { proxy: {
    '/api/v1/public/tcf': { target: process.env.TC_API || 'https://moalim.online', changeOrigin: true },
    '/api': { target: 'https://moalim.online', changeOrigin: true },
  } },
  build: {
    emptyOutDir: true,
    rollupOptions: { input: 'tcf.html' },
  },
}))
