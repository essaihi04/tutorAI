# Bobine

**Réaliste : enroulement de cuivre couché entre deux joues crème, fils de sortie ; noyau de fer doux gris.** **Symbole : 4 boucles (craie blanche).**

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| réaliste | cylindre cuivre #4a2207/#ffbe7a/#d9802f, joues #e8dfc4 | cuivre | « (L, r) » à la craie | montages | `Lexique.physique.bobine(ctx, x, y, w, h)` ; `noyau(ctx, …)` |
| symbole couché / debout | 4 créneaux arrondis | blanc | L, r | schéma, cahier | `symboleBobine(c, x1, y, x2)`, `symboleBobineV(c, x, y1, y2)` |

## Où il apparaît

RL, RLC.

## Pourquoi ce choix

7 pages avaient ce dessin. Restent à brancher : spires empilées d'observer (RL, RLC), `bobinePeinte`/`peindreBobine` (carte, figures, energie, rupture — 5 palettes de cuivre).

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
