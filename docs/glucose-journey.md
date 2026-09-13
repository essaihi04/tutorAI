# Voyage du glucose

Le preset existant `svt_ch1_schema_bilan_annote` utilise désormais
`GlucoseJourneyVisual` : cinq escales, détails à la demande et repère cellulaire.
Le contrat tuteur (`scene`, pas 0 à 21, démarrer/pause/reset/suivant/précédent)
reste inchangé. Aucun moteur, dépendance, image distante ou champ de payload ajouté.

Les pas sont regroupés en glycolyse, entrée des pyruvates, Krebs, chaîne, bilan.
Les boutons d’escale mettent la lecture en pause ; « Voyager » reprend le parcours.
Le bilan utilise explicitement la convention scolaire du cours : 38 ATP.
Les carbones sont représentés par des pastilles, pas par une formule structurale.

La diapositive `energy_a08_s02` conserve son objectif, sa question et sa narration,
avec un texte écrit allégé. Seul ce preset bénéficie de la zone visuelle élargie.

## Vérification

- `node frontend/scripts/test-glucose-journey.mjs` : conservation des six carbones,
  bilan ATP, rendements, navigation des cinq escales et raccord au cours.
- Depuis `frontend` : `npm run build` et contrôle ESLint des deux nouveaux fichiers TS/TSX.
- Depuis `backend` : `python -m pytest app/tests/test_scientific_visual_skill.py -q`.
- Banc léger : `/visual-lab.html?scene=glucose-journey`.
- Lecteur réel : `/dev/course-player?scene=glucose-journey`.

Contrôle visuel des cinq escales à 1280 × 720 et de la chaîne avec détails à
390 × 720. Les deux échecs de la suite générale `test_course_player.py`
concernent la durée totale du chapitre (299 contre 295) et la réponse de
`energy_a02_s01`, non modifiées par ce changement.
