# Rapport — cours /TCF « Synthèse d’une espèce chimique » (`tc_chim_synthese`)

Session cloud du 25/11/2026, branche `tcf-cours`. Contenu : section « Synthèse d’espèces chimiques » de
`docs/tcf/CONTENU_LIVRE.md` ; prérequis (espèce chimique, transformation, CCM, Rf, masse volumique) enseignés de zéro.

## Fichiers

- Cours : `frontend/src/publication/tcf/cours/tc_chim_synthese.json` ; voix : `tc_chim_synthese_voix.json`
  (écrite par `scripts/tcf/lister_voix_tcf.py`).
- Générateur du cours (à relancer après toute retouche, il contrôle que chaque `mot` est un extrait exact du texte parlé
  et qu’aucun chiffre ni symbole n’est dans la voix) : `scripts/tcf/synthese/{outils,partie1,partie2,construire}.py`
  → `python -X utf8 scripts/tcf/synthese/construire.py`, puis `lister_voix_tcf.py`.
- Simulations `frontend/public/media/simulations/chimie/tc_synthese-tableau/` :
  - gardées de l’agent interrompu, relues et corrigées : `commun.js` (ballon, réfrigérant, montage, plaque… un seul
    dessin par objet), `notions.html`, `montage.html`, `reflux.html` (deux textes hors cadre corrigés, repère des gouttes
    pendant l’observation), `traitement.html`, `constantes.html` ;
  - ajoutées : `ccm.html` (10 vues : principe, dépôt, élution, révélation, compter, identifier, rf, rf_eleve,
    application, application_rf), `bilan.html` (fiche « Ce qu’il faut retenir » et carte, avec imprimer et acquis),
    vues `situation` et `tri` de `notions.html`, vue `application` de `montage.html` ; dans `commun.js` : crayon,
    règle graduée, flacon de diiode.

## Le cours en chiffres

38 diapos, 5 séances, 13 blocs, 8 compétences (25 rappels), 11 questions « À toi » (une par bloc d’explication),
3 démonstrations (densité, Rf de X, Rf de B), 2 observations (reflux, chromatogramme de l’application),
146 pistes de voix (38 diapos, 11 énoncés, 55 réactions, 3 démonstrations, 14 pistes d’observation, 25 rappels).

## Ce qui est couvert (et comment)

- Ouverture et situation problème (reproduire / créer une espèce ; trois questions du chapitre).
- Rappels de zéro : espèce chimique (eau pure / eau minérale à la loupe), naturelle / synthétique, transformation
  chimique (billes qui se réarrangent).
- Synthèse : définition, réactifs → produit (animation), réactifs et produits du savon.
- Chimie de synthèse : nécessité, trois types (un dessin chacun : usine et plastiques, peintures, médicaments), puis
  une deuxième fois autrement (classer des objets du quotidien par quantité) + question.
- Savon : montage construit pièce par pièce et nommé (eau froide en bas → en haut) ; contenu du ballon avec la sécurité
  (soude corrosive : lunettes, gants) ; rôle de l’éthanol et de la pierre ponce (avec / sans, animé) ; rôle du
  chauffage (à froid / chauffé, barre de savon formé) ; reflux animé (ébullition, vapeurs, condensation sur les boules,
  gouttes qui retombent) avec question d’observation ; deuxième explication par trois montages (à froid, sans
  réfrigérant : perte, à reflux) ; traitement (refroidir, eau salée concentrée, précipitation, filtration, étapes).
- Identification : constantes physiques (température de fusion par le tuteur, ébullition par l’élève ; solubilité ;
  ρ = m/V puis d = ρ/ρ(eau) par le tuteur, refait par l’élève avec démonstration) ; CCM pas à pas animée (plaque et
  éluant, ligne au crayon et dépôts, cuve fermée, éluant sous la ligne, taches qui migrent, front, révélation UV /
  diiode) ; lecture : compter en allumant, même hauteur = même espèce, Rf = h/H mesuré à la règle (centimètres allumés
  un à un) par le tuteur puis par l’élève, comparaison des solubilités.
- Application de l’acétate de benzyle avec nos valeurs (H = 10 cm, h(A) = 3 cm, h(B) = 6 cm → 0,3 et 0,6) :
  montage numéroté, rôle du reflux, D : 3 espèces, C contient A et B, Rf(B) et l’espèce la plus soluble.
- Bilan (fiche 7 blocs), carte (7 branches), fermeture.

Valeurs simples : ρ = 8 g / 10 mL = 0,8 g/mL ; B : 22 g / 20 mL → d = 1,1 ; plaque 1 : H = 8 cm, Rf(A) = 0,5,
Rf(B) = 0,25 ; X : 6/10 = 0,6.

## Vérifications

- `python -I scripts/verifier_formules.py` (cours et dossier des simulations) : rien à remettre.
- `python -I backend/scripts/verifier_parcours.py` : rien.
- `python -I scripts/verifier_pointage.py` : 0 défaut (les repères des pages « en cases » sont posés par
  `Synthese.cases` ; un commentaire le dit dans chaque page).
- `python backend/scripts/verifier_figures_cahier.py` : 0 erreur.
- Rejeu de chaque diapo dans Chromium (`scripts/tcf/synthese/rejouer_diapos.js`) : chaque pointage, observation, `apres_reponse` et
  `allume` des démonstrations envoyé à la vraie simulation, repères présents à leur mot, aucun moment inconnu ni
  réservé joué trop tôt, aucune erreur console (résultat ci-dessous).
- Captures Playwright de chaque vue (état final) et des moments des vues nouvelles, à 760×420 et 429×250, regardées.
- Le cours joué dans la page /TCF (Vite, `?cours=tc_chim_synthese&diapo=…`) : chargé, simulation affichée et pilotée,
  sans erreur console, à 1280×720 et 724×350. En local, `/media` n’est pas servi sous `/TCF/` par Vite : pour le test,
  les requêtes `/media/…` ont été renvoyées vers un serveur statique de `frontend/public` (comme nginx en ligne).

Résultat du rejeu : 37 diapos à simulation sur 37 sans défaut (`défauts : 0`). Corrigé en route : le repère des gouttes du
reflux (absent pendant l’observation), deux chevauchements au téléphone dans `constantes.html` (table sur le bain,
réponse sur l’éprouvette), deux pointages qui remontaient le temps (application, reflux).

## Ce qui reste douteux

- **Voix** : le corpus de la voix n’a presque aucun mot de laboratoire. Termes du programme gardés, à écouter :
  savon, réfrigérant, vapeurs, éluant, soude, soluble / solubilité, dépôts, CCM, chromatographie, chromatogramme,
  chauffe-ballon, pierre ponce, élévateur, potence, ébullition, corrosive, précipite, entonnoir, diiode, incolores,
  frontal, benzyle / benzylique / l’acétate, benzoïque, cyclohexane, glycérol, magnésium, thermomètre, éprouvette,
  soixante-dix-huit. Darija rare gardée faute de mieux (à écouter) : كيغلي / يغلي, كيذوب / تذوب / ماكيذوبش, كنسخنو,
  كيبردو, صلب, ينشفو, كنسدو, مايتبخرش, كنصفيو, البلبولات, وكيتطرطق, القرعات, الياسمين, البوقال, قهويين, الرصاص.
  Déjà remplacés par des mots fréquents : صاوبنا → درنا, كيطيحو → كيهبطو, كيهربو → كيخرجو, الما المالح → l’eau
  salée, كيوزنو → « la masse ديالهم », كيطفو / كيغطس → كيبقى فوق / تحت.
- **Science** : le glycérol est cité comme deuxième produit du savon (vrai, mais le livre ne parle que du savon) ;
  « 122 °C acide benzoïque » et la table d’ébullition (eau, éthanol, cyclohexane) sont nos exemples, pas ceux du livre.
- **Vues** : à 429×250, les lettres sous la plaque de CCM et les numéros de la règle sont à la limite des 15 px ; les
  fiches et la carte s’écrivent bloc par bloc (il faut le temps de la voix pour tout voir).

## Dernier commit poussé sur `tcf-cours`

`216f1ff1` (cours, voix, simulations et vérifications) ; ce rapport est complété par le commit qui suit.
