# phys_ch7_dipole_RL — corrections (26-27/11/2026)

Phase 1 dans le cours servi `backend/data/courses/phys_ch7_dipole_RL.json` (aucun texte parlé changé) ; phase 2 dans la
copie d'attente `backend/data/courses/en_attente/phys_ch7_dipole_RL.json` (refaite à partir du cours servi, l'ancienne
copie était périmée ; les cahiers revus par 8b0991df y sont repris). Aucune voix générée.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Diapos | Questions 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Notions clés | redites | annoncées (motifs ≠) | 1er mot le plus fréquent | Diapos qui suivent, même 1er mot | Débuts répétés |
|---|---|---|---|---|---|---|---|---|---|---|
| Avant (main, 26/11) | 90 | 1 | 152 | 7 | 30 | 10 | 0 (0) | « دابا » 23 % | 16 | « نفس التمرين » ×11, « قبل ما » ×8, « دابا غادي » ×7 |
| Servi après phase 1 | 90 | 0 | 50 | 0 | 37 | 10 | 0 (0) | « دابا » 23 % | 16 | inchangés (voix inchangée) |
| Attente après phase 2 | 92 | 0 | 48 | 0 | 38 | 38 (100 %) | 38 (17) | « هاد » 8 % | 0 | — |

- Les 47 « formules non écrites » restantes (46 en attente) sont dans les **énoncés lus du national** (`*_enonce*`) : le
  sujet est affiché à l'écran par `le.html` pendant la lecture ; rien à écrire en plus. Hors énoncés : 2 dans le cours
  servi (diapos 38 et 87, la question posée avant la méthode, corrigée en phase 2), 0 dans la copie d'attente.
- Annonces : 38 phrases d'annonce, **38 phrases toutes différentes** (mesuré sur la phrase entière). Le script compte
  « phrases ≠ » par motif reconnu (`ATTENTION`) : 17 motifs différents, il n'en connaît pas plus d'une vingtaine.
- Réactions : premier mot « مزيان » 48 → 8, « لا » 42 → 10 sur 156 ; plus aucun début de 6 mots répété ≥ 4 fois.
- Tournures recopiées restantes (6) : formules (« L dé i sur dé t، plus… », « exponentielle de moins t sur tau ») et le
  texte des sujets (« bobine d'inductance L et de résistance ») — on ne réécrit ni une formule ni un sujet.

## Phase 1 — cours servi (commit cfe571d7, puis écran seul en phase 2)

1. **Questions de bloc** (vérifiées dans le JSON) :
   - `rl_s0_b1` (diapos 1-4) posait ses questions après la diapo 4 (règle 53) → bloc `rl_s2_b2b` (ranger l'équation, sans question).
   - Défaut 9 (coefficient (R + r)/L, forme divisée par L enseignée diapos 29-30) : exercice de `rl_s2_b2` → `rl_s2_b3b`.
   - Défaut 11 (L₁ = 2L₀, effet de L diapo 50) : exercice de `rl_s3_b2` → `rl_s4_b1` ; l'exercice « r par I₀ » de `rl_s4_b1` → `rl_s4_b2`.
   - Défaut 12 (i à t = τ, rupture diapos 57-59) : retrouver de `rl_s4_b1` → `rl_s3_b4`.
   - Défaut 13 (énergie, diapo 65) : retrouver → `rl_s4_b2b` ; l'exercice 2016 R était le doublon exact de l'exercice de la diapo 66 : retiré du bloc, celui d'après la leçon gardé.
2. **Aucune question dans les 6 premières** : la question de `rl_rp2_additivite` (diapo 4) passe dans sa réserve `exercices_fin_de_cours` (réactions gardées).
3. **Dit = écrit** : cartes `centre` au mot qui dit la formule (I₀ = E/(R + r), τ = L/(R + r), L = τ·(R + r), solutions, tangentes, 63 %, 37 %…), `play_until` déplacés sur le mot qui dit ce que la figure écrit (diapos 34, 38, 41, 42, 43, 52, 58, 64, 74), gestes vers la carte relue (« نعاود نقرا ») ou vers la figure. Doublons de pointage retirés (diapos 44, 58). Passages ≥ 60 mots sans geste : 7 → 0.
4. **Écran** : la ligne u_Y2 = −u_R (oscilloscope jamais expliqué, défaut 6) remplacée par « u_R = R·i est l'image de i » (diapos 12-13), dans les deux copies.

Vérifié : `verifier_formules` 0 ; `verifier_parcours` rien ; `verifier_pointage` 36 défauts avant et après (tous déjà
là : moments des vues `lampes.html` et `national-pas-a-pas.html` que le contrôle statique ne lit pas) ;
`verifier_pointage_simulations` mêmes alertes avant/après ; `verifier_figures_cahier` mêmes 2 erreurs « 4 figures dans
le bloc » avant mes changements — disparues avec la revue des cahiers 8b0991df.

## Phase 2 — copie d'attente

### Ordre des notions (`ordre-des-notions/phys_ch7_dipole_RL.md`)

| # | Défaut | Fait |
|---|---|---|
| 1 | additivité avec la bobine avant la bobine | diapo `rl_rp2_additivite` placée après `rl_b1_bobine` (outils : Ohm, dérivée, puis bobine, puis additivité) ; voix 3, 4, 5 reliées (« جوج نعاودوهم دابا… والتالتة من بعد ») ; lignes du cahier déplacées au bloc 2 |
| 2 | L sans sens | diapo 6 : « L، عدد كيقول شحال la bobine كتعطل les variations ديال le courant » ; noyau de fer dit à la diapo 13 (après la mesure de L) — la vue `bobine.html?vue=objet` montre encore le noyau sans voix en passant vers `symbole` (simulation non modifiée) |
| 3 | lampes L₁/L₂ ≠ inductance L | voix « la lampe un / la lampe deux », écran « lampe 1 / lampe 2 » (diapos 7-11, observation, réactions, cahiers des blocs). Laissé : les étiquettes `L_1`, `L_2` dessinées par `lampes.html` (fichier partagé non modifié) |
| 4 | diapo 9 trop chargée | diapo 9 : même éclat → même courant final, régime permanent et I₀ nommés ; u_b = r·I₀ et sa question → réserve de la diapo 21 (régimes), où u_b = r·I₀ est établi |
| 5 | auto-induction + continuité dans une diapo | diapo 11 = auto-induction ; **nouvelle diapo `rl_b5b_continuite`** (vue `lampes.html`, moments k_ouvert, k_ferme, retard, ouverture) ; réserve de l'exercice continuité déplacée avec elle |
| 6 | oscilloscope | écran (voir phase 1) |
| 7 | énoncé 2025 R lu trop tôt (diode, énergie) | `rl_t4_enonce` placé juste avant `rl_t4_enonce_p2` (après la diode) ; diapo 18 ne calcule plus E_m (« غادي نحسبوها ملي نتعلمو l'énergie ») et n'écrit plus que u_bf = 0 ; E_m du 1-4 calculé à la diapo de l'énergie |
| 8 | τ nommé sans rappel (diapo 30) | rappel de τ du RC + « غادي نثبتوها ملي نحلو l'équation » |
| 9, 11, 12, 13 | questions de bloc | phase 1 |
| 10 | r demandé avant la méthode (2019 R) | question d'ouverture retirée de la voix ; I₀ = U_R/R, puis R + r = E/I₀, puis r, puis la relation du corrigé (3 cartes) |
| 14 | diode jamais expliquée (forte) | **nouvelle diapo `rl_t3a_diode` « Rappel : la diode »** avant la diapo 60 (sens passant, bloquée, symbole, diode idéale) — aucune vue de simulation ne convient (la vue `diode` de `rupture.html` commence par l'étincelle) : `visual.kind: none` + 4 cartes ; la diode est rappelée à la diapo 60 |
| 15 | surtension sans chiffre | diapo 60 : cause (di/dt énorme) + « u b égale moins cent volts، يعني dix fois E » (carte) |
| 16 | effet Joule | « l'énergie électrique كتولي حرارة ف la résistance » |

Autres défauts « moyens » des énoncés lus dans le désordre (2021 R, 2019 R) : laissés, chaque énoncé est déjà lu juste
avant sa résolution sauf le 2025 R (corrigé).

### Notions importantes (règle 55)
38 notions clés : 38 annoncées (phrase toujours différente, juste avant la notion), 38 redites autrement
(« بطريقة أخرى / بمعنى آخر / بكلمة أخرى » + image ou autre point de vue), rappels ajoutés dans les diapos qui les
réutilisent : continuité (diapos 32, 45, 56, 59, 64), bobine réelle (27), additivité-escalier (25), deux lampes (21, 57),
I₀ (30, 43), RC (30, 46, 51), diode (60), règle « u_b suit la pente » (15), expérience des curseurs (50).

### Tuteur humain (règle 56)
- Débuts de voix : « دابا » 23 % → 6 %, premier mot le plus fréquent « هاد » 8 % ; 0 diapo qui suit avec le même mot.
- Énoncés : 18 débuts différents (« يلا نجربو… », « مرة أخرى… », « التتمة ديال le sujet… »…) et 8 fins différentes au lieu de « دابا نفهمو التمرين خطوة بخطوة » partout.
- Questions rhétoriques « قبل ما نشوفو، سؤال » / « قبل الحساب، سؤال » (diapos 38, 48, 55, 56, 66, 87) remplacées par une annonce ou un lien.
- Réactions : 73 débuts réécrits — juste : « بالضبط! », « هادا هو! », « صافي »… ; à moitié juste : « قريب، … صحيح » , « فهمت علاش ختاريتي هادا: », « جزء صحيح: » ; faux : « خليني نوريك فين تلفنا: », « ما تخافش، هاد الغلطة عادية »… Le reste de chaque réaction (ce qui est juste dans le choix, puis l'idée qui coince) est gardé.
- Touches humaines : partage de la difficulté (« هادي غلطة كيديرها بزاف ديال التلاميذ »), images (voiture lourde, verre d'eau, porte qui ne s'ouvre que d'un côté), raison d'apprendre (« كتطيح ف كل sujet »).

### Voix
- `nombres_fr.py` : 0 nombre darija à côté du français (« جوج tensions » corrigé).
- `verifier_mots.py` sur les 119 pistes changées : mots nouveaux rares remplacés (écoute, curseurs, كتفرانا → كتعطل, خزان → الكاس, نحميو → نحافظو, كيورينا → كيبين, حلينا, ضاوية, ركبنا, transformateur/détecteur → موطور/شارجور). **Mots douteux gardés (termes du programme, à écouter)** : passante, bloquée, surtension, étincelle, membre (« le second membre »), الشارجور (2), نحافظو (2), كيتحل (2), كتعطل (3). Les autres mots rares listés étaient déjà dans le cours (énoncés : kiloohm, informatisé, schématisé… ; millianri/anri = henry réécrit par la prononciation).
- « السؤال un point … » (numéro français après un mot darija) reste dans les diapos du national qui ne changeaient pas pour autre chose : à reprendre dans une passe voix dédiée.

### Pistes à générer
`docs/audit-pedagogie/voix_a_generer/phys_ch7_dipole_RL.json` : **119 pistes** — 70 diapositives (dont 2 nouvelles),
49 réactions ou énoncés. Les `audio` correspondants sont retirés de la copie d'attente.

### Vérifications (copie d'attente)
`verifier_formules` 0 ; `verifier_parcours` rien ; `verifier_figures_cahier` 0 erreur ; `verifier_pointage` 39 (les 36
d'avant + 4 moments de `lampes.html` sur la nouvelle diapo, que le contrôle statique ne lit pas comme pour les autres
diapos des lampes ; « noyau » n'est plus joué) ; `verifier_pointage_simulations` : mêmes alertes qu'avant, + DEPART
de la nouvelle diapo (comme les autres diapos des lampes) ; les alertes GESTE viennent de l'absence de piste (durée
estimée), elles disparaîtront avec la voix.

## Cours de référence du prof (`reference-prof/phys_ch7_dipole_RL.md`, 27/11/2026)

| n° | Recommandation | Appliqué / laissé |
|---|---|---|
| 1 | rappel de la diode avant la diapo 60 ; diode citée au montage | **appliqué** : diapo `rl_t3a_diode` ; diapo 19 : « ومرات كنزيدو une diode ف le montage، باش نتفاداو واحد l'étincelle؛ غادي نشوفو علاش من بعد » |
| 2 | cause de la surtension dès u_b = L·di/dt ; chiffre à la diapo 60 | **appliqué** : diapo 13 (« يلا i طاحت ل zéro دقة وحدة؟ dé i sur dé t كتولي كبيرة بزاف، و u b حتى هي: une surtension », carte) ; diapo 60 : cause redite + −100 V = −10·E |
| 3 | τ du RC rappelé diapo 30 | **appliqué** |
| 4 | sens provisoire de L ; noyau de fer après la diapo 13 | **appliqué** (voix) ; la simulation de la diapo 6 montre encore le noyau en passant (non modifiée) |
| 5 | « lampe 1 », « lampe 2 » | **appliqué** (voix, écran, réactions, cahiers) ; étiquettes dessinées L₁/L₂ de `lampes.html` laissées |
| 6 | diapo 9 allégée | **appliqué** |
| 7 | diapo 4 après la diapo 6 | **appliqué** |
| 8 | moteur + effet Joule à la voix (diapo 65) | **appliqué** |
| 9 | diapo 57 : les deux montages de rupture, même équation | **appliqué** (« وف montage آخر، فيه une diode بلاصة la position deux… ») ; la diode y est annoncée, expliquée 3 diapos plus loin |
| 10 | usages de la bobine (diapo 2 ou 6) | **appliqué** diapo 6 (moteur de voiture, chargeur ; écran : allumage, chargeur, transformateur) |
| 11 | garder les autres corrections de l'audit | fait (défauts 6, 7, 9-13) |

Laissé, hors cadre ou déjà meilleur chez nous selon la référence : u_b découverte par la mesure (pas donnée d'emblée),
expérience des lampes avant u_b, démonstration de E_m par la puissance (expression admise, conforme au programme).
Rien d'ajouté hors du cadre de référence.
