# Modèles anatomiques du muscle

Ces cinq modèles originaux sont construits dans Blender 5.2 par
`frontend/scripts/blender/build_muscle_anatomy.py` et exportés en GLB.
Le générateur est la source modifiable ; il écrit aussi
`tmp/muscle-anatomy/muscle-anatomy.blend`, avec une scène par niveau.

Les matériaux et leurs textures de couleur/relief sont inclus dans chaque GLB.
Aucun modèle tiers ni aucune texture téléchargée n'est utilisé.
Les objets sont regroupés par identité anatomique pour limiter les appels de dessin.
Les métadonnées `anatomical_label` et `cover` permettent l'identification au clic
et l'ouverture de la coupe sans recharger le fichier.

Il s'agit d'une illustration anatomique pédagogique, sans échelle commune entre
les vues. Les quantités de fibres et de protéines sont réduites pour la lisibilité.
Les couleurs microscopiques sont conventionnelles. Le réticulum et la géométrie
moléculaire sont simplifiés, et ne constituent pas une reconstruction expérimentale.

Repères anatomiques : OpenStax, Anatomy and Physiology 2e, 10.2 Skeletal Muscle :
https://openstax.org/books/anatomy-and-physiology-2e/pages/10-2-skeletal-muscle

Validation navigateur : `frontend/scripts/test-muscle-structure.mjs`.
