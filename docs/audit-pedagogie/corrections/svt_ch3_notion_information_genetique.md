# Corrections — svt_ch3_notion_information_genetique (27/11/2026)

Suite de l'audit `docs/audit-pedagogie/` (règles 52 à 56). Longueur gardée (79 → 85 diapos). Aucune voix générée.

## Phase 1 — cours servi `backend/data/courses/svt_ch3_notion_information_genetique.json` (aucun texte parlé changé)

Commits f7e5b760, 2586cca6, puis un correctif de fraction dans le cahier.

**Questions de bloc** (vérifiées dans le JSON : six doublons ou questions avant leur leçon, pas quatre) :
- `ig_s1_b1` (après l'amibe) : le « retrouver » demandait le caractère héréditaire (pas encore défini) et la transmission parents → enfant (jamais enseignée) : retiré. Ensuite (9a05f156), l'amibe passe au bloc 2 et le bloc 1 (ouverture, rappel de la cellule) n'a plus de question ; l'exercice de l'amibe va dans la réserve `exercices_fin_de_cours` de la diapo de l'amibe. La première question de bloc tombe donc après la diapo 7 (greffe), et plus après la diapo 4.
- `ig_s1_b2` : doublon exact de `ig_s1_b3` (définition et Gurdon, vus aux diapos 8-9) : retiré. À la place, l'exercice « hypothèse ou preuve ? » : l'ancienne observation de la diapo 6, avec le même énoncé, la même voix et les mêmes retours.
- `ig_s2_b1` (après Feulgen) : doublon de `ig_s2_b3` (chromatide, centromère et G2, vus aux diapos 17-18) : retiré. En phase 2, il est remplacé par un « retrouver » sur Feulgen.
- `ig_s3_b3` / `ig_s4_b1` : l'exercice d'anaphase posé avant la diapo de l'anaphase est retiré de `s3_b3`, qui garde son « retrouver » (rôle de la mitose). `s4_b1` garde l'exercice et perd son « retrouver » en double.
- `ig_s4_b3` (après l'expérience 2) : il demandait l'expérience 3. Ses questions passent à `ig_s5_b1` (après le bilan de Griffith), dont les questions (Avery, diapos 40-42) étaient le doublon de `ig_s5_b2`. En phase 2, `s4_b3` reçoit un « retrouver » sur les expériences 1 et 2.
- `ig_s8_b3` : le vrai/faux était le même que celui de `ig_s7_b3` (et que celui de la réserve) : retiré, le « retrouver » reste.

**Questions dans les 6 premières diapos** : la question de la diapo 4 part dans la réserve de fin de cours (`exercices_fin_de_cours` et `reponses_fin_de_cours`). L'observation de la diapo 6 devient l'exercice du bloc `s1_b2`. Les voix des diapos 2 et 4 finissent encore sur « ? » : c'est corrigé en phase 2.

**Dit = écrit** (`concentration.centre` / `pointage`) :
- diapo 9 : la définition s'écrit morceau par morceau (quoi ? où ? rôle ?), puis en entier au mot « نعاود نقرا » (avant : 74 mots sans aucun geste) ;
- diapo 13 : à la relecture, la baguette revient sur « chromosome = ADN + protéines » ;
- diapo 32 : « 2n = 4 : 4 chromosomes, chacun à 2 chromatides » ;
- diapo 53 : le calcul G3 s'écrit ligne par ligne (4 × 2 = 8 ; 8 − 2 = 6 ; 2/8 = 25 % ; 6/8 = 75 %).

**Signalements faux, laissés en l'état** :
- diapo 23 « العدد كيولي deux fois » : ce n'est pas une formule, et l'écrire donnerait la réponse avant la question ;
- diapo 24 : la simulation écrit déjà G2 et M (`duree_g1`) ;
- diapo 31 : le mot « racine » est pris pour une formule ;
- diapo 51 : la simulation écrit la moyenne au moment `calcul_moyenne`.

**Erreurs d'écran** : diapo 14, « 2n = 46 (n = 23 paires) » devient « n = 23 chromosomes, un de chaque paire » (puce et `centre`). Diapo 23 : les fractions écrites à plat deviennent « (10·10³)/(2,5·10³) » et « (40 h)/2 » (`verifier_formules` : 3 → 0). Ensuite, « 60 h / 3 », apporté par la revue du cahier da226b37, devient « (60 h)/3 ».

## Phase 2 — copie d'attente `backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json`

La copie d'attente a été refaite à partir du cours servi après la phase 1. Ce cours contient déjà la revue du cahier da226b37, faite par une autre session : les cahiers revus sont gardés. Ils sont seulement partagés entre les deux moitiés des diapos coupées (10, 14, 43, 55), et les nouvelles diapos de rappel ajoutent une ligne au cahier de leur bloc.

**Diapos ajoutées (6)** — une notion par diapo, avec une vue déjà existante du cours :
- `ig_o1b_fecondation` (après la diapo 2), rappel : ovule + spermatozoïde → fécondation → cellule-œuf. Vue `documents.html?vue=ouverture&depart=cellule_oeuf`.
- `ig_n0_molecules` (avant le noyau), rappel : la molécule ; l'ADN et les protéines, deux molécules du noyau. **Carte simple** (`visual.kind: none` + `centre`) : aucune vue de simulation ne montrait des molécules sans dévoiler le nucléosome.
- `ig_n1c_nucleosome` : la diapo 10 est coupée en deux (a : enveloppe, nucléole, chromatine ; b : nucléosome = ADN + histones, collier de perles). Vue `zoom.html?vue=zoom&depart=chromatine`.
- `ig_p1b_diploide` : la diapo 14 est coupée en deux (a : 46 chromosomes, 23 paires d'homologues ; b : 2n = 46, n = 23 chromosomes et non 23 paires, diploïde, avec le piège dit). Vue `bases.html?vue=chromosomes&depart=k_paire`.
- `ig_s1b_bases` : la diapo 43 est coupée en deux (a : hydrolyse et nucléotide ; b : les quatre bases et le brin, avec la question de la diapo 43 et ses réactions). Les mots purique et pyrimidique restent à l'écran seulement. Vue `adn.html?vue=construire&depart=nucleotide`.
- `ig_r7b_colchicine` : la diapo 55 est coupée en deux (a : thymidine = nucléotide à T, autoradiographie ; b : colchicine, puis métaphase marquée). Vue `thymidine.html?vue=experience&depart=regle`.

**Diapo déplacée** : `ig_n3_chromatides` passe après `ig_c1_cycle`. La phase S est donc vue avant « le chromosome devient à deux chromatides », et la voix la rappelle (« تفكر: ف la phase S… »). Le bloc `s2_b3` est remis dans l'ordre.

**Autres corrections de l'ordre des notions** (`ordre-des-notions`) :
- caractère héréditaire défini en diapo 2 et rappelé en diapo 5 ;
- albinos expliqué (diapo 8) ;
- « la mitose » retiré de la diapo 10 (elle n'est vue qu'en diapo 15) ;
- yeux de réplication annoncés pour plus tard (diapo 21) ;
- fuseau et aster expliqués (diapo 26) ;
- origine de 5' et 3' donnée (diapo 45) ;
- azote 15 et centrifugation expliqués (diapo 50).

Les défauts 1, 2, 4, 6, 7 et 8 (blocs) sont corrigés en phase 1. Deux nouveaux « retrouver » remplacent des doublons : `s2_b1` (Feulgen) et `s4_b3` (Griffith, expériences 1 et 2).

**Laissés** :
- aucune question ajoutée dans les diapos coupées (10, 14) : la question du bloc qui suit suffit (règle 27, une seule « À toi » par bloc) ;
- défaut 17, diapo 55 : la colchicine est séparée sur sa propre diapo, mais sans question entre les deux diapos (même raison) ;
- défaut 13 de l'audit, diapo 43 : appliqué par la coupe.

**Règle 55** : 25 notions clés. La revue du cahier en a ajouté deux : la méthode « décrire, expliquer » (diapo 26) et le brin complémentaire.
- Chacune a une annonce avant elle, et chaque annonce est une phrase différente : 20 sont reconnues par l'audit (80 %) ; les 5 autres sont « خليك معايا », « رد بالك مزيان », « عطيني عينيك », « بغيت نشوفك معايا من اللول للخر » et « عطيني هاد الدقيقة كاملة ». Les trois premières ont été choisies parce que les annonces en français (« écoute bien », « sois attentif », « concentre-toi ») sont absentes du corpus de la voix.
- Chacune est redite autrement (« بطريقة أخرى », « يعني بالدارجة », « بمعنى آخر », « نعاود نقرا »).
- Rappels ajoutés dans des diapos plus loin : caractère héréditaire, fécondation, molécules, phase S, yeux de réplication, mitose.

**Règle 56** : la voix ne commence plus par « دابا » sur 24 diapos (sur 79) : aucune diapo ne commence par ce mot maintenant. Les débuts sont variés et font le lien avec la diapo d'avant.
- Ajouts : quelques touches humaines (amibe « غريبة شوية », piège 2n, piège du 2ᵉ cycle de thymidine, image de la fermeture éclair).
- 12 réactions : leurs premiers mots répétés sont remplacés. Elles disent maintenant ce qui était juste dans le choix, ou partagent la difficulté.

**Erreurs dans la voix** :
- « n égale vingt-trois paires » sort de la diapo 14 ; la diapo 14b dit « n = 23 chromosomes » et nomme le piège ;
- diapo 39 : « R vivants مع S deux cents » devient « S tués » (un mot mal converti).

**Pistes à générer** : 69, dont 57 voix de diapos (6 nouvelles, 51 au texte changé) et 12 réactions. S'y ajoutent 2 énoncés de « retrouver » de bloc, gardés en réserve parce que la fin de bloc n'est pas encore jouée. La liste est dans `docs/audit-pedagogie/voix_a_generer/svt_ch3_notion_information_genetique.json`. L'`audio` de chaque piste changée a été retiré.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Avant (servi) | Après phase 1 (servi) | Après phase 2 (attente) |
|---|---|---|---|
| Diapos | 79 | 79 | 85 |
| Questions dans les 6 premières | 3 | 2 (voix qui finissent sur « ? ») | 0 |
| Première question de bloc | après la diapo 4 | après la diapo 7 | après la diapo 8 |
| Formules dites non écrites | 9 | 4 (faux signalements) | 4 (les mêmes) |
| Passages ≥ 60 mots sans geste | 1 | 0 | 0 |
| Notions clés / redites / annoncées (phrases ≠) | 18 / 7 / 0 (0) | 18 / 7 / 0 | 25 / 25 / 20 (20), 80 % mesuré (25 annoncées en réalité) |
| Premier mot le plus fréquent | « دابا » 30 % | idem | « ف » 7 % |
| Diapos qui suivent avec le même premier mot | 18 | 18 | 0 |
| Réactions au même début (≥ 4) | 3 groupes (7, 6, 4) | idem | 0 |

**Vérifications** :
- `verifier_formules` : 0 ;
- `verifier_parcours` : rien ;
- `verifier_figures_cahier` : 0 erreur (3 avertissements, déjà là avant) ;
- `verifier_pointage` : 56 défauts contre 57 avant ; aucun nouveau. Ce sont les repères `donnee-*` des sujets d'examen, déjà là avant. Celui qui est corrigé : le mot « deux » de la prophase pointait à côté de « asters » ;
- `verifier_pointage_simulations` : aucun écart nouveau hors GESTE. Les avertissements GESTE (26 → 313) viennent des pistes sans voix (plus de durée connue) : il faudra le relancer après la génération ;
- `nombres_fr.py` : 0.

## Mots douteux pour la voix

`verifier_mots`, lancé sur la copie d'attente. Mots rares que j'ai ajoutés :
- darija : كور، حداه، طرافة، الجاكيط، كتحل، كنشوفوهاش، قدامها، كيتلصقو، كتدوز، ورثتيها، قريتيها، عطيني عينيك، خليك معايا، تقيل شوية كثر ;
- français : pigment, lot / lots (diapo 14b), spermatozoïde, l'ovule, fécondation, polynucléotide, désoxyribonucléique, colchicine, antiparallèles.

Les mots du programme (nucléosome, mérotomie, Feulgen…) étaient déjà rares avant. À écouter en priorité : `ig_p1b_diploide` (« lot ») et `ig_r9_yeux` (« الجاكيط »).
