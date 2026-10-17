# Professeur Moalim animé

**Statut : modèle Avaturn intégré localement, non déployé.** L'ancien modèle reconstruit à partir du portrait (tête FaceBuilder, corps projeté, variantes Blender) a été retiré du projet le 17 octobre 2026 et envoyé à la Corbeille de Windows.

## Modèle

`frontend/public/media/avatar/moalim-professeur.glb` provient de l'archive `professor-wit-felipe-boton.zip` fournie par l'utilisateur, générée par Avaturn puis Blender.

- Corps entier en costume, lunettes, chaussures ; 4 Mo, fichier autonome.
- Squelette humanoïde standard de 52 os, dont 30 phalanges (noms Mixamo sans préfixe).
- Une animation de repos `IdleV4.2`, de 8 secondes, jouée en boucle.
- **Aucune forme faciale exportée** : la bouche ne suit pas encore la voix, les yeux ne clignent pas. Le composant pilote automatiquement `jawOpen`, `viseme_*` et `eyeBlink*` dès qu'un export Avaturn les contient : il suffit de réexporter avec les blendshapes ARKit ou les visèmes activés et de remplacer le fichier.

`moalim-professeur.png` est un rendu Blender du même modèle avec le cadrage de la vue 3D. Il sert pendant le chargement et en secours si WebGL échoue.

## Comportement

Tout est dans `frontend/src/components/session/Professor3D.tsx` et `AIAvatar.tsx`.

- **Parole** : gestes d'explication sur les vrais os (bras, avant-bras, paumes, doigts), en fenêtres alternées avec des pauses, plus amples quand la voix porte.
- **Réflexion** : tête inclinée, regard vers le haut.
- **Pointage** : l'épaule puis le coude s'orientent vers l'élément montré, l'index se tend et les autres doigts se replient. La ligne de pointage part du bout de l'index.
- **Vol** : le professeur se déplace avec un ressort amorti, s'élève et s'incline dans le sens du vol, les jambes traînent. À l'arrêt, il flotte légèrement. Sans cible pendant 1,6 s, il retourne à la place choisie par l'élève.
- **Écriture au tableau** : quand la plume ✍️ du tableau avance, il vole sous la ligne, la tient de sa main droite et suit le trait. La plume emoji s'efface tant que sa main la remplace.
- **Simulation** : pour une commande de scène, il vole jusqu'au bouton correspondant (`data-professor-control`), tend l'index et appuie. La scène exécute la commande à ce moment-là, après `PROFESSOR_REACH_MS` (850 ms), et une onde de clic part du bouton. Aucun clic synthétique n'est envoyé.
- Le corps reste transparent aux clics ; seule sa petite barre d'outils, discrète, est cliquable. Le mode « animations réduites » du système est respecté.

## Synchronisation audio

Le moteur audio est `LipSyncAnalyser` du dépôt https://github.com/nirholas/three.ws, commit `800052ed822a409b6177c61b176a1bd6607fec0f`, sous licence Apache-2.0, copié sans modification dans `frontend/src/vendor/three-ws` avec sa licence. Il analyse l'audio réellement joué sans second lecteur. Son amplitude règle aujourd'hui l'ampleur des gestes ; elle pilotera la bouche dès que le modèle aura ses formes faciales.

## Vérifications

- `node --test tests/avatar-lipsync.test.mjs` : moteur audio, squelette, phalanges, animation de repos, GLB autonome et léger.
- Compilation TypeScript et ESLint sur les fichiers touchés.
- Navigateur Edge sans interface : chargement, gestes de parole, pointage à gauche et à droite, vol, écriture qui suit la plume, retour à la place, appui sur le bouton d'une scène.
