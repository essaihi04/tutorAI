# Professeur Moalim animé

**Statut : personnage de dessin animé en ligne.** Il remplace le modèle Avaturn (octobre 2026), lui-même successeur du modèle reconstruit à partir du portrait.

## Modèle

`frontend/public/media/avatar/moalim-professeur.glb` (1,06 Mo) est produit par `tools/prepare_moalim_cartoon.py` à partir de `ProfessorManaosTechBehance.blend`, contenu dans l'archive `cartoon-teacher-model.zip` fournie par l'utilisateur. Le fichier source n'est pas versionné ; sa licence d'utilisation doit être confirmée auprès de son auteur avant tout usage commercial.

- Vieux professeur à grosses lunettes, cheveux et moustache blancs, gilet ; 11 matériaux en couleurs unies, sans texture.
- Squelette de 48 os renommés en noms humanoïdes standard (`Hips`, `Head`, `LeftArm`, `RightHandIndex1`…), plus `Nose`, `Moustache`, `BrowLeft`, `BrowRight`. Quatre doigts de trois phalanges par main.
- Deux animations découpées dans l'animation source, sans l'apparition ni la disparition : `Idle` (4 s, bras le long du corps) et `Talking` (8,4 s, gestes et coucous). Les gestes source montent le bras en une seule image (plus de 900°/s) : `Talking` est lissé (gaussienne de 3 images, en boucle) pour rester sous 480°/s, sinon le personnage semble clignoter. Ces gestes agitaient aussi les deux bras jusqu'au-dessus des épaules toutes les une à deux secondes : en parlant, épaules, bras, avant-bras, mains et doigts restent en pose de repos ; corps, jambes et sourcils gardent l'animation source. Le pointage et l'écriture orientent le bras depuis l'application, indépendamment du clip.
- Les matériaux sources ont deux sorties ; le script active la sortie Principled, sinon l'export perd les couleurs.
- Le modèle source n'a pas de bouche : la moustache couvre le bas du visage et le nœud papillon est juste dessous. Le script lui en construit une, cachée derrière la moustache et devant le nœud papillon, rattachée à l'os `Head` : intérieur sombre, langue, dents du haut et lèvre inférieure couleur peau (quatre grilles de 17 × 5 sommets). Fermée, c'est un trait invisible sous la moustache ; ouverte, la lèvre descend sous le bord de la moustache. Six formes : `viseme_aa` (grande ouverture), `viseme_O` (ovale), `viseme_U` (petit rond), `viseme_E` (large), `viseme_I` (large et étroite, dents visibles), `viseme_SS` (dents presque serrées). Chacune est la même grille à d'autres demi-largeur, descente, arrondi et part de dents : les mélanges restent des bouches plausibles.
- Pas d'os pour les yeux : ce sont deux disques blancs avec un dôme noir (la pupille) devant. Le script crée cinq formes (`eyesClosed` : la pupille s'aplatit en trait, `lookLeft`/`lookRight`/`lookUp`/`lookDown` : la pupille se déplace de 2 cm), exportées sans normales pour rester sous 1 Mo.

`moalim-professeur.png` est un rendu du même modèle en pose de repos, utilisé pendant le chargement et en secours.

Pour régénérer :

```bash
blender --background --disable-autoexec --python tools/prepare_moalim_cartoon.py -- chemin/vers/ProfessorManaosTechBehance.blend
```

## Comportement

Tout est dans `frontend/src/components/session/Professor3D.tsx` et `AIAvatar.tsx`.

- **Cadrage** : le personnage est recentré et cadré automatiquement ; ses épaules et la longueur de son bras sont mesurées et transmises à l'enveloppe, qui s'en sert pour viser.
- **Parole** : mélange progressif `Idle` → `Talking` (une pause de moins de 0,8 s entre deux phrases ne rebascule pas) ; la bouche s'ouvre sous la moustache à chaque syllabe et prend la forme du son entendu (voir « Formes de bouche ») ; la moustache (réduite à 85 % pour rester dans le visage) l'accompagne en se soulevant jusqu'à 0,3 rad (0,55 rad pour un modèle sans bouche), calée sur la latence de sortie audio, avec une vitesse plafonnée pour glisser d'une position à l'autre sans saut (`syllableEnvelope.js`) ; les sourcils accompagnent.
- **Réflexion** : un sourcil levé, tête inclinée, regard en l'air.
- **Regard** : vers l'élément montré, sinon vers la souris pendant 8 s après chaque mouvement, sinon vers l'élève avec un coup d'œil de côté toutes les 3 à 7 s ; un grand changement de direction déclenche un clignement ; la tête accompagne un peu le regard. Clignement toutes les 3 à 7 s.
- **Respiration** : tête et épaules se soulèvent de quelques millimètres en continu.
- **Émotions** (`services/professorEmotion.js`) : déduites des mots du tuteur et de l'élève, une fois par message. « Bonjour / Salam » en début de message, ou un simple appui sur sa poignée → coucou de la main et 👋 ; « Bravo / Excellent / Mabrouk » → bras levés en V, petit saut, 🎉⭐✨👏 ; « fier de toi », ❤️, un « merci » de l'élève → mains sur le cœur, ❤️💖💕 ; « presque / réessaie / courage » → hochement, 💪👍 ; « haha / c'est drôle / mdr » → rire (le corps et les épaules sautent, la tête part en arrière, la moustache tremble même sans voix), 😂🤣😄 ; « oh ! / incroyable / waouh » → sursaut, sourcils très hauts, mains levées, 😮❗✨ ; « au revoir / à bientôt » → coucou d'adieu. Il salue aussi à la connexion, et un 🤔 part après 1,5 s de traitement. Au plus 40 émoticônes à la fois. Les émoticônes jaillissent de sa tête, là où il se trouve, et s'envolent (`.moalim-sparks`). Le bras qui pointe ou écrit n'est jamais emprunté par un geste. Le tuteur est informé de ces réactions dans son prompt.
- **Mains en parlant** : gestes procéduraux à la taille (avant-bras, paumes, doigts), le clip ne bougeant pas les bras ; francs quand il explique sans rien montrer ni écrire, plus discrets pour le bras libre pendant un pointage ou l'écriture.
- **Pointage** : l'épaule puis le coude s'orientent vers l'élément montré, l'index se tend ; la cible glisse d'un élément au suivant et reste en place pendant que le bras redescend.
- **Vol** : ressort amorti, élévation et inclinaison dans le sens du vol, jambes qui traînent, flottement à l'arrêt, retour à la place choisie par l'élève après 1,6 s sans cible.
- **Écriture au tableau** : il flotte juste sous la ligne en cours, tête comprise, et écrit au bout d'une fine baguette qui part de sa main jusqu'à la plume ✍️ (masquée tant qu'il écrit).
- **Simulation** : il vole jusqu'au bouton de la commande (`data-professor-control`), tend l'index et appuie ; la commande part après `PROFESSOR_REACH_MS` (850 ms), avec une onde de clic. Même chose pour les laboratoires HTML en iframe, qui localisent eux-mêmes leur bouton (voir `moalim-floating-tutor.md`).
- À chaque image, tous les os reviennent à la dernière pose écrite par le mixeur avant l'animation, sinon les gestes ajoutés s'accumuleraient (la tête finissait par tourner sur elle-même). Pas à la pose de référence (bras en croix) : three.js ne réécrit un os que si sa valeur animée change, et pendant une pose tenue l'os restait en croix, ce qui faisait sauter bras et mains par à-coups (`tests/avatar-held-pose.test.mjs`).

## Synchronisation audio

Un seul bus d'analyse (`services/avatarAudio.ts`) observe l'audio réellement joué, sans second lecteur : la forme d'onde donne l'ouverture syllabe par syllabe (`syllableEnvelope.js`), le spectre donne la forme de la bouche. `LipSyncAnalyser` (dépôt https://github.com/nirholas/three.ws, Apache-2.0, copié sans modification dans `frontend/src/vendor/three-ws`) n'est plus branché : il mélangeait toutes les formes à la fois, proportionnellement à trois bandes.

### Formes de bouche

`services/mouthShapes.js` lit le spectre en décibels sur quatre bandes (250–500, 550–1100, 1500–3000 et 3500–8000 Hz) et en tire trois axes continus : ouverture (« a » contre « i », « ou »), arrondi (« o », « ou »), avant (« i », « é »), plus la friction (« s », « ch », « f »). Indépendant de la langue : français, darija ou arabe, seul le son compte. Les poids d'un instant font au plus une bouche, multipliés par l'ouverture syllabique ; ils changent en douceur (18 par seconde) et sont retardés de la latence de sortie, comme l'ouverture. Un rire ouvre grand (« a »).

Réglage sur la voix française Hortense de Windows : les mots « papa la table », « beau gros mot », « ici midi lit » et « sss » donnent en moyenne « a », « o », « i » et « s » (`tests/fixtures/mouth-shape-frames.json`). « ou » et « é » se confondent plus souvent avec leurs voisins ; « f » ne se distingue pas de « s » dans le spectre, il n'a donc pas de forme à part. Pour une bouche de quelques dizaines de pixels, le mouvement juste compte plus que le phonème exact.

## Vérifications

- `node --test tests/professor-emotion.test.mjs` : détection des émotions dans les mots du tuteur et de l'élève.
- `node --test tests/syllable-envelope.test.mjs` : sur de vrais enregistrements, ouvertures syllabe par syllabe, sans blocage ni saut d'une image à l'autre ; fermeture au silence ; retard de latence.
- `node --test tests/mouth-shapes.test.mjs` : sur les mots mesurés, la forme dominante est la bonne pour « a », « o », « i », « s » ; jamais plus d'une bouche à la fois ; fermeture au silence ; passage en douceur d'une forme à l'autre ; retard de latence.
- `node --test tests/avatar-lipsync.test.mjs` : moteur audio ; squelette, doigts, moustache, sourcils, bouche et ses six formes, clips `Idle` et `Talking`, GLB autonome de moins de 3 Mo.
- Compilation TypeScript, ESLint et construction Vite.
- Navigateur : sur une phrase française synthétisée, la bouche s'ouvre sous la moustache et passe par « a », « i », « é », « o » ; la voix d'un vrai enregistrement de cours soulève la moustache ; le corps reste droit en parlant et en pointant ; écriture sous la ligne avec la baguette ; vol vers la scène et appui.
