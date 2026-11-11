# Audit : vidéos YouTube de profs marocains sur « Les ondes mécaniques progressives » (2ᵉ Bac PC/SM BIOF)

*Recherche du 2026-11-06. Uniquement des profs marocains (consigne utilisateur), 10 profs différents.*

## Méthode et limites (à lire d'abord)

- **Recherche** : WebSearch ne remonte pas YouTube (seulement des PDF Moutamadris, Talamidi, 9rayti). Toute la recherche s'est donc faite dans le navigateur intégré, sur la page de résultats YouTube (FR et AR), sans connexion.
- **Métadonnées** (titre, chaîne, durée, vues, date, description, chapitres) : lues dans `ytInitialPlayerResponse` de chaque page vidéo. **Vérifiées.** Les vues datent du 06/11/2026 ; la date est la `publishDate` YouTube.
- **Contenu** : relevé à partir de la **transcription automatique arabe** (ASR YouTube) quand elle existait, ce qui couvre 7 vidéos sur 10. J'ai indexé des mots-clés (FR, AR et darija translittérée) avec leurs horodatages et échantillonné le texte toutes les 1 à 8 minutes. J'ai aussi fait **2 à 3 captures d'image par vidéo** pour vérifier le support : tableau, slides ou papier.
  - L'ASR du darija mêlé de français est **bruitée**. Un mot-clé absent ne prouve pas que la notion manque, il veut seulement dire « non repéré ». Ce qui suit est donc une analyse par sondage, pas un visionnage intégral.
  - Les vidéos de Noureddine (mZbGQcaLhxk), Hassan El Omrani et Amine Laaouani n'ont **pas de sous-titres**. Pour elles, l'analyse repose sur le titre, la description et des captures d'écran.
  - La piste « fr » de la vidéo de Maria est une transcription quasi inexploitable (darija transcrit comme du français). Seuls des fragments ont servi.
- **Non vérifié** : commentaires épinglés (la section commentaires ne se charge pas sans interaction), nombre de likes (sauf exception), et reels Instagram ou TikTok. La recherche web n'a renvoyé aucun TikTok ou reel public sur ce chapitre, et je n'ai pas ouvert ces plateformes, faute de pouvoir les lire sans connexion. Ils sont donc **ignorés**, conformément à la consigne.
- Je n'ai pas vérifié formellement que la chaîne « TOP PHYSIQUE CHIMIE » est marocaine. Mais l'ASR montre un cours **en darija** (« الثانية بكالوريا مسار دولي ») qui suit le programme marocain : elle est retenue.

Légende de couverture : ✅ vu ou entendu (horodatage) · ◐ partiel ou indirect · ✗ non repéré · ? non vérifiable (pas de transcription).

---

## Tableau de synthèse

| # | Prof / chaîne | Vidéo | Durée | Vues | Date | Support |
|---|---|---|---|---|---|---|
| 1 | Noureddine Physique (Pr. Noureddine) | [mZbGQcaLhxk](https://www.youtube.com/watch?v=mZbGQcaLhxk) | 38 min | 1,03 M | 2021-05-06 | Tableau vert, craie |
| 1b | idem, live « tous les cas » | [GW-FyuY-rpA](https://www.youtube.com/watch?v=GW-FyuY-rpA) | 1 h 52 | 452 k | 2024-10-30 | Tableau vert, en classe |
| 2 | TOP PHYSIQUE CHIMIE | [YCzE0EZvsC8](https://www.youtube.com/watch?v=YCzE0EZvsC8) | 25 min | 1,60 M | 2024-08-16 | Slides animées, voix off |
| 3 | Zakaria Taousse | [27FyalYEXhg](https://www.youtube.com/watch?v=27FyalYEXhg) | 58 min | 21 k | 2026-09-23 | Tableau blanc |
| 4 | Driss DOTCOM | [00vbZrDiky0](https://www.youtube.com/watch?v=00vbZrDiky0) | 41 min | 118 k | 2026-09-17 | Tableau blanc, feutres |
| 5 | Hassan El Omrani | [8LCiTX1ZdX8](https://www.youtube.com/watch?v=8LCiTX1ZdX8) | 1 h 25 | 169 k | 2020-12-24 | 2 tableaux blancs |
| 6 | Comprendre la physique – Maria | [RrCM2o1dgC4](https://www.youtube.com/watch?v=RrCM2o1dgC4) | 22 min | 376 k | 2021-07-13 | Fiche manuscrite filmée |
| 7 | AdrarPhysic | [XLQdN4C9L5g](https://www.youtube.com/watch?v=XLQdN4C9L5g) | 32 min | 9,7 k | 2024-09-27 | Slides annotées au stylet |
| 8 | Amine Laaouani | [P-afb8EcG6I](https://www.youtube.com/watch?v=P-afb8EcG6I) | 24 min | 39 k | 2020-10-17 | Tableau blanc |
| 9 | Marwane Chargui | [lyiJmLP67Dk](https://www.youtube.com/watch?v=lyiJmLP67Dk) | 1 h 40 | 6,3 k | 2023-09-21 | Feuille filmée du dessus |
| 10 | Prof Laksabi | [W9XwPFD0sMU](https://www.youtube.com/watch?v=W9XwPFD0sMU) | 3 h 58 | 119 k | 2026-09-29 | Tableau vert, craie |

**Séances d'exercices populaires** (repérées, contenu non analysé en détail) :
- Noureddine, « Exercice + Correction » : [2bsT3QaB6lc](https://www.youtube.com/watch?v=2bsT3QaB6lc), 19 min, 467 k vues, 2022-10-19.
- TOP PHYSIQUE CHIMIE, « Exercices : série 1 » : [vG-rfo1TLAA](https://www.youtube.com/watch?v=vG-rfo1TLAA), 40 min, 368 k vues, 2025-09-22, 4 exercices corrigés d'après la description.
- AdrarPhysic, version arabe « سلسلة تمارين رقم 1 » : [1IipzI23nJ0](https://www.youtube.com/watch?v=1IipzI23nJ0), 26 min, 261 k vues.

**Autres vidéos repérées, non retenues comme principales** :
- Zakaria Taousse, ancienne version en arabe [XnMABlPLbsQ](https://www.youtube.com/watch?v=XnMABlPLbsQ) (29 min, **1,51 M** vues, 2018, sans sous-titres).
- AdrarPhysic, version en arabe [YA-QdIE3U0A](https://www.youtube.com/watch?v=YA-QdIE3U0A) (33 min, 348 k vues, 2020).
- bacfacile (Pr. Abderrahmane Ben Fateh), [iCQNAgZZors](https://www.youtube.com/watch?v=iCQNAgZZors) (21 min, 609 k vues, 2015).
- Prof Ridouan, [SttTIsKjH9M](https://www.youtube.com/watch?v=SttTIsKjH9M) (31 min, 165 k vues, 2023).
- Noureddine, « Révision intensive » [_pxp3llf9xg](https://www.youtube.com/watch?v=_pxp3llf9xg) (43 min, 636 k vues, 2020).
- Noureddine, « Représenter aspect & élongation » [uJAsjnQLHTU](https://www.youtube.com/watch?v=uJAsjnQLHTU) (16 min, 32 k vues, 2026-10-10).

### Matrice de couverture des notions essentielles

| Notion | Nour. | TOP | Taous. | Driss | Omrani | Maria | Adrar | Laaou. | Charg. | Laks. |
|---|---|---|---|---|---|---|---|---|---|---|
| Définition onde / perturbation / source / milieu | ✅ | ✅ | ✅ | ✅ | ✅ (plan) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Énergie sans transport de matière | ✅ | ✅ | ✅ | ✅ | ? | ✅ | ✅ | ? | ✅ | ✅ |
| Transversale / longitudinale | ✅ | ✅ | ✅ | ✅ | ✅ (plan) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ondes 1D / 2D / 3D | ? | ✅ | ✅ | ✅ | ? | ✅ | ✅ | ? | ✅ | ✅ |
| Son = onde longitudinale, milieu nécessaire (vide) | ? | ◐ | ✅ | ✅ | ✅ (plan) | ✅ | ✅ | ? | ✅ | ✅ |
| Superposition de deux ondes | ? | ◐ | ✗ | ✗ | ? | ✗ | ✅ | ? | ✗ | ✗ |
| Célérité v = d/Δt | ✅ | ✅ | ✅ | ✅ | ✅ (plan) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Facteurs : tension, μ, v = √(T/μ) | ✅ | ✅ | ✅ | ✗ | ? | ✗ | ◐ | ? | ✅ | ✅ |
| Inertie / rigidité / température / nature du milieu | ? | ✗ | ◐ | ◐ | ? | ◐ | ◐ | ? | ✅ | ✅ |
| Retard τ = SM/v et y_M(t) = y_S(t−τ) | ✅ | ✅ | ✅ | ✅ | ✅ (plan) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Deux capteurs / oscillogramme | ✅ | ✅ | ✅ | ✅ | ? | ? | ✗ | ? | ✅ | ✅ |
| Aspect à un instant vs élongation d'un point | ✅ | ✅ | ✅ | ✅ | ? | ✅ | ✅ | ? | ✅ | ✅ |
| Ultrasons (sonar, échographie) | ✅ | ✗ | ✅ | ✅ | ? | ◐ | ◐ | ? | ✅ | ✅ |
| Exercices type bac | ✅ | ✅ | ✅ | ✅ | ? | ✅ | ✅ | ? | ✅ | ✅ |

---

## Fiches détaillées

### 1. Pr. Noureddine (Noureddine Physique)

**1a. « Les Ondes Mécaniques Progressives : Cours + Astuces »** : https://www.youtube.com/watch?v=mZbGQcaLhxk
- 38 min · 1 031 888 vues · 2021-05-06 · pas de sous-titres, pas de chapitres. La description ne contient que des liens (Telegram, Facebook, Instagram, WhatsApp).
- **Ce qui est vérifié par capture d'écran** :
  - À 5:00, au tableau : « Les ondes mécaniques – Définition : c'est le phénomène de propagation d'une perturbation dans un milieu matériel élastique avec transport d'énergie et sans transport de matière ». Juste à côté : « Types d'onde : onde transversale … onde longitudinale ».
  - À 21:00 : partie « Influence de la corde ». Au tableau, la formule v = √(T/μ) (T tension, μ masse linéique) et une vérification de l'**homogénéité** par analyse dimensionnelle.
- **Plan suivi** : définition, puis types, puis célérité et facteurs (corde), puis la suite (retard, aspect et élongation), annoncée par le titre « Astuces » mais **non vérifiée** faute de transcription.
- **Présentation** : tableau vert à la craie, écriture structurée en colonnes, le prof écrit dos à la caméra. Pas de manip réelle repérée.
- **Points forts** : la vidéo de cours la plus vue du chapitre avec TOP (plus de 1 M de vues). Définition de référence écrite mot pour mot. Il traite v = √(T/μ) **et** l'homogénéité, qui sont des compléments utiles pour PC/SM.
- **Points faibles** : pas de sous-titres. Pas de chapitres, donc navigation difficile. Contenu au-delà de 21 min non vérifié.

**1b. « Ondes mécaniques : Cours complet (tous les cas), Astuces, Bonus »** : https://www.youtube.com/watch?v=GW-FyuY-rpA
- 1 h 52 · 452 420 vues · 2024-10-30. **Chapitres dans la description** (vérifiés) :
  - 00:00 les ondes mécaniques progressives
  - 05:45 retard temporel (cas de la corde)
  - 10:50 retard temporel en utilisant l'oscilloscope
  - 20:06 détermination de la vitesse d'une onde ultrasonore dans un milieu
  - 34:37 détermination des distances par les ultrasons
  - 46:58 propagation d'une perturbation sur une corde
  - 01:04:25 ondes mécaniques **périodiques**
  - 01:22:33 ultrasons et réception par 2 microphones
  - 01:47:00 diffraction
- **ASR** : aspect (7:39), oscilloscope ou sensibilité horizontale (14:26, 19:16), μ (37:12), tension (59:31), exercices (15:25, 34:42, 64:21).
- **Présentation** : séance **filmée en classe** devant des élèves (questions audibles), tableau vert, schéma d'un tube avec émetteur et deux récepteurs (capture à 21:40).
- **Points forts** : organisé « par cas d'exercice ». C'est la meilleure carte des **situations type bac** : corde, oscilloscope, ultrasons (vitesse, distance, deux micros).
- **Points faibles** : il mélange progressives **et** périodiques, plus la diffraction. Ce n'est pas un premier cours. L'audio de classe est bruité (ASR très pauvre).

### 2. TOP PHYSIQUE CHIMIE : « les ondes mécaniques progressives 2 bac »
- https://www.youtube.com/watch?v=YCzE0EZvsC8 · 25 min · **1 601 475 vues** (la plus vue) · 2024-08-16 · ASR arabe disponible.
- **Description** (plan déclaré) : notion d'onde mécanique, puis types, puis vitesse de propagation, puis aspect, instant, retard, élongation.
- **Plan vérifié (ASR + captures)** :
  - 0:56, perturbation (pierre dans l'eau).
  - 1:52, transport d'énergie sans transport de matière.
  - 2:47, source S et front (« المقدمة »).
  - 3:44–7:47, dimensions 1D/2D/3D.
  - Vers 6:40, capture : « Onde longitudinale : direction de la perturbation parallèle à la direction de propagation », avec un ressort animé et une « onde sonore » (membrane de haut-parleur, compression de l'air).
  - 7:28, croisement de deux perturbations (« تجمعين … تكمل الطريق بلا زيادة ولا نقصان »), ce qui correspond à la **superposition** (◐ : formulation orale, non titrée).
  - 8:03–16:41, célérité v = d/Δt avec lecture sur quadrillage et conversion d'unités.
  - 14:22 et 16:56, mention « examen ».
  - 17:34–19:25, **le retard** τ. Capture vers 19:10 : « Le retard τ est le décalage temporel entre deux instants », avec un oscillogramme à deux salves et une base de temps de 2 ms par division.
  - 21:15, facteurs de la célérité « spécifiques à la corde », puis à 22:00 la masse linéique μ = m/L.
  - 23:57, élongation y_M(t) = y_S(t−τ).
- **Présentation** : slides animées (titres en encadré rouge, texte bleu), **voix off sans visage**, sous-titres arabes incrustés, exemples numériques sur quadrillage.
- **Points forts** : très compact (25 min), progression canonique, animations ressort et son, oscillogramme réel. Il fait le lien entre l'aspect à un instant (quadrillage en cm) et le temps (quadrillage en ms) et prévient de ne pas confondre les deux axes (« هذا راه زمن … ماشي مسافات », 19:25).
- **Points faibles** : pas d'ultrasons ni de cloche à vide repérés. La superposition n'est qu'évoquée. Pas de manip réelle. Pas d'exercice bac complet dans la vidéo : ils sont dans la série séparée vG-rfo1TLAA.

### 3. Zakaria Taousse : « la leçon 01 les ondes – les ondes mécaniques progressives : 2BAC BIOF »
- https://www.youtube.com/watch?v=27FyalYEXhg · 58 min · 21 180 vues · 2026-09-23 (refonte BIOF). Son ancien cours en arabe [XnMABlPLbsQ](https://www.youtube.com/watch?v=XnMABlPLbsQ) a 1,5 M de vues.
- **Plan vérifié**. L'intro à 0:00 annonce le plan : « شنو هي onde mécanique ؟ types ؟ كيفاش نحسبو la vitesse de propagation ؟ le retard temporel ». Ensuite :
  - Au tableau : « I- Les définitions ».
  - 3:54, milieu.
  - 5:51–7:49, surface de l'eau, ondes circulaires et rectilignes.
  - 7:09, dimensions. À 9:46, le **son et les ultrasons sont des ondes 3D**. Au tableau : domaine audible 20 Hz – 20 kHz, infrasons et ultrasons (> 20 000 Hz).
  - 12:54–21:30, transversale (corde, surface de l'eau) puis longitudinale (son, haut-parleur).
  - 23:26, célérité.
  - 31:07–35:10, **corde tendue, tension** (μ à 31:46), avec l'erreur classique « distance parcourue par la perturbation ».
  - « IV- Le retard temporel » (capture à 41:40), avec un oscillogramme et sa sensibilité.
  - 37:08, expérience des **deux microphones** (disque de musique, haut-parleur).
  - 39:05, deux relations du retard, selon que l'énoncé donne des distances ou un oscillogramme.
  - 44:55, émetteur et récepteur.
  - 46:53, propriétés.
  - 48:49, vitesse du son selon le milieu (solide, liquide, gaz).
  - 52:43–57:59, **analyse dimensionnelle** pour vérifier v = √(T/μ).
- **Présentation** : tableau blanc, plan numéroté en chiffres romains, schémas au feutre de couleur, exemples numériques, ton très oral et motivant.
- **Points forts** : progression la plus « manuel scolaire ». Il traite explicitement les ultrasons, le domaine audible et deux méthodes pour le retard. Il signale les erreurs fréquentes des élèves.
- **Points faibles** : superposition non repérée. Vidéo récente, donc peu de vues. Un passage promotionnel autour de 50:46.

### 4. Driss DOTCOM : « Les Ondes Mécaniques Progressives | 2 BAC | Cours complet »
- https://www.youtube.com/watch?v=00vbZrDiky0 · 41 min · 118 362 vues · 2026-09-17 · ASR arabe, très bonne qualité. Version 2025 : [SJxz81bLbSc](https://www.youtube.com/watch?v=SJxz81bLbSc) (30 min, 137 k vues).
- **Plan vérifié** :
  - 0:00, présenté comme « premier cours du 1ᵉʳ contrôle ».
  - 1:22, annonce : cours, applications et examens.
  - 2:44, **expérience du téléphone placé dans une bouteille dont on retire l'air**. C'est la version « maison » de la cloche à vide : le son a besoin d'un milieu matériel.
  - 4:06–5:30, définition : perturbation, milieu matériel, sans transport de matière.
  - 6:52–9:36, transversale (exemple d'une personne sur une corde) puis longitudinale (ressort).
  - 10:58, le son et le ressort sont des ondes longitudinales.
  - 12:20, solides et particules liées.
  - 13:42, 1D/2D/3D.
  - 15:04, v = d/Δt.
  - 16:26, **exercice d'examen national** : vitesse du son dans l'air, avec le piège « onde sonore transversale = faux » (17:48).
  - 19:10, lecture d'un oscillogramme.
  - 21:55, insistance sur les unités.
  - 23:18–26:02, aspect de la corde et mouvement des points.
  - 27:24, retard.
  - 28:46, dessiner l'aspect de la corde à t = 10 ms.
  - 30:09, **élongation** (« dernière partie du cours »).
  - 31:32–35:39, **sonar** (profondeur, aller-retour divisé par 2) avec la sensibilité de l'oscilloscope.
  - 37:02, **échographie du fœtus** (examen national).
  - 39:46, conclusion.
- **Présentation** (captures) : grand tableau blanc en 3 colonnes, feutres rouge, bleu et vert. Schémas de corde, de ressort et de vibreur. Formules encadrées (V = L/Δt).
- **Points forts** : cours **entièrement adossé aux examens nationaux**. Applications ultrasons concrètes (sonar, échographie). Démonstration expérimentale accessible. Discours très clair.
- **Points faibles** : pas de superposition, pas de v = √(T/μ), pas de μ repérés. Seulement une mention de la température (20:01). Long passage publicitaire dans la description.

### 5. Hassan El Omrani : « Ondes mécaniques progressives : cours détaillé »
- https://www.youtube.com/watch?v=8LCiTX1ZdX8 · 1 h 25 · 169 385 vues · 2020-12-24 · **pas de sous-titres**. Description : promotion d'une offre payante (« 40 ans d'expérience »).
- **Plan lu au tableau** (capture, bilingue FR/AR) :
  1. L'onde mécanique / الموجة الميكانيكية
  2. Types des ondes
  3. Les ondes sonores
  4. Vitesse de propagation d'une onde
  5. Retard temporel
  6. Longueur et durée d'un signal (lecture approximative)
- **Présentation** : deux tableaux blancs. À droite, le plan reste affiché en permanence et en deux langues. Dessin d'un ressort (spires) pour l'onde longitudinale (capture à 30:00). Le prof parle face caméra.
- **Points forts** : plan explicite et bilingue, visible tout au long de la vidéo. Rythme lent et détaillé.
- **Points faibles** : contenu réel **non vérifiable** au-delà des captures. Vidéo longue pour 6 parties. Ancienne (2020).

### 6. Maria (Comprendre la physique) : « les ondes mécaniques progressives : 2BAC »
- https://www.youtube.com/watch?v=RrCM2o1dgC4 · 22 min · 375 711 vues · 2021-07-13. Description : « leçon 1 : 2BAC (PC, SM, SVT), شرح جد مبسط ».
- **Vérifié** :
  - Capture à 5:30, fiche « 1. Définition » : « Une onde mécanique progressive est le phénomène de propagation d'une perturbation dans un milieu matériel élastique avec transport d'énergie mais sans transport de matière ». Viennent ensuite le sens de mécanique, progressive et élastique, puis les exemples (corde, ressort, surface de l'eau).
  - Capture à 16:40, « II. Vitesse de propagation » : v = d/Δt avec unités, exemple numérique, puis **retard temporel** τ = t₂ − t₁ avec schéma de la corde en M₁ et M₂.
  - Fragments ASR exploitables : transport d'énergie sans transport de matière (4:01), son et milieu matériel, vide (5:50–6:11), compression et dilatation de l'air (6:44), 1D/2D/3D (7:25–8:46), transversale (8:53), son longitudinal (vers 10:58), retard (vers 14:54), 1 500 m/s dans l'eau (18:36), élongation (20:06), exercices (21:48).
- **Présentation** : **fiche manuscrite** déjà rédigée au feutre de couleur, filmée ; le stylo pointe en lisant. Sous-titres arabes incrustés. Voix off.
- **Points forts** : synthèse très propre, idéale pour la révision, en 22 min. Définitions exactes.
- **Points faibles** : pas d'écriture en direct. Pas de facteurs de la célérité (T, μ) repérés. Superposition non repérée. Exercices réduits.

### 7. AdrarPhysic : « 2BAC BIOF : Cours – Les ondes mécaniques progressives »
- https://www.youtube.com/watch?v=XLQdN4C9L5g · 32 min · 9 710 vues · 2024-09-27 · ASR arabe. La version arabe [YA-QdIE3U0A](https://www.youtube.com/watch?v=YA-QdIE3U0A) a 348 k vues. La description renvoie au cours PDF sur adrarphysic.fr et à deux séries.
- **Plan vérifié** :
  - 0:06, « premier cours du 2ᵉ Bac, parcours international ».
  - 1:10, perturbation (corde, eau).
  - 2:14, milieux solide, liquide et gaz.
  - 3:18, transport d'énergie sans transport de matière.
  - 5:47–7:21, longitudinale et transversale. Capture vers 6:40 : slide « Onde longitudinale … même direction », avec l'exemple d'un ressort comprimé.
  - 8:02, le son nécessite un milieu matériel (vide, 8:50).
  - 11:18, dimensions.
  - **13:29, superposition de deux ondes** (« تراكب موجتين »), avec des hauteurs de 2 m et 1 m.
  - 15:57, célérité. À 17:02, milieu homogène et v constante. À 17:32, inertie (◐).
  - 18:01, retard. Capture à 23:20 : « Le retard temporel : τ = t_M2 − t_M1 = M₁M₂/V » et « y_M(t) = y_S(t−τ) ou y_S(t) = y_M(t+τ) ».
  - 21:17, élongation de S et de M.
  - 24:08, aspect et sens du mouvement des points.
  - 27:37, exercice.
  - 30:06, les deux relations.
- **Présentation** : **slides** au texte français, annotées en arabe au stylet (rouge et bleu), illustrations (ressort, corde), voix off sans visage.
- **Points forts** : **seul cours de l'échantillon où la superposition apparaît clairement**. Formalisme rigoureux (les deux écritures de y_M). Support PDF assorti.
- **Points faibles** : pas de v = √(T/μ) ni de capteurs ou d'oscillogramme repérés. Ultrasons à peine évoqués. Peu de vues pour la version BIOF.

### 8. Amine Laaouani : « leçon 1 physique : les ondes mécaniques progressives BIOF »
- https://www.youtube.com/watch?v=P-afb8EcG6I · 24 min · 38 972 vues · 2020-10-17 · **pas de sous-titres**. Même prof : « أجي تدي الباك » [LSURGdcqXOI](https://www.youtube.com/watch?v=LSURGdcqXOI) (22 min, 123 k vues, 2019), plus plusieurs exercices et lives en 2024.
- **Vérifié par captures** :
  - 3:20, « Les ondes mécaniques progressives – 1) Onde mécanique » : source, perturbation (ressort, surface de l'eau) et milieu, avec un schéma de corde (source S, perturbation, onde).
  - 13:20, « Onde longitudinale » : ressort dessiné en spires, direction de la perturbation et de la propagation.
  - 20:50, v = d/Δt, durée de la perturbation, longueur de la perturbation (« longueur d'onde »), puis « 5) Retard ».
- **Présentation** : tableau blanc en 3 colonnes, feutres de couleur, schémas, le prof parle face caméra.
- **Points forts** : court et visuel. Il traite la **longueur et la durée de la perturbation**, un point souvent oublié.
- **Points faibles** : contenu oral non vérifiable. Probablement sans facteurs de célérité ni ultrasons (non vérifié). Ancien (2020).

### 9. Marwane Chargui : « Onde Mécanique Progressive | Cours complet + Méthodes & Astuces – 2 BAC PC SM SVT »
- https://www.youtube.com/watch?v=lyiJmLP67Dk · 1 h 40 · 6 274 vues · 2023-09-21 · ASR arabe. La description liste : définition, propagation et célérité, retard, relations, méthodes, erreurs fréquentes, applications. La chaîne est très active : version 2027 en plusieurs parties, et « Tous les extraits du national 2008–2025 » [r3VtLA71Fuw](https://www.youtube.com/watch?v=r3VtLA71Fuw), 2 h, 15 k vues.
- **Plan vérifié** :
  - 3:21, perturbation, avec un **dispositif décrit** (coton au bout d'une corde pour éviter la réflexion).
  - 6:46, milieu matériel.
  - 10:10, onde progressive et onde « continue ».
  - 13:36, le son est une onde 3D.
  - 17:05–19:44, transversale (corde, eau) puis longitudinale (son).
  - 22:45–29:13, **aspect** puis **élongation**, avec la méthode « bien distinguer aspect et élongation ».
  - 30:42, y_M(t) = y_S(t−τ) et le signe ±.
  - 34:03, front et queue de l'onde, et quels points montent ou descendent.
  - 36:54, retard.
  - 40:48, célérité.
  - 43:07–50:59, μ et **analyse dimensionnelle** de v = √(F/μ) (« F » noté pour la tension).
  - 54:21, domaine audible et **ultrasons > 20 kHz**.
  - 57:42, **sonar**.
  - 61:06, réflexion sur un obstacle.
  - 64:28, **« la célérité dépend de la nature du milieu »**.
  - 67:51, deux récepteurs R₁, R₂ séparés de L.
  - 77:49–85:21, oscillogrammes et calcul de v.
  - 84:55, « 3ᵉ cas » : mesure d'épaisseur.
  - 91:41–98:41, exercice (« un exercice d'hier de France » ; relation 1/v_A − 1/v_B).
- **Présentation** : **feuille de papier filmée du dessus**, écriture en direct au stylo, titres en arabe (« الموجة الميكانيكية »), schémas (tube, récepteurs). Le prof parle aux élèves (« وليداتي »).
- **Points forts** : couverture **la plus complète** des cas d'exploitation (2 récepteurs, sonar, épaisseur, milieux successifs), en rapport direct avec le national. Il insiste sur les méthodes et les erreurs.
- **Points faibles** : qualité vidéo modeste (papier, cadrage). Superposition non repérée. Très peu de vues. Coupures avec musique (20:31).

### 10. Prof Laksabi : « Les ondes mécaniques progressives (tout est dans les détails) »
- https://www.youtube.com/watch?v=W9XwPFD0sMU · **3 h 58** · 118 746 vues en environ 5 semaines · 2026-09-29 · ASR arabe · description vide.
- **Plan vérifié** :
  - 0:08, intro.
  - 6:06–12:04, accroches concrètes (voiture et mur, bateau sur la vague : le bateau monte et descend sans avancer, donc pas de transport de matière).
  - 18:02, définition (« phénomène de propagation d'une vibration dans un milieu matériel élastique », transport d'énergie).
  - 19:37–23:18, transversale et longitudinale, son, vide (22:42).
  - 24:00, exercice.
  - 25:58, dimensions.
  - 33:25, célérité.
  - 41:56, retard temporel.
  - 44:31–51:31, tension.
  - 53:54, retard entre deux points du milieu.
  - 59:52, règle de trois sur les images.
  - 65:50, M₁ et M₂ (signe ±).
  - 69:23, oscilloscope.
  - 76:29–83:46, μ, kg/m et homogénéité.
  - 89:45, émetteur, récepteur, sensibilité horizontale.
  - 91:13, ultrasons.
  - 101:42–131:34, **variantes** (déplacer le récepteur, rapprocher, éloigner).
  - 119:38, élongation.
  - 143:30, passage de l'air au pétrole (changement de milieu).
  - 155:30, densité du milieu et célérité.
  - 167:30, profondeur (sonar).
  - 179:28–238:26, démonstrations algébriques (τ_MS, relations 1/v_A − 1/v_B, mise au même dénominateur).
- **Présentation** : tableau vert en 4 colonnes, craie de couleur, icônes de haut-parleur et micro, quadrillage d'oscillogramme, v = 340 m/s (captures à 25:00 et 2 h 13).
- **Points forts** : **exhaustif**, avec tous les cas et démonstrations d'exercice. Bonne accroche concrète. Insiste sur le « pourquoi ».
- **Points faibles** : 4 h, donc impraticable comme premier cours. Superposition non repérée. Pas de chapitres. Beaucoup de digressions motivationnelles (vers 197:25).

---

## Constats transversaux

**Progression commune** (presque tous les profs) :
1. Perturbation (exemples : corde, ressort, surface de l'eau, voire bateau ou pierre).
2. Définition : propagation dans un milieu matériel élastique, avec transport d'énergie sans transport de matière.
3. Transversale ou longitudinale, avec le ressort comme exemple type.
4. Le son est longitudinal et a besoin d'un milieu (vide).
5. Ondes 1D, 2D, 3D.
6. Célérité v = d/Δt (lecture sur quadrillage, conversion d'unités).
7. Facteurs de la célérité (corde : T et μ, √(T/μ) avec analyse dimensionnelle).
8. Retard τ = SM/v et y_M(t) = y_S(t−τ).
9. Exploitation : deux capteurs et oscillogramme, aspect et élongation, ultrasons (sonar, échographie), puis exercices du national.

**Notion la moins traitée** : la **superposition de deux ondes**. Seul AdrarPhysic la traite clairement (13:29). TOP l'évoque oralement (7:28). Elle est non repérée ailleurs. Même chose pour la **température** et l'**inertie ou rigidité** comme facteurs de célérité, à peine évoquées. Les profs leur préfèrent « nature du milieu, solide, liquide, gaz » (Chargui 64:28, Laksabi 155:30, Taousse 48:49).

**Manips réelles** : rares. Driss DOTCOM fait le téléphone dans une bouteille vidée. Chargui décrit une corde avec du coton. Tous les autres sont au tableau ou sur slides. Aucun n'utilise de simulation interactive (aucune repérée).

**Deux styles de présentation** :
- **Tableau** (craie ou feutre, écriture en direct) : Noureddine, Taousse, Driss, Omrani, Laaouani, Laksabi, et Chargui sur papier.
- **Support préparé** : slides animées (TOP, AdrarPhysic) ou fiche manuscrite (Maria).

Les vidéos les plus vues (TOP 1,6 M, Taousse en arabe 1,5 M, Noureddine 1 M) durent **25 à 38 min**. Les cours de plus d'1 h 30 servent d'approfondissement « tous les cas ».

**Pièges signalés par les profs** (utiles pour un tuteur) :
- Confondre l'axe des distances (aspect) et l'axe des temps (oscillogramme) : TOP 19:25, Chargui 22:45.
- « L'onde sonore est transversale » est faux : Driss 17:48.
- Mesurer la distance parcourue depuis le front de l'onde, pas depuis un autre point : Taousse 35:10, 41:03.
- Oublier les unités et les conversions (cm vers m, ms vers s) : Driss 21:55, Taousse 25:24.
- Sonar : diviser l'aller-retour par 2 : Driss 34:16.
