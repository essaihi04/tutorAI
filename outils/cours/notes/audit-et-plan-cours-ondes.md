# Premier cours de physique 2ᵉ Bac PC BIOF : audit et plan de la nouvelle version

*Session du 2026-11-06. Rien n'a été modifié dans les cours. Ce document attend la validation de l'utilisateur.*

## 0. Le cours concerné

- **Chapitre** : « Ondes mécaniques progressives » (stable_id `phys_ch1_waves`, version 3, publié).
- **Source lue** : `backend/data/courses/phys_ch1_waves_course_v1.json`. Elle est synchronisée vers `course_decks` par `scripts/sync_course_decks.py`. La base de prod n'a pas pu être lue (accès refusé), donc la copie en ligne n'a pas été comparée.
- **Programme officiel** (cadre de référence de l'examen national) : « définitions, célérité, retard temporel ». TP officiel : « Mesure de la célérité d'une onde mécanique ». Le sous-domaine Ondes pèse 11 % de la note, pour 3 chapitres.

### Le deck actuel en bref (9 activités, 31 diapos, environ 195 min)

| # | Activité | Durée | Contenu |
|---|---|---|---|
| 0 | Diagnostic | 15 min | Goutte sur l'eau, impulsion et deux capteurs, situation-problème |
| 1 | Propagation de proche en proche | 25 min | Simulation corde et ressort, énergie sans matière, transversale/longitudinale, définitions |
| 2 | TP son | 25 min | Cloche à vide (simulation), son longitudinal |
| 3 | TP dimensions et superposition | 25 min | Eau 2D, 1D/2D/3D, superposition |
| 4 | Compte rendu | 15 min | Tableau d'observation corde/ressort/son/eau |
| 5 | Retard et célérité | 25 min | v = d/Δt, deux capteurs, τ = tB − tA, calcul guidé |
| 6 | Pourquoi la célérité change | 20 min | Tension, μ, amplitude sans effet, gaz/température |
| 7 | Laboratoire | 25 min | Deux mesures de v, puis τ = SM/v et y_M(t) = y_S(t − τ) |
| 8 | Méthode BAC | 20 min | Décalage de deux signaux, exercice avec deux micros, bilan, auto-évaluation, transition vers les ondes périodiques |

Supports déjà disponibles :
- Simulation `progressive/` avec les variantes cord, spring, water, sound, vacuum, superposition, medium et progressive.
- 14 croquis craie `phys_croquis_*`.
- Images `eau_source.svg` et `cloche.svg`.
- Pas encore de manip 3D : la manip P1 est inscrite dans `labo-2bac/inventaire-manips.md` mais n'est pas codée.

---

## 1. AUDIT des vidéos de profs marocains

10 profs différents, YouTube uniquement : aucun reel Instagram ou TikTok public lisible sur ce chapitre. Le contenu a été vérifié par sondage, pas par visionnage intégral : transcription automatique arabe pour 7 vidéos, 2 à 3 captures par vidéo, chapitres de la description. Fiches détaillées avec horodatages dans `audit-ondes-videos-maroc.md`, dans le même dossier.

### 1.1 Tableau comparatif

| Prof | Lien | Durée / vues | Présentation | Points forts | Points faibles |
|---|---|---|---|---|---|
| **TOP PHYSIQUE CHIMIE** | [YCzE0EZvsC8](https://www.youtube.com/watch?v=YCzE0EZvsC8) | 25 min · 1,6 M | Slides animées, voix off ; animations du ressort et du haut-parleur, oscillogramme réel | Compact, progression canonique ; prévient de ne pas confondre l'axe des distances et l'axe des temps | Pas d'ultrasons ni de cloche à vide ; superposition seulement évoquée ; aucun exercice bac complet |
| **Pr. Noureddine** | [mZbGQcaLhxk](https://www.youtube.com/watch?v=mZbGQcaLhxk) et live [GW-FyuY-rpA](https://www.youtube.com/watch?v=GW-FyuY-rpA) | 38 min · 1 M ; 1 h 52 · 452 k | Tableau vert à la craie, plan en colonnes ; le live est filmé en classe | Définition de référence mot pour mot ; v = √(T/μ) avec homogénéité ; le live est organisé « par cas » d'exercice (corde, oscilloscope, ultrasons, distances) | Pas de sous-titres ni de chapitres sur le cours ; le live mélange progressives, périodiques et diffraction |
| **Zakaria Taousse** | [27FyalYEXhg](https://www.youtube.com/watch?v=27FyalYEXhg) | 58 min · 21 k (ancien cours : 1,5 M) | Tableau blanc, plan en chiffres romains, schémas en couleur | La progression la plus proche du manuel : domaine audible et ultrasons, deux méthodes pour le retard, vitesse selon solide/liquide/gaz, analyse dimensionnelle, erreurs d'élèves | Superposition absente ; un passage promotionnel |
| **Driss DOTCOM** | [00vbZrDiky0](https://www.youtube.com/watch?v=00vbZrDiky0) | 41 min · 118 k | Grand tableau blanc en 3 colonnes ; **manip réelle** du téléphone dans une bouteille vidée | Entièrement adossé aux examens nationaux : piège « son transversal », dessiner l'aspect à t = 10 ms, sonar, échographie ; insiste sur les unités | Pas de T, μ ni √(T/μ) ; pas de superposition ; température juste citée |
| **Hassan El Omrani** | [8LCiTX1ZdX8](https://www.youtube.com/watch?v=8LCiTX1ZdX8) | 1 h 25 · 169 k | Deux tableaux, **plan bilingue FR/AR affiché en permanence** | Hiérarchie très lisible en 6 parties, dont la « longueur et durée d'un signal » | Pas de sous-titres, donc contenu peu vérifiable ; long ; date de 2020 |
| **Maria (Comprendre la physique)** | [RrCM2o1dgC4](https://www.youtube.com/watch?v=RrCM2o1dgC4) | 22 min · 376 k | Fiche manuscrite déjà écrite, filmée | Synthèse propre, définitions exactes, idéale pour réviser | Pas d'écriture en direct ; ni T, μ ni superposition ; peu d'exercices |
| **AdrarPhysic** | [XLQdN4C9L5g](https://www.youtube.com/watch?v=XLQdN4C9L5g) | 32 min · 9,7 k (version AR : 348 k) | Slides annotées au stylet, PDF fourni | **Seul cours avec une vraie superposition** ; formalisme rigoureux (y_M(t) = y_S(t − τ) et y_S(t) = y_M(t + τ)) ; aspect et sens du mouvement des points | Pas de √(T/μ) ; ni capteurs ni oscillogramme ; ultrasons à peine abordés |
| **Amine Laaouani** | [P-afb8EcG6I](https://www.youtube.com/watch?v=P-afb8EcG6I) | 24 min · 39 k | Tableau blanc en 3 colonnes | Court ; traite la **durée et la longueur de la perturbation** | Pas de sous-titres ; facteurs de la célérité et ultrasons non vérifiés |
| **Marwane Chargui** | [lyiJmLP67Dk](https://www.youtube.com/watch?v=lyiJmLP67Dk) | 1 h 40 · 6 k | Feuille filmée du dessus, écriture en direct | La couverture **la plus complète des cas bac** : aspect et élongation, front et queue, points qui montent ou descendent, sonar, 2 récepteurs, épaisseur, milieux successifs (1/v_A − 1/v_B), « nature du milieu » | Image modeste ; pas de superposition ; coupures musicales |
| **Prof Laksabi** | [W9XwPFD0sMU](https://www.youtube.com/watch?v=W9XwPFD0sMU) | 3 h 58 · 119 k | Tableau vert en 4 colonnes, icônes haut-parleur et micro, quadrillage d'oscillogramme | Exhaustif ; bonnes accroches (bateau sur la vague) ; nombreuses variantes et démonstrations | 4 h : impossible comme premier cours ; pas de chapitres ; digressions |

Séances d'exercices populaires :
- Noureddine [2bsT3QaB6lc](https://www.youtube.com/watch?v=2bsT3QaB6lc) (467 k vues).
- TOP série 1 [vG-rfo1TLAA](https://www.youtube.com/watch?v=vG-rfo1TLAA) (368 k).
- AdrarPhysic série 1 [1IipzI23nJ0](https://www.youtube.com/watch?v=1IipzI23nJ0) (261 k).

### 1.2 Progression commune (8 profs sur 10)

1. Perturbation : corde, ressort, eau.
2. Définition : propagation dans un milieu matériel élastique, avec transport d'énergie sans transport de matière.
3. Transversale ou longitudinale.
4. Le son a besoin d'un milieu.
5. Propagation 1D, 2D, 3D.
6. Célérité v = d/Δt.
7. Facteurs de la célérité : T, μ, √(T/μ).
8. Retard τ, puis y_M(t) = y_S(t − τ).
9. Exploitation : deux capteurs, aspect et élongation, ultrasons, examens nationaux.

**Hiérarchie** : seuls Taousse (I, II, III, IV) et El Omrani (plan affiché) rendent la hiérarchie visible. Les autres enchaînent sans plan écrit.

**Présentation** : 7 profs sur 10 écrivent au tableau en direct. Une seule manip réelle (Driss). **Aucune simulation.** Les cours les plus vus durent 25 à 38 min.

### 1.3 Éléments essentiels du programme et ce qui manque à chacun

**Éléments essentiels** (programme officiel complété par les situations des examens nationaux) :

| Code | Élément essentiel |
|---|---|
| E1 | Perturbation, source, milieu matériel élastique ; définition de l'onde mécanique progressive |
| E2 | Transport d'énergie sans transport de matière |
| E3 | Onde transversale ou longitudinale (exemples : corde, ressort, son, ondes sismiques P et S) |
| E4 | Le son est une onde mécanique longitudinale qui a besoin d'un milieu (vide) ; domaine audible, ultrasons |
| E5 | Propagation 1D, 2D, 3D ; propagation dans toutes les directions offertes |
| E6 | Superposition (croisement) de deux ondes |
| E7 | Célérité v = d/Δt ; milieu homogène, donc v constante ; on mesure depuis le front |
| E8 | Facteurs de la célérité : nature du milieu (inertie, rigidité ; solide, liquide, gaz), température ; corde : T et μ, √(T/μ) avec analyse dimensionnelle ; l'amplitude ne joue pas |
| E9 | Retard τ = SM/v (et entre deux points M₁M₂) ; y_M(t) = y_S(t − τ) |
| E10 | Durée θ et longueur L = v·θ de la perturbation ; front et queue |
| E11 | Aspect de la corde à un instant y(x) et élongation d'un point y(t) : lire, dessiner, ne pas confondre les axes ; sens du mouvement des points |
| E12 | Deux capteurs ou deux micros, oscillogramme et sensibilité horizontale (TP officiel) |
| E13 | Ultrasons : sonar, écho, échographie, épaisseur (τ = 2d/v) ; milieux successifs ; séisme (ondes P et S) |
| E14 | Méthode et exercices type examen national |

**Ce qui manque à chaque prof** (✗ non repéré, ◐ partiel) :

| Prof | Manques |
|---|---|
| TOP | E4 ultrasons ✗, E6 ◐, E8 inertie/température ✗, E10 ✗, E13 ✗, E14 ◐ |
| Noureddine (cours de 38 min) | Pas vérifiable après 21 min ; le live couvre E12 et E13 mais déborde sur les ondes périodiques |
| Taousse | E6 ✗, E10 non repéré |
| Driss | E6 ✗, E8 (T, μ) ✗, E10 non repéré |
| El Omrani | E6, E8, E13 non vérifiables ; E10 présent dans le plan |
| Maria | E6 ✗, E8 ✗, E12 ?, E13 ◐, E14 ◐ |
| AdrarPhysic | E8 ◐, E12 ✗, E13 ◐ |
| Laaouani | E8 et E13 non vérifiables |
| Chargui | E6 ✗ ; E5 et E2 brefs |
| Laksabi | E6 ✗ ; trop long pour un premier passage |
| **Moalim (deck actuel)** | **E10 ✗, E11 ✗** (aucune diapo sur l'aspect ni sur le sens du mouvement des points), **E13 ✗** (ni ultrasons, ni sonar, ni séisme ; ondes P et S simplement citées), **E4 ◐** (ni domaine audible ni ultrasons), **E8 ◐** (pas de tableau de vitesses solide/liquide/gaz, pas d'analyse dimensionnelle), **E12 ◐** (ni oscillogramme ni sensibilité horizontale) |

**Conclusion de l'audit** : le deck Moalim est le seul à avoir des simulations et une vraie superposition avec le rendu « craie ». Il couvre bien E1 à E7 et E9. Mais il lui manque **le cœur des exercices du national** : l'aspect et l'élongation (E11), la longueur et la durée de la perturbation (E10), les ultrasons, le sonar et les séismes (E13), l'oscillogramme (E12). Ce sont justement les points que les profs les plus vus et les plus complets (Driss, Chargui, Noureddine en live) traitent en détail. Sa **hiérarchie** est aussi brouillée : TP et compte rendu viennent avant la célérité, et τ = SM/v est rangé dans l'activité « Laboratoire » au lieu de la partie sur le retard. Enfin, il dure 195 min, contre 25 à 40 min pour les cours vidéo de référence.

---

## 2. SYNTHÈSE : plan de la nouvelle version

### Principe

- Reprendre l'ordre de **Taousse et El Omrani** (I, II, III, IV, avec un plan visible au tableau).
- Reprendre la **concision de TOP et Noureddine** pour les notions.
- Reprendre la **carte des cas bac de Chargui, Driss et Noureddine (live)** pour l'exploitation.
- Garder la **superposition d'AdrarPhysic** sous forme de propriété courte.
- Ajouter ce qu'aucun prof n'a : simulations, labo 3D, dessins au tableau qui se construisent en direct.

**Cible** : 6 parties, environ 30 diapos, environ 140 min de travail actif (contre 195). Le plan du cours s'affiche dans un coin du tableau tout au long du cours, comme chez El Omrani.

### Plan détaillé

**Ouverture : situation-problème (2 diapos, 8 min)**
- Diapo « goutte sur l'eau » (gardée), plus la **bouée ou le bateau qui monte et descend sans avancer** (accroche de Laksabi).
- Question : « comment un signal avance-t-il sans transporter la matière ? » (gardée).
- *Supports* :
  - image `eau_source.svg` (gardée) ;
  - dessin au tableau : bouée et vague, avec les flèches du mouvement local et de la propagation.

**Partie I : L'onde mécanique progressive (définitions)** (≈ 9 diapos, 35 min)
- **I.1 Perturbation, source, milieu.** Corde, ressort, eau. Vocabulaire : élongation, milieu élastique.
  - Simulation `cord` (point orange suivi).
  - Dessin au tableau `phys_croquis_propagation_locale`.
- **I.2 Définition** encadrée, mot pour mot : « phénomène de propagation d'une perturbation dans un milieu matériel élastique, avec transport d'énergie, sans transport de matière ». Propagation de proche en proche.
  - Dessin au tableau : la définition s'écrit à la craie et les 3 mots-clés sont soulignés.
- **I.3 Le son est une onde mécanique.**
  - Simulation `vacuum`, plus une photo ou un dessin du téléphone dans une bouteille vidée (manip de Driss).
  - Image : réveil sous une cloche à vide.
- **I.4 Transversale ou longitudinale.** Corde et eau d'un côté ; ressort et son de l'autre ; séismes : ondes S transversales, ondes P longitudinales.
  - Simulations `spring` et `sound`.
  - Dessin au tableau `phys_croquis_transversale_longitudinale`.
  - **Image nouvelle** : sismographe avec arrivées P et S.
  - Piège du national : « le son est transversal » est faux.
- **I.5 Dimensions 1D, 2D, 3D.**
  - Simulation `water`.
  - Dessin au tableau `phys_croquis_dimensions`.
- **I.6 Propriété : superposition.** Les déplacements s'ajoutent, puis chaque onde repart intacte. Deux diapos au lieu de quatre.
  - Simulation `superposition`.
  - Dessin au tableau `phys_croquis_superposition`.
- **Synthèse I** : le tableau corde/ressort/son/eau (milieu, type, dimension), corrigé dans la même diapo. Il remplace l'activité « Compte rendu ».

**Partie II : La célérité** (≈ 5 diapos, 25 min)
- **II.1 Définition et loi.** v = d/Δt (m, s, m·s⁻¹). Milieu homogène, donc v constante. On mesure la distance **depuis le front**.
  - **Courbe à tracer** : position du front x en fonction de t ; c'est une droite dont la pente vaut v.
  - Dessin au tableau `phys_croquis_front_dates` (deux photos de la corde).
- **II.2 Facteurs.**
  - Nature du milieu (inertie, rigidité), avec un **tableau de vitesses** : air ≈ 340 m/s, eau ≈ 1 500 m/s, acier ≈ 5 000 m/s.
  - Température.
  - Corde : v croît avec T et décroît avec μ.
  - L'amplitude n'a pas d'effet.
  - Simulation `medium` (gardée).
  - **Courbe** : v en fonction de √T, pour μ fixé.
  - Dessin au tableau `phys_croquis_corde_poulie`.
- **II.3 Complément : v = √(T/μ) et analyse dimensionnelle** (Noureddine, Taousse, Chargui). Une diapo, avec un exercice de vérification d'unités.

**Partie III : Le retard temporel** (≈ 5 diapos, 25 min)
- **III.1 τ = t_M − t_S = SM/v**, et entre deux points : τ = M₁M₂/v.
  - Dessin au tableau `phys_croquis_retard`.
  - Diapo déplacée : elle était dans l'activité « Laboratoire ».
- **III.2 Relation y_M(t) = y_S(t − τ)**, avec sa forme équivalente y_S(t) = y_M(t + τ) (AdrarPhysic).
  - **Courbes à tracer** : y_S(t) et y_M(t), même forme décalée de τ.
- **III.3 Durée θ et longueur L = v·θ de la perturbation**, front et queue (Laaouani, El Omrani, Chargui). **Nouveau.**
  - Dessin au tableau : impulsion avec front, queue et L annotés.

**Partie IV : Lire et dessiner une onde (méthode)** (≈ 5 diapos, 25 min). **Partie entièrement nouvelle.**
- **IV.1 Aspect de la corde à un instant t (y en fonction de x) et élongation d'un point (y en fonction de t).** Ne pas confondre les axes, distance et temps (TOP, Chargui). L'aspect est l'image miroir de l'élongation.
  - **Nouvelle simulation**, variante `aspect` : deux vues synchronisées, la photo de la corde et la courbe y_M(t) tracée en direct.
  - **Courbes** : les deux graphes côte à côte, avec la flèche de propagation.
- **IV.2 Sens du mouvement des points à un instant.** Quels points montent, descendent ou sont au repos ; points atteints et non atteints.
  - Dessin au tableau : petites flèches à la craie sur l'aspect.
  - Question QCM de type « clic sur un point ».
- **IV.3 Dessiner l'aspect à un instant donné**, à partir de y_S(t) (exercice de Driss : « aspect à t = 10 ms »).
  - Méthode en 3 étapes : position du front x = v·t, longueur L, sens inversé.

**Partie V : Mesurer et appliquer (TP et ultrasons)** (≈ 5 diapos, 25 min)
- **V.1 TP officiel : mesurer la célérité.** Deux capteurs sur une corde, puis deux micros et un oscilloscope. Lecture de la sensibilité horizontale ; deux événements identiques (même nature).
  - **Labo 3D**, nouvelle manip P1 (voir plus bas).
  - Simulation `progressive` (gardée).
  - Dessin au tableau `phys_croquis_signaux_retard` complété d'un **quadrillage d'oscillogramme** (2 ms/div).
- **V.2 Ultrasons.** Domaine audible 20 Hz – 20 kHz, ultrasons au-delà. **Sonar et écho : τ = 2d/v.** Échographie, mesure d'épaisseur. **Nouveau.**
  - Images : bateau et sonar, échographie.
  - Dessin au tableau : émetteur, aller-retour et récepteur.
  - **Nouvelle simulation**, variante `echo` : on déplace l'obstacle et on lit τ.
- **V.3 Séisme et milieux successifs.** Δt = d/v_S − d/v_P, d'où d (distance à l'épicentre) ; traversée de deux milieux, relation 1/v_A − 1/v_B (Chargui, Laksabi).
  - **Courbes** : sismogramme avec arrivées P et S.
  - Dessin au tableau : station et épicentre.

**Partie VI : Méthode bac et bilan** (≈ 4 diapos, 15 min)
- **Pièges des profs** : axes distance et temps, son « transversal », mesurer depuis le front, unités (ms, cm), division par 2 au sonar.
- **Exercice type national complet** : deux micros, aspect et élongation, sonar. Il remplace l'exercice actuel, trop court.
- **Bilan au tableau** (`phys_croquis_bilan_ondes` refait en carte : I, II, III, IV, V) et auto-évaluation (gardée).
- Transition vers les ondes périodiques (gardée).

### Labo 3D (`Desktop/labo-2bac`, skill `labo-virtuel-2bac`)

- **Manip P1a : célérité le long d'une corde.**
  - Montage : corde tendue sur une poulie avec une masse accrochée (T = m·g), deux capteurs optiques A et B sur une règle, un chronomètre ou une interface.
  - Réglages : masse accrochée (T), choix de la corde (μ), distance AB.
  - Objectif chiffré : mesurer τ pour deux distances AB, puis vérifier que v = AB/τ reste constante. Ensuite, montrer que v augmente avec T.
- **Manip P1b : vitesse du son, deux micros et un oscilloscope** (clap ou émetteur).
  - Réglages : distance entre les micros, base de temps.
  - Objectif : lire τ sur l'oscillogramme et trouver v ≈ 340 m/s.
- **Option : cloche à vide.** Pompe à vide et réveil ; le niveau sonore baisse quand on retire l'air. C'est surtout qualitatif (◐), donc à faire seulement si c'est peu coûteux.

### Ce qu'on garde ou change par rapport au deck actuel

| Élément actuel | Décision |
|---|---|
| Situation-problème goutte et corde | **Garder**, raccourcir, ajouter la bouée |
| Simulations cord, spring, sound, vacuum, water, superposition, medium, progressive | **Garder toutes** et les replacer dans le nouveau plan |
| 14 croquis craie | **Garder**, en compléter 2 (bilan en carte, oscillogramme quadrillé) |
| Diagnostic (3 diapos) | Réduire à une seule question de prédiction |
| Activités TP son et TP dimensions et superposition | Fusionner dans la partie I (environ 2 diapos par notion au lieu de 4) |
| Activité « Compte rendu » (2 diapos) | Remplacer par la synthèse en tableau de la fin de la partie I |
| Activité « Retard et célérité » | Scinder : la célérité va en partie II, le retard en partie III |
| « De la source S au point M » (dans l'activité Laboratoire) | **Déplacer** en partie III |
| Activité « Pourquoi la célérité change » | Garder et ajouter le tableau des vitesses par milieu, plus l'analyse dimensionnelle |
| Méthode BAC (deux signaux) | Garder ; ajouter l'oscillogramme quadrillé et un exercice national plus complet |
| Bilan, auto-évaluation, transition | Garder |
| **Absent aujourd'hui** | **Ajouter** : θ et L ; aspect et élongation ; sens du mouvement des points ; dessiner l'aspect ; ultrasons ; sonar et échographie ; séisme ; milieux successifs ; 2 nouvelles variantes de simulation (`aspect`, `echo`) ; 2 manips 3D |
| Voix | Réécrire la parole selon le skill professeur ; puis **réenregistrer les phrases du tableau dans le cache vocal** (`exporter_decks.py`, puis `phrases_cours.cjs`, puis `python -m scripts.kaggle_tts cours`) |

### Ordre de réalisation proposé (après validation)

1. Réécrire le manifeste : structure, textes, questions.
2. Ajouter les 2 variantes de simulation (`aspect`, `echo`) et les nouveaux croquis.
3. Coder les manips 3D P1a et P1b, puis publier le labo (`scripts/publier_labo.py`).
4. Écrire la parole darija/français, synchroniser le deck en brouillon, enregistrer le cache vocal, vérifier, puis publier.

---

## 3. Corrections du plan après vérification du programme (6 novembre 2026)

Vérification faite contre `perimetre.json` (CDR-PC-2015, OP-PC-2007) et les examens nationaux de 2016 à 2025 (voir `examens-nationaux-ondes-mecaniques.md`).

**Retirés du nouveau cours, car hors programme :**
- La **superposition** (I.6) : `perimetre.json` la classe hors programme, et le national ne l'a jamais posée. Les 4 diapos actuelles sont à supprimer. La simulation `superposition` reste dans le labo, mais n'est plus appelée par le cours.
- Le **séisme et les ondes P et S** (V.3 et la mention dans I.4).
- **v = √(T/μ) avec analyse dimensionnelle comme formule à retenir** (II.3). Le programme précise que la formule de célérité est donnée par l'énoncé. On garde seulement « vérifier l'homogénéité d'une formule donnée », comme au national 2024 N (v = √(g·h)).
- **« Inertie, rigidité »** comme mécanisme. On donne seulement le constat (solide > liquide > gaz, dépend de la nature du milieu et de la température), jamais une explication par la « densité ».

**Ajoutés, car au programme et posés au national :**
- La droite Δt = f(d), dont la pente vaut 1/v (2021 R).
- L'émetteur placé entre deux micros, τ = (d − 2ℓ)/v (2024 R).
- Deux milieux, τ = L(1/v_lent − 1/v_rapide) (2018).
- Le rayon du front d'onde (2024 N).
- La rédaction selon le barème : relation, application numérique, résultat, unité.

**Manips et simulations : consignes d'affichage de l'utilisateur (6 novembre 2026) :**
- **Le strict minimum de boutons.** Un bouton principal, plus Recommencer. Les réglages se font sur le dessin, avec des poignées à glisser.
- **Fond transparent**, qui se fond dans le tableau du cours (kit `shared/tableau`, écriture à la craie en direct).
- **Penser à l'affichage de tous les éléments.** Rien de coupé ni de caché, tout lisible dans le cadre, sur ordinateur comme sur téléphone, sans défilement. À vérifier dans le navigateur pour chaque manip.
