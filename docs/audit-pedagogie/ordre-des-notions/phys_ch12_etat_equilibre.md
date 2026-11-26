# phys_ch12_etat_equilibre

## Ordre proposé des premières notions
1. Concentration (diapo 2)
2. Puissances de dix et log (diapo 3)
3. Acide, base, couple (diapo 4)
4. L'eau dans deux couples, le pH (diapo 5)
5. Rappel : état d'équilibre dynamique (diapo 8, avancée avant le taux)
6. Rappel : tableau d'avancement d'un acide avec l'eau, x_max, x_éq (première moitié de la diapo 6)
7. Rappel : τ = x_éq/x_max = 10^(−pH)/C (seconde moitié de la diapo 6)
8. La question du chapitre : τ change avec C (diapo 7), puis le quotient Qr (diapo 9)

La porte d'entrée est bonne (les rappels d'abord, puis « τ change, quel nombre ne change pas ? »). Mais la diapo 6 condense trois rappels (tableau, x_max, état d'équilibre, τ et sa démonstration) et parle de x_éq avant le rappel de l'équilibre (diapo 8).

## Défauts
| # | Diapo | Type | Ce qui est dit (citation courte) | Pourquoi ça perturbe | Correction proposée | Gravité |
|---|---|---|---|---|---|---|
| 1 | Bloc après 21 (`ee_b05`) | 4 question tôt | « écris Qr,éq d'un acide avec l'eau en fonction de C et du pH » + calcul 10^(−2pH)/(C − 10^(−pH)) | Qr,éq est défini en 23 et la relation avec C et le pH est établie en 24. L'élève doit écrire une formule qu'il n'a jamais vue. | Déplacer ce bloc après la diapo 24 (ou 26, en fusion avec `ee_b06`) | forte |
| 2 | 6 | 2 trop vite | Un seul rappel avec tableau en trois lignes, x_max, « état d'équilibre : x égale x éq », x_f = x_éq, démonstration de τ = 10^(−pH)/C et calcul | Quatre notions du chapitre précédent dans une diapo, dont l'équilibre, qui n'est rappelé qu'en 8. Un élève faible décroche dès la deuxième diapo de contenu. | Couper en deux diapos (tableau + x_max ; puis τ), et placer le rappel 8 (équilibre) avant | forte |
| 3 | 15 | 4 question tôt | EXERCICE « Calcule Qr,i de HCOOH + CH₃COO⁻ ⇌ … » (mélange à concentrations différentes) | Le calcul de Qr,i d'un mélange (V_T qui se simplifie, travail avec les quantités) n'est montré qu'en 16. | Déplacer l'exercice sur la diapo 16 (garder en 15 la seule QUESTION sur « après le mélange ») | moyenne |
| 4 | 18 (2017 N) | 1 notion avant | Énoncé : « La constante d'équilibre associée à la réaction… est K = 10²⁰⁰ » ; « la pile aluminium – cuivre » | K n'est défini qu'en 29 ; la pile et les électrodes ne sont pas au programme du semestre. L'élève lit un mot clé du chapitre sans savoir ce que c'est. | Placer ce sujet après la diapo 29, ou dire en 18 « K : on la verra dans quelques diapos ; ici on ne demande que Qr,i » | moyenne |
| 5 | 34-35 (2022 R) | 1 notion avant | Énoncé : « le produit ionique de l'eau, Kₑ = 10⁻¹⁴ » ; « Question 1.3 : calculer le taux d'avancement final τ » ; 35 : « tau égale zéro virgule vingt, il est donné » | Kₑ n'est jamais enseigné (chapitre suivant). La question 1.3 est lue puis contournée (« il est donné »), ce qui laisse l'élève sans méthode pour une base. | Retirer Kₑ et la question 1.3 de l'énoncé lu, ou dire clairement « question 1.3 : au chapitre suivant (Kₑ) » | moyenne |
| 6 | 10 | 1 notion avant | « Un exemple : la réaction du chapitre de cinétique. Deux ions iodure, plus un ion peroxodisulfate… » | Le chapitre de cinétique a utilisé l'eau oxygénée, jamais le peroxodisulfate. L'élève cherche un souvenir qu'il n'a pas. | Retirer « du chapitre de cinétique », ou prendre un exemple déjà vu | moyenne |
| 7 | Bloc après 49 (`ee_b10`) | 4 question tôt | « de quoi dépend le taux d'avancement final τ ? » | La dépendance à la nature de la réaction (K) est montrée en 50-51, après cette question. Le même bloc est reposé après 52 (`ee_b11`). | Supprimer `ee_b10` et garder seulement `ee_b11` après 52 | moyenne |
| 8 | 9 | 1 notion avant | « les concentrations molaires effectives, en mole par litre » | Expression jamais expliquée (« effective » = réellement présente dans la solution). | Ajouter : « effective : la concentration de l'espèce réellement présente à cet instant » | moyenne |
| 9 | 12 | 2 trop vite | ÉCRAN « Autre exemple, une précipitation : Fe³⁺ + 3HO⁻ ⇌ Fe(OH)₃(s)… Qr = 1/([Fe³⁺]·[HO⁻]³) » | Deuxième réaction (précipitation), avec un exposant 3 et un quotient inversé, dans la diapo qui introduit les solides. | Garder cette réaction pour une diapo d'exercice après 13 | moyenne |

## Notions importantes dites une seule fois
- Qr augmente depuis Qr,i jusqu'à Qr,éq puis reste constant — diapo 17
- « Concentration molaire effective » — diapo 9
- Le pH et σ lus sont ceux de l'équilibre (réaction rapide) — diapos 22 et 36, mais absent du bilan
- Conversions µS·cm⁻¹ et mS·cm⁻¹ vers S·m⁻¹ — diapo 38
- Dans l'estérification, l'eau est un produit et entre dans K — diapo 55
- Chiffres significatifs d'un pH au centième — diapo 22
- Qr,i d'un mélange : V_T se simplifie, on peut calculer avec les quantités — diapo 16 (bilan : seulement [X]ᵢ = C·V/V_T)
