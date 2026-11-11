# Deuxième analyse des vidéos sur les ondes : autre méthode, nouvelles pistes (7 novembre 2026)

## Méthode, différente de la première lecture par grille

1. **Commentaires des élèves sous les 23 vidéos**, y compris les 5 sans sous-titres. Ce sont 4 770 commentaires, dont 419 retenus comme questions ou incompréhensions. C'est une source nouvelle : elle montre où les élèves bloquent, dans leurs propres mots.
2. **Phrases marquées extraites des 10 transcriptions** : 734 phrases de mise en garde, de renvoi au bac, de question à la classe, d'image ou analogie, et de méthode. Deux lecteurs les ont triées en parallèle :
   - `pistes-nouvelles-A.md` (mises en garde, renvois au bac, questions à la classe) ;
   - `pistes-nouvelles-B.md` (images et méthodes).
3. **Mesure du temps passé par notion : abandonnée.** La reconnaissance vocale écrit les termes français en lettres arabes (« أوند ميكانيك »), si bien que 77 % du temps n'était pas attribuable. On ne donne pas de chiffres faux.

Erreur corrigée en cours de route : mon script avait mélangé les noms des profs dans les extraits. Les deux lecteurs l'ont repéré, et les fichiers ont été régénérés avec la bonne table.

## Ce qui est entré dans `experience_profs.json`

Tout a été vérifié contre le programme. Rien ne relève du chapitre suivant ni du hors-programme.

**9 pièges nouveaux :**
- τ confondu avec θ ;
- θ appelé « période » et L appelé « λ » ;
- θ mesuré sur la seule partie en cloche ;
- images comptées au lieu des intervalles ;
- temps de l'écho doublé ;
- 0,4 écrit pour 40 ms ;
- y_S(t) = y_M(t + τ) rejetée ;
- aspect dessiné depuis la source ;
- « retard impair ».

**4 cas types nouveaux :**
- chronophotographie à 25 images/s (Laksabi dit que c'est tombé au national, sans dire quelle année : à vérifier) ;
- dessiner l'aspect à une date t ;
- source qui démarre à t₀ ;
- formule de célérité donnée par l'énoncé (v = √(g·h)).

**5 images validées :**
- le trajet en voiture, pour le signe de τ ;
- Casa–Rabat à 120 et à 50 km/h, pour le cas « deux milieux » ;
- « Salam » qui met environ 30 ms à traverser la classe ;
- le son en 3D (« à côté, en haut, en bas ») ;
- le mur des voisins et l'écoute sous l'eau.

**1 « ne dis pas » :** définir la dimension par le mouvement du point en x et y (Laksabi). C'est faux : la dimension compte les directions de propagation.

**21 questions d'élèves, avec la réponse juste** (nouveau champ `questions_eleves`). Le tuteur reçoit les deux questions les plus proches de ce que l'élève demande. Exemples :
- l'onde, est-ce la déformation ?
- pourquoi double-t-on la distance et pas le temps ?
- θ, est-ce la période ?
- aspect ou élongation, quand l'axe manque ?
- les vagues de la mer ne transportent-elles pas de l'eau ?
- quand sert la sensibilité verticale ?
- je comprends le cours mais je bloque aux exercices.

## Signaux généraux tirés des commentaires (pour le produit, pas pour la fiche)

- **Demande n°1 : des exercices.** De nombreux élèves écrivent « je comprends le cours mais pas les exercices ». C'est le lien cours → exercice qui manque. Les règles « cas type par mot-code » et « double lecture de l'énoncé » répondent exactement à cela.
- **« Tu vas trop vite »** revient chez plusieurs profs. La pause du professeur après chaque bloc est justifiée.
- **La langue.** Les élèves BIOF bloquent sur les termes français et demandent une traduction. La voix en darija avec les termes en français est le bon choix ; un petit lexique arabe-français serait utile.
- **Le son de la vidéo** est souvent critiqué : la qualité audio de la voix compte.

## À trancher

- **La synthèse de la première analyse recommandait de dire « rigidité et inertie »**, alors que la fiche JSON exclut « rigidité ». Recommandation : s'en tenir aux facteurs de perimetre.json (nature du milieu, température, tension et masse linéique, profondeur). Le cours exemple suit déjà cette ligne.
- **Taousse affirme que √(T/μ) « tombe au national ».** Ce n'est pas confirmé sur les 10 nationaux dépouillés ; ce n'est pas repris.
