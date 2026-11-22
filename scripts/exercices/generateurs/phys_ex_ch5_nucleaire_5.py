# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau moyen n° 5 : la fusion de deux noyaux de deutérium —
# lois de Soddy, énergies de liaison à partir de E_ℓ/A, diagramme énergétique (sens des flèches), ΔE par les énergies
# de liaison, vérification par les masses.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration energie_nucleaire.json : cas_types « énergie libérée à partir des énergies de liaison » (tableau d'E_ℓ ou
#    de E_ℓ/A ; E_ℓ = A·(E_ℓ/A) ; nucléon seul : 0), « diagramme énergétique » (nommer les trois niveaux ; flèche =
#    arrivée − départ), « équation : déterminer A et Z » ; pièges « bilan par E_ℓ à l'envers », « ξ soustraits sans × A »
#    (QCM 2019 N) ; Oualid : « même bilan par deux routes » (masses et E_ℓ) qui se recoupent.
#  - nationaux : 2023 N (fusion ³H + ²H par un tableau d'énergies de liaison), 2019 N (E_ℓ = A·ξ puis E_lib), 2020 N
#    (diagramme d'énergie) : mêmes gestes, sur une autre fusion (²H + ²H) et un diagramme sans valeurs à lire.
#  - séries en ligne (fusion deutérium-deutérium, « diagramme énergétique ») : extraits de recherche lus ; pages non
#    joignables depuis cette session.
#  - cours : diagramme.html?vue=fusion (10,841 MeV ; 28,296 MeV ; ΔE = −17,455 MeV), figures.html?fig=fig_methode_liaison,
#    fig_soddy, balance.html?vue=fusion (−0,01889 u ; −17,6 MeV) : l'explication dit d'abord les valeurs que la
#    simulation montre (exemple du cours), puis applique la même méthode à nos données.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_5"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
U = 931.5


def diagramme(titre, haut, milieu, bas, e_mil, e_bas):
    """Trois paliers (énergies comptées à partir du palier des nucléons séparés), flèches (1) (2) (3) sans valeur."""
    k = 2.7 / e_bas
    yh, ym, yb = 3.6, 3.6 - k * e_mil, 3.6 - k * e_bas
    els = [{"f": "fleche", "de": [0.5, 0.3], "a": [0.5, 4.1], "couleur": "blanc"},
           {"f": "texte", "at": [0.75, 4.0], "t": "E", "ancre": "gauche"}]
    for y, t, c in ((yh, haut, "cyan"), (ym, milieu, "jaune"), (yb, bas, "vert")):
        els.append({"f": "ligne", "pts": [[0.8, y], [5.2, y]], "couleur": c, "epais": True})
        els.append({"f": "texte", "at": [5.4, y - 0.1], "t": t, "couleur": c, "ancre": "gauche"})
    els += [{"f": "fleche", "de": [1.6, ym], "a": [1.6, yh], "couleur": "orange"},
            {"f": "texte", "at": [1.35, (ym + yh) / 2 - 0.1], "t": "(1)", "couleur": "orange", "ancre": "droite"},
            {"f": "fleche", "de": [3.0, yh], "a": [3.0, yb], "couleur": "rose"},
            {"f": "texte", "at": [3.25, (yh + ym) / 2 - 0.1], "t": "(2)", "couleur": "rose", "ancre": "gauche"},
            {"f": "fleche", "de": [4.4, ym], "a": [4.4, yb], "couleur": "jaune"},
            {"f": "texte", "at": [4.65, (ym + yb) / 2 - 0.1], "t": "(3)", "couleur": "jaune", "ancre": "gauche"},
            {"f": "texte", "at": [8.6, 0.35], "t": "échelle non respectée", "couleur": "faible", "ancre": "droite", "taille": "petit"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 9, "h": 4.3}, "elements": els,
            "legende": "Diagramme énergétique : nucléons séparés au repos (haut), réactifs au repos, produits au repos."}


# ---------------------------------------------------------------- calculs (énoncé : ²H + ²H → ³He + n)
A_X, Z_X = 2 + 2 - 1, 1 + 1 - 0
assert (A_X, Z_X) == (3, 2)
EL_D = 2 * 1.11                       # 2,22 MeV
EL_HE3 = 3 * 2.57                     # 7,71 MeV
F1 = 2 * EL_D                         # 4,44 MeV (flèche 1)
DE = F1 - EL_HE3                      # −3,27 MeV
assert round(EL_D, 2) == 2.22 and round(EL_HE3, 2) == 7.71 and round(F1, 2) == 4.44 and round(DE, 2) == -3.27
DM = 3.01493 + 1.00866 - 2 * 2.01355  # −0,00351 u
assert abs(DM + 0.00351) < 1e-9 and round(DM * U, 2) == -3.27
# cohérence des données : E_ℓ/A tirées des mêmes masses (m_p = 1,00728 u ; m_n = 1,00866 u)
assert round((1.00728 + 1.00866 - 2.01355) * U / 2, 2) == 1.11 and round((2 * 1.00728 + 1.00866 - 3.01493) * U / 3, 2) == 2.57
# semblable : ²H + ³He → ⁴He + ¹₁p
EL_HE4 = 4 * 7.07                     # 28,28
F1b = EL_D + EL_HE3                   # 9,93
DEb = F1b - EL_HE4                    # −18,35
DMb = 4.00150 + 1.00728 - 2.01355 - 3.01493   # −0,0197 u
assert round(F1b, 2) == 9.93 and round(DEb, 2) == -18.35 and abs(DMb + 0.0197) < 1e-9 and round(DMb * U, 2) == -18.35

DIAG = SIMD + "diagramme.html?vue=fusion"

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "La fusion de deux noyaux de deutérium : bilan par les énergies de liaison", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire l'équation d'une fusion (lois de Soddy)", "Calculer E_ℓ = A·(E_ℓ/A)", "Exploiter un diagramme énergétique",
                  "Calculer ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)", "Vérifier un bilan par les masses"],
  "enonce": {
    "intro": "Dans certaines étoiles, deux noyaux de deutérium fusionnent selon l'équation :\n²₁H + ²₁H → ᴬX + ¹₀n\nLe noyau ᴬX a pour nombre de masse A et pour nombre de charge Z.\nLa figure représente le diagramme énergétique de cette réaction (l'échelle n'est pas respectée).",
    "intro_dit": "دابا نقراو l'énoncé. فبعض النجوم، deux noyaux de deutérium كيديرو la fusion. l'équation: le deutérium plus le deutérium، كيعطيو noyau X، A و Z ما عارفينهمش، plus un neutron. la figure هي le diagramme énergétique ديال هاد la réaction، و l'échelle ماشي محترمة.",
    "figures": [diagramme("Figure : diagramme énergétique de la fusion", "2 ¹₁p + 2 ¹₀n", "2 ²₁H", "^{A}_{Z}X + ¹₀n", 4.44, 7.71)],
    "donnees": ["E_ℓ/A(²₁H) = 1,11 MeV/nucléon ; E_ℓ/A(³₂He) = 2,57 MeV/nucléon",
                "m(²₁H) = 2,01355 u ; m(³₂He) = 3,01493 u ; m(¹₀n) = 1,00866 u", "1 u = 931,5 MeV/c²"],
    "questions": [
      question("1", "Déterminer A et Z, puis identifier le noyau X parmi : ³₁H, ³₂He, ⁴₂He.",
        "السؤال un: حدد A و Z، ومن بعد عرف النواة X: واش le tritium، ولا l'hélium trois، ولا l'hélium quatre.",
        phrase("Conservation de A : 2 + 2 = A + 1, donc A = 3. Conservation de Z : 1 + 1 = Z + 0, donc Z = 2. X est ³₂He (hélium 3) : ²₁H + ²₁H → ³₂He + ¹₀n."),
        ["conservation de A", "conservation de Z", "³₂He"], ["A = 4", "Z = 1"],
        [aide("Écris l'égalité des nombres du haut (A), puis celle des nombres du bas (Z), en comptant le neutron.",
              "كتب المساواة ديال les nombres اللي الفوق، A، ومن بعد اللي لتحت، Z، وحسب حتى le neutron."),
         aide("2 + 2 = A + 1 et 1 + 1 = Z + 0. Le noyau de Z = 2 est l'hélium.",
              "deux plus deux égale A plus un، et un plus un égale Z plus zéro. النواة اللي عندها Z égale deux هي l'hélium.")],
        corr([("1 : conservation de A : 2 + 2 = A + 1 ⇒ A = 3", "la conservation ديال A"),
              ("conservation de Z : 1 + 1 = Z + 0 ⇒ Z = 2", "la conservation ديال Z"),
              ("X = ³₂He : ²₁H + ²₁H → ³₂He + ¹₀n", "X هو l'hélium trois")],
             "السؤال un. la conservation ديال A: deux plus deux égale A plus un، إذن A égale trois. la conservation ديال Z: un plus un égale Z plus zéro، إذن Z égale deux. X هو l'hélium trois."),
        "ex_n5_1", "fa_n5_1"),
      question("2", "Calculer, en MeV, les énergies de liaison E_ℓ(²₁H) et E_ℓ(³₂He).",
        "السؤال deux: حسب ب méga électron volt l'énergie de liaison ديال le deutérium، و ديال l'hélium trois.",
        valeur("E_ℓ(³He)", 7.71, "MeV", "E_ℓ(²H) = 2 × 1,11 = 2,22 MeV ; E_ℓ(³He) = 3 × 2,57 = 7,71 MeV"),
        ["E_ℓ = A·(E_ℓ/A)", "A = 2", "A = 3", "MeV"], ["E_ℓ = (E_ℓ/A)/A", "E_ℓ = Z·(E_ℓ/A)"],
        [aide("Les données sont des énergies de liaison PAR NUCLÉON. Combien de nucléons dans chaque noyau ?",
              "les données راهم énergies de liaison par nucléon. شحال من nucléon فكل نواة؟"),
         aide("E_ℓ = A × (E_ℓ/A) : on multiplie par A (2 pour ²H, 3 pour ³He).",
              "E l égale A fois E l sur A. كنضربو ف A: deux بالنسبة ل le deutérium، et trois بالنسبة ل l'hélium trois.")],
        corr([("2 : E_ℓ = A·(E_ℓ/A)", "E l égale A fois E l sur A"),
              ("E_ℓ(²H) = 2 × 1,11 = 2,22 MeV", "deux virgule vingt-deux méga électron volt"),
              ("E_ℓ(³He) = 3 × 2,57 = 7,71 MeV", "sept virgule soixante et onze méga électron volt")],
             "السؤال deux. E l égale A fois E l sur A. le deutérium: deux fois un virgule onze، يعني deux virgule vingt-deux méga électron volt. l'hélium trois: trois fois deux virgule cinquante-sept، يعني sept virgule soixante et onze méga électron volt."),
        "ex_n5_2", "fa_n5_2"),
      question("3", "Que représentent les énergies associées aux flèches (1) et (2) du diagramme ? Donner leurs valeurs.",
        "السؤال trois: شنو كتمثل l'énergie ديال la flèche un، و ديال la flèche deux فle diagramme؟ عطي القيم ديالهم.",
        phrase("Flèche (1) : l'énergie qu'il faut fournir pour séparer les deux noyaux de deutérium en nucléons au repos : 2·E_ℓ(²H) = 4,44 MeV. Flèche (2) : l'énergie libérée quand les nucléons séparés forment ³₂He et le neutron : E_ℓ(³He) + E_ℓ(n) = 7,71 + 0 = 7,71 MeV (un neutron seul n'a pas d'énergie de liaison)."),
        ["2·E_ℓ(²H)", "E_ℓ(³He)", "E_ℓ(n) = 0", "fournie", "libérée"], ["flèche (1) = E_ℓ(²H)", "E_ℓ(n) = 1,00866 MeV"],
        [aide("La flèche (1) monte des réactifs vers les nucléons séparés ; la flèche (2) descend des nucléons séparés vers les produits.",
              "la flèche un كتطلع من les réactifs ل les nucléons بعاد. la flèche deux كتهبط من les nucléons بعاد ل les produits."),
         aide("Séparer un noyau coûte E_ℓ ; il y a deux noyaux de deutérium. Former les produits libère leurs E_ℓ ; le neutron seul : E_ℓ = 0.",
              "باش نفرقو النواة خاصنا نعطيو E l، وعندنا، les deux noyaux de deutérium. ملي كتكون les produits كتخرج les énergies de liaison ديالهم، و le neutron بوحدو E l ديالو égale zéro.")],
        corr([("3 : flèche (1) : énergie fournie pour séparer 2 ²H : 2·E_ℓ(²H) = 2 × 2,22 = 4,44 MeV", "la flèche un"),
              ("flèche (2) : énergie libérée en formant ³He + n : E_ℓ(³He) + 0 = 7,71 MeV", "la flèche deux"),
              ("(un nucléon seul : E_ℓ = 0)", "le neutron بوحدو")],
             "السؤال trois. la flèche un: l'énergie اللي خاصنا نعطيو باش نفرقو les deux noyaux de deutérium، deux fois deux virgule vingt-deux، يعني quatre virgule quarante-quatre méga électron volt. la flèche deux: l'énergie اللي كتخرج ملي كيتكون l'hélium trois و le neutron، sept virgule soixante et onze méga électron volt. le neutron بوحدو ما عندو حتى énergie de liaison."),
        "ex_n5_3", "fa_n5_3"),
      question("4", "En exploitant le diagramme, montrer que ΔE = 2·E_ℓ(²H) − E_ℓ(³He), puis calculer l'énergie libérée E_lib.",
        "السؤال quatre: بالاستعانة ب le diagramme، بين بلي delta E égale deux E l du deutérium moins E l de l'hélium trois، ومن بعد حسب l'énergie libérée.",
        valeur("E_lib", 3.27, "MeV", "ΔE = 2·E_ℓ(²H) − E_ℓ(³He) = 4,44 − 7,71 = −3,27 MeV ; E_lib = |ΔE| = 3,27 MeV"),
        ["ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)", "flèche (3) = (1) + (2)", "E_lib = |ΔE|"], ["ΔE = 7,71 − 4,44", "ΔE = 2,22 − 7,71"],
        [aide("Pour aller des réactifs aux produits, on peut passer par le palier du haut : on monte de (1), puis on descend de (2).",
              "باش نمشيو من les réactifs ل les produits، نقدرو نفوتو من الفوق: كنطلعو ب la flèche un، ومن بعد كنهبطو ب la flèche deux."),
         aide("ΔE = (+4,44) + (−7,71) : une flèche qui monte compte +, une flèche qui descend compte −. Puis E_lib = |ΔE|.",
              "delta E égale plus quatre virgule quarante-quatre، plus moins sept virgule soixante et onze. la flèche اللي كتطلع positive، واللي كتهبط négative. ومن بعد E libérée égale la valeur absolue de delta E.")],
        corr([("4 : ΔE = E_f − E_i = (1) + (2) = 2·E_ℓ(²H) − [E_ℓ(³He) + E_ℓ(n)]", "delta E égale E f moins E i"),
              ("ΔE = 4,44 − 7,71 = −3,27 MeV", "delta E égale moins trois virgule vingt-sept"),
              ("ΔE < 0 : E_lib = |ΔE| = 3,27 MeV", "E libérée égale trois virgule vingt-sept")],
             "السؤال quatre. delta E égale E f moins E i. من les réactifs ل les produits: كنطلعو de quatre virgule quarante-quatre، ومن بعد كنهبطو de sept virgule soixante et onze. إذن delta E égale deux E l du deutérium moins E l de l'hélium trois، يعني quatre virgule quarante-quatre moins sept virgule soixante et onze: delta E égale moins trois virgule vingt-sept méga électron volt. E libérée égale trois virgule vingt-sept méga électron volt."),
        "ex_n5_4", "fa_n5_4"),
      question("5", "Retrouver l'énergie libérée à partir des masses des noyaux. Conclure.",
        "السؤال cinq: عاود لقى l'énergie libérée ب les masses ديال les noyaux، وستنتج.",
        valeur("E_lib", 3.27, "MeV", "Δm = m(³He) + m_n − 2m(²H) = 3,01493 + 1,00866 − 2 × 2,01355 = −0,00351 u ; E_lib = |Δm|·c² = 0,00351 × 931,5 = 3,27 MeV"),
        ["Δm = Σm(produits) − Σm(réactifs)", "2m(²H)", "931,5"], ["oublier le neutron", "Δm = 2m(²H) − m(³He)"],
        [aide("Écris Δm de la réaction : produits (³He et le neutron) moins réactifs (deux noyaux ²H).",
              "كتب delta m ديال la réaction: les produits، l'hélium trois و le neutron، moins les réactifs، deux noyaux de deutérium."),
         aide("Δm = 3,01493 + 1,00866 − 2 × 2,01355 ; puis ΔE = Δm × 931,5 et E_lib = |ΔE|. Compare avec la question 4.",
              "delta m égale trois virgule zéro un quatre cent quatre-vingt-treize plus un virgule zéro zéro huit cent soixante-six، moins deux fois deux virgule zéro un trois cent cinquante-cinq. ومن بعد fois neuf cent trente et un virgule cinq، وقارن مع السؤال quatre.")],
        corr([("5 : Δm = m(³He) + m_n − 2m(²H) = 3,01493 + 1,00866 − 4,02710 = −0,00351 u", "moins zéro virgule zéro zéro trois cent cinquante et un u"),
              ("ΔE = −0,00351 × 931,5 = −3,27 MeV ; E_lib = 3,27 MeV", "trois virgule vingt-sept méga électron volt"),
              ("Même résultat par les deux méthodes : le bilan est cohérent.", "نفس النتيجة par les deux méthodes")],
             "السؤال cinq. delta m égale la masse de l'hélium trois plus la masse du neutron، moins deux fois la masse du deutérium. يعني moins zéro virgule zéro zéro trois cent cinquante et un u. delta E égale delta m fois neuf cent trente et un virgule cinq، يعني moins trois virgule vingt-sept، و E libérée égale trois virgule vingt-sept méga électron volt. نفس النتيجة par les deux méthodes: الحساب صحيح."),
        "ex_n5_5", "fa_n5_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n5_1", "Question 1 : A et Z du noyau X", "A : 2 + 2 = A + 1 ⇒ A = 3 ; Z : 1 + 1 = Z ⇒ Z = 2 ; X = ³₂He",
      SIMD + "figures.html?fig=fig_soddy", "La méthode de Soddy, sur l'exemple de la fission du cours",
      "شوف la méthode على l'exemple ديال le cours: la fission ديال l'uranium. la conservation ديال A: deux cent trente-six égale deux cent trente-quatre plus x، إذن x égale deux. la conservation ديال Z: quatre-vingt-douze على اليسار، et quatre-vingt-douze على اليمين. نفس الطريقة فالتمرين ديالنا: deux plus deux égale A plus un، إذن A égale trois. un plus un égale Z plus zéro، إذن Z égale deux. Z égale deux هو l'hélium: X هو l'hélium trois.",
      centre=[("2 + 2 = A + 1 ⇒ A = 3", "إذن A égale trois"), ("1 + 1 = Z + 0 ⇒ Z = 2 : X = ³₂He", "إذن Z égale deux")],
      pointage=[{"mot": "شوف la méthode", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "la conservation ديال A", "commande": "play_until", "parametres": {"moment": "A"}},
                {"mot": "la conservation ديال Z", "commande": "play_until", "parametres": {"moment": "Z"}}]),
    diapo_sim("ex_n5_2", "Question 2 : E_ℓ = A × (E_ℓ/A)", "E_ℓ(²H) = 2 × 1,11 = 2,22 MeV ; E_ℓ(³He) = 3 × 2,57 = 7,71 MeV",
      SIMD + "figures.html?fig=fig_methode_liaison", "Énergie libérée par les énergies de liaison : E_ℓ = A·(E_ℓ/A)",
      "شوف la formule: delta E égale la somme des E l des réactifs moins la somme des E l des produits. ولكن يلا التمرين عطاك E l sur A، ضرب اللول ف A: E l égale A fois E l sur A. le deutérium، A égale deux: deux fois un virgule onze، يعني deux virgule vingt-deux. l'hélium trois، A égale trois: trois fois deux virgule cinquante-sept، يعني sept virgule soixante et onze méga électron volt. و nucléon بوحدو، E l ديالو égale zéro.",
      centre=[("E_ℓ(²H) = 2 × 1,11 = 2,22 MeV", "deux fois un virgule onze"), ("E_ℓ(³He) = 3 × 2,57 = 7,71 MeV", "trois fois deux virgule cinquante-sept")],
      pointage=[{"mot": "شوف la formule", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "ضرب اللول ف A", "commande": "play_until", "parametres": {"moment": "A_fois"}},
                {"mot": "و nucléon بوحدو", "commande": "play_until", "parametres": {"moment": "nucleon_libre"}}]),
    diapo_sim("ex_n5_3", "Question 3 : les flèches du diagramme", "(1) : fournir 2·E_ℓ(²H) = 4,44 MeV ; (2) : récupérer E_ℓ(³He) = 7,71 MeV",
      DIAG, "Le diagramme du cours : nucléons séparés, réactifs, produits",
      "شوف le diagramme ديال le cours. الفوق: les nucléons بعاد. فالوسط: les réactifs. التحت: les produits. la flèche اللي كتطلع: باش نهرسو les réactifs، كنعطيو les énergies de liaison ديالهم، ici dix virgule huit cent quarante et un. la flèche اللي كتهبط: ملي كتكون les produits، كناخدو E l ديالهم، ici vingt-huit virgule deux cent quatre-vingt-seize. le neutron بوحدو: zéro. فالتمرين ديالنا: la flèche un égale deux fois deux virgule vingt-deux، يعني quatre virgule quarante-quatre méga électron volt. la flèche deux égale sept virgule soixante et onze méga électron volt.",
      centre=[("(1) = 2·E_ℓ(²H) = 4,44 MeV (fournie)", "la flèche un égale deux fois"), ("(2) = E_ℓ(³He) + 0 = 7,71 MeV (libérée)", "la flèche deux égale sept")],
      pointage=[{"mot": "الفوق: les nucléons", "commande": "play_until", "parametres": {"moment": "niveau_nucleons"}},
                {"mot": "فالوسط: les réactifs", "commande": "play_until", "parametres": {"moment": "niveau_reactifs"}},
                {"mot": "التحت: les produits", "commande": "play_until", "parametres": {"moment": "niveau_produits"}},
                {"mot": "la flèche اللي كتطلع", "commande": "play_until", "parametres": {"moment": "fleche_El_reactifs"}},
                {"mot": "la flèche اللي كتهبط", "commande": "play_until", "parametres": {"moment": "fleche_El_produits"}}]),
    diapo_sim("ex_n5_4", "Question 4 : ΔE par le diagramme", "ΔE = (1) + (2) = 4,44 − 7,71 = −3,27 MeV ; E_lib = 3,27 MeV",
      DIAG, "La flèche ΔE va des réactifs aux produits",
      "شوف la flèche delta E: من les réactifs ل les produits. delta E égale E f moins E i. فle cours: dix virgule huit cent quarante et un moins vingt-huit virgule deux cent quatre-vingt-seize، يعني moins dix-sept virgule quatre cent cinquante-cinq. فالتمرين ديالنا: كنطلعو de quatre virgule quarante-quatre، ومن بعد كنهبطو de sept virgule soixante et onze. delta E égale moins trois virgule vingt-sept méga électron volt. négatif: l'énergie كتخرج. E libérée égale trois virgule vingt-sept méga électron volt.",
      centre=[("ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)", "delta E égale E f moins E i"), ("ΔE = 4,44 − 7,71 = −3,27 MeV ; E_lib = 3,27 MeV", "delta E égale moins trois virgule vingt-sept")],
      pointage=[{"mot": "شوف la flèche delta E", "commande": "play_until", "parametres": {"moment": "fleche_delta_E"}},
                {"mot": "فle cours:", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_n5_5", "Question 5 : la même énergie par les masses", "Δm = 3,01493 + 1,00866 − 4,02710 = −0,00351 u ; E_lib = 0,00351 × 931,5 = 3,27 MeV",
      SIMD + "balance.html?vue=fusion", "La balance : les produits sont plus légers que les réactifs",
      "شوف الميزان ديال le cours: les réactifs على اليسار، les produits على اليمين، والميزان كيهبط من جيهة les réactifs. فle cours، delta m égale moins zéro virgule zéro un mille huit cent quatre-vingt-neuf u. فالتمرين ديالنا: les produits، l'hélium trois و le neutron: quatre virgule zéro deux mille trois cent cinquante-neuf u. les réactifs، deux noyaux de deutérium: quatre virgule zéro deux mille sept cent dix u. delta m égale moins zéro virgule zéro zéro trois cent cinquante et un u. fois neuf cent trente et un virgule cinq: E libérée égale trois virgule vingt-sept méga électron volt، نفس النتيجة.",
      centre=[("Δm = 4,02359 − 4,02710 = −0,00351 u", "delta m égale moins zéro virgule zéro zéro"), ("E_lib = 0,00351 × 931,5 = 3,27 MeV", "E libérée égale trois virgule vingt-sept")],
      pointage=[{"mot": "شوف الميزان", "commande": "play_until", "parametres": {"moment": "balance_penche"}},
                {"mot": "فle cours، delta m", "commande": "play_until", "parametres": {"moment": "delta_m"}}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n5_1", "Plus facile : identifier X", "نتمرنو: شنو هي النواة X؟",
      "²₁H + ²₁H → ᴬX + ¹₀n (X : nombre de masse A, nombre de charge Z). Le noyau X est :",
      ["⁴₂He", "³₂He", "³₁H"], 1, {
        "1": {"juste": rep("برافو! A égale trois، و Z égale deux: l'hélium trois.", "Juste : A = 3, Z = 2 : ³₂He.")},
        "0": {"1": rep("ما تقلقش. حسب A: deux plus deux égale A plus un. واش نسيتي le neutron؟ عاود اختار.", "As-tu compté le neutron dans la conservation de A ? Réessaie."),
              "2": rep("الجواب هو l'hélium trois: A égale quatre moins un، يعني trois.", "Réponse : ³₂He (A = 4 − 1 = 3).")},
        "2": {"1": rep("قريب، A صحيح. ولكن حسب Z: un plus un égale Z plus zéro. عاود اختار.", "A est juste ; vérifie Z : 1 + 1 = Z. Réessaie."),
              "2": rep("الجواب هو l'hélium trois: Z égale deux، et pas un.", "Réponse : ³₂He (Z = 2).")}},
      "Deutérium plus deutérium donne X plus un neutron. Le noyau X est lequel ?"),
    qcm_facile("fa_n5_2", "Plus facile : de E_ℓ/A à E_ℓ", "سؤال ساهل: من E l sur A ل E l.",
      "E_ℓ/A(³₂He) = 2,57 MeV/nucléon. Alors E_ℓ(³₂He) vaut :",
      ["0,86 MeV", "5,14 MeV", "7,71 MeV"], 2, {
        "2": {"juste": rep("برافو! trois fois deux virgule cinquante-sept، يعني sept virgule soixante et onze.", "Juste : 3 × 2,57 = 7,71 MeV.")},
        "0": {"1": rep("ما تقلقش. قسمتي على A، ولكن خاصك تضرب. عاود اختار.", "Tu as divisé par A ; il faut multiplier. Réessaie."),
              "2": rep("الجواب: E l égale A fois E l sur A، يعني sept virgule soixante et onze méga électron volt.", "Réponse : E_ℓ = A × (E_ℓ/A) = 7,71 MeV.")},
        "1": {"1": rep("قريب. ضربتي ف Z égale deux. ولكن E l sur A ديال كل les nucléons. عاود اختار.", "Tu as multiplié par Z ; il faut multiplier par A. Réessaie."),
              "2": rep("الجواب: كنضربو ف A égale trois، يعني sept virgule soixante et onze.", "Réponse : on multiplie par A = 3 : 7,71 MeV.")}},
      "E l sur A de l'hélium trois égale deux virgule cinquante-sept méga électron volt par nucléon. Alors E l vaut combien ?"),
    association_facile("fa_n5_3", "Plus facile : les flèches du diagramme", "سؤال ساهل: ربط كل flèche بالمعنى ديالها.",
      "Relie chaque flèche du diagramme à ce qu'elle représente.", "Associer chaque flèche à son énergie.",
      [("1", "flèche (1) : des réactifs vers les nucléons séparés"), ("2", "flèche (2) : des nucléons séparés vers les produits"), ("3", "flèche (3) : des réactifs vers les produits")],
      [("a", "ΔE de la réaction"), ("b", "énergie fournie : somme des E_ℓ des réactifs"), ("c", "énergie récupérée : somme des E_ℓ des produits")],
      {"1": "b", "2": "c", "3": "a"},
      {"1-b": (True, "Oui : pour casser les réactifs en nucléons, on fournit leurs énergies de liaison.", "صحيح. باش نهرسو les réactifs، كنعطيو les énergies de liaison ديالهم."),
       "1-c": (False, "La flèche (1) monte : on fournit de l'énergie. Est-ce aux produits ou aux réactifs ?", "la flèche un كتطلع: كنعطيو l'énergie. ل les réactifs ولا ل les produits؟"),
       "1-a": (False, "ΔE va directement des réactifs aux produits ; la flèche (1) s'arrête aux nucléons séparés.", "delta E كتمشي من les réactifs ل les produits مباشرة. la flèche un كتوقف عند les nucléons."),
       "2-c": (True, "Oui : quand les nucléons forment les produits, leurs énergies de liaison sont libérées.", "صحيح. ملي les nucléons كيكونو les produits، كتخرج les énergies de liaison ديالهم."),
       "2-b": (False, "La flèche (2) descend vers les produits : c'est de l'énergie récupérée, pas fournie.", "la flèche deux كتهبط ل les produits: l'énergie كتخرج، ماشي كنعطيوها."),
       "2-a": (False, "La flèche (2) part du palier des nucléons séparés, pas des réactifs.", "la flèche deux كتبدا من les nucléons بعاد، ماشي من les réactifs."),
       "3-a": (True, "Oui : ΔE = E(produits) − E(réactifs).", "صحيح. delta E égale E f moins E i."),
       "3-b": (False, "La flèche (3) ne passe pas par les nucléons séparés : c'est le bilan direct.", "la flèche trois ما كتفوتش من les nucléons: هادي الحصيلة."),
       "3-c": (False, "La flèche (3) part des réactifs : c'est le bilan de la réaction.", "la flèche trois كتبدا من les réactifs: هادي الحصيلة ديال la réaction.")},
      "(1 ; b) (2 ; c) (3 ; a) : on fournit ΣE_ℓ(réactifs), on récupère ΣE_ℓ(produits), ΔE est le bilan.",
      "الأزواج: un avec b، deux avec c، trois avec a. كنعطيو E l ديال les réactifs، كناخدو E l ديال les produits، و delta E هي الحصيلة."),
    qcm_facile("fa_n5_4", "Plus facile : la formule par les E_ℓ", "سؤال ساهل: الترتيب ف la formule.",
      "À partir des énergies de liaison, on écrit :",
      ["ΔE = ΣE_ℓ(produits) − ΣE_ℓ(réactifs)", "ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)", "ΔE = ΣE_ℓ(réactifs) + ΣE_ℓ(produits)"], 1, {
        "1": {"juste": rep("برافو! les réactifs اللولين: كنعطيوها، ومن بعد كناخدو ديال les produits.", "Juste : on fournit E_ℓ(réactifs), on récupère E_ℓ(produits).")},
        "0": {"1": rep("فخ معروف: هاد الترتيب ديال les masses. ب les énergies de liaison، الترتيب بالمقلوب. عاود اختار.", "C'est l'ordre des masses ; avec les E_ℓ, il est inversé. Réessaie."),
              "2": rep("الجواب: delta E égale la somme des E l des réactifs moins la somme des E l des produits.", "Réponse : ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits).")},
        "2": {"1": rep("لا، la flèche اللي كتهبط كتحسب négative. عاود اختار.", "La flèche qui descend compte négativement. Réessaie."),
              "2": rep("الجواب: delta E égale la somme des E l des réactifs moins la somme des E l des produits.", "Réponse : ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits).")}},
      "À partir des énergies de liaison, on écrit delta E comment ?"),
    vrai_faux_facile("fa_n5_5", "Plus facile : vrai ou faux", "سؤال ساهل على les deux méthodes.",
      "²H + ²H → ³He + n : E_lib = 3,27 MeV par les énergies de liaison.",
      [("Par les masses, on doit retrouver environ la même énergie libérée.", True, "Les deux méthodes donnent le même bilan (aux arrondis près)."),
       ("Dans Δm, on peut oublier le neutron car il est léger.", False, "Toutes les particules de l'équation comptent : 1,00866 u, c'est énorme devant 0,00351 u."),
       ("Pour cette réaction, Δm est négatif.", True, "Les produits sont plus légers : Δm = −0,00351 u.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, une autre fusion : deutérium et hélium 3",
    "enonce": {
      "intro": "Une autre fusion : ²₁H + ³₂He → ⁴₂He + ᴬY (Y : nombre de masse A, nombre de charge Z). La figure donne son diagramme énergétique (échelle non respectée).",
      "intro_dit": "fusion أخرى: le deutérium plus l'hélium trois، كيعطيو l'hélium quatre، plus particule Y.",
      "figures": [diagramme("Figure : diagramme énergétique de la fusion", "3 ¹₁p + 2 ¹₀n", "²₁H + ³₂He", "⁴₂He + ^{A}_{Z}Y", 9.93, 28.28)],
      "donnees": ["E_ℓ/A : ²₁H : 1,11 ; ³₂He : 2,57 ; ⁴₂He : 7,07 MeV/nucléon",
                  "m(²₁H) = 2,01355 u ; m(³₂He) = 3,01493 u ; m(⁴₂He) = 4,00150 u ; m_p = 1,00728 u", "1 u = 931,5 MeV/c²"],
      "questions": [
        question_semblable("1", "Déterminer A et Z, puis identifier la particule Y parmi : ¹₀n, ¹₁p, ⁰₋₁e.",
          phrase("A : 2 + 3 = 4 + A, donc A = 1 ; Z : 1 + 2 = 2 + Z, donc Z = 1 : Y est un proton ¹₁p."),
          ["conservation de A", "conservation de Z"], ["Y = ¹₀n"],
          corr([("1 : A = 5 − 4 = 1 ; Z = 3 − 2 = 1 : Y = ¹₁p (proton)", "Y، c'est un proton")],
               "A égale un، et Z égale un: Y، c'est un proton.")),
        question_semblable("2", "Calculer, en MeV, les énergies de liaison des noyaux ²₁H, ³₂He et ⁴₂He.",
          valeur("E_ℓ(⁴He)", 28.28, "MeV", "E_ℓ(²H) = 2,22 MeV ; E_ℓ(³He) = 7,71 MeV ; E_ℓ(⁴He) = 4 × 7,07 = 28,28 MeV"),
          ["E_ℓ = A·(E_ℓ/A)"], ["E_ℓ = Z·(E_ℓ/A)"],
          corr([("2 : E_ℓ(²H) = 2 × 1,11 = 2,22 MeV ; E_ℓ(³He) = 3 × 2,57 = 7,71 MeV ; E_ℓ(⁴He) = 4 × 7,07 = 28,28 MeV", "vingt-huit virgule vingt-huit")],
               "E l égale A fois E l sur A: deux virgule vingt-deux، sept virgule soixante et onze، et vingt-huit virgule vingt-huit méga électron volt.")),
        question_semblable("3", "Que représentent les énergies associées aux flèches (1) et (2) ? Donner leurs valeurs.",
          phrase("(1) : énergie fournie pour séparer ²H et ³He en nucléons : E_ℓ(²H) + E_ℓ(³He) = 9,93 MeV. (2) : énergie libérée en formant ⁴He et le proton : E_ℓ(⁴He) + 0 = 28,28 MeV (un proton seul : E_ℓ = 0)."),
          ["E_ℓ(p) = 0"], ["E_ℓ(p) = 1,00728 MeV"],
          corr([("3 : (1) = 2,22 + 7,71 = 9,93 MeV (fournie) ; (2) = 28,28 + 0 = 28,28 MeV (libérée)", "neuf virgule quatre-vingt-treize")],
               "la flèche un: neuf virgule quatre-vingt-treize méga électron volt، كنعطيوها. la flèche deux: vingt-huit virgule vingt-huit، كتخرج.")),
        question_semblable("4", "Montrer que ΔE = E_ℓ(²H) + E_ℓ(³He) − E_ℓ(⁴He), puis calculer E_lib.",
          valeur("E_lib", 18.35, "MeV", "ΔE = 9,93 − 28,28 = −18,35 MeV ; E_lib = |ΔE| = 18,35 MeV"), ["ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)"], ["ΔE = 28,28 − 9,93"],
          corr([("4 : ΔE = (1) + (2) = 9,93 − 28,28 = −18,35 MeV ; E_lib = 18,35 MeV", "dix-huit virgule trente-cinq")],
               "delta E égale neuf virgule quatre-vingt-treize moins vingt-huit virgule vingt-huit، يعني moins dix-huit virgule trente-cinq. E libérée égale dix-huit virgule trente-cinq méga électron volt.")),
        question_semblable("5", "Retrouver l'énergie libérée à partir des masses. Conclure.",
          valeur("E_lib", 18.35, "MeV", "Δm = 4,00150 + 1,00728 − 2,01355 − 3,01493 = −0,01970 u ; E_lib = 0,01970 × 931,5 = 18,35 MeV"),
          ["Δm = Σm(produits) − Σm(réactifs)"], ["oublier le proton"],
          corr([("5 : Δm = −0,01970 u ; E_lib = 0,01970 × 931,5 = 18,35 MeV : même résultat.", "moins zéro virgule zéro dix-neuf mille sept cents u")],
               "delta m égale moins zéro virgule zéro dix-neuf mille sept cents u. E libérée égale dix-huit virgule trente-cinq méga électron volt: نفس النتيجة.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
