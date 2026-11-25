# La révision des trois chapitres n'est PAS à écrire (25/11/2026)

Demande de l'utilisateur : la révision `tc_tcf_revision` est construite uniquement avec les diapos déjà faites dans les
trois cours, « sans rien générer » (aucun texte nouveau, aucune voix nouvelle). Elle est produite par
`python -X utf8 scripts/tcf/assembler_revision.py` (choix des 31 diapos dans `DIAPOS`), relancé après la pose des voix
des cours ; `--verifier` signale toute diapo sans voix ou tout MP3 absent.
Une session cloud qui écrirait une révision de diapos nouvelles doit s'arrêter : ne pousse ni `tc_tcf_revision.json`
ni `RAPPORT_tc_tcf_revision.md`, ne lance aucun lot de voix.
