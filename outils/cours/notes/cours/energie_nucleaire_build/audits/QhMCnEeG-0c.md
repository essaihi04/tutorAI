# Audit QhMCnEeG-0c — Prof Bazhar, exercice 1 « Noyaux, masse, énergie » (national 2020 SN, PC)

## Fiche
- Id QhMCnEeG-0c ; chaîne Prof Bazhar ; 19 min (1141 s) ; 18 229 vues ; publiée en décembre 2023.
- Support : diapos/PDF déjà rédigés (énoncé puis correction toute prête), pointeur jaune, émulateur Casio fx-991ES à l'écran ; voix off en darija, pas de classe.
- Exercice : désintégration α du polonium 210 (national 2020, session normale, 2,5 pts). Données : t½ = 138 jours ; 1 u = 931,41 MeV/c² ; 1 u = 1,66·10⁻²⁷ kg ; diagramme d'énergie chiffré.
- Utile : modèle de la question nationale « lire un diagramme énergétique » (E_lib et E_ℓ tirées du diagramme, puis Δm en kg). Les questions 3-4 relèvent de la décroissance radioactive.

## Ordre des notions
- 00:24 lecture de l'énoncé.
- 01:48 Q1 équation (0,5 pt) : lois de Soddy.
- 03:30 Q2.1 E_lib lue sur le diagramme (≈ 3 min).
- 06:50 Q2.2 défaut de masse en kg (≈ 6 min, le plus long).
- 12:52 Q3 λ en s⁻¹.
- 14:50 Q4 date t₁ en jours (lien avec le chapitre « décroissance radioactive »).
- 18:40 fin.

## Situation d'ouverture
Aucune : énoncé lu tel quel, il rappelle que chaque question vaut 0,5 point au national.

## Diagramme énergétique (cœur de la vidéo)
Tel qu'au tableau : axe vertical E(MeV) ; niveau haut « 126n + 84p » à 1,971820·10⁵ ; niveau ²¹⁰₈₄Po à 1,955372·10⁵ (encadré E_i) ; niveau ²⁰⁶₈₂Pb + ⁴₂He à 1,955318·10⁵ (encadré E_f). Flèche vers le haut du Po vers « 126n + 84p » notée E_ℓ(²¹⁰Po) ; flèche vers le bas du Po vers Pb + He notée ΔE.
Sa méthode orale, très claire : une flèche = un vecteur ; comme en maths (x_B − x_A), on fait toujours « énergie du bout de la flèche − énergie du départ ». D'où ΔE = E_f − E_i (négatif) et E_ℓ = E(nucléons séparés) − E(noyau) (positif). Il rappelle que la ligne du haut contient toujours les nucléons séparés.

## Formules telles qu'écrites
- Q1 : ²¹⁰₈₄Po → ᴬ_ZPb + ⁴₂He ; « Loi de Soddy » : 210 = A + 4, 84 = Z + 2 ⇒ A = 206, Z = 82 ; ²¹⁰₈₄Po → ²⁰⁶₈₂Pb + ⁴₂He.
- Q2.1 : E_lib = |ΔE| ; ΔE = E_f − E_i = 1,955318·10⁵ − 1,955372·10⁵ = −5,4 MeV ; E_lib = 5,4 MeV (encadré). Il dit que ΔE d'une désintégration α ou β est toujours négatif, donc un résultat positif signale une erreur.
- Q2.2 : « L'énergie de liaison : E_ℓ(²¹⁰₈₄Po) = Δm·c² ⇒ Δm = E_ℓ/c² » ; Δm = (1,971820·10⁵ − 1,955372·10⁵)/c² = 1644,8 MeV·c⁻² ; Δm = 1644,8/931,5 = 1,766 u ⇒ Δm = 1,766 × 1,66·10⁻²⁷ ⇒ Δm ≈ 2,93·10⁻²⁷ kg.
- Q3 : λ = ln2/t½ ⇒ λ = ln2/(138 × 24 × 3600) ⇒ λ = 5,81·10⁻⁸ s⁻¹.
- Q4 : a₁ = a₀·e^(−λt₁) ⇒ … ⇒ t₁ = (t½/ln2)·ln(a₀/a₁) ; t₁ = 138/ln2 × ln(3,5·10¹¹ / 3,7·10⁴) = 3197,92 jours ≈ 3198 jours.

## Méthode et raisonnement explicités
- Δm : il commence par dire que la formule du cours Δm = Z·m_p + (A−Z)·m_n − m(noyau) est inutilisable ici (aucune masse donnée), puis cherche « une autre relation contenant Δm » : E_ℓ = Δm·c², avec E_ℓ lue sur le diagramme. Bon réflexe à enseigner : choisir la formule selon les données.
- Il garde c² littéral (« je ne remplace pas c ») pour obtenir des MeV/c², puis conversion en deux étapes : MeV/c² → u (on DIVISE par 931,5, inverse de la multiplication habituelle u → MeV/c²), puis u → kg avec la donnée 1,66·10⁻²⁷.
- Conversion des jours en secondes : × 24 puis × 3600, sans calcul intermédiaire.
- Q4 : il ne convertit PAS t½, puisque la réponse est demandée en jours.

## Courbe d'Aston, bilan par mole/kg, fission/fusion
Absents (exercice de type désintégration α seulement).

## Ce sur quoi il insiste / erreurs signalées
- Le signe : ΔE < 0 pour α et β, E_lib = valeur absolue.
- Lire l'unité de la grandeur demandée (kg, s⁻¹, jours) et convertir en fin de calcul.
- Calculatrice : sans la touche fraction, mettre des parenthèses au dénominateur (138 × 24 × 3600), sinon résultat faux.
- Isoler t dans l'exponentielle : passer au ln, puis le « − » devant le ln inverse la fraction (ln(a₁/a₀) devient ln(a₀/a₁)).

## Erreurs / incohérences
- L'énoncé donne 1 u = 931,41 MeV/c², mais il divise par 931,5 (à l'oral « c'est dans les données ») : écart sans effet sur 2 chiffres significatifs, mais à corriger : utiliser la valeur de l'énoncé.
- À l'oral il appelle Δm « la masse en kg » / « l'énergie en kg » (lapsus).
- Sur la diapo, t₁ = 1/(−λ)·ln(a₁/a₀) : étape correcte mais il passe vite sur le signe.
- À l'oral il lit 3197,92 jours comme « 397,92 » (lapsus) ; diapo juste.
- Rien de hors programme.

## Commentaires d'élèves (14)
Uniquement des remerciements et émojis (12) + la publicité du professeur. Aucune question ni incompréhension signalée.

## Meilleure explication à reprendre
La lecture du diagramme énergétique par analogie au vecteur : « une flèche va d'un niveau à un autre ; sa valeur = énergie à la pointe − énergie au départ ». Ordre à reprendre :
1) repérer le niveau de départ et d'arrivée ;
2) ΔE = E_f − E_i, signe négatif attendu ;
3) E_lib = |ΔE| ;
4) E_ℓ = flèche du noyau vers « nucléons séparés » (toujours en haut) ;
5) Δm = E_ℓ/c² en MeV/c², ÷ 931,5 → u, × 1,66·10⁻²⁷ → kg.
Aussi : « quand la formule du cours manque de données, cherche une autre relation qui contient la grandeur demandée ».
