# Modulation d'amplitude — cours manquant : plan de référence et base pour l'écrire

Source : cours polycopié d'un professeur marocain (2ᵉ Bac SP, 2022/2023), leçon 9 « Transmission d'information — Modulation d'amplitude », pages 62 à 69. Résumé avec nos mots ; le texte du professeur n'est pas reproduit.

## Pourquoi ce cours manque, et ce qu'il coûte
- Le cadre officiel range « transmission d'informations, modulation d'amplitude, démodulation » dans l'électricité (21 % de la note), et la liste des TP officiels contient « modulation et démodulation » (`docs/audit-programme-officiel/physique.md`, étape 1). Nous n'avons **aucun** cours.
- Au national, la modulation est la dernière partie d'un exercice d'électricité dans au moins six sujets que nos cours lisent déjà : 2019 R ex. 3, 2022 R ex. 3, 2023 N ex. 3, 2023 R ex. 3, 2025 N ex. 3, 2025 R ex. 3 (`docs/audit-national/physique.md`). Nos diapos lisent ces énoncés, jouent les parties RC, RL ou RLC, et laissent la partie AM sans réponse.

## Plan du professeur (ordre des notions, en une liste courte)
1. Porte d'entrée : la radio transmet des informations loin ; trois questions (principe de l'AM, comment transmettre vite et loin, comment la radio reçoit et traite le signal).
2. Ondes électromagnétiques : champ électrique et magnétique couplés, célérité c dans le vide et l'air, λ = c/f ; le spectre électromagnétique (γ, X, UV, visible, IR, micro-ondes, radio).
3. Expérience : une antenne émettrice reliée à un GBF, une antenne réceptrice reliée à un oscilloscope ; le signal reçu a la même fréquence ; conclusion : l'onde transporte l'information sans transport de matière, à la vitesse de la lumière.
4. Nécessité de moduler : les signaux sonores (20 Hz à 20 kHz) ne peuvent pas être émis directement — ils s'amortissent vite, les émetteurs se brouilleraient, l'antenne devrait mesurer environ λ/2 (calcul : des dizaines ou centaines de kilomètres).
5. Porteuse haute fréquence et signal modulant basse fréquence ; on module l'amplitude (AM) ou la fréquence (FM) ; chaque émetteur a sa fréquence de porteuse ; chaîne émission → transmission → réception → démodulation.
6. Tension sinusoïdale : u(t) = U_m·cos(2π·f·t + φ), amplitude, fréquence, phase.
7. Le multiplieur (AD633) : deux entrées, une sortie, u_s = k·u₁·u₂.
8. Modulation : porteuse sur une entrée, signal modulant + tension de décalage U₀ sur l'autre ; expression u_s(t) = A·[1 + m·cos(2π·f_s·t)]·cos(2π·f_p·t) ; l'amplitude varie comme le signal ; l'information est dans l'enveloppe supérieure.
9. Taux de modulation : m = S_m/U₀ ; lu sur la courbe : m = (U_max − U_min)/(U_max + U_min).
10. Qualité de la modulation : f_p très grande devant f_s ; U₀ > S_m (m < 1) pour éviter la surmodulation ; en mode XY, une bonne modulation donne un trapèze.
11. Démodulation en deux étapes : détection d'enveloppe (diode, puis R et C en parallèle ; condition T_p ≪ R·C < T_s), puis élimination de la composante continue (R et C en série).
12. Récepteur AM complet : antenne, circuit LC d'accord (on règle L ou C pour que f₀ = 1/(2π√(LC)) égale f_p), amplification, démodulation, amplification, haut-parleur.

## Ordre des notions proposé pour notre cours (une notion jamais avant celle dont elle dépend)
| # | Notion | Dépend de | Rappel à placer juste avant |
|---|---|---|---|
| 1 | Porte d'entrée : on parle dans un micro au studio, une radio à 100 km nous entend ; comment ? | — | — |
| 2 | Le son à transmettre : une tension qui varie, fréquences de 20 Hz à 20 kHz | fréquence, période | Rappel f = 1/T, sinusoïde, amplitude (nos ondes ch2 ; RLC, diapo 26) |
| 3 | Une onde électromagnétique transporte un signal : expérience des deux antennes | λ = c/f, célérité de la lumière | Rappel λ = c/f et c = 3·10⁸ m/s (nos ondes lumineuses, ch3) |
| 4 | Pourquoi on n'émet pas le son directement : taille de l'antenne (calcul λ/2), portée, brouillage | 3 | Puissances de dix et km (rappel court) |
| 5 | L'idée : une porteuse haute fréquence, dont on fait varier l'amplitude au rythme du son | 2, 4 | — |
| 6 | Le multiplieur : u_s = k·u₁·u₂ (constante k, en V⁻¹) | produit de deux tensions | « multiplier deux nombres de signe quelconque » (signe du produit) |
| 7 | Pourquoi ajouter U₀ : sans décalage, l'enveloppe ne ressemble pas au son | 6 | — |
| 8 | Expression de la tension modulée, amplitude A(t) = A·[1 + m·cos(2π·f_s·t)], enveloppe | 6, 7 | Développer et factoriser (maths) |
| 9 | Taux de modulation m = S_m/U₀, puis lecture graphique (U_max, U_min) | 8 | Lire une amplitude sur un oscillogramme (RLC, diapo 38) |
| 10 | Qualité : f_p ≫ f_s, m < 1 ; surmodulation ; trapèze en mode XY | 9 | L'oscilloscope en mode XY (jamais vu : à enseigner ici) |
| 11 | La diode : un seul sens | — | Rappel de la diode (à créer pour le RL, voir `reference-prof/phys_ch7_dipole_RL.md`, correction 1) |
| 12 | Détection d'enveloppe : diode + R, C en parallèle ; le condensateur se charge vite et se décharge lentement | 11, charge/décharge RC | Rappel τ = R·C, « plus τ est grand, plus la décharge est lente » (RC, diapos 48-49, 59) |
| 13 | Condition T_p ≪ R·C < T_s : trop petit, l'enveloppe suit la porteuse ; trop grand, elle ne suit plus le son | 12 | Période et fréquence (2) |
| 14 | Élimination de la composante continue (R et C en série) : on retire U₀, il reste le son | 12 | « un condensateur ne laisse pas passer un courant continu » (RC, régime permanent i = 0, diapo 23) |
| 15 | Choisir la station : circuit LC d'accord, f₀ = 1/(2π√(LC)) = f_p | — | Rappel T₀ = 2π√(LC) et f₀ = 1/T₀ (RLC, diapos 30, 48) |
| 16 | Le récepteur complet : antenne, accord, amplification, démodulation, amplification, haut-parleur | 12-15 | — |
| 17 | Les parties AM des nationaux déjà lus par nos cours, jouées pas à pas | tout | — |

Remarque d'ordre : le prof place le multiplieur avant l'expression de la tension modulée, et la diode seulement à la démodulation ; nous suivons ce choix. Il ne fait aucun rappel ; tous les rappels de la colonne de droite sont les nôtres, pris à nos cours RC, RL, RLC et ondes.

## Prérequis venant de nos cours (à rappeler, pas à réenseigner)
- **RC (phys_ch6)** : τ = R·C ; charge rapide si τ petit, décharge lente si τ grand ; régime permanent : i = 0, le condensateur bloque le continu ; exponentielle e^(−t/τ).
- **RL (phys_ch7)** : la diode (rappel à créer) ; la surtension n'est pas utile ici.
- **RLC (phys_ch8)** : sinusoïde, amplitude, période (diapo 26) ; T₀ = 2π√(LC) et « isoler L ou C : le carré d'abord » (diapos 30, 48) ; lecture d'un oscillogramme et de la sensibilité (diapos 12, 44).
- **Ondes (phys_ch1 à ch3)** : fréquence, période, λ = c/f, célérité de la lumière, spectre.
- **Maths** : produit de deux cosinus (seulement pour le spectre à trois raies, si on le garde) ; développer A·(1 + m·cos x).

## Définitions et formules à écrire exactement (et pièges)
- **Taux de modulation** : m = S_m/U₀ (amplitude du signal modulant sur la tension de décalage), **pas** rapporté à l'amplitude de la porteuse ; c'est une erreur que notre programme a déjà corrigée une fois (`docs/audit-programme-officiel/physique.md`, étape 1 (c)). Lu sur la courbe : m = (U_max − U_min)/(U_max + U_min).
- **Bonne modulation** : m < 1 (U₀ > S_m) et f_p ≫ f_s.
- **Détection d'enveloppe** : T_p ≪ R·C < T_s (formulation des corrigés ; à vérifier sur chaque sujet).
- **Vocabulaire** : le prof parle de « filtre passe-bas » et « passe-haut ». Notre cadre a retiré ces noms (hors programme) et parle de « détection d'enveloppe » et d'« élimination de la composante continue » (`docs/audit-programme-officiel/physique.md`, étape 1 (a)) : écrire ces deux expressions, et citer les noms de filtres seulement comme mots qu'un élève peut croiser.
- **Spectre à trois raies et méthode du trapèze** : gardés dans notre périmètre « à confirmer » ; le prof cite le trapèze (mode XY), pas le spectre. Faire le trapèze ; le spectre en dernier, seulement s'il est confirmé.

## Méthodes du national à enseigner (une diapo chacune, avec un exemple chiffré)
1. Calculer la taille d'antenne pour un son (λ = c/f, puis λ/2) et conclure qu'il faut moduler.
2. Identifier, dans une expression donnée, A, m, f_p et f_s ; écrire l'expression à partir de k, P_m, U₀, S_m.
3. Lire U_max et U_min sur l'oscillogramme de la tension modulée, calculer m, juger la qualité.
4. Reconnaître la surmodulation (enveloppe déformée) et dire quoi changer (augmenter U₀).
5. Reconnaître un trapèze (bonne modulation) ou sa déformation en mode XY.
6. Vérifier la condition sur R·C du détecteur ; choisir parmi plusieurs condensateurs celui qui convient.
7. Circuit d'accord : calculer L ou C pour recevoir une porteuse de fréquence donnée (f₀ = f_p, le carré d'abord).
8. Ordonner les étages d'un récepteur et dire le rôle de chacun.

## Expériences et animations à montrer (dessinées au tableau, comme nos autres cours)
- **Les deux antennes** : GBF → antenne émettrice ; antenne réceptrice → oscilloscope ; même fréquence à l'arrivée. On éloigne l'antenne : le signal baisse.
- **L'antenne géante** : une antenne de 150 km dessinée à l'échelle d'une ville, pour un son de 1 kHz ; puis la même pour une porteuse de 1 MHz (150 m) : l'élève voit pourquoi on module.
- **Le multiplieur** : porteuse et signal entrent, la tension modulée sort ; l'enveloppe se dessine en pointillés au-dessus et au-dessous.
- **Le curseur U₀** : on baisse U₀ jusqu'à S_m, puis en dessous ; l'enveloppe se déforme (surmodulation) ; m s'affiche en direct.
- **Le mode XY** : trapèze pour m < 1, triangle à m = 1, figure déformée au-delà.
- **La détection d'enveloppe** : d'abord la diode seule (les alternances négatives disparaissent), puis le condensateur qui se charge à chaque sommet et se décharge un peu ; curseur R·C : trop petit (dents de scie qui suivent la porteuse), bon, trop grand (le son est perdu).
- **L'élimination du continu** : le signal détecté décalé de U₀ redescend autour de zéro.
- **Le récepteur complet** : chaîne d'étages avec le signal dessiné à la sortie de chacun ; le bouton d'accord (C variable) fait passer d'une station à l'autre.

## Porte d'entrée et rappels : principe pour ce cours
- Entrer par un besoin concret (la voix doit traverser le pays), pas par la définition d'une onde électromagnétique : le prof commence par la théorie des ondes, ce qui retarde la question « pourquoi moduler ? ».
- Chaque rappel juste avant son usage (colonne de droite du tableau) ; le rappel de la diode et celui du mode XY sont nouveaux.
- Notions redites : m (définition, lecture, condition) au moins trois fois ; la condition sur R·C deux fois ; f₀ = f_p au moment du récepteur et au bilan.

## Lien avec nos cours existants (à faire en même temps ou après)
- Dans les diapos qui lisent un énoncé contenant une partie AM (RC diapo 33, RL diapos 17 et 35, RLC diapos 9 et 49), dire en une phrase : « la partie modulation sera faite dans le cours de modulation » ; puis, une fois ce cours écrit, y jouer ces parties.
- Dans le RLC, une phrase « ce circuit choisit la station d'une radio » (voir `reference-prof/phys_ch8_circuit_RLC.md`, correction 8) prépare la notion 15.
