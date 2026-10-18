# Professeur Moalim animé

**Statut : personnage de dessin animé en ligne.** Il remplace le modèle Avaturn (octobre 2026), lui-même successeur du modèle reconstruit à partir du portrait.

## Modèle

`frontend/public/media/avatar/moalim-professeur.glb` (0,98 Mo) est produit par `tools/prepare_moalim_cartoon.py` à partir de `ProfessorManaosTechBehance.blend`, contenu dans l'archive `cartoon-teacher-model.zip` fournie par l'utilisateur. Le fichier source n'est pas versionné ; sa licence d'utilisation doit être confirmée auprès de son auteur avant tout usage commercial.

- Vieux professeur à grosses lunettes, cheveux et moustache blancs, gilet ; 11 matériaux en couleurs unies, sans texture.
- Squelette de 48 os renommés en noms humanoïdes standard (`Hips`, `Head`, `LeftArm`, `RightHandIndex1`…), plus `Nose`, `Moustache`, `BrowLeft`, `BrowRight`. Quatre doigts de trois phalanges par main.
- Deux animations découpées dans l'animation source, sans l'apparition ni la disparition : `Idle` (4 s, bras le long du corps) et `Talking` (8,4 s, gestes et coucous). Les gestes source montent le bras en une seule image (plus de 900°/s) : `Talking` est lissé (gaussienne de 3 images, en boucle) pour rester sous 480°/s, sinon le personnage semble clignoter. Ces gestes agitaient aussi les deux bras jusqu'au-dessus des épaules toutes les une à deux secondes : en parlant, épaules, bras, avant-bras, mains et doigts restent en pose de repos ; corps, jambes et sourcils gardent l'animation source. Le pointage et l'écriture orientent le bras depuis l'application, indépendamment du clip.
- Les matériaux sources ont deux sorties ; le script active la sortie Principled, sinon l'export perd les couleurs.
- Il n'a ni bouche ni lèvres sous la moustache : la voix fait parler la moustache, comme dans un dessin animé.
- Pas d'os pour les yeux : ce sont deux disques blancs avec un dôme noir (la pupille) devant. Le script crée cinq formes (`eyesClosed` : la pupille s'aplatit en trait, `lookLeft`/`lookRight`/`lookUp`/`lookDown` : la pupille se déplace de 2 cm), exportées sans normales pour rester sous 1 Mo.

`moalim-professeur.png` est un rendu du même modèle en pose de repos, utilisé pendant le chargement et en secours.

Pour régénérer :

```bash
blender --background --disable-autoexec --python tools/prepare_moalim_cartoon.py -- chemin/vers/ProfessorManaosTechBehance.blend
```

## Comportement

Tout est dans `frontend/src/components/session/Professor3D.tsx` et `AIAvatar.tsx`.

- **Cadrage** : le personnage est recentré et cadré automatiquement ; ses épaules et la longueur de son bras sont mesurées et transmises à l'enveloppe, qui s'en sert pour viser.
- **Parole** : mélange progressif `Idle` → `Talking` (une pause de moins de 0,8 s entre deux phrases ne rebascule pas) ; la moustache (réduite à 85 % pour rester dans le visage) se soulève jusqu'à 0,55 rad à chaque syllabe, calée sur la latence de sortie audio, avec une vitesse plafonnée pour glisser d'une position à l'autre sans saut (`syllableEnvelope.js`) ; les sourcils accompagnent.
- **Réflexion** : un sourcil levé, tête inclinée, regard en l'air.
- **Regard** : vers l'élément montré, sinon vers l'élève avec un coup d'œil de côté toutes les 3 à 7 s ; un grand changement de direction déclenche un clignement ; la tête accompagne un peu le regard. Clignement toutes les 3 à 7 s.
- **Respiration** : tête et épaules se soulèvent de quelques millimètres en continu.
- **Mains en parlant** : gestes procéduraux à la taille (avant-bras, paumes, doigts), le clip ne bougeant pas les bras ; francs quand il explique sans rien montrer ni écrire, plus discrets pour le bras libre pendant un pointage ou l'écriture.
- **Pointage** : l'épaule puis le coude s'orientent vers l'élément montré, l'index se tend ; la cible glisse d'un élément au suivant et reste en place pendant que le bras redescend.
- **Vol** : ressort amorti, élévation et inclinaison dans le sens du vol, jambes qui traînent, flottement à l'arrêt, retour à la place choisie par l'élève après 1,6 s sans cible.
- **Écriture au tableau** : il flotte juste sous la ligne en cours, tête comprise, et écrit au bout d'une fine baguette qui part de sa main jusqu'à la plume ✍️ (masquée tant qu'il écrit).
- **Simulation** : il vole jusqu'au bouton de la commande (`data-professor-control`), tend l'index et appuie ; la commande part après `PROFESSOR_REACH_MS` (850 ms), avec une onde de clic.
- À chaque image, tous les os reviennent à la dernière pose écrite par le mixeur avant l'animation, sinon les gestes ajoutés s'accumuleraient (la tête finissait par tourner sur elle-même). Pas à la pose de référence (bras en croix) : three.js ne réécrit un os que si sa valeur animée change, et pendant une pose tenue l'os restait en croix, ce qui faisait sauter bras et mains par à-coups (`tests/avatar-held-pose.test.mjs`).

## Synchronisation audio

Le moteur audio est `LipSyncAnalyser` du dépôt https://github.com/nirholas/three.ws, commit `800052ed822a409b6177c61b176a1bd6607fec0f`, sous licence Apache-2.0, copié sans modification dans `frontend/src/vendor/three-ws` avec sa licence. Il analyse l'audio réellement joué, sans second lecteur.

## Vérifications

- `node --test tests/syllable-envelope.test.mjs` : sur de vrais enregistrements, ouvertures syllabe par syllabe, sans blocage ni saut d'une image à l'autre ; fermeture au silence ; retard de latence.
- `node --test tests/avatar-lipsync.test.mjs` : moteur audio ; squelette, doigts, moustache, sourcils, clips `Idle` et `Talking`, GLB autonome de moins de 3 Mo.
- Compilation TypeScript, ESLint et construction Vite.
- Navigateur : la voix d'un vrai enregistrement de cours soulève la moustache ; le corps reste droit en parlant et en pointant ; écriture sous la ligne avec la baguette ; vol vers la scène et appui.
