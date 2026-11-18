# NAD⁺ / NADH,H⁺ (le « taxi »)

Le transporteur d'hydrogène. **Capsule CYAN** : courte « NAD+ » (oxydée, vide), longue et lumineuse « NADH,H+ » (réduite, chargée).

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| capsule (défaut) | capsule peinte, 54 × 24 vide, 82 × 24 chargée + halo | cyan [34,190,220] | « NAD+ » / « NADH,H+ » sombre et gras dedans (#0b1f2a) | partout | `Lexique.nad(ctx, x, y, { etat: 'oxyde' | 'reduit', echelle, alpha })` |

## Où il apparaît

SVT ch1 : glycolyse, taxi, pyruvate, krebs, compteur, fermentations, chaine.

## Pourquoi ce choix

Déjà cohérent dans tout SVT ch1 (même cyan partout).

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
