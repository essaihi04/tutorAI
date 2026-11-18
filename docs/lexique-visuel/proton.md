# Proton / ion H⁺

Un ion H⁺ EST un proton : **bille ROSE marquée « H+ »** (dans un noyau atomique : marquée « p » ou sans texte). Le pompage des H⁺ se dessine avec des flèches roses.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| bille (défaut) | bille r 7 | rose [244,114,182] | « H+ » sombre dedans ; « p » dans un noyau | partout | `Lexique.proton(ctx, x, y, { r, echelle, alpha, texte, nom })` |

## Où il apparaît

SVT ch1 : chaine, exao, vesicules. Chimie : `Rendu.EL.Hp` (JAUNE), PROTON des pages acides-bases (jaune), prérequis (ROUGE). Physique nucléaire : rouge #d9534f / rouge-orangé #f2683a.

## Pourquoi ce choix

Il avait trois couleurs : rouge (= l'oxygène), jaune (= le carbone), rouge-orangé. Le rose n'est pris par aucun atome ; c'est déjà la craie « rose ».

## Partout (décision du 18 novembre 2026)

SVT (H⁺ de la chaîne respiratoire), chimie (H⁺, H acide des modèles, H₃O⁺, flèches de transfert du proton en craie rose), physique (proton du noyau : radioactivité, énergie nucléaire). Les voix de chimie ch11 et de physique ch5 sont réécrites (« boule rose », « sphères roses »).

## Dessins remplacés (inventaire du 18 novembre 2026)

- `chaine.html`, `exao.html`, `vesicules.html` : rouge [225,62,62] / [240,80,80] → rose ; flèches de pompage et textes « H+ » rouges → roses ;
- chimie : H⁺ jaune → rose (`Rendu.EL.Hp`, PROTON des pages, ATOME.P), H₃O⁺ orange/jaune → rose, carbone gris → jaune ;
- physique nucléaire : proton rouge #d9534f / rouge-orangé #f2683a → rose ; étiquettes « proton » roses.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
