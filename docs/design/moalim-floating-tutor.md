# Professeur flottant Moalim

Voir `moalim-three-ws-integration.md` pour le modèle actuel, ses gestes, le vol, l'écriture au tableau et l'appui sur les simulations.

Le composant AIAvatar est rendu dans un portail hors des conteneurs mis à l'échelle. L'élève peut le déplacer par la poignée (souris, tactile ou flèches du clavier) : cet endroit devient sa place de repos, où il revient après chaque explication. Il se réduit et reste dans la fenêtre après redimensionnement. Son corps laisse passer les clics ; seuls ses deux boutons interceptent les interactions.

Les simulations dans des iframes ne sont pas encore pilotées par ce mécanisme.
