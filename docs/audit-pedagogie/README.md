# Audit pédagogique des cours — 26/11/2026

Demande de l'utilisateur : garder la longueur, mais ne pas perturber l'élève — ordre des notions, pas de question
aux premières diapos, dit = écrit au même instant, notions importantes annoncées et redites (annonce chaque fois
différente), tuteur humain et pas robotique. 26 cours audités (23 du 2ᵉ Bac servis, 3 du Tronc Commun /TCF).

## Fichiers

- `mesures.md` / `mesures.json` — mesures automatiques (`python -I scripts/audit/audit_pedagogie.py … --md docs/audit-pedagogie/mesures.md`).
- `ordre-des-notions/<deck>.md` — lecture diapo par diapo (agents Opus) : ordre proposé des premières notions,
  défauts (notion avant d'être enseignée, trop vite, question trop tôt) avec correction proposée, notions dites une seule fois.
- `textes/<deck>.md` — chaque cours exporté en texte lisible (voix, écran, questions dans l'ordre joué).
- `regles-52-56-a-ajouter.md` — texte des règles 52 à 56, ajoutées au skill professeur le 26/11/2026.
- `banque-de-phrases.md` — annonces d'attention, redites, rappels, ouvertures, réactions variées.

## Ce qui ressort

1. **Ordre des notions** : environ 94 défauts forts et 280 moyens sur 26 cours. Les plus fréquents :
   - **questions de bloc qui portent sur la diapo d'après** (ex. `ab_b02` demande Ke, défini à la diapo 9 ; `ee_b05`
     demande Qr,éq établi en 23-24 ; `ci_s1_b2` demande le titrage enseigné en 12-16) — vérifié dans les JSON ;
     SVT ch3 en a quatre, doublons de blocs placés plus loin ;
   - **rappels d'années d'avant absents ou placés après leur premier usage** (dérivée, trigonométrie, colinéarité,
     tableau d'avancement, ATP, protons/pH, conversions d'unités, notation des particules) ;
   - **plusieurs notions nouvelles dans une même diapo** (SVT ch1 diapo 6 : ATP, phosphate, hydrolyse, phosphorylation).
2. **Questions trop tôt** : 25 cours sur 26 ont une question dans leurs 6 premières diapos.
3. **Dit = écrit** : beaucoup de formules dites sans être écrites à leur mot, surtout en physique-chimie et en maths
   (RLC, RL, acides-bases) ; à confirmer à l'œil sur les diapos listées (exemples sûrs : `op_t5_convertir` sans
   aucun geste, `lc_rp2_bobine` qui n'écrit la formule qu'à la relecture).
4. **Annonce d'attention** : 0 dans 25 cours sur 26. « رد البال » existe (182 fois) mais signale un piège après coup.
5. **Redites** : entre 0 % et 55 % des notions clés ont une deuxième façon de les dire dans leur diapo (Tronc Commun : presque 0).
6. **Robotique** : 413 voix sur 1 696 commencent par « دابا » (jusqu'à 48 % dans un cours) ; 18 diapos de RLC
   commencent par « نفس التمرين ديال الامتحان الوطني » ; 303 réactions fausses commencent par « شوف، الجواب »,
   155 justes par « مزيان، الجواب ».

## Erreurs de contenu trouvées en passant

- SVT ch3 diapo 14 : « 2n = 46 (n = 23 paires) » — n = 23 chromosomes, pas 23 paires.
- Physique ch5 diapos 25, 44, 51 : N_A lu « newton ampère », m lu « mètre », ᴬ_Z e lu « Ag » ; ch2 diapo 58 « célérité nu » ; ch3 diapo 53 « teta environ teta » (tan θ ≈ θ).
- SVT ch1 et ch2 (national 2016) : valeurs du document 2 dans l'ordre inverse de la diapo suivante.
