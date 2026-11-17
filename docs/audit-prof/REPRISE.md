# Reprise du travail : audit face aux cours de professeurs (17 novembre 2026)

Ce fichier permet de reprendre le travail depuis un autre compte ou une autre session.

## Ce qui est fait (sur `main`, dans `backend/data/courses/en_attente/`, rien en ligne)

| Matière | Audit | Corrections des manques | Démonstrations « au fond » |
|---|---|---|---|
| Maths ch1-ch6 | `maths.md`, `maths-autres-profs.md`, `maths-longueur.md` | faites (`corrections/maths-ch1..6.md`) | faites |
| Physique ch1-ch8 | `physique.md` (111 manques) | faites (`corrections/physique-ch1..8.md`) | faites |
| Physique ch9 + chimie ch10-ch13 | `chimie.md` (62 manques) | faites (`corrections/chimie-ch9..13.md`) | démonstrations reprises le matin (`corrections/demos-chimie.md`) |
| SVT ch1-ch4 | — | — | faites (`corrections/demos-svt.md`) |

Règles ajoutées aux skills : `professeur` règles 37 (avec son volet physique-chimie) et 38, `cours-concentration` étape 9b.

## Ce qui reste

1. **Chimie** : faite (ch9 à ch13). Les états physiques sont absents dans `attendu`, car le skill l'interdit dans ce champ. Il faut décider s'il faut les y ajouter, puisque l'attendu d'un « retrouver » s'affiche au tableau de correction.
2. **Vérifier chaque copie** : `python3 -I docs/audit-prof/outils/verif_attente.py backend/data/courses/en_attente/<deck>.json`. Le résultat attendu est 0 mot absent et 0 diapo hors bloc. Pour les maths, lancer aussi `backend/scripts/verifier_figures_cahier.py`.
3. **Voix** : `python -I backend/scripts/lister_voix_attente.py > voix_attente.json`, puis enregistrer avec la voix Bodi sur le VPS (procédure dans `docs/audit-rythme/README.md`). Ensuite, la copie en attente remplace le cours en ligne.
4. **Décisions en suspens** (détail dans chaque rapport `corrections/`) :
   - RC : Q_max 12 µC ou 120 µC (sujet national 2023 R).
   - Ajouter dans `cadre_reference_2bac_pc.json` les capacités et formules nouvellement enseignées : énergie nucléaire EN9 « applications et dangers », nouvelles écritures du ch1, angles et ensembles de points en complexes.
   - Mettre à jour côté frontend les simulations `bilan.html` et `carte.html` de plusieurs chapitres. Ajouter les états physiques dans les équations dessinées par les simulations du ch13 (eau, base, dosage, exploiter, acidité, comparer).
   - Diapos nouvelles sans visuel, listées dans les rapports.
   - SVT ch2 : le chapitre dit 36 ATP, le ch1 en dit 38.

## Sources des professeurs (non versionnées, à retélécharger si besoin)

- Pr Nidal Naceiri Mrabti, 2 PC partie 1 (physique et chimie) : https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/2PC-Prof-partie%201.pdf
- moutamadris, 2 bac BIOF : `https://moutamadris.ma/wp-content/uploads/2022/07/cours-<Chapitre>-2bac-BIOF-...-N.pdf`. Il faut un User-Agent de navigateur, sinon le site répond 403. Pages de chimie : `resume-et-exercices-...-2bac-svt-biof/`.
- Outils : `outils/dump_cours.py <deck.json> <sortie.txt>` extrait le texte d'un cours (écran, cahier, voix, questions, démonstrations).
