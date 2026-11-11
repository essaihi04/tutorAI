# Ce que demandent les examens nationaux sur les ondes mécaniques (PC BIOF, 2016-2025)

Source : `backend/data/exams/physique/*/exam.json`. 10 exercices touchent aux ondes mécaniques, de 2 à 3,5 points chacun : 2017 N, 2018 N, 2019 N, 2020 N, 2020 R, 2021 R, 2022 N, 2022 R, 2024 N, 2024 R. Pas d'exercice d'ondes mécaniques en 2016, 2023 et 2025 (ces années-là, les ondes sont lumineuses ou absentes).

## Ce qui tombe, du plus fréquent au moins fréquent

| Type de question | Fréquence | Années | Ce que l'élève doit faire |
|---|---|---|---|
| **QCM / vrai-faux de définitions** | 6 sur 10 | 2018, 2020 N, 2020 R, 2021 R, 2022 N, 2024 R | Le son est longitudinal ; il ne se propage pas dans le vide ; l'ultrason se propage seulement dans un milieu matériel ; la célérité dépend du milieu ; une onde ne transporte pas la matière (« une onde longitudinale transporte la matière » est faux) ; la lumière n'est pas une onde mécanique ; il faut définir une onde transversale ou longitudinale |
| **Retard lu sur un oscillogramme** (sensibilité horizontale × nombre de divisions) | 5 | 2018 (2 ms/div), 2020 R, 2021 R, 2022 N, 2024 R (0,5 ms/div) | Choisir deux points homologues, compter les divisions, convertir en s |
| **Célérité v = d/Δt** depuis une distance et une durée | 6 | 2019, 2020 N, 2021 R, 2022 N, 2024 N, 2024 R | Souvent à partir du **rayon du front d'onde** à deux instants (2024 N : v = Δr/Δt, puis t₁ = r₁/v) |
| **Relation y_M(t) = y_S(t − τ)** sous forme de QCM | 2 | 2017, 2020 N | Reconnaître la bonne relation parmi quatre |
| **Instant d'une photographie** à partir de la position du front | 2 | 2017, 2024 N | t = distance parcourue par le front / v |
| **Montrer une expression du retard** entre deux milieux | 1 | 2018 | τ = L·(1/V_air − 1/V_p), puis en déduire V_p |
| **Montrer une expression du retard** avec un émetteur placé entre deux micros | 1 | 2024 R | τ = (d − 2ℓ)/v, puis en déduire ℓ |
| **Pente d'une droite** Δt = f(d) | 1 | 2021 R (barre métallique, coup de marteau) | Pente = 1/v ; identifier le métal dans un tableau de célérités |
| **Écho et échographie** (aller-retour) | 1 | 2020 R (épaisseur du fœtus, v = 1540 m/s) | Distance = v·t/2 ; épaisseur à partir de deux échos |
| **Homogénéité d'une formule** par les équations aux dimensions | 1 | 2024 N (v = √(g·h)) | Vérifier que [√(g·h)] = L·T⁻¹ |

Dans les exercices du **national**, la plupart des questions mélangent ce chapitre avec le suivant (λ, N, diffraction, milieu dispersif). Le premier chapitre doit donc préparer à ce mélange, sans traiter le suivant.

## Ce qui ne tombe PAS au national (2016-2025)

- **Superposition de deux ondes** : jamais. De plus, `perimetre.json` la classe **hors programme** (« interférences, battements, superposition de deux ondes »). Or le deck actuel lui consacre 4 diapos. **C'est une contradiction à trancher.**
- **Séisme, ondes P et S** : jamais au national sur cette période. C'est un contexte possible, mais pas prioritaire.
- **Dessiner l'aspect d'une corde ou le sens du mouvement des points** : pas au national sur cette période. Les profs l'enseignent beaucoup (devoirs, contrôles continus). C'est utile, mais moins prioritaire que l'oscillogramme.
- **v = √(T/μ)** n'est pas demandée en tant que telle. En revanche, **vérifier l'homogénéité** d'une formule de célérité donnée par l'énoncé est demandé (2024 N). Le périmètre dit d'ailleurs « l'expression de la célérité … est fournie par l'énoncé ».

## Conséquences pour le tuteur et pour le cours

1. **Priorité 1 : les définitions mot pour mot**, travaillées en vrai-faux, car 6 exercices sur 10 commencent ainsi. Les pièges récurrents sont : le son dans le vide, le son « transversal », le « transport de matière », la lumière vue comme une onde mécanique, et la célérité qui dépendrait de l'amplitude.
2. **Priorité 2 : l'oscillogramme.** Sensibilité horizontale, points homologues, conversion des ms en s. Cette notion manque presque entièrement au deck actuel.
3. **Priorité 3 : les géométries de retard.** Deux capteurs ; émetteur entre deux micros (d − 2ℓ) ; deux milieux (1/v₁ − 1/v₂) ; écho (aller-retour) ; front circulaire (rayon). Pour chacune, faire le schéma et écrire « distance parcourue = v × durée » **avant** toute formule.
4. **Priorité 4 : graphes linéaires et homogénéité.** Δt = f(d) donne une droite de pente 1/v. La position du front en fonction du temps a pour pente v. Les équations aux dimensions servent à vérifier une formule de célérité.
5. **Superposition** : la retirer, ou la réduire à une mention « hors bac ». C'est à décider avec l'utilisateur, à cause de `perimetre.json`.
