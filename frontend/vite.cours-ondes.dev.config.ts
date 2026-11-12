// Aperçu local du lien libre AVEC les médias (simulations, voix) : publicDir réactivé, et /media/... servi comme
// sur le site (où nginx le sert à la racine), malgré la base /cours-ondes/ (12 novembre 2026).
// Usage : npx vite --config vite.cours-ondes.dev.config.ts --port 5174  (.claude/launch.json « cours-ondes »)
import { defineConfig, mergeConfig } from 'vite'
import base from './vite.cours-ondes.config'

export default mergeConfig(base, defineConfig({
  publicDir: 'public',
  plugins: [{
    name: 'media-a-la-racine',
    configureServer(server) {
      server.middlewares.use((req, _res, next) => {
        if (req.url?.startsWith('/media/')) req.url = '/cours-ondes' + req.url;
        next();
      });
    },
  }],
}))
