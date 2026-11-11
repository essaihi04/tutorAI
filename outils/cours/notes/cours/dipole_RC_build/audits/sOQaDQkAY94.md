# Audit — TOP PHYSIQUE CHIMIE (« Si Fouad »), dipôle RC, parties 1 et 2

> Audit établi sur les transcriptions et les commentaires SEULEMENT : les images du tableau n'ont pas été lues
> (extraction en flux lancée mais interrompue avant lecture). Les écritures « telles qu'au tableau » ci-dessous sont
> reconstituées d'après ce que le professeur dicte en lisant ; à confirmer par une passe d'images.

## Fiche
- Partie 1 : sOQaDQkAY94, « dipôle RC 2bac partie 1 », 2018 s (33 min 36), ≈ 608 000 vues, publiée déc. 2024.
- Partie 2 : 1xgsRm7SQI8, « dipôle RC 2bac partie 2 », 1326 s (22 min), ≈ 301 000 vues, publiée déc. 2024.
- Professeur : chaîne TOP PHYSIQUE CHIMIE (appelé « Si Fouad » dans un commentaire). Darija + termes français.
- Support : tableau (écran / tablette d'après la façon de dicter « هنا », « هذا »), sans classe ; cours seul, pas d'exercices.
- Pourquoi elle compte : très forte audience, réputation de « seul prof que je comprends » ; démarche entièrement
  calculatoire, très lente et répétitive sur l'établissement des équations différentielles et la détermination des
  constantes — modèle de « marches » pas à pas.

## Plan horodaté
Partie 1
- 00:00–02:50 Rappel courant : I constant = q/t (coulomb, seconde, conversions mA) ; i variable → minuscule.
- 02:50–07:00 Rappel tension : flèche, lecture « u_AB » de la pointe vers la queue ; générateur idéal de tension
  (u_PN = E, cercle barré) vs réel (E − r·I, évoqué) ; générateur idéal de courant (I₀) ; conducteur ohmique,
  convention récepteur (flèches de i et de u opposées), loi d'Ohm u = R·i.
- 07:00–10:40 Condensateur : deux armatures séparées par un isolant, symbole ; charge : électrons qui quittent une
  armature et s'accumulent sur l'autre → +q / −q ; q du condensateur = charge de l'armature où entre le courant.
  Relation q = C·u_C, C en farad (≈ 4 min).
- 10:40–14:55 Charge à courant constant (générateur de courant idéal) : q = I₀·t ⇒ u_C = (I₀/C)·t, droite ;
  exploitation graphique (coefficient directeur = 2 V/s par deux points) puis identification a = I₀/C ⇒ C = I₀/a.
  Exemple I₀ = 0,2 (unité confuse dans la transcription) ⇒ C = 0,1 F.
- 15:00–17:50 Association : série 1/C_éq = 1/C₁ + 1/C₂ (exemple 10 F + 10 F → 5 F, « la capacité diminue ») ;
  parallèle C_éq = C₁ + C₂ (10 + 10 = 20 F).
- 17:50–21:00 Montage à interrupteur K : position 1 = charge (générateur présent), position 2 = décharge (le générateur
  n'intervient plus, le condensateur joue le rôle de générateur). Oscilloscope : voie Y et masse M, branchement
  pour visualiser u_C ; allure de la charge (monte puis palier) et de la décharge (descend).
- 21:00–23:10 Notion d'équation différentielle (« c'est des maths, vous ne l'avez pas encore vu ») :
  f + a·f′ = constante ; exemple f + 3f′ = 5. Annonce : 3 équations à savoir établir, en q, en u_C, en i, pour la
  charge et la décharge.
- 23:10–31:20 Charge : additivité u_C + u_R = E ; u_R = R·i ; u_C = q/C ⇒ q/C + R·i = E ; × C ⇒
  q + RC·dq/dt = C·E (équation en q). Puis en u_C : q = C·u_C ⇒ u_C + RC·du_C/dt = E. Puis en i : dérivée de
  toute l'équation (E constante ⇒ dérivée nulle) ⇒ i + RC·di/dt = 0 (≈ 8 min : notion longue).
- 31:20–33:30 Décharge : même méthode avec E remplacé par 0 : q + RC·dq/dt = 0 ; u_C + RC·du_C/dt = 0
  (l'équation en i pour la décharge n'est PAS faite — relevé par plusieurs élèves).

Partie 2
- 00:00–01:50 Solution donnée par l'énoncé : u_C(t) = A·e^(−m·t) + B (même forme pour q, u_C, i) ; but : trouver A, B, m.
- 01:50–06:40 Méthode en étapes : dériver la solution ; remplacer dans l'équation ; factoriser par A·e^(−mt) ;
  écrire (B − E) + A·e^(−mt)·(1 − RC·m) = 0 ; « vrai pour tout t » ⇒ chaque terme nul ⇒ B = E et m = 1/(RC).
- 06:40–08:30 A par la condition initiale : condensateur vide à t = 0 ⇒ u_C(0) = 0 ⇒ A + B = 0 ⇒ A = −E.
  Il reconnaît que ça « paraît compliqué » et renvoie aux exercices.
- 08:30–10:10 q(t) = C·u_C(t) = C·E(1 − e^(−t/RC)) ; i(t) = dq/dt = (E/R)·e^(−t/RC).
- 10:10–14:10 Constante de temps τ = R·C ; réécriture des solutions avec τ ; analyse dimensionnelle détaillée :
  [R] = [U]/[I], [C] = [I]·[t]/[U] (depuis i = C·du/dt, « la dérivée ne change pas l'unité ») ⇒ [τ] = temps (≈ 4 min).
- 14:10–16:20 Graphiques de charge : valeur maximale = E (pour u_C), C·E (pour q) ; τ par la tangente à l'origine qui
  coupe l'asymptote ; ou 0,63 × max ; pour i(t) : max E/R, τ à 0,37 × max ou tangente qui coupe l'axe des temps.
- 16:20–20:10 Décharge : q + RC·dq/dt = 0, solution q = A·e^(−mt) + B ⇒ B = 0, m = 1/(RC), q(0) = C·E ⇒ A = C·E ;
  u_C = E·e^(−t/τ) ; i(t) = −(E/R)·e^(−t/τ) (négatif, courbe partant de −E/R et remontant vers 0).
  τ par 0,37 × max ou tangente.
- 21:00–21:55 Énergie emmagasinée : en joules, E_e = ½·C·u_C² et, avec q = C·u, ½·q²/C (passage très bref).

## Rappels (tronc commun / 1re)
Revoit longuement I = q/t et le passage majuscule/minuscule, la lecture d'une flèche de tension, le générateur idéal,
la convention récepteur (i et u en sens opposés pour un récepteur), la loi d'Ohm et la loi d'additivité des tensions,
qu'il présente comme « le point de départ » de toute équation différentielle. i = dq/dt est donné au moment de la charge.

## Définitions (dites)
- Condensateur : deux armatures conductrices face à face séparées par un isolant ; symbole deux traits parallèles.
- Charge q : charge de l'armature par laquelle entre le courant (+q), l'autre porte −q.
- Capacité : C = q/u_C, en farad. Aucun mot sur « échelon de tension » ni définition formelle des régimes
  transitoire / permanent (un élève le reproche : « تدويتي على régime transitoire et permanent »).
- Équation différentielle : relation entre une fonction et sa dérivée.

## Formules (écrites / dites)
q = C·u_C ; i = dq/dt = C·du_C/dt ; u_R = R·i ; u_C + u_R = E.
Charge : q + RC·dq/dt = C·E ; u_C + RC·du_C/dt = E ; i + RC·di/dt = 0.
Décharge : q + RC·dq/dt = 0 ; u_C + RC·du_C/dt = 0.
Solution générale proposée : A·e^(−m·t) + B (lettre m, pas α ni λ), constantes trouvées par identification puis
condition initiale. τ = R·C. u_C = E(1 − e^(−t/τ)) ; i = (E/R)·e^(−t/τ) ; décharge u_C = E·e^(−t/τ), i = −(E/R)e^(−t/τ).
Énergie ½·C·u² = ½·q²/C (symbole non vérifié sur image). Séries/parallèle des condensateurs (voir plan).

## Méthodes graphiques
Tangente à l'origine ∩ asymptote → τ ; 0,63 × valeur max (montée) ; 0,37 × valeur max (descente, i(t) de charge
et grandeurs de décharge) ; pour une décharge, tangente ∩ axe des temps. Pas de 5τ, pas de ln, pas de courbe du/dt = f(u)
entendus dans la transcription.

## Montages
Générateur de courant idéal traité (charge à courant constant, droite u_C = (I₀/C)·t, C tiré du coefficient directeur).
Oscilloscope : voie Y et masse, branchement pour u_C ; pas de discussion « −u_R / inverser » ni d'ExAO.

## Exemples chiffrés, analogies
Coefficient directeur calculé avec deux points (20 ; 10) et l'origine ; C₁ = C₂ = 10 F (valeurs irréalistes,
choisies pour le calcul). Exemple E = 12 V ⇒ B = 12 V. Aucune analogie (ni réservoir, ni seau).

## Insistances, conseils
- « Tenez une feuille avec les relations de base » (u_C = q/C, u_R = R·i, i = dq/dt) et réutilisez-les comme des
  « noyaux ».
- « Retenez les étapes » : dériver → remplacer → factoriser → chaque terme nul → condition initiale.
- Multiplier par C « pour enlever ce qui est au dénominateur ».
- Même logique charge/décharge : on remplace E par 0. Pas de national cité.

## Faux, imprécis ou à ne pas répéter
- Rappel du courant : formule I = q/t présentée comme générale pour un courant constant, ok ; mais confusion orale
  fréquente entre u_C et q ; valeurs de capacité en farads (10 F) irréalistes.
- Décharge : « le générateur n'est plus là donc E = 0 » — formulation à garder mais en précisant que le circuit
  de décharge ne contient pas le générateur.
- Signe de i en décharge donné sans justifier le sens choisi pour i.
- Équation différentielle en i de décharge omise. Rien hors programme (pas de Laplace, pas de régime sinusoïdal),
  mais la notion d'équation différentielle est présentée « avant les maths ».

## Commentaires d'élèves (300 lus, 150 par vidéo)
- Majorité : prières pour le bac (≈ 60 %), remerciements (« seul prof que je comprends », ≈ 25 fois).
- Demandes : cours RL (≈ 25 fois), exercices (≈ 15 fois).
- Difficultés : équation différentielle de i en décharge non faite (4 fois ; réponse donnée par un élève :
  u_C + u_R = 0 ⇒ dériver ⇒ i + RC·di/dt = 0) ; à 14:46 « où est passé t ? » dans C = 0,2/2 (le t se simplifie
  entre u_C = 2t et u_C = I·t/C) ; « pourquoi u_PN = E − r·i » (générateur réel) ; solution donnée sous la forme
  A(1 − e^(−mt)) dans certains exercices ; régimes transitoire/permanent non traités ; « cours dense, beaucoup de
  formules » ; problème de piste audio sur la vidéo.

## Ce que notre cours doit lui prendre
1. L'ordre « additivité → remplacer chaque tension par sa relation de base → éliminer le dénominateur » pour établir
   les équations en q, u_C puis i, avec la feuille des trois relations de base toujours visible.
2. Les cinq étapes de détermination de A, B, m (dériver, remplacer, factoriser, chaque terme nul, condition initiale),
   et la remarque que la forme de solution est la même pour q, u_C, i.
3. La charge à courant constant : droite, coefficient directeur, identification a = I₀/C (et dire explicitement que t se simplifie).
4. L'analyse dimensionnelle de τ via i = C·du/dt et u = R·i.
5. Lecture de τ : tangente, 0,63 (montée), 0,37 (descente) — et y ajouter ce qui manque : décharge en i,
   régimes transitoire/permanent, 5τ, sens du courant en décharge.
