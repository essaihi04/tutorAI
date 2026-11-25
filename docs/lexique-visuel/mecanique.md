# Mécanique : les couleurs des vecteurs et des objets

Fixé le 25 novembre 2026 (finitions du cours de Tronc Commun « Le mouvement et le principe d'inertie »,
`physics/tc_mouvement_inertie-tableau/`). Une grandeur de la mécanique garde sa couleur de craie partout (flèche, nom,
valeur, cote) et dans **tous les cours de mécanique** (Tronc Commun, 1ʳᵉ Bac, 2ᵉ Bac). Ce sont les couleurs déjà dites
et montrées dans le cours mouvement (la voix dit « le vecteur v trois en vert »), aucune ne contredit le lexique.

## Les couleurs (`Lexique.physique.MECANIQUE`)

| Objet | Clé | Craie | Dessin |
|---|---|---|---|
| vecteur vitesse v⃗ (v⃗₃, v⃗_G) | `v`, `vitesse` | `vert` | flèche épaisse, un point à l'origine (`mecanique.fleche`) |
| poids P⃗ | `P`, `poids` | `rouge` | appliqué en G, vers le bas |
| réaction R⃗ | `R`, `reaction` | `bleu` | au contact, vers le haut |
| tension T⃗ (fil, câble, corde) | `T`, `tension` | `orange` | au point d'attache |
| force quelconque F⃗ (F⃗₁, F⃗₂ d'un dynamomètre, la main qui pousse) | `F`, `force` | `violet` | — |
| vecteur position OM⃗ (et OG⃗, CA⃗ᵢ, G₁G⃗ de la relation barycentrique) | `OM`, `position` | `rose` | de l'origine au point |
| vecteurs unitaires i⃗, j⃗, k⃗ | `i`, `j`, `k`, `unitaire` | `cyan` | courts, sans point |
| centre d'inertie G (et centre de masse C) | `G`, `centreInertie` | `rose` | point rose cerclé de sombre (`mecanique.G`) |
| points d'un enregistrement M₀, M₁… | `point` | `jaune` | point jaune cerclé de sombre (`mecanique.point`) = `Lexique.maths.ROLES.point` |
| trajectoire | `trajectoire` | `cyan`, pointillé `[9, 6]` (`POINTILLE_TRAJECTOIRE`) | = `Lexique.maths.ROLES.courbe` ; sur une feuille claire : la même teinte en encre foncée `rgba(8,145,178,.9)` |
| repère, axes, graduations, axes de symétrie Δ | `repere`, `axes` | `blanc` / `faible` | — |
| éclateur central A / du bord B (autoporteur) | `eclateurA`, `eclateurB` | `rouge` / `orange` | leurs points : jaunes (A) / orange (B) |

Graphes x(t), v(t) : `Lexique.maths.ROLES` (courbe cyan, points jaunes, triangle de pente et tangente orange, signe
+ vert / − rouge pour v_x).

## Les dessins (`Lexique.physique.mecanique`)

| Objet | Appel |
|---|---|
| point d'enregistrement | `point(ctx, x, y, r = 4.5, { alpha, halo })` |
| centre d'inertie | `G(ctx, x, y, r = 5)` |
| étincelle d'éclateur | `etincelle(ctx, x, y, r = 10, alpha)` |
| table à coussin d'air (dessus) | `table(ctx, x, y, w, h, { feuille: true \| {x,y,w,h} })` |
| autoporteur vu de dessus | `autoporteur(ctx, x, y, r, { b, angle, alpha })` |
| autoporteur vu de côté (renvoie G) | `autoporteurCote(ctx, x, yb, w, h, { alpha })` |
| règle graduée (cm) | `regle(ctx, x, y, n, pxParCm, { h, alpha })` |
| chronomètre | `chrono(ctx, x, y, r, texte, { alpha })` |
| vecteur à la craie, couleur de sa grandeur | `fleche(craie, x1, y1, x2, y2, { quoi: 'v' \| 'P' \| 'R' \| 'T' \| 'F' \| 'OM' \| 'i'…, largeur, tete, point })` |

## L'écriture (`Lexique.physique.ECRITURE`)

Le code de la craie de [craie.md](craie.md), en code : `titre`, `motCle`, `relation` → jaune ; `legende`, `donnee` →
blanc ; `resultat`, `conclusion` → vert ; `piege` → rose. Une valeur lue sur l'enregistrement (MᵢMᵢ₊₁ = 2 cm) est une
donnée (blanc) ; le calcul qui en sort (v₃ = 1 m/s) est un résultat (vert) ; la relation générale (vᵢ = Mᵢ₋₁Mᵢ₊₁/2τ)
est jaune.

## Où il apparaît

Le mouvement et le principe d'inertie (14 pages, `commun.js` lit `MECANIQUE`, `ROLES`, `ECRITURE` dans `Mvt.COUL`).

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
