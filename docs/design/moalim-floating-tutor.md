# Professeur flottant Moalim

Voir `moalim-three-ws-integration.md` pour le modèle actuel, ses gestes, le vol, l'écriture au tableau et l'appui sur les simulations.

Le composant AIAvatar est rendu dans un portail hors des conteneurs mis à l'échelle. L'élève peut le déplacer par la poignée (souris, tactile ou flèches du clavier) : cet endroit devient sa place de repos, où il revient après chaque explication. Il se réduit et reste dans la fenêtre après redimensionnement. Son corps laisse passer les clics ; seuls ses deux boutons interceptent les interactions.

Les laboratoires HTML dans une iframe (`iframe[title="Simulation"]`) sont pilotés de la même façon : une commande `simulation_control` du tuteur est mise en file dans `LearningSession` (une à la fois), le professeur demande au laboratoire où est le bouton (`simulation_locate` → `simulation_control_rect`, rectangle en px de l'iframe remis à l'échelle de la page), vole jusqu'à lui, appuie après `PROFESSOR_REACH_MS`, et le message est alors relayé à l'iframe. Sans réponse du laboratoire, il vise l'iframe entière ; professeur réduit ou indisponible, la commande part immédiatement. Le laboratoire des ondes (`media/simulations/physics/progressive`) expose `run_until` et `set_time` pour arrêter la scène à un instant donné, et le statut `paused`.
