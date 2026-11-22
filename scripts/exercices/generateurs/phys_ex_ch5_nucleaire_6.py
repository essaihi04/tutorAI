# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau difficile n° 6 : énergie d'un échantillon d'uranium 235
# (bilan par les énergies de liaison par nucléon, N = m·N_A/M, E en joule) puis masse de combustible de fusion qui
# libère la même énergie, et lecture critique « la fission libère plus ».
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration energie_nucleaire.json : cas_types « énergie d'un échantillon » (N = m·N_A/M, E = N·E_lib),
#    « énergie libérée à partir des énergies de liaison » (E_ℓ = A·(E_ℓ/A)) ; pièges « ξ soustraits sans × A » (QCM
#    2019 N), « bilan par E_ℓ à l'envers », « 1 MeV = 1,6·10⁻¹⁹ J » ; capacité EN8 « comparer fission, fusion » ;
#    valeurs_reperes (fission ≈ 185 MeV ≈ 0,8 MeV/nucléon ; fusion 17,6 MeV ≈ 3,5 MeV/nucléon).
#  - nationaux : 2019 N (E_lib par les E_ℓ/A), 2025 N (énergie libérée par un échantillon), 2023 N (vrai/faux sur la
#    fission) : au-dessus du national ici (deux notions combinées, une masse de combustible à établir, une lecture
#    critique), même forme (Établir, Calculer, Discuter).
#  - séries en ligne (énergie d'une masse d'uranium, comparaison avec la fusion et le pétrole) : extraits de recherche
#    lus ; pages non joignables depuis cette session.
#  - cours : figures.html?fig=fig_methode_liaison, fig_echantillon (1 g : 2,56·10²¹ noyaux ; 7,6·10¹⁰ J),
#    balance.html?vue=fusion (17,6 MeV), comparaison.html (0,78 contre 3,5 MeV/nucléon ; 47 fusions ≈ 827 MeV) :
#    l'explication dit les valeurs de la simulation, puis applique la méthode à nos données.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_6"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
NA, MEV = 6.02e23, 1.6e-13


def tableau(titre, colonnes, valeurs):
    """Tableau des énergies de liaison par nucléon (traits à la craie)."""
    n = len(colonnes)
    l = 3.2 + 1.9 * n
    els = [{"f": "rect", "de": [0.1, 0.2], "a": [l - 0.1, 2.0]},
           {"f": "ligne", "pts": [[0.1, 1.1], [l - 0.1, 1.1]]},
           {"f": "ligne", "pts": [[3.2, 0.2], [3.2, 2.0]]},
           {"f": "texte", "at": [1.65, 1.45], "t": "noyau", "ancre": "centre"},
           {"f": "texte", "at": [1.65, 0.55], "t": "E_{ℓ}/A (MeV/nucléon)", "ancre": "centre", "taille": "petit"}]
    for i, (c, v) in enumerate(zip(colonnes, valeurs)):
        x = 3.2 + 1.9 * i
        if i: els.append({"f": "ligne", "pts": [[x, 0.2], [x, 2.0]]})
        els.append({"f": "texte", "at": [x + 0.95, 1.45], "t": c, "ancre": "centre", "couleur": "jaune"})
        els.append({"f": "texte", "at": [x + 0.95, 0.55], "t": v, "ancre": "centre", "couleur": "cyan"})
    return {"type": "schema", "titre": titre, "cadre": {"l": l, "h": 2.2}, "elements": els}


# ---------------------------------------------------------------- calculs (énoncé)
DE = 235 * 7.59 - (94 * 8.59 + 140 * 8.29)      # −184,41 MeV
assert round(DE, 2) == -184.41
N = 50 * NA / 235                               # 1,28·10²³
assert abs(N - 1.2809e23) < 1e19
E = 1.28e23 * 184.4 * MEV                       # 3,78·10¹² J
assert abs(E - 3.7765e12) < 1e9
DMf = 4.00150 + 1.00866 - 2.01355 - 3.01550     # −0,01889 u
assert abs(DMf + 0.01889) < 1e-9 and round(abs(DMf) * 931.5, 1) == 17.6
NF = 3.78e12 / (17.6 * MEV)                     # 1,34·10²⁴ fusions
MF = 1.34e24 * 5 / NA                           # 11,1 g
assert abs(NF - 1.342e24) < 1e21 and round(MF, 1) == 11.1
assert round(50 / MF, 1) == 4.5 and round((17.6 / 5) / (184.4 / 236), 1) == 4.5
# semblable : Ba 141 + Kr 92 + 3 n ; 20 g
DE2 = 235 * 7.59 - (141 * 8.32 + 92 * 8.51)     # −172,39
N2 = 20 * NA / 235                              # 5,12·10²²
E2 = 5.12e22 * 172.4 * MEV                      # 1,41·10¹² J
NF2 = 1.41e12 / (17.6 * MEV)                    # 5,01·10²³
MF2 = 5.01e23 * 5 / NA                          # 4,16 g
assert round(DE2, 2) == -172.39 and abs(N2 - 5.1234e22) < 1e18 and abs(E2 - 1.4123e12) < 1e9 and abs(NF2 - 5.007e23) < 1e20 and round(MF2, 2) == 4.16

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "Uranium ou deutérium-tritium : quelle masse pour la même énergie ?", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir E_lib à partir des énergies de liaison par nucléon", "Calculer le nombre de noyaux N = m·N_A/M",
                  "Calculer l'énergie libérée par un échantillon, en joule", "Comparer fission et fusion à masse égale"],
  "enonce": {
    "intro": "Une centrale consomme de l'uranium 235. Chaque fission s'écrit : ²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n. Le tableau donne les énergies de liaison par nucléon des noyaux concernés. On compare ensuite avec la fusion ²₁H + ³₁H → ⁴₂He + ¹₀n.",
    "intro_dit": "دابا نقراو l'énoncé. une centrale كتستهلك l'uranium deux cent trente-cinq. كل fission: l'uranium plus un neutron، كيعطيو le strontium quatre-vingt-quatorze، le xénon cent quarante، et deux neutrons. le tableau كيعطي E l sur A ديال هاد les noyaux. ومن بعد غادي نقارنو مع la fusion ديال le deutérium و le tritium.",
    "figures": [tableau("Tableau : énergies de liaison par nucléon", ["²³⁵₉₂U", "⁹⁴₃₈Sr", "¹⁴⁰₅₄Xe"], ["7,59", "8,59", "8,29"])],
    "donnees": ["N_A = 6,02·10²³ mol⁻¹ ; M(²³⁵U) = 235 g/mol ; M(²H) = 2 g/mol ; M(³H) = 3 g/mol",
                "m(²₁H) = 2,01355 u ; m(³₁H) = 3,01550 u ; m(⁴₂He) = 4,00150 u ; m(¹₀n) = 1,00866 u",
                "1 u = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J"],
    "questions": [
      question("1", "Établir l'expression de ΔE de la fission en fonction des énergies de liaison par nucléon, puis montrer que l'énergie libérée par une fission vaut E_lib ≈ 184,4 MeV.",
        "السؤال un: بين l'expression ديال delta E ديال la fission ب les énergies de liaison par nucléon، ومن بعد بين بلي l'énergie libérée ب fission وحدة كتساوي environ cent quatre-vingt-quatre virgule quatre méga électron volt.",
        valeur("E_lib", 184.4, "MeV", "ΔE = 235·(E_ℓ/A)(U) − [94·(E_ℓ/A)(Sr) + 140·(E_ℓ/A)(Xe)] = 1783,65 − 1968,06 = −184,41 MeV ; E_lib = |ΔE| = 184,4 MeV"),
        ["ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)", "E_ℓ = A·(E_ℓ/A)", "E_ℓ(n) = 0"], ["7,59 − 8,59 − 8,29", "ΔE = ΣE_ℓ(produits) − ΣE_ℓ(réactifs)"],
        [aide("Chaque noyau a son énergie de liaison E_ℓ = A·(E_ℓ/A) ; les neutrons libres n'en ont pas.",
              "كل نواة، E l ديالها égale A fois E l sur A. و les neutrons بوحدهم، E l ديالهم égale zéro."),
         aide("ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) = 235 × 7,59 − (94 × 8,59 + 140 × 8,29). Ne soustrais jamais les E_ℓ/A directement.",
              "delta E égale la somme des E l des réactifs moins la somme des E l des produits. يعني deux cent trente-cinq fois sept virgule cinquante-neuf، moins، quatre-vingt-quatorze fois huit virgule cinquante-neuf plus cent quarante fois huit virgule vingt-neuf. ما تنقصش E l sur A مباشرة.")],
        corr([("1 : ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits), avec E_ℓ = A·(E_ℓ/A) et E_ℓ(n) = 0", "delta E égale la somme des E l des réactifs"),
              ("ΔE = 235 × 7,59 − (94 × 8,59 + 140 × 8,29) = 1783,65 − 1968,06", "mille sept cent quatre-vingt-trois virgule soixante-cinq"),
              ("ΔE = −184,41 MeV ; E_lib = |ΔE| ≈ 184,4 MeV", "E libérée égale environ cent quatre-vingt-quatre virgule quatre")],
             "السؤال un. delta E égale la somme des E l des réactifs moins la somme des E l des produits، و E l égale A fois E l sur A، و le neutron، E l égale zéro. les réactifs: deux cent trente-cinq fois sept virgule cinquante-neuf، يعني mille sept cent quatre-vingt-trois virgule soixante-cinq. les produits: quatre-vingt-quatorze fois huit virgule cinquante-neuf، plus cent quarante fois huit virgule vingt-neuf، يعني mille neuf cent soixante-huit virgule zéro six. delta E égale moins cent quatre-vingt-quatre virgule quarante et un méga électron volt، إذن E libérée égale environ cent quatre-vingt-quatre virgule quatre méga électron volt."),
        "ex_n6_1", "fa_n6_1"),
      question("2", "La centrale consomme une masse m = 50 g d'uranium 235. Calculer le nombre N de noyaux contenus dans cette masse.",
        "السؤال deux: la centrale كتستهلك m égale cinquante grammes ديال l'uranium deux cent trente-cinq. حسب N، عدد les noyaux اللي فهاد la masse.",
        valeur("N", 1.28e23, "noyaux", "N = m·N_A/M = 50 × 6,02·10²³/235 = 1,28·10²³ noyaux"),
        ["N = m·N_A/M", "n = m/M", "g/mol"], ["N = m·M/N_A", "m en kg avec M en g/mol"],
        [aide("Combien de moles dans 50 g d'uranium 235 ? Et combien de noyaux dans une mole ?",
              "شحال من mole، dans cinquante grammes ديال l'uranium؟ و شحال من noyau ف mole؟"),
         aide("n = m/M, puis N = n·N_A, donc N = m·N_A/M (m en g, M en g/mol).",
              "n égale m sur M، و N égale n fois N A، إذن N égale m fois N A sur M، مع m ب gramme و M ب gramme par mole.")],
        corr([("2 : N = n·N_A = m·N_A/M", "N égale m fois N A sur M"),
              ("A.N. : N = 50 × 6,02·10²³/235", "cinquante fois six virgule zéro deux fois dix puissance vingt-trois، sur deux cent trente-cinq"),
              ("N = 1,28·10²³ noyaux", "un virgule vingt-huit fois dix puissance vingt-trois noyaux")],
             "السؤال deux. N égale m fois N A sur M. l'application numérique: cinquante fois six virgule zéro deux fois dix puissance vingt-trois، sur deux cent trente-cinq. N égale un virgule vingt-huit fois dix puissance vingt-trois noyaux."),
        "ex_n6_2", "fa_n6_2"),
      question("3", "En supposant que tous ces noyaux subissent la fission, calculer en joule l'énergie E libérée.",
        "السؤال trois: يلا جميع هاد les noyaux دارو la fission، حسب ب joule l'énergie E اللي كتخرج.",
        valeur("E", 3.78e12, "J", "E = N·E_lib = 1,28·10²³ × 184,4 × 1,6·10⁻¹³ = 3,78·10¹² J"),
        ["E = N·E_lib", "1 MeV = 1,6·10⁻¹³ J", "J"], ["E = E_lib/N", "1 MeV = 1,6·10⁻¹⁹ J"],
        [aide("Chaque noyau qui se casse libère E_lib. Combien de noyaux se cassent ?",
              "كل noyau كيتقسم كيعطي E libérée. شحال من noyau كيتقسم؟"),
         aide("E = N × E_lib (en MeV), puis × 1,6·10⁻¹³ pour passer en joule.",
              "E égale N fois E libérée ب méga électron volt، ومن بعد fois un virgule six fois dix puissance moins treize باش نوصلو ل joule.")],
        corr([("3 : E = N·E_lib", "E égale N fois E libérée"),
              ("E = 1,28·10²³ × 184,4 = 2,36·10²⁵ MeV", "deux virgule trente-six fois dix puissance vingt-cinq méga électron volt"),
              ("E = 2,36·10²⁵ × 1,6·10⁻¹³ = 3,78·10¹² J", "trois virgule soixante-dix-huit fois dix puissance douze joule")],
             "السؤال trois. E égale N fois E libérée. un virgule vingt-huit fois dix puissance vingt-trois، fois cent quatre-vingt-quatre virgule quatre، يعني deux virgule trente-six fois dix puissance vingt-cinq méga électron volt. fois un virgule six fois dix puissance moins treize: E égale trois virgule soixante-dix-huit fois dix puissance douze joule."),
        "ex_n6_3", "fa_n6_3"),
      question("4", "Pour la fusion ²₁H + ³₁H → ⁴₂He + ¹₀n, calculer l'énergie libérée par une réaction (en MeV), puis la masse m′ du mélange deutérium-tritium (autant de noyaux ²H que de ³H) qui libère la même énergie E qu'à la question 3.",
        "السؤال quatre: بالنسبة ل la fusion ديال le deutérium و le tritium، حسب l'énergie libérée ب réaction وحدة، ومن بعد la masse m prime ديال le mélange اللي كيعطي نفس l'énergie E ديال السؤال trois.",
        valeur("m′", 11.1, "g", "E_lib = |4,00150 + 1,00866 − 2,01355 − 3,01550| × 931,5 = 17,6 MeV ; N′ = E/E_lib = 3,78·10¹²/(17,6 × 1,6·10⁻¹³) = 1,34·10²⁴ ; m′ = N′·(2 + 3)/N_A = 1,34·10²⁴ × 5/6,02·10²³ = 11,1 g"),
        ["E_lib = |Δm|·c²", "N′ = E/E_lib", "m′ = N′·M/N_A", "M = 2 + 3 = 5 g/mol"], ["m′ = N′·4/N_A", "N′ = E × E_lib"],
        [aide("D'abord E_lib d'une fusion par les masses. Ensuite : combien de fusions faut-il pour obtenir E ? Chaque fusion consomme un ²H et un ³H.",
              "اللول E libérée ديال fusion ب les masses. ومن بعد: شحال من fusion خاصنا باش نوصلو ل E؟ كل fusion كتستهلك un deutérium et un tritium."),
         aide("N′ = E/(E_lib en J) ; une paire ²H + ³H a une masse molaire 2 + 3 = 5 g/mol, donc m′ = N′ × 5/N_A.",
              "N prime égale E sur E libérée ب joule. و la paire deutérium tritium، la masse molaire ديالها égale deux plus trois، يعني cinq grammes par mole. إذن m prime égale N prime fois cinq sur N A.")],
        corr([("4 : Δm = 4,00150 + 1,00866 − 2,01355 − 3,01550 = −0,01889 u ; E_lib = 0,01889 × 931,5 = 17,6 MeV", "E libérée égale dix-sept virgule six méga électron volt"),
              ("N′ = E/E_lib = 3,78·10¹²/(17,6 × 1,6·10⁻¹³) = 1,34·10²⁴ fusions", "un virgule trente-quatre fois dix puissance vingt-quatre"),
              ("m′ = N′·(M(²H) + M(³H))/N_A = 1,34·10²⁴ × 5/6,02·10²³", "m prime égale N prime fois cinq sur N A"),
              ("m′ = 11,1 g", "onze virgule un grammes")],
             "السؤال quatre. delta m égale moins zéro virgule zéro un mille huit cent quatre-vingt-neuf u، إذن E libérée égale dix-sept virgule six méga électron volt. N prime égale E sur E libérée: trois virgule soixante-dix-huit fois dix puissance douze، sur dix-sept virgule six fois un virgule six fois dix puissance moins treize، يعني un virgule trente-quatre fois dix puissance vingt-quatre fusions. m prime égale N prime fois cinq sur N A، يعني onze virgule un grammes."),
        "ex_n6_4", "fa_n6_4"),
      question("5", "Un élève conclut : « la fission est plus énergétique que la fusion, car 184,4 MeV > 17,6 MeV ». Discuter cette conclusion à l'aide des résultats précédents.",
        "السؤال cinq: تلميذ قال: la fission كتعطي كثر من la fusion، parce que cent quatre-vingt-quatre virgule quatre plus grand que dix-sept virgule six. ناقش هاد الكلام بالنتائج اللي لقيتي.",
        phrase("La conclusion compare une réaction à une réaction, mais une fission met en jeu 236 nucléons et une fusion seulement 5. À masse égale, il faut comparer l'énergie par nucléon (0,78 MeV pour la fission, 3,5 MeV pour la fusion) ou la masse consommée pour la même énergie : 50 g d'uranium contre 11,1 g de mélange ²H + ³H, environ 4,5 fois moins. Donc, à masse égale, la fusion libère environ 4,5 fois plus d'énergie que la fission : la conclusion de l'élève est fausse."),
        ["à masse égale", "par nucléon", "50/11,1 ≈ 4,5"], ["comparer 184,4 et 17,6", "fission plus énergétique"],
        [aide("Combien de nucléons participent à une fission ? à une fusion ? Est-ce juste de comparer une réaction à une réaction ?",
              "شحال من nucléon كيشارك ف fission؟ و ف fusion؟ واش معقول نقارنو réaction ب réaction؟"),
         aide("Compare les masses trouvées : 50 g (fission) et 11,1 g (fusion) pour la même énergie. Calcule le rapport.",
              "قارن les masses اللي لقيتي: cinquante grammes ل la fission، et onze virgule un grammes ل la fusion، لنفس l'énergie. حسب le rapport.")],
        corr([("5 : une fission met en jeu 236 nucléons, une fusion seulement 5 : on doit comparer à masse égale", "à masse égale"),
              ("Pour la même énergie : 50 g d'uranium contre 11,1 g de ²H + ³H ; 50/11,1 ≈ 4,5", "cinquante sur onze virgule un"),
              ("(par nucléon : 3,5 MeV contre 0,78 MeV, rapport ≈ 4,5)", "trois virgule cinq contre zéro virgule soixante-dix-huit"),
              ("À masse égale, la fusion libère environ 4,5 fois plus : la conclusion est fausse.", "la fusion كتعطي environ quatre virgule cinq fois كثر")],
             "السؤال cinq. une fission، c'est deux cent trente-six nucléons، et une fusion، seulement cinq. إذن خاصنا نقارنو à masse égale. لنفس l'énergie: cinquante grammes ديال l'uranium، contre onze virgule un grammes ديال le mélange. cinquante sur onze virgule un، environ quatre virgule cinq. و par nucléon، trois virgule cinq contre zéro virgule soixante-dix-huit، نفس le rapport. إذن à masse égale، la fusion كتعطي environ quatre virgule cinq fois كثر، والتلميذ غالط."),
        "ex_n6_5", "fa_n6_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n6_1", "Question 1 : ΔE par les E_ℓ/A", "ΔE = 235 × 7,59 − (94 × 8,59 + 140 × 8,29) = −184,41 MeV",
      SIMD + "figures.html?fig=fig_methode_liaison", "Énergie libérée à partir des énergies de liaison",
      "شوف la formule: delta E égale la somme des E l des réactifs moins la somme des E l des produits. الخطوة الثانية: E l égale A fois E l sur A، لكل نواة. الخطوة الثالثة: nucléon بوحدو، E l ديالو égale zéro. فle cours، l'exemple ديال la fusion، delta E égale moins dix-sept virgule quatre cent cinquante-cinq. فالتمرين ديالنا: l'uranium، deux cent trente-cinq fois sept virgule cinquante-neuf، يعني mille sept cent quatre-vingt-trois virgule soixante-cinq. les produits: mille neuf cent soixante-huit virgule zéro six. delta E égale moins cent quatre-vingt-quatre virgule quarante et un méga électron volt.",
      centre=[("E_ℓ = A·(E_ℓ/A) ; E_ℓ(n) = 0", "E l égale A fois E l sur A"),
              ("ΔE = 1783,65 − 1968,06 = −184,41 MeV", "delta E égale moins cent quatre-vingt-quatre")],
      pointage=[{"mot": "شوف la formule", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "الخطوة الثانية", "commande": "play_until", "parametres": {"moment": "A_fois"}},
                {"mot": "الخطوة الثالثة", "commande": "play_until", "parametres": {"moment": "nucleon_libre"}},
                {"mot": "فle cours، l'exemple", "commande": "play_until", "parametres": {"moment": "E_lib"}}]),
    diapo_sim("ex_n6_2", "Question 2 : combien de noyaux ?", "N = m·N_A/M = 50 × 6,02·10²³/235 = 1,28·10²³",
      SIMD + "figures.html?fig=fig_echantillon", "L'échantillon : N = m·N_A/M",
      "noyau بوحدو ديال l'uranium كيعطي environ cent quatre-vingt-cinq méga électron volt. ولكن l'échantillon فيه بزاف ديال les noyaux. N égale m fois N A sur M، مع m ب gramme. فle cours، pour un gramme: deux virgule cinquante-six fois dix puissance vingt et un noyaux. فالتمرين ديالنا، m égale cinquante grammes: cinquante fois six virgule zéro deux fois dix puissance vingt-trois، sur deux cent trente-cinq، يعني un virgule vingt-huit fois dix puissance vingt-trois noyaux.",
      centre=[("N = m·N_A/M", "N égale m fois N A sur M"),
              ("N = 50 × 6,02·10²³/235 = 1,28·10²³", "un virgule vingt-huit fois dix puissance vingt-trois noyaux")],
      pointage=[{"mot": "noyau بوحدو", "commande": "play_until", "parametres": {"moment": "un_noyau"}},
                {"mot": "N égale m fois N A sur M", "commande": "play_until", "parametres": {"moment": "nombre"}}]),
    diapo_sim("ex_n6_3", "Question 3 : l'énergie de l'échantillon", "E = N·E_lib = 1,28·10²³ × 184,4 × 1,6·10⁻¹³ = 3,78·10¹² J",
      SIMD + "figures.html?fig=fig_echantillon&depart=nombre", "E = N·E_lib, puis en joule",
      "كل noyau كيعطي نفس l'énergie. إذن E égale N fois E libérée. فle cours، pour un gramme: sept virgule six fois dix puissance dix joules. فالتمرين ديالنا: un virgule vingt-huit fois dix puissance vingt-trois، fois cent quatre-vingt-quatre virgule quatre، يعني deux virgule trente-six fois dix puissance vingt-cinq méga électron volt. ب joule، كنضربو fois un virgule six fois dix puissance moins treize: trois virgule soixante-dix-huit fois dix puissance douze joules.",
      centre=[("E = N·E_lib = 2,36·10²⁵ MeV", "إذن E égale N fois E libérée"),
              ("E = 2,36·10²⁵ × 1,6·10⁻¹³ = 3,78·10¹² J", "trois virgule soixante-dix-huit fois dix puissance douze joules")],
      pointage=[{"mot": "إذن E égale N fois", "commande": "play_until", "parametres": {"moment": "total"}},
                {"mot": "ب joule، كنضربو", "commande": "play_until", "parametres": {"moment": "joule"}}]),
    diapo_sim("ex_n6_4", "Question 4 : la masse de combustible de fusion", "E_lib = 17,6 MeV ; N′ = 1,34·10²⁴ ; m′ = N′ × 5/N_A = 11,1 g",
      SIMD + "balance.html?vue=fusion", "La fusion ²H + ³H : Δm = −0,01889 u, E_lib = 17,6 MeV",
      "شوف الميزان: le deutérium و le tritium على اليسار، l'hélium و le neutron على اليمين. delta m égale moins zéro virgule zéro un mille huit cent quatre-vingt-neuf u، و E libérée égale dix-sept virgule six méga électron volt. باش نوصلو à trois virgule soixante-dix-huit fois dix puissance douze joules، خاصنا N prime égale E sur E libérée، يعني un virgule trente-quatre fois dix puissance vingt-quatre fusions. كل fusion كتاكل un deutérium et un tritium: deux plus trois، cinq grammes par mole. m prime égale N prime fois cinq sur N A، يعني onze virgule un grammes.",
      centre=[("N′ = E/E_lib = 1,34·10²⁴", "N prime égale E sur E libérée"),
              ("m′ = N′ × 5/N_A = 11,1 g", "m prime égale N prime fois cinq sur N A")],
      pointage=[{"mot": "شوف الميزان", "commande": "play_until", "parametres": {"moment": "produits_poses"}},
                {"mot": "delta m égale moins", "commande": "play_until", "parametres": {"moment": "delta_m"}},
                {"mot": "و E libérée égale dix-sept", "commande": "play_until", "parametres": {"moment": "energie"}}]),
    diapo_sim("ex_n6_5", "Question 5 : comparer à masse égale", "Fission 0,78 MeV/nucléon ; fusion 3,5 MeV/nucléon ; 50 g contre 11,1 g",
      SIMD + "comparaison.html", "Par réaction, par nucléon, à masse égale",
      "شوف: ل réaction وحدة، la fission، cent quatre-vingt-cinq méga électron volt، و la fusion، dix-sept virgule six. ولكن par nucléon: la fission، zéro virgule soixante-dix-huit، و la fusion، trois virgule cinq. à masse égale، la fusion كتعطي كثر. فالتمرين ديالنا: cinquante grammes ديال l'uranium، contre onze virgule un grammes ديال le mélange، لنفس l'énergie. le rapport environ quatre virgule cinq.",
      centre=[("3,5/0,78 ≈ 4,5", "par nucléon"), ("50 g / 11,1 g ≈ 4,5", "le rapport environ quatre virgule cinq")],
      pointage=[{"mot": "ل réaction وحدة", "commande": "play_until", "parametres": {"moment": "par_reaction"}},
                {"mot": "ولكن par nucléon", "commande": "play_until", "parametres": {"moment": "par_nucleon"}},
                {"mot": "à masse égale، la fusion", "commande": "play_until", "parametres": {"moment": "conclusion"}}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n6_1", "Plus facile : le piège des E_ℓ/A", "نتمرنو على فخ معروف.",
      "Pour X → Y + Z, on connaît E_ℓ/A de chaque noyau. On calcule ΔE avec :",
      ["(E_ℓ/A)(X) − (E_ℓ/A)(Y) − (E_ℓ/A)(Z)", "A_X·(E_ℓ/A)(X) − [A_Y·(E_ℓ/A)(Y) + A_Z·(E_ℓ/A)(Z)]", "A_X·(E_ℓ/A)(X) + A_Y·(E_ℓ/A)(Y) + A_Z·(E_ℓ/A)(Z)"], 1, {
        "1": {"juste": rep("برافو! كنضربو كل E l sur A ف A ديالها، ومن بعد les réactifs moins les produits.", "Juste : E_ℓ = A·(E_ℓ/A), puis réactifs moins produits.")},
        "0": {"1": rep("هادا هو الفخ. E l sur A راها par nucléon: خاصك اللول ترجع ل E l ديال النواة كاملة. عاود اختار.", "E_ℓ/A est par nucléon : il faut d'abord retrouver E_ℓ. Réessaie."),
              "2": rep("الجواب: E l égale A fois E l sur A لكل نواة، ومن بعد les réactifs moins les produits.", "Réponse : A_X·ξ_X − (A_Y·ξ_Y + A_Z·ξ_Z).")},
        "2": {"1": rep("لا، delta E هو فرق: les réactifs moins les produits. عاود اختار.", "ΔE est une différence : réactifs moins produits. Réessaie."),
              "2": rep("الجواب: E l des réactifs moins E l des produits، مع E l égale A fois E l sur A.", "Réponse : ΣE_ℓ(réactifs) − ΣE_ℓ(produits).")}},
      "Pour X donne Y plus Z, on connaît E l sur A de chaque noyau. On calcule delta E comment ?"),
    qcm_facile("fa_n6_2", "Plus facile : le nombre de noyaux", "سؤال ساهل: شحال من noyau؟",
      "Dans m = 235 g d'uranium 235 (M = 235 g/mol), il y a :",
      ["235 noyaux", "6,02·10²³ noyaux", "1 noyau"], 1, {
        "1": {"juste": rep("برافو! هادي mole وحدة، إذن N A noyaux، six virgule zéro deux fois dix puissance vingt-trois.", "Juste : 1 mol, donc N_A noyaux.")},
        "0": {"1": rep("ما تقلقش. deux cent trente-cinq grammes هي la masse ديال mole. شحال من noyau ف mole؟ عاود اختار.", "235 g, c'est la masse d'une mole. Combien de noyaux par mole ? Réessaie."),
              "2": rep("الجواب: N égale m fois N A sur M، يعني six virgule zéro deux fois dix puissance vingt-trois noyaux.", "Réponse : N = m·N_A/M = 6,02·10²³.")},
        "2": {"1": rep("لا، noyau بوحدو كيزن، seulement deux cent trente-cinq u، صغير بزاف. عاود اختار.", "Un seul noyau pèse 235 u, minuscule. Réessaie."),
              "2": rep("الجواب: six virgule zéro deux fois dix puissance vingt-trois noyaux، mole وحدة.", "Réponse : 6,02·10²³ noyaux (1 mol).")}},
      "Dans m égale deux cent trente-cinq grammes d'uranium deux cent trente-cinq, il y a combien de noyaux ?"),
    vrai_faux_facile("fa_n6_3", "Plus facile : vrai ou faux", "سؤال ساهل على l'énergie ديال l'échantillon.",
      "N = 1,28·10²³ noyaux ; E_lib = 184,4 MeV par fission.",
      [("L'énergie totale est E = N × E_lib.", True, "Chaque noyau libère E_lib : on multiplie par le nombre de noyaux."),
       ("Pour passer de MeV en joule, on multiplie par 1,6·10⁻¹⁹.", False, "1 MeV = 1,6·10⁻¹³ J (1,6·10⁻¹⁹ J, c'est 1 eV)."),
       ("E = E_lib/N.", False, "On multiplie, on ne divise pas.")]),
    qcm_facile("fa_n6_4", "Plus facile : la masse molaire d'une paire", "سؤال ساهل: la masse ديال le mélange.",
      "Chaque fusion consomme un noyau ²H et un noyau ³H. La masse d'une mole de paires (²H + ³H) vaut environ :",
      ["4 g", "5 g", "6 g"], 1, {
        "1": {"juste": rep("برافو! deux plus trois، يعني cinq grammes.", "Juste : 2 + 3 = 5 g.")},
        "0": {"1": rep("ما تقلقش. quatre grammes هي ديال l'hélium، ماشي ديال اللي كنستهلكو. عاود اختار.", "4 g, c'est l'hélium produit, pas ce qu'on consomme. Réessaie."),
              "2": rep("الجواب: cinq grammes: le deutérium deux plus le tritium trois.", "Réponse : 5 g (2 + 3).")},
        "2": {"1": rep("لا، ما كنزيدوش le neutron، هو اللي كيخرج. عاود اختار.", "Le neutron est produit, pas consommé. Réessaie."),
              "2": rep("الجواب: cinq grammes: deux plus trois.", "Réponse : 5 g.")}},
      "Chaque fusion consomme un deutérium et un tritium. La masse d'une mole de paires vaut combien ?"),
    qcm_facile("fa_n6_5", "Plus facile : comparer comment ?", "سؤال ساهل: كيفاش نقارنو؟",
      "Pour comparer l'efficacité de deux combustibles nucléaires, on compare :",
      ["l'énergie libérée par une réaction", "l'énergie libérée à masse égale (ou par nucléon)", "le nombre de neutrons produits"], 1, {
        "1": {"juste": rep("برافو! à masse égale، ولا par nucléon: هكا المقارنة عادلة.", "Juste : à masse égale ou par nucléon.")},
        "0": {"1": rep("فخ! la fission، c'est deux cent trente-six nucléons، et la fusion، seulement cinq. واش المقارنة عادلة؟ عاود اختار.", "Une fission met en jeu 236 nucléons, une fusion 5 : est-ce équitable ? Réessaie."),
              "2": rep("الجواب: à masse égale ولا par nucléon.", "Réponse : à masse égale (ou par nucléon).")},
        "2": {"1": rep("لا، les neutrons ما كيقيسوش l'énergie. عاود اختار.", "Les neutrons ne mesurent pas l'énergie. Réessaie."),
              "2": rep("الجواب: l'énergie à masse égale.", "Réponse : l'énergie à masse égale.")}},
      "Pour comparer deux combustibles nucléaires, on compare quoi ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, une autre fission et 20 g d'uranium",
    "enonce": {
      "intro": "Une autre fission : ²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3 ¹₀n. La centrale consomme m = 20 g d'uranium 235. Même fusion de comparaison.",
      "intro_dit": "fission أخرى، مع le baryum و le krypton، et trois neutrons. la centrale كتستهلك m égale vingt grammes.",
      "figures": [tableau("Tableau : énergies de liaison par nucléon", ["²³⁵₉₂U", "¹⁴¹₅₆Ba", "⁹²₃₆Kr"], ["7,59", "8,32", "8,51"])],
      "donnees": ["N_A = 6,02·10²³ mol⁻¹ ; M(²³⁵U) = 235 g/mol ; M(²H) = 2 g/mol ; M(³H) = 3 g/mol",
                  "m(²₁H) = 2,01355 u ; m(³₁H) = 3,01550 u ; m(⁴₂He) = 4,00150 u ; m(¹₀n) = 1,00866 u",
                  "1 u = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J"],
      "questions": [
        question_semblable("1", "Établir ΔE de la fission à partir des énergies de liaison par nucléon et calculer E_lib.",
          valeur("E_lib", 172.4, "MeV", "ΔE = 235 × 7,59 − (141 × 8,32 + 92 × 8,51) = 1783,65 − 1956,04 = −172,39 MeV ; E_lib = 172,4 MeV"),
          ["E_ℓ = A·(E_ℓ/A)", "E_ℓ(n) = 0"], ["7,59 − 8,32 − 8,51"],
          corr([("1 : ΔE = 235 × 7,59 − (141 × 8,32 + 92 × 8,51) = −172,39 MeV ; E_lib ≈ 172,4 MeV", "cent soixante-douze virgule quatre")],
               "delta E égale mille sept cent quatre-vingt-trois virgule soixante-cinq moins mille neuf cent cinquante-six virgule zéro quatre، يعني moins cent soixante-douze virgule trente-neuf. E libérée égale environ cent soixante-douze virgule quatre méga électron volt.")),
        question_semblable("2", "Calculer le nombre N de noyaux dans m = 20 g d'uranium 235.",
          valeur("N", 5.12e22, "noyaux", "N = 20 × 6,02·10²³/235 = 5,12·10²² noyaux"), ["N = m·N_A/M"], ["N = m·M/N_A"],
          corr([("2 : N = m·N_A/M = 20 × 6,02·10²³/235 = 5,12·10²²", "cinq virgule douze fois dix puissance vingt-deux")],
               "N égale m fois N A sur M، يعني cinq virgule douze fois dix puissance vingt-deux noyaux.")),
        question_semblable("3", "Calculer en joule l'énergie E libérée par la fission de tous ces noyaux.",
          valeur("E", 1.41e12, "J", "E = 5,12·10²² × 172,4 × 1,6·10⁻¹³ = 1,41·10¹² J"), ["E = N·E_lib", "1 MeV = 1,6·10⁻¹³ J"], ["1 MeV = 1,6·10⁻¹⁹ J"],
          corr([("3 : E = N·E_lib = 5,12·10²² × 172,4 × 1,6·10⁻¹³ = 1,41·10¹² J", "un virgule quarante et un fois dix puissance douze joules")],
               "E égale N fois E libérée، fois un virgule six fois dix puissance moins treize: un virgule quarante et un fois dix puissance douze joules.")),
        question_semblable("4", "Calculer la masse m′ de mélange ²H + ³H dont la fusion libère la même énergie E.",
          valeur("m′", 4.16, "g", "N′ = 1,41·10¹²/(17,6 × 1,6·10⁻¹³) = 5,01·10²³ ; m′ = 5,01·10²³ × 5/6,02·10²³ = 4,16 g"),
          ["N′ = E/E_lib", "M = 5 g/mol"], ["M = 4 g/mol"],
          corr([("4 : E_lib(fusion) = 17,6 MeV ; N′ = E/E_lib = 5,01·10²³ ; m′ = N′ × 5/N_A = 4,16 g", "quatre virgule seize grammes")],
               "E libérée ديال la fusion égale dix-sept virgule six méga électron volt. N prime égale cinq virgule zéro un fois dix puissance vingt-trois، و m prime égale quatre virgule seize grammes.")),
        question_semblable("5", "« La fission est plus énergétique, car 172,4 MeV > 17,6 MeV. » Discuter cette conclusion.",
          phrase("Faux à masse égale : pour la même énergie, il faut 20 g d'uranium mais seulement 4,16 g de ²H + ³H (rapport ≈ 4,8) ; par nucléon, 172,4/236 ≈ 0,73 MeV contre 3,5 MeV. La fusion libère plus d'énergie à masse égale."),
          ["à masse égale", "par nucléon"], ["comparer 172,4 et 17,6"],
          corr([("5 : 20 g contre 4,16 g pour la même énergie (rapport ≈ 4,8) : à masse égale, la fusion libère plus ; la conclusion est fausse.", "à masse égale")],
               "لنفس l'énergie: vingt grammes ديال l'uranium contre quatre virgule seize grammes. à masse égale، la fusion كتعطي كثر.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
