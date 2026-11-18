# Mitochondrie

**Coupe longitudinale peinte** : membrane externe corail, espace intermembranaire orangé, membrane interne en crêtes dorées, matrice bleu lumineux granuleuse. Au moins ~90 px de long à l'écran.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| coupe (défaut) | ellipse à crêtes alternées | externe [240,100,62], espace [255,176,110], crêtes [255,222,150], matrice [86,180,236] | « mitochondrie » à la craie orange | animations | `Lexique.mitochondrie(ctx, cx, cy, rx, ry, { cretes, angle, graine })` |
| membrane interne de près | double couche de phospholipides | doré [250,204,96] | « membrane interne » | chaîne respiratoire | `Lexique.membrane(ctx, x, y, w, h)` |
| sphère pédonculée | pied + tête dorée | [252,196,70] | « sphère pédonculée (ATP synthase) » | phosphorylation | `Lexique.spherePedonculee(ctx, x, yM, ep, tete)` |

## Où il apparaît

SVT ch1 : carrefour, comparer, fermentations, glycolyse, mitochondrie, chaine, exao, vesicules, krebs.

## Pourquoi ce choix

Unique dessin du site.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
