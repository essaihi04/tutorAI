// Construction à part du lien libre du Tronc Commun (https://moalim.online/TCF/).
// Usage : npx vite build --config vite.tcf.config.ts --outDir <dossier>  (voir scripts/publier_tcf.py)
// En local : npx vite --config vite.tcf.config.ts --port 5173  puis http://localhost:5173/TCF/tcf.html?cours=<id>
// (les cours, les simulations et l'avatar lisent /media/… à la racine : servi en local par medias_a_la_racine)
import fs from 'node:fs'
import path from 'node:path'
import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const TYPES: Record<string, string> = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.glb': 'model/gltf-binary', '.gltf': 'model/gltf+json', '.bin': 'application/octet-stream',
  '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.ogg': 'audio/ogg', '.mp4': 'video/mp4', '.webm': 'video/webm',
  '.pdf': 'application/pdf', '.txt': 'text/plain; charset=utf-8', '.woff2': 'font/woff2', '.woff': 'font/woff',
}

// En local seulement : sert public/media à /media (en plus de /TCF/media), et renvoie /tcf.html vers /TCF/tcf.html.
// La construction n'en dépend pas : scripts/publier_tcf.py copie les médias lui-même.
function medias_a_la_racine(): Plugin {
  return {
    name: 'tcf-medias-a-la-racine',
    apply: 'serve',
    configureServer(server) {
      const racine = path.resolve(server.config.root, 'public', 'media')
      server.middlewares.use((req, res, next) => {
        const url = new URL(req.url || '/', 'http://x')
        if (url.pathname === '/tcf.html') {
          res.statusCode = 302
          res.setHeader('Location', '/TCF/tcf.html' + url.search)
          return res.end()
        }
        if (!url.pathname.startsWith('/media/') || (req.method !== 'GET' && req.method !== 'HEAD')) return next()
        let fichier: string
        try { fichier = path.join(racine, decodeURIComponent(url.pathname.slice('/media/'.length))) } catch { return next() }
        if (!fichier.startsWith(racine + path.sep)) return next()
        if (fs.existsSync(fichier) && fs.statSync(fichier).isDirectory()) fichier = path.join(fichier, 'index.html')
        if (!fs.existsSync(fichier) || !fs.statSync(fichier).isFile()) return next()
        const taille = fs.statSync(fichier).size
        res.setHeader('Content-Type', TYPES[path.extname(fichier).toLowerCase()] || 'application/octet-stream')
        res.setHeader('Accept-Ranges', 'bytes')
        res.setHeader('Cache-Control', 'no-cache')
        let debut = 0, fin = taille - 1
        const plage = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '')
        if (plage && taille > 0) {
          if (plage[1]) { debut = Number(plage[1]); if (plage[2]) fin = Math.min(Number(plage[2]), taille - 1) }
          else if (plage[2]) debut = Math.max(0, taille - Number(plage[2]))
          if (debut > fin) { res.statusCode = 416; res.setHeader('Content-Range', `bytes */${taille}`); return res.end() }
          res.statusCode = 206
          res.setHeader('Content-Range', `bytes ${debut}-${fin}/${taille}`)
        }
        res.setHeader('Content-Length', String(fin - debut + 1))
        if (req.method === 'HEAD' || taille === 0) return res.end()
        fs.createReadStream(fichier, { start: debut, end: fin }).pipe(res)
      })
    },
  }
}

export default defineConfig(({ command }) => ({
  base: '/TCF/',
  plugins: [react(), tailwindcss(), medias_a_la_racine()],
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
