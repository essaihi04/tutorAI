# Générateur (pile, alimentation, GBF)

**Coffret gris peint, afficheur vert, bornes rouge (+) et noire (−)** ; le GBF : coffret bleu ardoise à petit écran de signal.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| réaliste (défaut) | coffret gris #5b6670→#262c32, afficheur #0d1a10 / texte #7dfc8a | gris, vert | la tension affichée (« 6V ») sur l'afficheur | montages, TP | `Lexique.physique.generateur(ctx, x, y, w, h, '6V', a)` ; bornes : `borne(ctx, x, y, rouge)` |
| GBF | coffret #4f6a86, signal triangulaire vert | bleu ardoise | « GBF » à la craie | ondes, RL en triangle | `gbf(ctx, x, y, w, h)` |
| symbole | cercle + flèche / deux traits (craie) | blanc | E | schéma normalisé, cahier | craie (`c.ligne`) |

## Où il apparaît

RC (circuit-rc, condensateur, generateur-courant, intensite, rappels, tau-rc), RL (bobine, circuit-rl, lampes, triangle, observer), RLC (circuit-lc, entretien, equation).

## Pourquoi ce choix

11 pages avaient déjà ce coffret gris ; les autres (bleu acier de lampes.html, ardoise, à bornes intégrées) le prennent ; observer et tau-rc gardent leurs bornes dessinées par le lexique.

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
