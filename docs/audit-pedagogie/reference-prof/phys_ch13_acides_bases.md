# phys_ch13_acides_bases — comparaison avec le cours de référence d'un professeur

Source : cours polycopié d'un professeur marocain (2ᵉ Bac SP, 2022/2023), leçon 5 de chimie (pages 91 à 102). Résumé et comparaison avec nos mots ; le texte du professeur n'est pas reproduit.

## Plan du professeur (ordre des notions, en une liste courte)
1. Porte d'entrée : l'eau d'une piscine dont le pH doit rester dans une fourchette ; comment ajuster ces valeurs ?
2. L'eau pure conduit un peu le courant et a un pH de 7 : d'où viennent ses ions ? L'eau est un ampholyte : autoprotolyse, très limitée.
3. Produit ionique Ke (constante d'équilibre de l'autoprotolyse), pKe ; ne dépend que de la température.
4. Échelle de pH : acide, neutre, basique, démontrés à partir de Ke (pH < pKe/2, = pKe/2, > pKe/2).
5. Constante d'acidité Ka, pKa ; puis tout de suite la relation pH = pKa + log([A⁻]/[AH]), démontrée.
6. Comportement des acides : même concentration, l'acide qui a le pH le plus bas a le τ le plus grand et le Ka le plus grand.
7. Comportement des bases : même chose avec [HO⁻] obtenue par Ke ; la base la plus dissociée a le pKa le plus grand ; constante de la réaction d'une base avec l'eau = Ke/Ka.
8. Diagramme de prédominance (trois cas autour du pKa), puis diagramme de distribution (pourcentages ; 50 % au pKa).
9. Indicateurs colorés : couple HInd/Ind⁻, teinte acide sous pKa − 1, teinte basique au-dessus de pKa + 1, zone de virage entre les deux.
10. Constante d'une réaction acide-base K = Ka₁/Ka₂.
11. Titrage : définition (espèce titrée, espèce titrante), qualités de la réaction (rapide, totale, unique), équivalence (définition, réactif limitant avant et après), repérage (pH, σ, couleur).
12. Titrage pH-métrique d'un acide par la soude : équation, tableau, relation d'équivalence, courbe en trois parties, K de la réaction de titrage, τ calculé avec un point de la courbe pour montrer qu'elle est totale.
13. Titrage d'une base par un acide : même plan, courbe qui descend.
14. Repérer l'équivalence : tangentes parallèles ; dérivée (maximum pour un acide titré, minimum pour une base titrée).
15. Titrage colorimétrique : choisir l'indicateur dont la zone de virage contient pH_E ; tableau d'indicateurs.

## Porte d'entrée et rappels : où le prof les place, et nous
- **Porte d'entrée.** Prof : une situation concrète (piscine), puis l'eau pure : « elle a un pH de 7 et conduit un peu ; d'où viennent ses ions ? ». Nous : diapo 5, trois liquides, trois pH, et le BBT. **Le prof confirme l'idée de notre audit** (défaut 10 : ne pas employer le BBT avant de l'expliquer) : sa question d'entrée porte sur l'eau pure seule et ne demande rien d'inconnu.
- **Rappel de la constante d'équilibre.** Le prof ne la rappelle pas : elle termine la leçon précédente. Nous définissons Ke comme « constante d'équilibre » (9) avant le rappel de K (13). **Le prof ne contredit pas le défaut 4 de notre audit** : chez lui la notion est fraîche ; chez nous, après plusieurs diapos, un rappel avant la diapo 5 reste nécessaire.
- **Rappel « soude ».** Le prof ne s'en sert pas avant de l'avoir présentée. Nous l'utilisons en 8, présentée en 14. **Confirme le défaut 7.**
- **Rappel K avant le titrage.** Le prof place K = Ka₁/Ka₂ juste avant le titrage, puis l'applique aussitôt à la réaction de titrage. Nous plaçons K en 27-31, onze diapos avant le titrage (41), mais la diapo 41 recalcule K = Ka/Ke : le rappel juste avant usage est donc fait. Pas de changement nécessaire.

## Différences d'ordre qui comptent
| Notion | Place chez le prof | Place chez nous (diapo) | Ce qu'il faut changer chez nous |
|---|---|---|---|
| pH = pKa + log([A⁻]/[AH]) | Juste après Ka, avant de comparer acides et bases | Diapo 32, après la comparaison (24-26) et K (27-31) | Rien d'obligatoire : notre comparaison passe par τ, sans la relation. Mais citer la relation dès la diapo 20 (« on la démontrera en 32 ») aide à relier Ka et pH. |
| Acide / neutre / basique | Démontré à partir de Ke | Diapo 10 énoncé, 11 démontré | Même ordre que le prof, en deux temps : bien. |
| Les mots « fort » et « faible » | Le prof les emploie de façon relative (« plus dissocié ») | Utilisés en 15 et 47 sans définition | Définir (voir plus bas). **Confirme le défaut 6**, avec une précision : il faut deux sens distincts. |
| Qualités de la réaction de titrage et τ du titrage | Juste avant le titrage pH-métrique, puis τ calculé sur la courbe | Diapo 41 ; mais le bloc `ab_b12` les demande après 39 | Déplacer le bloc après 42. **Confirme le défaut 2.** |
| Tangente : rappel | Pas de rappel (supposée connue) | Rappel en 45, après l'usage en 44 | Mettre 45 avant 44. **Confirme le défaut 8.** |
| Repérage de l'équivalence par σ | Annoncé avec pH et couleur, dans la définition de l'équivalence | Diapos 51-52 (dosage conductimétrique) | Annoncer les trois repérages (pH, σ, couleur) en 42, puis les traiter. Notion redite. |

## Ce que le prof explique et que nous n'expliquons pas (ou mal) — avec la diapo où l'ajouter
- **La dérivée pour un titrage de base.** Le prof dit : maximum de dpH/dV pour un acide titré, minimum pour une base titrée (la courbe descend). Nous disons seulement « abscisse du maximum » (46) ; la diapo 50 (base par un acide) ne parle pas de la dérivée. Un élève qui voit un pic vers le bas au national sera perdu. Ajouter en 50 : « la courbe descend : dpH/dV_A est négative, son extremum est un minimum ».
- **τ de la réaction de titrage lu sur la courbe.** Le prof prend un point avant l'équivalence, lit le pH, calcule le reste de HO⁻ (par Ke) et trouve τ ≈ 1. Nous l'annonçons en 41 et renvoyons le calcul au bloc. Faire le calcul complet sur une diapo après 42 (avec le point V_B = 10 mL de l'exemple J), puisque le national le demande (2024 R, au ch11).
- **Les trois parties de la courbe décrites en mots.** Le prof nomme les trois zones et dit à chaque fois si le mélange est acide ou basique. Notre diapo 43 donne les zones en chiffres ; ajouter « avant le saut : il reste de l'acide, le mélange est acide ; après : la soude est en excès, le mélange est basique ».
- **Constante de la réaction d'une base avec l'eau = Ke/Ka.** Le prof l'écrit en sens direct. Nous l'écrivons sous la forme Ka = Ke/Qr,éq (22). C'est la même relation ; ajouter l'autre écriture à l'écran de 22, car les sujets emploient les deux.
- **Ke indépendant des espèces dissoutes.** Le prof le dit (vrai dans toute solution aqueuse, pas seulement l'eau pure). Nous montrons trois solutions (8) mais l'écran de 9 ne le dit pas. Ajouter « Ke a la même valeur dans toute solution aqueuse à 25 °C ».

## Définitions et méthodes : formulation du prof vs la nôtre
- **Acide fort / faible.** Le prof dit « plus dissocié, donc acide fort » quand il compare deux acides faibles : c'est imprécis (deux sens mélangés). Notre cours n'en donne aucune définition. Proposition conforme au programme, à placer en 24 : « acide fort : sa réaction avec l'eau est totale (τ = 1, ex. HCl) ; acide faible : limitée (τ < 1) ; entre deux acides faibles de même concentration, le plus fort a le Ka le plus grand ». Idem pour les bases (soude forte ; ammoniac, méthylamine faibles) en 25. Ne pas reprendre la formulation du prof.
- **Équivalence.** Prof : les deux réactifs disparaissent ensemble. Nous (42) : proportions stœchiométriques, les deux épuisés. Conforme ; la nôtre est la formulation attendue.
- **Zone de virage.** Même règle (pKa − 1 ; pKa + 1). Conforme.

## Ce que nous faisons mieux (court ; à garder)
- τ de l'autoprotolyse calculé (7) : montre ce que veut dire « très limitée ».
- pKa de l'eau (0 et 14) et l'axe des pKa (23, 26) : le prof ne les a pas.
- pH_E = 7, > 7, < 7 selon le dosage (47) et la demi-équivalence pH = pKa (48) : absents chez le prof.
- Le dosage conductimétrique traité (51-52) ; le sujet 2018 N joué étape par étape.

## Corrections recommandées pour notre cours (sans raccourcir le cours)
1. **Diapo 50 :** ajouter la courbe dérivée d'un titrage de base : l'extremum est un minimum. (Absent de notre cours, présent chez le prof.)
2. **Diapos 24-25 :** définir acide fort / faible et base forte / faible (réaction totale ou limitée avec l'eau), puis la comparaison par Ka entre deux espèces faibles ; redire ces mots en 47. (Confirme le défaut 6.)
3. **Diapo 5 :** porte d'entrée sans BBT : « l'eau pure a un pH de 7 et conduit un tout petit peu : d'où viennent ses ions ? » ; garder les trois béchers pour la diapo 37. (Confirme le défaut 10.)
4. **Avant la diapo 5 :** placer le rappel de K (13). **Avant 8 :** présenter la soude. (Défauts 4 et 7 : le prof ne les contredit pas.)
5. **Après la diapo 42 :** une diapo « la réaction de titrage est totale : on le vérifie sur la courbe » (pH lu avant l'équivalence → [HO⁻] par Ke → τ ≈ 1), puis le bloc `ab_b12`. (Confirme le défaut 2.)
6. **Diapo 42 :** annoncer les trois façons de repérer l'équivalence (pH, conductivité, couleur), traitées en 43-46, 51-52, 49.
7. **Diapo 43 :** dire, pour chaque zone de la courbe, ce qui est en excès et si le mélange est acide ou basique.
8. **Diapos 44-45 :** mettre le rappel de la tangente (45) avant la méthode des tangentes (44). (Confirme le défaut 8.)
9. **Diapo 22 :** écrire aussi K(base + eau) = Ke/Ka. **Diapo 9 :** « Ke a la même valeur dans toute solution aqueuse à une température donnée ».
