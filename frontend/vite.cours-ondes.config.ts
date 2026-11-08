// Construction à part de la page publique du cours des ondes (https://moalim.online/cours-ondes/).
// Usage : npx vite build --config vite.cours-ondes.config.ts --outDir <dossier>  (voir scripts/publier_cours_ondes.py)
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: '/cours-ondes/',
  plugins: [react(), tailwindcss()],
  publicDir: false,   // les médias sont copiés un à un par le script de publication
  build: {
    emptyOutDir: true,
    rollupOptions: { input: 'cours-ondes.html' },
  },
})
