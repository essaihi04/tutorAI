// Aperçu local du lien libre SANS rechargement automatique (14 novembre 2026) : d'autres sessions écrivent les cours
// JSON en continu, et Vite rechargeait la page à chaque écriture, au milieu d'un essai. Même chose que
// vite.cours-ondes.dev.config.ts, mais sans HMR ni surveillance des fichiers : on recharge soi-même.
// Usage : npx vite --config vite.cours-ondes.sanshmr.config.ts --port 5176  (.claude/launch.json « cours-ondes-sans-hmr »)
import { defineConfig, mergeConfig } from 'vite'
import dev from './vite.cours-ondes.dev.config'

export default mergeConfig(dev, defineConfig({
  server: { hmr: false, watch: null },
}))
