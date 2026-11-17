## Fonction logarithme népérien

Copie en attente : `backend/data/courses/en_attente/math_ch5_fonctions_ln.json` (partie du cours en ligne, aucune copie en attente avant). 65 → 69 diapos. Le cours en ligne n'a pas été touché.

### Manques corrigés

| Constat | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Limite de ln(u(x)) par composition + phrase « asymptote verticale » (haute, confirmé) | Nouvelle diapo : règle (u → 0⁺ ⇒ ln u → −∞ ; u → +∞ ⇒ +∞), exemple ln(x + 1) en −1⁺, phrase « la droite d'équation x = −1 est asymptote verticale à (C_f) », limite en +∞ ; deux explications (directe, puis X = x + 1). Visuel réutilisé : `limites.html?vue=plonge` | **ln_l9** (nouvelle, bloc ln_s4_b1, K5) |
| Étude complète d'une fonction ln(u) (haute, confirmé) | f(x) = ln((x + 2)/(1 − x)) : domaine par tableau de signe, limites aux bornes par composition, deux asymptotes verticales ; puis f′ = u′/u = 3/((1 − x)(x + 2)) > 0, tableau de variations ; figures du cahier (courbe + tableau) | **ln_e6**, **ln_e6_b** (nouvelles, nouveau bloc ln_s5_b1c, K8) |
| Concavité par f″ (haute ; propre au Prof Fayssal, mais **exigée par le cadre 1.2.13 et 1.2.22**) | Rappel des règles f″ < 0 / > 0 / point d'inflexion ; f″(x) = 3(2x + 1)/((1 − x)²(x + 2)²), concave puis convexe, I(−½ ; 0). Question du bloc : concavité de ln ((ln x)″ = −1/x² < 0), avec démonstration et 5 réactions | **ln_e6_c** (nouvelle) ; fiche ln_b1 point 8 |
| Croissances comparées avec xⁿ, n ∈ ℕ* (haute, confirmé) | lim (ln x)/xⁿ = 0 « car 0 ≤ (ln x)/xⁿ ≤ (ln x)/x pour x ≥ 1 » ; lim_{0⁺} xⁿ ln x = 0 « car xⁿ ln x = xⁿ⁻¹ × x ln x » : écran, centre, cahier, voix | ln_l3, ln_l4, ln_b1 (point 5) |
| Piste HAUTE : justifier la branche parabolique par lim (ln x)/x = 0 | Phrase complète « lim ln x = +∞ et lim (ln x)/x = 0, donc … branche parabolique de direction l'axe des abscisses » (écran, centre, cahier, voix) ; renvoi dans la trace de ln_l1 | ln_l3, ln_l1 |
| Tableau de variations complet de ln (moyenne, confirmé) | Ligne au cahier + figure « variations » (double barre en 0, −∞ → 0 → +∞) sur la diapo et dans le bloc | ln_l2, bloc ln_s3_b2 |
| ln continue et strictement croissante ⇒ e unique (moyenne + oral seulement, confirmé) | « ln est continue (car dérivable) et strictement croissante sur ]0 ; +∞[, et ln 2 < 1 < ln 3 : ln x = 1 admet une solution unique, notée e » (écran, cahier, voix) | ln_c3 |
| 10ˣ ≤ a, 10ˣ ≥ a (moyenne, confirmé, cadre 1.2.18) | Règle + exemple 10ˣ ≥ 5 ⇔ x ≥ log 5, « car log est strictement croissante » (écran, centre, cahier, voix) | ln_g2, ln_b1 (point 9) |
| Quantificateur ∀ (moyenne, confirmé) | ∀x ∈ ]0 ; +∞[ / ∀x ∈ I dans les traces | ln_c1, ln_e1, ln_p3, ln_e5_c |
| D_E / D_I et « S = … » (basse → moyenne, confirmé) | D_E, D_I nommés à l'écran, au cahier et dans les démonstrations ; conclusion « S = … » | ln_q1, ln_q1_b, ln_q3 |
| (ln\|u\|)′ = u′/u si u ≠ 0 sur I (basse → moyenne, confirmé) | Ligne écran, centre, cahier, voix | ln_v1, ln_b1 (point 6) |
| ln : ]0 ; +∞[ → ℝ (basse, confirmé) | Écrit dans la définition | ln_n3, ln_b1 (point 1) |
| Exemple avec quantité conjuguée (basse, confirmé) | Exercice de réserve A = ln(√6 − √5) + ln(√6 + √5) = 0, démonstration en 5 lignes, 5 réactions | ln_a5 (exercices_fin_de_cours e1) |
| e irrationnel (basse, confirmé) | Ligne écran + cahier + voix | ln_c3 |
| Oral seulement (règles 37-38, non confirmés mais simples) | Écrit à l'écran ce que la voix dit déjà : factorisation de x − ln x (ln_l6), calcul de f′ et de f(1), f(e) (ln_e5_b), « −2 minimum » et « on divise par 2x > 0 » (ln_e5_c), f(1) = 3/2 (ln_e3), « ne coupe pas l'axe car 0 ∉ ]0 ; +∞[ » (ln_l2), taux d'accroissement complet (ln_l8), ln(10⁻⁴) = −4 ln 10 (ln_q7), développement + Δ (ln_q1_b) | ln_l6, ln_e5_b, ln_e5_c, ln_e3, ln_l2, ln_l8, ln_q7, ln_q1_b |

### Non corrigés et pourquoi

- Propres au Prof Fayssal, non exigés par le cadre : unique α avec ln (TVI vu au ch1), changement X = 1/x, inéquation en (ln x)², primitive de 1/(x ln x), ln(xy) = ln|x| + ln|y| et ln x²ⁿ, démonstrations (récurrence, encadrement 2√x), liste des formes indéterminées, 0 ≤ ln(1 + x) ≤ x et suite.
- Nouvelles pistes moyennes et basses (consigne) : lim ln(x + 2)/x, « x ∈ D_u et u(x) > 0 », domaine de √(ln x), 1/(3 − ln x), 1/(x ln x) en 0⁺, ln(x + 1)/x³, règles ln x < r, ln ∛a, « dérivée logarithmique ».
- Hors fichiers autorisés : les simulations `bilan.html` et `carte.html` (fiche et carte dessinées) ne montrent pas les lignes ajoutées à ln_b1 ; seules les bullets de ln_b1 sont à jour. À reprendre côté frontend.
- À décider : ln_e6, ln_e6_b, ln_e6_c n'ont **pas de visuel** (`visual.kind = none`) : aucune vue existante ne montre ln((x + 2)/(1 − x)) ; les figures du cahier (courbe + tableau) la montrent. ln_l9 réutilise la vue `plonge` (elle montre ln X près de 0, pas la courbe de ln(x + 1)).
- Non lancés ici (outils sur le poste Windows) : `verifier_texte_corpus.py` (mots à vérifier : irrationnel, concave, convexe, inflexion, seconde, identité remarquable), `controler_cadre.py`, `preparer_reponses.py verifier`.

### Démonstrations

- Relues : 82 (toutes : questions, exercices, réserve, exercices de bloc). Réécrites : 28 (21 + 7 copies identiques dans les blocs). Ajoutées : 4 (ln_e6_c question, ln_e6_b réserve e0 et sa copie dans le bloc ln_s5_b1c, ln_a5 réserve e1). Les autres étaient déjà complètes.
- Avant → après :
  - ln_z4_sens : « ÷ (−3), négatif : le sens change | x > −2 » → « x > 6/(−3) (on divise par −3 < 0) | 6/(−3) = −2 | donc −3x < 6 ⇔ x > −2 ».
  - ln_q1_b : « ⇔ x² + x − 6 = 0 ⇔ x = 2 ou x = −3 » → D_E, ln a + ln b = ln(ab), ln a = ln b ⇔ a = b, développement, Δ = 25, deux racines calculées, tri, S = {2} (8 lignes).
  - ln_l5 (réserve) : « ln(1 + 3x)/(2x) = (3/2) × ln(1 + X)/X ; la limite vaut 3/2 » → on multiplie et divise par 3x, (3x)/(2x) = 3/2, limite de base = 1, donc 1 × 3/2 = 3/2.
- Toutes vérifiées avec sympy (Δ, racines, ln 18 ≈ 2,89, 3/2, f′, f″, f(−½) = 0, limites, ln(√6 − √5) + ln(√6 + √5) = 0, (ln x)″ = −1/x²).

### Voix à enregistrer

- Diapos (voix nouvelle ou modifiée, `audio.mixed` retiré) : ln_c3, ln_l3, ln_l4, ln_v1, ln_g2, ln_l9, ln_e6, ln_e6_b, ln_e6_c.
- Démonstrations jouées (audio retiré) : ln_z4_sens question, ln_d1 question, ln_q1_b question, ln_a5 question, ln_c2 exercice e0, ln_a1 exercice e0, ln_a5 exercice e0 ; nouvelle : ln_e6_c question.
- Énoncé : ln_e6_c question (`enonce_dit`, pas d'`enonce_audio`).
- Réactions : ln_e6_c `concentration.reponses.q` (1/juste, 0/1, 0/2, 2/1, 2/2). En réserve (non jouées aujourd'hui) : ln_e6_b `reponses_fin_de_cours.e0`, ln_a5 `reponses_fin_de_cours.e1` ; démonstrations de réserve et de bloc réécrites (sans voix, comme avant).

### Vérifications faites

- `json.load` : OK ; écrit avec `json.dumps(ensure_ascii=False, indent=2)`, LF.
- Script : chaque `mot` des 86 démonstrations est dans sa parole (et dans l'ordre pour les nouvelles) ; chaque `mot` de pointage et de centre est dans `speech_text.mixed` : 0 erreur.
- Chaque diapo est dans un seul bloc, l'ordre des blocs suit l'ordre des diapos, une seule « À toi » par bloc, chaque `competence_id` existe, chaque question a ses réactions (juste / 1 / 2) : 0 erreur.
- Textes dits nouveaux : aucun chiffre ni symbole (contrôle automatique).
- `verifier_figures_cahier.py` : 11 figures, 0 erreur, 0 avertissement.
- `git status` : le cours en ligne n'est pas modifié ; rien de commité.
