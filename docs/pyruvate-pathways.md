# Carrefour du pyruvate

La diapositive `energy_a10_s01` conserve son URL et son identifiant de simulation
`ordre_respiration_svt`. Elle remplace le classement de cartes par un trajet SVG
piloté par la présence d’O₂ et l’activité mitochondriale. Le bouton pas à pas
permet une lecture sans lecture automatique ; la préférence de réduction des
animations est respectée. L’explication SVG reste accessible sans animation.

Le modèle suit seulement les deux NAD⁺ de la glycolyse. Il sépare artificiellement
la formation des produits et la régénération du NAD⁺ pour faire observer leur
couplage. Le second glucose est bloqué avant le recyclage, puis peut entrer dans
la glycolyse. Les variantes terminées restent acquises lorsque les conditions
changent ; la remise à zéro les efface. La progression atteint 100 % après un
parcours respiratoire et un parcours fermentaire, chacun avec recyclage.

Les déshydrogénases transfèrent les hydrogènes/électrons ; la coupure du dérivé
hexose en deux trioses est catalysée par l’aldolase. Les navettes transmettent les
équivalents réducteurs du NADH cytoplasmique à la respiration. Références :
[Molecular Biology of the Cell](https://www.ncbi.nlm.nih.gov/books/NBK26882/),
[compartimentation du NAD⁺](https://pmc.ncbi.nlm.nih.gov/articles/PMC6657305/).

La fermentation n’ajoute pas d’ATP aux deux ATP nets glycolytiques. La voie
respiratoire indique un rendement élevé sans imposer ici un rendement universel.
Les carbones restent visibles : glucose C6, deux pyruvates C3, deux lactates C3,
ou deux éthanols C2 accompagnés de deux CO₂.

Prévisualisation locale : `/dev/course-player?scene=pyruvate`.
Test navigateur : `node frontend/scripts/test-pyruvate-pathways.mjs`.
Le test accepte `PLAYWRIGHT_MODULE`, `CHROMIUM_PATH` et `TEST_BASE_URL` pour les
runtimes externes. Les commandes du tuteur et le message final `finished` sont
vérifiés, ainsi que les boutons, le blocage NAD⁺, les variantes et les petits écrans.
