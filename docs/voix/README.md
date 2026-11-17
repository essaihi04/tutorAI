# Voix à enregistrer (17 novembre 2026, mise à jour du soir)

Liste produite par `python -I backend/scripts/lister_voix_attente.py --en-ligne > docs/voix/voix_a_enregistrer.json`.
Format : `{cours: [{id, type, texte}]}`. Les cours `en_ligne/…` sont publiés, mais des pistes y manquent encore. En attendant, ils jouent avec la voix en direct.
Types : `diapo`, `demonstration`, `reaction` (réaction préparée), `enonce` (énoncé lu ; sans piste, il est lu par la voix en direct).
Ces fichiers JSON sont ajoutés de force (`git add -f`), car `.gitignore` exclut les `*.json`.

| Cours | Pistes | Diapos | Démonstrations | Réactions | Énoncés | Caractères |
|---|---|---|---|---|---|---|
| math_ch1_limites_continuite | 153 | 0 | 29 | 65 | 59 | 29 834 |
| math_ch2_derivation_etude_fonctions | 175 | 0 | 23 | 95 | 57 | 36 936 |
| math_ch3_suites_numeriques | 130 | 0 | 33 | 54 | 43 | 32 294 |
| math_ch4_primitives | 525 | 0 | 39 | 395 | 91 | 136 925 |
| math_ch5_fonctions_ln | 711 | 0 | 65 | 532 | 114 | 174 785 |
| math_ch6_nombres_complexes | 774 | 0 | 62 | 583 | 129 | 193 495 |
| phys_ch10_cinetique | 457 | 0 | 45 | 340 | 72 | 153 989 |
| phys_ch11_transformations_deux_sens | 295 | 0 | 26 | 220 | 49 | 88 824 |
| phys_ch12_etat_equilibre | 288 | 0 | 32 | 213 | 43 | 103 147 |
| phys_ch13_acides_bases | 462 | 0 | 44 | 348 | 70 | 159 700 |
| phys_ch1_waves_exemple | 192 | 6 | 24 | 133 | 29 | 46 346 |
| svt_ch1_reactions_responsables_liberation_energie | 139 | 15 | 9 | 79 | 36 | 44 287 |
| svt_ch2_role_muscle_strie_squelettique | 150 | 20 | 11 | 83 | 36 | 52 635 |
| svt_ch3_notion_information_genetique | 155 | 15 | 29 | 72 | 39 | 41 110 |
| svt_ch4_relation_gene_proteine | 126 | 12 | 20 | 50 | 44 | 25 655 |
| en_ligne/phys_ch2_ondes_periodiques | 119 | 0 | 10 | 70 | 39 | 27 846 |
| en_ligne/phys_ch3_ondes_lumineuses | 150 | 0 | 12 | 99 | 39 | 38 241 |
| en_ligne/phys_ch4_radioactivite | 131 | 0 | 11 | 85 | 35 | 34 697 |
| en_ligne/phys_ch5_energie_nucleaire | 94 | 0 | 6 | 60 | 28 | 27 172 |
| en_ligne/phys_ch6_dipole_RC | 328 | 0 | 32 | 238 | 58 | 91 902 |
| en_ligne/phys_ch7_dipole_RL | 331 | 0 | 30 | 245 | 56 | 96 379 |
| en_ligne/phys_ch8_circuit_RLC | 344 | 0 | 31 | 256 | 57 | 108 471 |
| en_ligne/phys_ch9_transformations_lentes_rapides | 276 | 0 | 16 | 215 | 45 | 78 699 |
| **Total** | **6505** | **68** | **639** | **4530** | **1268** | **1 823 369** |

## Lot 1 : diapos et démonstrations — `lot_diapos_demos.json`

707 pistes, environ 308 000 caractères. Sans elles, une copie en attente ne peut pas remplacer le cours en ligne.

## Lot 2 : réactions de la physique ch4 à ch8, déjà en ligne — `lot_reactions_phys_ch4_ch8.json`

884 réactions, environ 263 000 caractères : radioactivité 85, noyaux 60, RC 238, RL 245, RLC 256. Poser avec `scripts/voix/poser_en_ligne.py`.

## Procédure

Voir le skill `voix-du-cours` §3 et `docs/audit-rythme/README.md`, « Pour passer en ligne » :
1. Construire les dossiers du lot avec `scripts/voix/attente_construire.py`.
2. Générer les voix Bodi.
3. Les poser avec `scripts/voix/attente_poser.py` (copies en attente) ou `scripts/voix/poser_en_ligne.py` (cours en ligne).
4. Relancer la commande du haut : les pistes posées disparaissent de la liste.
