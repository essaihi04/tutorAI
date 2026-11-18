# Dioxyde de carbone CO₂

**O = C = O : une bille jaune (le carbone, il vient du glucose) entre deux billes rouges (oxygènes)**, liaison peinte ; dans un liquide, dans sa bulle de gaz.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| billes (défaut) | O–C–O en ligne | C jaune [250,204,21], O rouge [235,85,70] | « CO₂ » à la craie blanche | animations | `Lexique.co2(ctx, x, y, { echelle, alpha, bulle })` (l'ancienne signature `co2(ctx, x, y, k, a)` est acceptée) |
| brute | CO₂ | craie | — | équations | `craie.texte('CO_{2}')` |

## Où il apparaît

SVT ch1 : pyruvate, krebs (compteur et sortie), comparer, fermentations (bulles). Chimie : écrit seulement.

## Pourquoi ce choix

Le carbone garde sa couleur : le ¹⁴C du glucose marqué se retrouve dans le CO₂ (même bille jaune).

## Dessins remplacés (inventaire du 18 novembre 2026)

- `peinture.js` (co2) et `krebs.html` (picto) : carbone GRIS [150,160,175] → jaune ;
- `comparer.html` : déjà jaune, oxygènes [214,64,58] → rouge du lexique.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
