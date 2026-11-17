# Voix à enregistrer (17 novembre 2026)

Liste produite par `python -I backend/scripts/lister_voix_attente.py --en-ligne > docs/voix/voix_a_enregistrer.json`.
Format : `{cours: [{id, type, texte}]}`. Les cours `en_ligne/…` sont déjà publiés, mais des pistes y manquent encore : les nouvelles réactions et démonstrations. Ils jouent en attendant avec la voix en direct.
Types : `diapo` (voix de la diapo), `demonstration`, `reaction` (réaction préparée), `enonce` (énoncé lu ; sans piste, il est lu par la voix en direct).

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
| phys_ch2_ondes_periodiques | 134 | 5 | 20 | 70 | 39 | 35 733 |
| phys_ch3_ondes_lumineuses | 167 | 13 | 16 | 99 | 39 | 48 474 |
| phys_ch9_transformations_lentes_rapides | 290 | 9 | 19 | 217 | 45 | 89 409 |
| svt_ch1_reactions_responsables_liberation_energie | 139 | 15 | 9 | 79 | 36 | 44 287 |
| svt_ch2_role_muscle_strie_squelettique | 150 | 20 | 11 | 83 | 36 | 52 635 |
| svt_ch3_notion_information_genetique | 155 | 15 | 29 | 72 | 39 | 41 110 |
| svt_ch4_relation_gene_proteine | 126 | 12 | 20 | 50 | 44 | 25 655 |
| en_ligne/phys_ch4_radioactivite | 146 | 0 | 20 | 90 | 36 | 40 241 |
| en_ligne/phys_ch5_energie_nucleaire | 112 | 0 | 19 | 65 | 28 | 35 640 |
| en_ligne/phys_ch6_dipole_RC | 342 | 0 | 45 | 239 | 58 | 96 842 |
| en_ligne/phys_ch7_dipole_RL | 347 | 0 | 46 | 245 | 56 | 101 668 |
| en_ligne/phys_ch8_circuit_RLC | 354 | 0 | 41 | 256 | 57 | 113 096 |
| **Total** | **6624** | **95** | **717** | **4543** | **1269** | **1 881 065** |

## Ordre conseillé

1. Les diapos et les démonstrations : sans elles, une copie en attente ne peut pas remplacer le cours en ligne.
2. Les réactions préparées des cours déjà en ligne (physique ch4 à ch8) : le lecteur les utilise tout de suite.
3. Les réactions, puis les énoncés, des copies en attente.

Procédure : skill `voix-du-cours` §3 et `docs/audit-rythme/README.md`, pour le lot Bodi sur le VPS. Après la pose des voix, relancer la commande ci-dessus : la liste doit se vider.
