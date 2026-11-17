## Ondes mécaniques progressives

Fichier modifié : `backend/data/courses/en_attente/phys_ch1_waves_exemple.json`. Le cours en ligne n'a pas été touché. Le travail part de la copie en attente, et rien de ce qu'elle contenait n'a été perdu. Le cours passe de 22 à 25 diapos et de 7 à 8 blocs.
Scripts : `scratchpad/corr/ch1p/apply.py` (écriture), `scratchpad/corr/ch1p/verif.py` (contrôles). La sauvegarde d'avant est `scratchpad/corr/ch1p/orig.json`.

### Étape 0 : les 14 corrections de l'audit du 15 novembre
| # | Élément | État |
|---|---|---|
| 1 | C3_r2, reponses.0.1 (« 0,12 = 6 × 0,02 ») | reportée |
| 2 | C7_r2, reponses.0.1 (« 1 ÷ 3 ») | reportée |
| 3 | C8_r2, reponses.2.1 (« 3400 m ne vient pas de v·τ ») | reportée |
| 4 | C8_r2, reponses.2.2 (« division par τ ») | reportée |
| 5 | C4_r2, reponses.1.2 (« 1 s = v × SM ») | reportée |
| 6 | C8_r3, reponses.0.juste (sans « fréquence ») | reportée |
| 7 | C8_r3, reponses.1.1 | reportée |
| 8 | C8_r3, reponses.1.2 | reportée |
| 9 | C1_r3, reponses.0.2 (sans « lumière ») | reportée |
| 10 | wx_s2_b1, exercice.reponses.2.1 (« 3,06 = 1,02 × 3 ») | reportée |
| 11 | wx_s2_b1, exercice.reponses.2.2 | reportée |
| 12 | wx_b2_national, reponses.e0.2.2 (« il fallait inverser la pente ») | reportée |
| 13 | `milieux.html`, protocole.texte (sans 331·√…) | sans objet dans le JSON : fichier de simulation partagé, déjà corrigé |
| 14 | `milieux.html`, ce_qui_se_voit (valeurs calculées, 0,67 s) | sans objet dans le JSON : déjà corrigé |

Les réactions 1 à 12 ont été copiées du cours en ligne avec leur piste v14. Le texte est identique à celui de la piste : il n'y a rien à réenregistrer.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : y_M(t) = y_S(t − τ) donnée sans la condition « non amortie » | Nouvelle diapo. La relation y est justifiée (« à la date t, M fait ce que S faisait à t − τ »), avec la condition « onde non amortie » au centre, à la voix et au cahier. Bilan et carte : condition ajoutée. | wx_r1b_elongation (nouvelle), wx_b3_bilan, wx_b4_carte |
| Haute : cas général entre deux points M₁, M₂ | τ = t₂ − t₁ → SM₂/v − SM₁/v → M₁M₂/v, puis y_M₂(t) = y_M₁(t − τ), une ligne au centre par étape | wx_r1b_elongation, bloc wx_s1_b3, bilan |
| Haute : date d'arrêt et état d'un point à une date t | Nouvelle diapo : t_M = t₀ + SM/v, arrêt à t_M + θ, et l'état du point avant, pendant et après. Question du bloc avec sa démonstration (8 lignes) et ses réactions. | wx_r2b_dates (nouvelle) |
| Haute : source démarrant à t₀ | t₀ écrit sur wx_c1 (d = v·(t − t₀)) et enseigné à la voix sur wx_r2b. Exercice de réserve « dater le départ » (t₀ = t₁ − d₁/v), avec sa démonstration et ses réactions. | wx_c1_celerite, wx_r2b_dates (e0) |
| Haute : même distance dans deux milieux | t = d / v écrit pour chaque milieu (acier 0,2 s, eau 0,67 s), au centre et à la voix. Exercice de réserve « rail acier/air » (d ≈ 1000 m), avec sa démonstration et ses réactions. Ligne ajoutée au tableau des mots-codes (voix et pointage ligne:4). | wx_c2_facteurs (e1), wx_b2_national |
| Moyenne : la célérité ne dépend pas de la forme de la perturbation | Centre, voix, puces et cahier | wx_c2b_temperature |
| Moyenne : élasticité et inertie | « tension → élasticité ; masse linéique → inertie » au centre, à la voix et au cahier | wx_c2b_temperature, bloc wx_s1_b2b |
| Moyenne : cloche à vide ; haut-parleur et bougie | Nouvelle diapo avec les deux expériences, l'une après l'autre (centre ligne par ligne). La question du bloc (le son est longitudinal) y a été déplacée depuis wx_i3b. | wx_i3c_son (nouvelle) |
| Moyenne : échelle d'une photo | Puce et cahier : « distance réelle = mesure × échelle » | wx_c1_celerite |
| Moyenne : tracer l'aspect à une date t₃ | Méthode : front à v·(t − t₀), puis L = v·θ derrière lui. Elle figure au centre, à la voix, dans les puces et au cahier. | wx_r2b_dates |
| Moyenne : µs et µs/div | 1 µs = 10⁻⁶ s, au centre, à la voix et au cahier ; S_H en ms/div ou µs/div | wx_p2_milli, wx_m1b_lecture, bloc wx_s2_b1 |
| Moyenne : un ressort peut porter une onde transversale | « Attention » au centre, à la voix et au cahier | wx_i3b_longitudinale |
| Moyenne : micro M₂ déplacé de d' | τ' = (d + d')/v au centre et à la voix. Exercice de réserve (τ' = 3,5 ms), avec sa démonstration et ses réactions. | wx_m1b_lecture (e0) |
| Basse : « dans toutes les directions qui lui sont offertes », milieux uni-, bi- et tridimensionnel | Phrase relue à la voix et écrite au centre et au cahier | wx_i3b_longitudinale |
| Basse : perturbation = modification temporaire d'une propriété du milieu | Puce | wx_i1_corde |
| Basse : isolants phoniques | Puce et cahier | wx_c2_facteurs |
| Oral seulement : milieu élastique, « de proche en proche » | Ajouté au centre (avec un nouveau centre:3 sur une phrase déjà dite), aux puces et au cahier. La piste est gardée. | wx_i2_definition, bloc wx_s1_b1 |
| Oral seulement : justification de L = v·θ ; θ = L/v | « Pendant θ, le front avance de v·θ » ajouté au centre, aux puces et au cahier. La piste est gardée. | wx_r2_duree_longueur |
| Oral seulement : « plus M est loin, plus τ est grand » | Centre et cahier | wx_r1_retard |
| Notation : θ peut s'appeler Δt dans un énoncé ; S_H | Puce sur wx_r2 ; S_H sur wx_m1b et au cahier | wx_r2_duree_longueur, wx_m1b_lecture |

Organisation : le bloc wx_s1_b3 contient maintenant [r1, r1b, r2, r2b]. Sa question est celle de wx_r2b. Un nouveau bloc wx_s1_b3b [l1, l2] a été créé, avec son cahier, sa figure, son « retrouver » et son exercice (C6, avec réactions). Le bloc wx_s2_b1b passe en séance 3, ce qui garde 3 blocs par séance. Les competence_ids et competences[].slide_ids ont été mis à jour (C2, C4, C5).

### Non corrigés et pourquoi
- Les manques chez un seul professeur (comparaison corps/onde, chronophotographie, échographie chiffrée) n'ont pas été corrigés : le cadre ne les exige pas.
- Rien de hors cadre n'a été ajouté (superposition, v = √(F/μ), séismes, fréquence).
- Les simulations `bilan.html` et `carte.html` n'ont pas été modifiées : la fiche dessinée n'affiche pas encore « onde non amortie » ni M₁M₂. Ces deux points ne figurent que dans les puces et le cahier du bilan.
- Diapos sans visuel adapté :
  - wx_r1b réutilise `corde.html?vue=retard`, qui montre S et M. Le cas M₁M₂ n'est donc qu'écrit et dit, sans figure.
  - wx_i3c réutilise la case « son » de `types.html`. La cloche à vide n'a pas de figure.
- La fiche `cadre_reference_2bac_pc.json` ne connaît pas les nouvelles écritures : t_M = t₀ + SM/v, τ = d/v₂ − d/v₁, τ' = (d + d')/v, v·(t − t₀). Il faut les ajouter aux `variantes_admises` avant `controler_cadre.py` (fichier hors de ma zone).
- Défauts déjà présents dans la copie en attente, non touchés :
  - chiffres ou symboles dans 3 paroles de réactions : C4_r2 0.2, C5_r2 0.1 et wx_s2_b1 exercice 0.1 ;
  - exercices de bloc sans réactions préparées : wx_s1_b2, wx_s1_b2b, wx_s2_b1b, wx_s2_b2.
- Le bloc wx_s1_b3b n'a que 2 diapos.

### Démonstrations
Ont été relues : 4 démonstrations existantes, les réactions « 2 » des calculs (rappels C3, C4, C5, C7, C8, C9 et exercices de bloc) et les exemples écrits sur les diapos.
- Démonstrations réécrites : blocs wx_s1_b3 et wx_s2_b1.
- Démonstrations ajoutées : wx_b2_national e0 et son bloc wx_s2_b2, wx_r2b q, wx_r2b e0, wx_c2_facteurs e1, wx_m1b e0.
- Preuves et exemples sur diapo, une ligne par entrée centre :
  - wx_r1 : démonstration de τ = SM/v ;
  - wx_r1b : y_M et M₁M₂ ;
  - wx_r2 : L = v·θ et l'exemple ;
  - wx_p1 : d, Δt, v = 100/5, 20 m/s ;
  - wx_p2 : les conversions ;
  - wx_m1 et wx_m2b : « pendant τ, le son parcourt d / 2d » ;
  - wx_b1 : données, conversion, substitution, résultat, unité.
- Gardées telles quelles : wx_p2_milli q et wx_s2_b1b (déjà complètes). Les réactions « 2 » donnent déjà relation, substitution, résultat et unité ; elles n'ont pas été modifiées, pour garder leurs pistes.

Exemples :
- Bloc wx_s1_b3 : `τ = SM/v → 1,5/5 → 0,3 s` devient `le front parcourt SM pendant τ (corde homogène) → v = SM/τ → τ = SM/v → 1,5/5 → 0,3 s`.
- wx_r1_retard (centre) : `τ = SM/v` posé seul devient `τ = t_M − t_S → pendant τ le front parcourt SM → v = SM/(t_M − t_S) → v = SM/τ → τ = SM/v (unités) → M plus loin, τ plus grand`.
- wx_b2_national e0 : pas de démonstration avant ; maintenant `v = d/Δt (milieu homogène) → Δt = (1/v)·d → pente = 1/v → v = 1/pente → 1/(2,9 × 10⁻³) → v ≈ 345 m/s → cohérent avec le son dans l'air`.

### Voix à enregistrer (id)
- Diapos (`speech_text.mixed`) :
  - pistes retirées : wx_r1_retard, wx_b1_redaction, wx_b2_national ;
  - diapos nouvelles : wx_i3c_son, wx_r1b_elongation, wx_r2b_dates ;
  - diapos déjà sans piste, voix modifiée : wx_i3b_longitudinale, wx_c2_facteurs, wx_c2b_temperature, wx_p2_milli, wx_m1b_lecture.
- Démonstrations (`parole`) : wx_r2b_dates/q, wx_r2b_dates/e0, wx_c2_facteurs/e1, wx_m1b_lecture/e0, wx_b2_national/e0, blocs wx_s1_b3, wx_s2_b1, wx_s2_b2.
- Réactions préparées (juste / 1 / 2) : wx_r2b_dates q et e0, wx_c2_facteurs e1, wx_m1b_lecture e0, bloc wx_s1_b3b exercice.
- Énoncés (`enonce_dit`) : les mêmes, plus wx_s1_b3b retrouver. La question déplacée sur wx_i3c garde son énoncé et ses réactions.

### Vérifications faites
- JSON valide (`json.dumps(ensure_ascii=False, indent=2)`, LF, retour à la ligne final). Le fichier n'avait pas changé depuis la sauvegarde avant l'écriture.
- `verif_attente.py` : 25 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue, 16 diapos sans piste.
- `verif.py` :
  - chaque `mot` des démonstrations est dans sa parole, et dans l'ordre ;
  - chaque `mot` de pointage et de centre est dans `speech_text.mixed` ;
  - les cibles `centre:N` et `ligne:N` existent ;
  - chaque diapo est dans un seul bloc, et les blocs suivent l'ordre du cours ;
  - un seul « À toi » par bloc ;
  - chaque option des nouvelles questions a ses réactions ;
  - les nouvelles voix et paroles ne contiennent ni chiffres ni symboles. Les 7 alertes restantes existaient déjà (voir plus haut).
- Calculs refaits en Python :
  - 100/5 = 20 ; 1000/5000 = 0,2 ; 1000/1500 = 0,667 ;
  - 2,74/(1/340 − 1/5000) = 999,6 ≈ 1000 ; distracteurs 340 × 2,74 = 931,6 et 5000 × 2,74 = 13 700 ;
  - 0,6/2 + 0,1 = 0,4 (distracteurs 0,3 et 0,5) ; 0,5 − 0,6/2 = 0,2 (distracteur 0,8) ;
  - 1,19/340 = 3,5 ms (distracteurs 1,5 et 2,0 ms) ; 0,68/0,002 = 340 ; 1/0,0029 = 344,8 ;
  - 1,5/5 = 0,3 ; 1,02/0,003 = 340 ; 1500 × 0,04/2 = 30.
- Simulations réutilisées : les moments (m_atteint, m_revenu, fin, m_sommet, son) et les repères (point_m, duree_theta, longueur_l, retard_tau, son, son_type) existent dans `corde.html` et `types.html`.
