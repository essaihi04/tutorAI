# phys_ch12_etat_equilibre — comparaison avec le cours de référence d'un professeur

Source : cours polycopié d'un professeur marocain (2ᵉ Bac SP, 2022/2023), leçon 4 de chimie (pages 87 à 90). Résumé et comparaison avec nos mots ; le texte du professeur n'est pas reproduit.

## Plan du professeur (ordre des notions, en une liste courte)
1. Porte d'entrée : un système limité finit dans un état d'équilibre ; on annonce une constante K ; trois questions (qu'est-ce que K, comment la trouver, de quoi dépend-elle).
2. Quotient de réaction Qr : définition, forme générale avec exposants, sans unité ; solides absents ; eau solvant remplacée par 1.
3. Exemples en milieu homogène (acide + eau, acide + base, une oxydoréduction), puis hétérogène (précipitation, réactions avec un solide).
4. Qr à l'équilibre, noté avec x_éq.
5. Rappel juste avant usage : conductance G = I/U, G = k·σ, σ = Σλᵢ[Xᵢ].
6. Activité : trois solutions d'acide éthanoïque de concentrations différentes, σ mesurée, tableau d'avancement, [H₃O⁺]éq puis Qr,éq : même valeur pour les trois.
7. Constante d'équilibre K = Qr,éq : sans unité, ne dépend que de la température, pas de l'état initial ; valeurs pour trois acides.
8. Facteurs du taux d'avancement final : l'état initial (plus dilué, τ plus grand), puis K (même C, K plus grand, τ plus grand), avec la relation entre K, C et τ à démontrer.
9. Si K dépasse 10⁴, la transformation est considérée comme totale.

## Porte d'entrée et rappels : où le prof les place, et nous
- **Porte d'entrée.** Prof : on annonce K et on pose trois questions. Nous : rappels (2-6), puis « τ change avec C, un nombre ne change-t-il pas ? » (7). **Notre entrée est meilleure** : elle fait sentir le besoin d'un nombre constant avant de le nommer. Notre audit le disait déjà.
- **Rappel de l'équilibre dynamique.** Le prof le suppose connu (il termine la leçon précédente). Nous le rappelons en 8, après la diapo 6 qui parle déjà de x_éq. **Le prof ne contredit pas le défaut 2 de notre audit** (couper la diapo 6 et placer le rappel 8 avant) : chez lui, l'équilibre est la toute dernière notion vue, donc présente à l'esprit.
- **Rappel conductimétrie.** Le prof le place juste avant l'activité qui mesure σ. Nous aussi (36 avant 37). Même choix, bon.
- **Rappel dilution.** Le prof n'en fait pas ; nous oui (47), juste avant son usage. À garder.

## Différences d'ordre qui comptent
| Notion | Place chez le prof | Place chez nous (diapo) | Ce qu'il faut changer chez nous |
|---|---|---|---|
| K découvert par une mesure | Conductimétrie sur trois concentrations | pH sur trois concentrations (27), conductimétrie plus loin (36-38) | Rien d'obligatoire : notre chemin par le pH réutilise τ = 10^(−pH)/C. Pour la conductimétrie (37-38), dire en tête « même idée que la diapo 27, autre appareil ». |
| Qr,i | Absent de cette leçon | Diapos 14-21 | Garder (le national le demande : piles, mélanges). Le prof confirme seulement que ce n'est pas le cœur de la leçon. |
| K employé dans un sujet avant sa définition | — | 2017 N, diapo 18 (K = 10²⁰⁰), K défini en 29 | Dire en 18 « K : on la définit dans quelques diapos ». **Confirme le défaut 4** (le prof ne nomme K qu'après Qr,éq). |
| Dépendance de τ à C et à K | En dernier, après K | Constaté en ch11 (38-39) puis expliqué ici (48-52) | Garder l'ordre ; ajouter au début de la diapo 48 le rappel du constat du ch11. |
| Question « de quoi dépend τ ? » | Après les deux facteurs | Bloc `ee_b10` après 49, avant que K soit relié à τ (50-51) | Supprimer `ee_b10`. **Confirme le défaut 7.** |

## Ce que le prof explique et que nous n'expliquons pas (ou mal) — avec la diapo où l'ajouter
- **La conductance G = I/U.** Le prof rappelle d'où vient G (courant sur tension) avant G = k·σ. Nous donnons G = k·σ directement (diapo 36, et ch10 diapo 22). Ajouter « G = I/U : la conductance mesure la facilité à laisser passer le courant » en 36.
- **L'eau solvant « vaut 1 ».** Le prof dit qu'on remplace sa concentration par 1. Nous disons « elle n'apparaît pas » (11). C'est la même chose ; la formulation du prof aide à comprendre pourquoi l'eau produit d'une estérification, elle, apparaît (55). Ajouter une ligne en 11 : « elle n'apparaît pas car elle est le solvant ; si l'eau n'est pas le solvant (estérification), elle apparaît ».
- **Exemples de réactions hétérogènes variées.** Le prof en donne trois (précipitation, solide qui réagit, solide formé). Nous en avons un dans la diapo 12, plus la précipitation glissée à la fin (audit, défaut 9). Le prof montre qu'on peut en faire une série d'exemples ; la mettre dans une diapo d'exercice après 13, comme le propose l'audit.
- **K grande, réaction pratiquement totale.** Le prof termine par ce repère, qui fait le lien avec τ. Nous l'avons en 29-30, loin des facteurs de τ. Le redire en 51-52 : « si K > 10⁴, τ ≈ 1 ».

## Définitions et méthodes : formulation du prof vs la nôtre
- **Qr.** Le prof ajoute que la valeur de Qr renseigne sur le sens d'évolution. C'est une notion du semestre 2 (critère d'évolution spontanée) ; nous avons raison de ne pas la dire ici, mais notre carte finale (57) l'annonce bien.
- **K.** Même définition, même propriété (ne dépend que de la température). Conforme.
- **Référence au « chapitre de cinétique » (diapo 10).** Notre audit (défaut 6) dit que le peroxodisulfate n'a jamais été vu. En fait, il a été vu au ch9 (diapo 38, le catalyseur ions fer II), mais pas au ch10. Correction juste : écrire « la réaction du catalyseur, au chapitre des transformations lentes et rapides » plutôt que retirer l'exemple. **Le prof utilise aussi cette réaction dans son cours de cinétique** : l'exemple est légitime.

## Ce que nous faisons mieux (court ; à garder)
- La question qui ouvre le chapitre (τ change, quel nombre reste ?).
- Qr,éq = 10^(−2pH)/(C − 10^(−pH)) et K = C·τ²/(1 − τ) démontrés pas à pas (24, 31), avec le piège « C − 10^(−pH) » (26).
- K' = 1/K pour la réaction inverse (30).
- Les sujets du national, dont 2019 N joué en cinq étapes.

## Corrections recommandées pour notre cours (sans raccourcir le cours)
1. **Diapo 6 :** couper en deux (tableau + x_max ; puis τ) et placer le rappel de l'équilibre (8) avant. (Le prof ne contredit pas le défaut 2 ; chez lui l'équilibre est la notion vue juste avant.)
2. **Bloc `ee_b05` :** le déplacer après la diapo 24. **Bloc `ee_b10` :** le supprimer. (Défauts 1 et 7, cohérents avec l'ordre du prof : notion, puis question.)
3. **Diapo 18 :** annoncer que K sera défini en 29. (Confirme le défaut 4.)
4. **Diapo 10 :** garder l'exemple du peroxodisulfate mais citer le bon chapitre (ch9, diapo 38, le catalyseur). (Corrige le défaut 6 de l'audit.)
5. **Diapo 36 :** ajouter G = I/U avant G = k·σ.
6. **Diapo 11 :** ajouter « l'eau n'apparaît que si elle n'est pas le solvant (estérification, diapo 55) ».
7. **Diapo 48 :** commencer par le rappel du constat du ch11 (« diluer augmente τ ») puis l'expliquer par K. **Diapo 51 ou 52 :** redire « K > 10⁴ : τ ≈ 1, réaction pratiquement totale ».
8. **Diapos 37-38 :** une phrase d'entrée « même idée que la diapo 27 (trois concentrations, même Qr,éq), avec un autre appareil ».
