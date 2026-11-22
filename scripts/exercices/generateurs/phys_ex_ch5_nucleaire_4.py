# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau moyen n° 4 : la fission de l'uranium 235 — lois de
# Soddy, Δm de la réaction, ΔE et E_lib en MeV puis en joule, énergie libérée par nucléon (comparée à la fusion).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration energie_nucleaire.json : cas_types « énergie libérée par une réaction, masses données » (7/20, le plus
#    fréquent), « équation d'une fission : déterminer A et Z, x neutrons » ; pièges « E_lib négative », « neutrons
#    oubliés dans Δm », « 1 MeV = 1,6·10⁻¹⁹ J » ; rédaction : équation complète → Δm → ΔE → E_lib = |ΔE| (10/10 profs) ;
#    conseil « E_lib d'une fission ≈ 200 MeV ».
#  - nationaux : 2016 N (Soddy puis E_lib d'une fusion par les masses), 2017 R, 2018 R, 2022 N, 2024 R (« Calculer, en
#    MeV, l'énergie libérée ») ; la fission n'est pas tombée depuis 2016 mais elle est au programme (cours en_b4) :
#    même chaîne de questions que ces sujets, sur une fission.
#  - séries en ligne (talamidi, alloschool : fission ²³⁵U + n → Sr + Xe + x n, « trouver x », « énergie libérée en MeV
#    et en J ») : extraits de recherche lus ; pages non joignables depuis cette session.
#  - cours : figures.html?fig=fig_soddy (x = 2 pour Sr 94 + Xe 140), balance.html?vue=fission (236,00216 u ;
#    235,80382 u ; −0,19834 u ; −184,8 MeV ; ≈ 185 MeV), fig_unites (1 MeV = 1,6·10⁻¹³ J), comparaison.html
#    (0,78 MeV/nucléon contre 3,5) : nos données sont exactement celles de ces simulations.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_4"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
MN, U, MEV = 1.00866, 931.5, 1.6e-13


def fission(titre, f1, f2, x):
    """Le neutron, le noyau d'uranium, puis les deux fragments et x neutrons (schéma qualitatif)."""
    els = []
    def boule(c, r, t, coul):
        els.append({"f": "cercle", "c": c, "r": r, "couleur": coul, "remplir": coul})
        els.append({"f": "texte", "at": [c[0], c[1] - 0.12], "t": t, "ancre": "centre"})
    boule([0.5, 1.8], 0.22, "n", "bleu")
    els.append({"f": "fleche", "de": [0.8, 1.8], "a": [1.5, 1.8], "couleur": "blanc"})
    boule([2.6, 1.8], 0.95, "²³⁵₉₂U", "violet")
    els.append({"f": "fleche", "de": [3.75, 1.8], "a": [4.75, 1.8], "couleur": "orange", "texte": "fission", "pos": "n"})
    boule([5.8, 2.6], 0.62, f1, "violet")
    boule([5.8, 0.85], 0.75, f2, "violet")
    # le nombre x de neutrons est demandé : un seul neutron dessiné, marqué « x ¹₀n » (la figure ne donne pas x)
    els.append({"f": "fleche", "de": [6.65, 1.75], "a": [7.25, 1.75], "couleur": "faible"})
    boule([7.5, 1.75], 0.22, "n", "bleu")
    els.append({"f": "texte", "at": [7.5, 1.05], "t": "x ¹₀n", "couleur": "cyan", "ancre": "centre"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 9, "h": 3.6}, "elements": els,
            "legende": "Un neutron lent frappe un noyau d'uranium 235, qui se scinde en deux noyaux plus légers et libère x neutrons."}


# ---------------------------------------------------------------- calculs (énoncé : Sr 94 + Xe 140)
X = 235 + 1 - 94 - 140                       # 2
Zs = 92 + 0 - 54                             # 38
assert X == 2 and Zs == 38
MR = 234.9935 + MN                           # 236,00216
MP_ = 93.8945 + 139.8920 + X * MN            # 235,80382
DM = MP_ - MR                                # −0,19834
DE = DM * U                                  # −184,75
ELIB = abs(DE)
EJ = 184.8 * MEV                             # 2,96·10⁻¹¹ J
PN = 184.8 / 236                             # 0,78 MeV/nucléon
assert abs(MR - 236.00216) < 1e-9 and abs(MP_ - 235.80382) < 1e-9 and abs(DM + 0.19834) < 1e-9
assert round(ELIB, 1) == 184.8 and abs(EJ - 2.957e-11) < 1e-14 and round(PN, 2) == 0.78
assert round(17.6 / 5, 1) == 3.5
# semblable : Ba 141 + Kr 92 + 3 n
X2 = 236 - 141 - 92; Zk = 92 - 56
assert X2 == 3 and Zk == 36
MP2 = 140.88367 + 91.90639 + X2 * MN         # 235,81604
DM2 = MP2 - MR                               # −0,18612
ELIB2 = abs(DM2 * U)                         # 173,4
EJ2 = 173.4 * MEV                            # 2,77·10⁻¹¹
PN2 = 173.4 / 236                            # 0,73
assert abs(DM2 + 0.18612) < 1e-9 and round(ELIB2, 1) == 173.4 and abs(EJ2 - 2.7744e-11) < 1e-14 and round(PN2, 2) == 0.73

BAL = SIMD + "balance.html?vue=fission"

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "La fission de l'uranium 235 : équation et énergie libérée", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire l'équation d'une fission avec les lois de Soddy", "Calculer Δm d'une réaction et l'énergie libérée E_lib = |ΔE|",
                  "Convertir des MeV en joule", "Comparer fission et fusion par nucléon"],
  "enonce": {
    "intro": "Dans le cœur d'une centrale nucléaire, un neutron lent provoque la fission d'un noyau d'uranium 235 selon l'équation :\n²³⁵₉₂U + ¹₀n → ⁹⁴Sr + ¹⁴⁰₅₄Xe + x ¹₀n\nLe nombre de charge Z du strontium ⁹⁴Sr est à déterminer.",
    "intro_dit": "دابا نقراو l'énoncé. فقلب une centrale nucléaire، un neutron lent كيضرب le noyau ديال l'uranium deux cent trente-cinq، وكيدير la fission. l'équation: l'uranium deux cent trente-cinq plus un neutron، كيعطيو le strontium quatre-vingt-quatorze، Z ما عارفينهش، plus le xénon cent quarante، plus x neutrons.",
    "figures": [fission("Figure : la fission d'un noyau d'uranium 235", "⁹⁴Sr", "¹⁴⁰Xe", 2)],
    "donnees": ["m(²³⁵₉₂U) = 234,9935 u ; m(⁹⁴Sr) = 93,8945 u ; m(¹⁴⁰₅₄Xe) = 139,8920 u", "m(¹₀n) = 1,00866 u",
                "1 u = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J"],
    "questions": [
      question("1", "En appliquant les lois de conservation, déterminer le nombre x de neutrons et le numéro atomique Z du strontium.",
        "السؤال un: طبق les lois de conservation، وحدد x، عدد les neutrons، و Z ديال le strontium.",
        phrase("Conservation du nombre de nucléons A : 235 + 1 = 94 + 140 + x, donc x = 2. Conservation du nombre de charge Z : 92 + 0 = Z + 54 + 0, donc Z = 38. Équation : ²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n."),
        ["conservation de A", "conservation de Z", "x", "Z"], ["oublier le neutron incident", "Z = 92 − 54 − 2"],
        [aide("Écris deux égalités : la somme des nombres du haut (A) à gauche = à droite, puis la somme des nombres du bas (Z). N'oublie pas le neutron qui frappe.",
              "كتب les deux égalités: مجموع les nombres اللي الفوق، A، على اليسار، كيساوي اللي على اليمين. ومن بعد les nombres اللي لتحت، Z. ما تنساش le neutron اللي كيضرب."),
         aide("Pour A : 235 + 1 = 94 + 140 + x. Pour Z : 92 + 0 = Z + 54 + x × 0 (un neutron a Z = 0).",
              "بالنسبة ل A: deux cent trente-cinq plus un égale quatre-vingt-quatorze plus cent quarante plus x. بالنسبة ل Z: quatre-vingt-douze plus zéro égale Z plus cinquante-quatre، حيت le neutron عندو Z égale zéro.")],
        corr([("1 : conservation de A : 235 + 1 = 94 + 140 + x ⇒ x = 2", "la conservation ديال A"),
              ("conservation de Z : 92 + 0 = Z + 54 + 2 × 0 ⇒ Z = 38", "la conservation ديال Z"),
              ("²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n", "l'équation كاملة")],
             "السؤال un. la conservation ديال A: deux cent trente-cinq plus un égale quatre-vingt-quatorze plus cent quarante plus x، يعني deux cent trente-six égale deux cent trente-quatre plus x، إذن x égale deux. la conservation ديال Z: quatre-vingt-douze plus zéro égale Z plus cinquante-quatre، إذن Z égale trente-huit. ونكتبو l'équation كاملة، avec deux neutrons."),
        "ex_n4_1", "fa_n4_1"),
      question("2", "Calculer, en u, la variation de masse Δm qui accompagne cette réaction.",
        "السؤال deux: حسب ب u la variation de masse، delta m، ديال هاد la réaction.",
        valeur("Δm", -0.19834, "u", "Δm = [m(Sr) + m(Xe) + 2m_n] − [m(U) + m_n] = 235,80382 − 236,00216 = −0,19834 u"),
        ["Δm = Σm(produits) − Σm(réactifs)", "2m_n", "u"], ["Δm = Σm(réactifs) − Σm(produits)", "oublier les 2 neutrons"],
        [aide("Fais deux sommes : la masse des réactifs (U et le neutron) et la masse des produits (Sr, Xe et les 2 neutrons).",
              "دير les deux sommes: la masse ديال les réactifs، l'uranium و le neutron، و la masse ديال les produits، le strontium، le xénon و les deux neutrons."),
         aide("Δm = Σm(produits) − Σm(réactifs) : les produits d'abord. Pour une réaction qui libère de l'énergie, Δm < 0.",
              "delta m égale la somme des masses des produits، moins la somme des masses des réactifs. les produits هوما اللولين. و delta m كيجي négatif.")],
        corr([("2 : Δm = Σm(produits) − Σm(réactifs)", "delta m égale la somme des masses des produits"),
              ("Σm(réactifs) = 234,9935 + 1,00866 = 236,00216 u", "deux cent trente-six virgule zéro zéro deux cent seize u"),
              ("Σm(produits) = 93,8945 + 139,8920 + 2 × 1,00866 = 235,80382 u", "deux cent trente-cinq virgule quatre-vingt mille trois cent quatre-vingt-deux u"),
              ("Δm = 235,80382 − 236,00216 = −0,19834 u", "moins zéro virgule dix-neuf mille huit cent trente-quatre u")],
             "السؤال deux. delta m égale la somme des masses des produits، moins la somme des masses des réactifs. les réactifs: deux cent trente-six virgule zéro zéro deux cent seize u. les produits، مع les deux neutrons: deux cent trente-cinq virgule quatre-vingt mille trois cent quatre-vingt-deux u. إذن delta m égale moins zéro virgule dix-neuf mille huit cent trente-quatre u. négatif: la masse نقصات."),
        "ex_n4_2", "fa_n4_2"),
      question("3", "Calculer la variation d'énergie ΔE (en MeV), puis en déduire l'énergie libérée E_lib par la fission d'un noyau.",
        "السؤال trois: حسب delta E ب méga électron volt، ومن بعد استنتج l'énergie libérée ب la fission ديال noyau.",
        valeur("E_lib", 184.8, "MeV", "ΔE = Δm·c² = −0,19834 × 931,5 = −184,8 MeV ; E_lib = |ΔE| = 184,8 MeV"),
        ["ΔE = Δm·c²", "E_lib = |ΔE|", "931,5", "MeV"], ["E_lib = −184,8 MeV", "ΔE = Δm × 9·10¹⁶"],
        [aide("Tu as Δm en u : quelle relation donne l'énergie correspondante ? Quel est le signe de ΔE ?",
              "عندك delta m ب u. شنو هي la relation اللي كتعطي l'énergie؟ وشنو هي الإشارة ديال delta E؟"),
         aide("ΔE = Δm × 931,5 (en MeV) ; ΔE < 0, donc l'énergie libérée est E_lib = |ΔE|, un nombre positif.",
              "delta E égale delta m fois neuf cent trente et un virgule cinq. delta E négatif، إذن E libérée égale la valeur absolue de delta E، عدد positif.")],
        corr([("3 : ΔE = Δm·c² = −0,19834 u·c² = −0,19834 × 931,5 MeV", "delta E égale delta m fois c au carré"),
              ("ΔE = −184,8 MeV < 0 : la réaction libère de l'énergie", "delta E égale moins cent quatre-vingt-quatre virgule huit"),
              ("E_lib = |ΔE| = 184,8 MeV (≈ 185 MeV)", "E libérée égale cent quatre-vingt-quatre virgule huit")],
             "السؤال trois. delta E égale delta m fois c au carré، يعني moins zéro virgule dix-neuf mille huit cent trente-quatre fois neuf cent trente et un virgule cinq. delta E égale moins cent quatre-vingt-quatre virgule huit méga électron volt. négatif، إذن la réaction كتعطي l'énergie. E libérée égale cent quatre-vingt-quatre virgule huit méga électron volt، environ cent quatre-vingt-cinq."),
        "ex_n4_3", "fa_n4_3"),
      question("4", "Exprimer E_lib en joule.",
        "السؤال quatre: عبر على E libérée ب joule.",
        valeur("E_lib", 2.96e-11, "J", "E_lib = 184,8 × 1,6·10⁻¹³ = 2,96·10⁻¹¹ J"),
        ["1 MeV = 1,6·10⁻¹³ J", "×", "J"], ["1 MeV = 1,6·10⁻¹⁹ J", "E_lib = 184,8/1,6·10⁻¹³"],
        [aide("Combien de joules dans 1 MeV ? (1 MeV = 10⁶ eV et 1 eV = 1,6·10⁻¹⁹ J.)",
              "شحال من joule، dans un méga électron volt؟ تفكر: un méga électron volt égale dix puissance six électron volts، et un électron volt égale un virgule six fois dix puissance moins dix-neuf joule."),
         aide("E (J) = E (MeV) × 1,6·10⁻¹³.",
              "E ب joule égale E ب méga électron volt، fois un virgule six fois dix puissance moins treize.")],
        corr([("4 : 1 MeV = 1,6·10⁻¹³ J", "un méga électron volt égale un virgule six fois dix puissance moins treize joule"),
              ("E_lib = 184,8 × 1,6·10⁻¹³", "cent quatre-vingt-quatre virgule huit fois un virgule six"),
              ("E_lib = 2,96·10⁻¹¹ J", "deux virgule quatre-vingt-seize fois dix puissance moins onze joule")],
             "السؤال quatre. un méga électron volt égale un virgule six fois dix puissance moins treize joule. إذن E libérée égale cent quatre-vingt-quatre virgule huit fois un virgule six fois dix puissance moins treize، يعني deux virgule quatre-vingt-seize fois dix puissance moins onze joule."),
        "ex_n4_4", "fa_n4_4"),
      question("5", "Les 236 nucléons des réactifs participent à la réaction. Calculer l'énergie libérée par nucléon, puis la comparer à celle de la fusion ²₁H + ³₁H → ⁴₂He + ¹₀n, qui libère 17,6 MeV pour 5 nucléons.",
        "السؤال cinq: deux cent trente-six nucléons كيشاركو فla réaction. حسب l'énergie libérée par nucléon، وقارنها مع la fusion ديال le deutérium و le tritium، qui donne dix-sept virgule six méga électron volt pour cinq nucléons.",
        valeur("E_lib/nucléon", 0.78, "MeV/nucléon", "E_lib/236 = 184,8/236 = 0,78 MeV/nucléon"),
        ["E_lib/A", "236", "MeV/nucléon", "17,6/5"], ["184,8/235", "comparer 184,8 et 17,6"],
        [aide("Pour comparer deux réactions, ramène chaque énergie libérée à un seul nucléon.",
              "باش تقارن les deux réactions، قسم كل énergie libérée على عدد les nucléons ديالها."),
         aide("Fission : 184,8/236 ; fusion : 17,6/5. Puis compare les deux nombres.",
              "la fission: cent quatre-vingt-quatre virgule huit sur deux cent trente-six. la fusion: dix-sept virgule six sur cinq. ومن بعد قارن.")],
        corr([("5 : fission : E_lib/236 = 184,8/236 = 0,78 MeV/nucléon", "zéro virgule soixante-dix-huit méga électron volt par nucléon"),
              ("fusion : 17,6/5 = 3,5 MeV/nucléon", "trois virgule cinq"),
              ("3,5 > 0,78 : à masse égale, la fusion libère environ 4,5 fois plus d'énergie que la fission.", "à masse égale، la fusion كتعطي كثر")],
             "السؤال cinq. la fission: cent quatre-vingt-quatre virgule huit sur deux cent trente-six، يعني zéro virgule soixante-dix-huit méga électron volt par nucléon. la fusion: dix-sept virgule six sur cinq، يعني trois virgule cinq. trois virgule cinq plus grand que zéro virgule soixante-dix-huit: à masse égale، la fusion كتعطي كثر، environ quatre virgule cinq fois."),
        "ex_n4_5", "fa_n4_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n4_1", "Question 1 : les lois de Soddy", "A : 235 + 1 = 94 + 140 + x ⇒ x = 2 ; Z : 92 = Z + 54 ⇒ Z = 38",
      SIMD + "figures.html?fig=fig_soddy", "L'équation de la fission et la conservation de A et de Z",
      "شوف l'équation: l'uranium plus le neutron، كيعطيو le strontium، le xénon، و x neutrons. la conservation ديال A، les nombres اللي الفوق: deux cent trente-cinq plus un، يعني deux cent trente-six. على اليمين: quatre-vingt-quatorze plus cent quarante plus x. إذن x égale deux. la conservation ديال Z، les nombres اللي لتحت: quatre-vingt-douze égale Z plus cinquante-quatre. إذن Z ديال le strontium égale trente-huit. عمرك ما تنسى le neutron اللي كيضرب، على اليسار.",
      centre=[("235 + 1 = 94 + 140 + x ⇒ x = 2", "إذن x égale deux"),
              ("92 + 0 = Z + 54 ⇒ Z = 38", "égale trente-huit")],
      pointage=[{"mot": "شوف l'équation", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "la conservation ديال A", "commande": "play_until", "parametres": {"moment": "A"}},
                {"mot": "la conservation ديال Z", "commande": "play_until", "parametres": {"moment": "Z"}}]),
    diapo_sim("ex_n4_2", "Question 2 : Δm de la réaction", "Δm = 235,80382 − 236,00216 = −0,19834 u",
      BAL, "La balance : les réactifs à gauche, les produits à droite",
      "شوف الميزان. على اليسار les réactifs: l'uranium و le neutron اللي كيضرب، deux cent trente-six virgule zéro zéro deux cent seize u. على اليمين les produits: le strontium، le xénon، et deux neutrons. ما تنسى حتى neutron: deux cent trente-cinq virgule quatre-vingt mille trois cent quatre-vingt-deux u. الميزان كيهبط من جيهة les réactifs: les produits خفاف. delta m égale la somme des produits moins la somme des réactifs: moins zéro virgule dix-neuf mille huit cent trente-quatre u.",
      centre=[("Δm = Σm(produits) − Σm(réactifs)", "delta m égale la somme des produits"),
              ("Δm = 235,80382 − 236,00216 = −0,19834 u", "moins zéro virgule dix-neuf mille")],
      pointage=[{"mot": "على اليسار les réactifs", "commande": "play_until", "parametres": {"moment": "reactifs_poses"}},
                {"mot": "على اليمين les produits", "commande": "play_until", "parametres": {"moment": "produits_poses"}},
                {"mot": "الميزان كيهبط", "commande": "play_until", "parametres": {"moment": "balance_penche"}},
                {"mot": "delta m égale la somme", "commande": "play_until", "parametres": {"moment": "delta_m"}}]),
    diapo_sim("ex_n4_3", "Question 3 : ΔE puis E_lib", "ΔE = −0,19834 × 931,5 = −184,8 MeV ; E_lib = |ΔE| ≈ 185 MeV",
      BAL, "La colonne des masses : ΔE = Δm·c², puis E_lib = |ΔE|",
      "شوف la colonne. delta m égale moins zéro virgule dix-neuf mille huit cent trente-quatre u. delta E égale delta m fois c au carré: fois neuf cent trente et un virgule cinq، يعني moins cent quatre-vingt-quatre virgule huit méga électron volt. delta E négatif: le système كيعطي l'énergie للخارج. E libérée égale la valeur absolue: cent quatre-vingt-quatre virgule huit، environ cent quatre-vingt-cinq méga électron volt. عدد positif ديما.",
      centre=[("ΔE = Δm·c² = −0,19834 × 931,5 = −184,8 MeV", "delta E égale delta m fois c au carré"),
              ("E_lib = |ΔE| ≈ 185 MeV", "E libérée égale la valeur absolue")],
      pointage=[{"mot": "شوف la colonne", "commande": "play_until", "parametres": {"moment": "delta_m"}},
                {"mot": "delta E égale delta m", "commande": "play_until", "parametres": {"moment": "energie"}},
                {"mot": "E libérée égale la valeur absolue", "repere": "energie"}]),
    diapo_sim("ex_n4_4", "Question 4 : de MeV à joule", "1 MeV = 1,6·10⁻¹³ J : E_lib = 184,8 × 1,6·10⁻¹³ = 2,96·10⁻¹¹ J",
      SIMD + "figures.html?fig=fig_unites", "L'escalier des unités : eV, puis MeV",
      "شوف l'escalier ديال les unités. l'électron volt: un électron volt égale un virgule six fois dix puissance moins dix-neuf joule. le méga électron volt: un million d'électron volts، يعني un virgule six fois dix puissance moins treize joule. رد البال: moins treize، ماشي moins dix-neuf. إذن E libérée égale cent quatre-vingt-quatre virgule huit fois un virgule six fois dix puissance moins treize، يعني deux virgule quatre-vingt-seize fois dix puissance moins onze joule.",
      centre=[("1 MeV = 10⁶ eV = 1,6·10⁻¹³ J", "le méga électron volt: un million"),
              ("E_lib = 184,8 × 1,6·10⁻¹³ = 2,96·10⁻¹¹ J", "deux virgule quatre-vingt-seize fois dix puissance moins onze joule")],
      pointage=[{"mot": "شوف l'escalier", "commande": "play_until", "parametres": {"moment": "u"}},
                {"mot": "l'électron volt: un", "commande": "play_until", "parametres": {"moment": "eV"}},
                {"mot": "le méga électron volt: un million", "commande": "play_until", "parametres": {"moment": "MeV"}}]),
    diapo_sim("ex_n4_5", "Question 5 : par nucléon, fission contre fusion", "Fission : 185/236 ≈ 0,78 MeV/nucléon ; fusion : 17,6/5 ≈ 3,5 MeV/nucléon",
      SIMD + "comparaison.html", "Fission ou fusion : par réaction, puis par nucléon",
      "شوف: la fission على اليسار، و la fusion على اليمين. ل réaction وحدة، la fission، cent quatre-vingt-cinq méga électron volt، و la fusion dix-sept virgule six. ولكن la fission، c'est deux cent trente-six nucléons، و la fusion، seulement cinq. par nucléon: la fission، zéro virgule soixante-dix-huit. la fusion، trois virgule cinq. إذن à masse égale، la fusion كتعطي كثر من la fission.",
      centre=[("fission : 184,8/236 = 0,78 MeV/nucléon", "la fission، zéro virgule soixante-dix-huit"),
              ("fusion : 17,6/5 = 3,5 MeV/nucléon", "la fusion، trois virgule cinq")],
      pointage=[{"mot": "شوف: la fission", "commande": "play_until", "parametres": {"moment": "trace"}},
                {"mot": "ل réaction وحدة", "commande": "play_until", "parametres": {"moment": "par_reaction"}},
                {"mot": "par nucléon:", "commande": "play_until", "parametres": {"moment": "par_nucleon"}},
                {"mot": "إذن à masse égale", "commande": "play_until", "parametres": {"moment": "conclusion"}}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n4_1", "Plus facile : trouver x", "نتمرنو: شحال من neutron؟",
      "²³⁵₉₂U + ¹₀n → ¹³⁹₅₄Xe + ⁹⁵₃₈Sr + x ¹₀n. Que vaut x ?",
      ["1", "2", "3"], 1, {
        "1": {"juste": rep("برافو! deux cent trente-six égale deux cent trente-quatre plus x، إذن x égale deux.", "Juste : 236 = 139 + 95 + x, donc x = 2.")},
        "0": {"1": rep("ما تقلقش. حسب A على اليسار: واش نسيتي le neutron اللي كيضرب؟ عاود اختار.", "As-tu compté le neutron incident à gauche ? Réessaie."),
              "2": rep("الجواب هو x égale deux. deux cent trente-cinq plus un égale cent trente-neuf plus quatre-vingt-quinze plus x.", "Réponse : x = 2 (235 + 1 = 139 + 95 + x).")},
        "2": {"1": rep("قريب. جمع مزيان: cent trente-neuf plus quatre-vingt-quinze، وقارن avec deux cent trente-six. عاود اختار.", "Additionne 139 + 95 et compare à 236. Réessaie."),
              "2": rep("الجواب هو x égale deux: deux cent trente-six moins deux cent trente-quatre.", "Réponse : x = 236 − 234 = 2.")}},
      "Uranium deux cent trente-cinq plus un neutron donne xénon cent trente-neuf plus strontium quatre-vingt-quinze plus x neutrons. Que vaut x ?"),
    qcm_facile("fa_n4_2", "Plus facile : l'ordre dans Δm", "سؤال ساهل: delta m ديال réaction.",
      "Pour une réaction nucléaire, on écrit :",
      ["Δm = Σm(réactifs) − Σm(produits)", "Δm = Σm(produits) − Σm(réactifs)", "Δm = Σm(produits) + Σm(réactifs)"], 1, {
        "1": {"juste": rep("برافو! داكشي اللي فالأخير، ناقص داكشي اللي كان فالأول. و delta m كيجي négatif.", "Juste : produits moins réactifs ; Δm < 0.")},
        "0": {"1": rep("ما تقلقش. فla réaction، الفرق كيتحسب: la fin moins le début. شكون اللي فالأخير؟ عاود اختار.", "Une variation, c'est fin moins début. Réessaie."),
              "2": rep("الجواب: delta m égale la somme des produits moins la somme des réactifs.", "Réponse : Δm = Σm(produits) − Σm(réactifs).")},
        "2": {"1": rep("لا، variation معناها فرق، ماشي مجموع. عاود اختار.", "Une variation est une différence, pas une somme. Réessaie."),
              "2": rep("الجواب: delta m égale la somme des produits moins la somme des réactifs.", "Réponse : Δm = Σm(produits) − Σm(réactifs).")}},
      "Pour une réaction nucléaire, on écrit delta m comment ?"),
    vrai_faux_facile("fa_n4_3", "Plus facile : vrai ou faux", "سؤال ساهل على delta E و E libérée.",
      "Fission : ΔE = −184,8 MeV.",
      [("L'énergie libérée est E_lib = −184,8 MeV.", False, "E_lib = |ΔE| est toujours positive : 184,8 MeV."),
       ("ΔE < 0 signifie que le système cède de l'énergie au milieu extérieur.", True, "La masse diminue, l'énergie correspondante est libérée."),
       ("ΔE s'obtient par Δm (en u) × 931,5 en MeV.", True, "1 u·c² = 931,5 MeV.")]),
    qcm_facile("fa_n4_4", "Plus facile : MeV et joule", "سؤال ساهل على les unités.",
      "1 MeV vaut :",
      ["1,6·10⁻¹⁹ J", "1,6·10⁻¹³ J", "931,5 J"], 1, {
        "1": {"juste": rep("برافو! un méga électron volt égale un virgule six fois dix puissance moins treize joule.", "Juste : 1 MeV = 1,6·10⁻¹³ J.")},
        "0": {"1": rep("قريب. هادي هي la valeur de un électron volt. et méga، معناها un million. عاود اختار.", "C'est 1 eV. Et méga = 10⁶. Réessaie."),
              "2": rep("الجواب: un méga électron volt égale un virgule six fois dix puissance moins treize joule. moins dix-neuf plus six égale moins treize.", "Réponse : 1,6·10⁻¹³ J (10⁻¹⁹ × 10⁶).")},
        "2": {"1": rep("لا، neuf cent trente et un virgule cinq هي la valeur de un u fois c au carré، ب méga électron volt. عاود اختار.", "931,5 concerne 1 u·c² en MeV. Réessaie."),
              "2": rep("الجواب: un méga électron volt égale un virgule six fois dix puissance moins treize joule.", "Réponse : 1 MeV = 1,6·10⁻¹³ J.")}},
      "Un méga électron volt vaut combien de joules ?"),
    qcm_facile("fa_n4_5", "Plus facile : fission ou fusion ?", "سؤال ساهل: شكون كتعطي كثر par nucléon؟",
      "Par nucléon, quelle réaction libère le plus d'énergie ?",
      ["la fission de l'uranium 235", "la fusion ²H + ³H", "les deux libèrent autant"], 1, {
        "1": {"juste": rep("برافو! la fusion: trois virgule cinq par nucléon، و la fission: zéro virgule soixante-dix-huit.", "Juste : 3,5 MeV/nucléon contre 0,78.")},
        "0": {"1": rep("فخ! la fission كتعطي كثر ل réaction وحدة، ولكن فيها بزاف ديال les nucléons. قسم على A. عاود اختار.", "Par réaction oui, mais elle met en jeu 236 nucléons. Divise. Réessaie."),
              "2": rep("الجواب: la fusion. trois virgule cinq par nucléon، plus grand que zéro virgule soixante-dix-huit.", "Réponse : la fusion (3,5 > 0,78 MeV/nucléon).")},
        "2": {"1": rep("لا. حسب: cent quatre-vingt-cinq sur deux cent trente-six، et dix-sept virgule six sur cinq. عاود اختار.", "Calcule 185/236 et 17,6/5. Réessaie."),
              "2": rep("الجواب: la fusion، trois virgule cinq contre zéro virgule soixante-dix-huit.", "Réponse : la fusion, 3,5 contre 0,78 MeV/nucléon.")}},
      "Par nucléon, quelle réaction libère le plus d'énergie ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, une autre fission : baryum et krypton",
    "enonce": {
      "intro": "Une autre fission possible de l'uranium 235 :\n²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²Kr + x ¹₀n\nLe nombre de charge Z du krypton ⁹²Kr est à déterminer.",
      "intro_dit": "fission أخرى: l'uranium deux cent trente-cinq plus un neutron، كيعطيو le baryum cent quarante et un، plus le krypton quatre-vingt-douze، plus x neutrons.",
      "figures": [fission("Figure : une autre fission de l'uranium 235", "⁹²Kr", "¹⁴¹Ba", 3)],
      "donnees": ["m(²³⁵₉₂U) = 234,9935 u ; m(¹⁴¹₅₆Ba) = 140,88367 u ; m(⁹²Kr) = 91,90639 u", "m(¹₀n) = 1,00866 u",
                  "1 u = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J"],
      "questions": [
        question_semblable("1", "Déterminer x et Z en appliquant les lois de conservation.",
          phrase("A : 235 + 1 = 141 + 92 + x, donc x = 3 ; Z : 92 + 0 = 56 + Z, donc Z = 36 : ²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + ⁹²₃₆Kr + 3 ¹₀n."),
          ["conservation de A", "conservation de Z"], ["oublier le neutron incident"],
          corr([("1 : A : 236 = 233 + x ⇒ x = 3 ; Z : 92 = 56 + Z ⇒ Z = 36", "x égale trois")],
               "la conservation ديال A كتعطي x égale trois، و la conservation ديال Z كتعطي Z égale trente-six.")),
        question_semblable("2", "Calculer, en u, la variation de masse Δm de cette réaction.",
          valeur("Δm", -0.18612, "u", "Δm = (140,88367 + 91,90639 + 3 × 1,00866) − (234,9935 + 1,00866) = 235,81604 − 236,00216 = −0,18612 u"),
          ["Δm = Σm(produits) − Σm(réactifs)", "3m_n"], ["oublier les 3 neutrons"],
          corr([("2 : Δm = 235,81604 − 236,00216 = −0,18612 u", "moins zéro virgule dix-huit mille six cent douze u")],
               "les produits: deux cent trente-cinq virgule quatre-vingt-un mille six cent quatre u. les réactifs: deux cent trente-six virgule zéro zéro deux cent seize u. delta m égale moins zéro virgule dix-huit mille six cent douze u.")),
        question_semblable("3", "Calculer ΔE (en MeV), puis en déduire l'énergie libérée E_lib.",
          valeur("E_lib", 173.4, "MeV", "ΔE = −0,18612 × 931,5 = −173,4 MeV ; E_lib = |ΔE| = 173,4 MeV"), ["E_lib = |ΔE|", "MeV"], ["E_lib = −173,4 MeV"],
          corr([("3 : ΔE = −0,18612 × 931,5 = −173,4 MeV ; E_lib = |ΔE| = 173,4 MeV", "cent soixante-treize virgule quatre")],
               "delta E égale moins cent soixante-treize virgule quatre méga électron volt، و E libérée égale cent soixante-treize virgule quatre méga électron volt.")),
        question_semblable("4", "Exprimer E_lib en joule.",
          valeur("E_lib", 2.77e-11, "J", "E_lib = 173,4 × 1,6·10⁻¹³ = 2,77·10⁻¹¹ J"), ["1 MeV = 1,6·10⁻¹³ J"], ["1 MeV = 1,6·10⁻¹⁹ J"],
          corr([("4 : E_lib = 173,4 × 1,6·10⁻¹³ = 2,77·10⁻¹¹ J", "deux virgule soixante-dix-sept fois dix puissance moins onze joule")],
               "E libérée égale cent soixante-treize virgule quatre fois un virgule six fois dix puissance moins treize، يعني deux virgule soixante-dix-sept fois dix puissance moins onze joule.")),
        question_semblable("5", "Calculer l'énergie libérée par nucléon (236 nucléons) et la comparer à celle de la fusion ²H + ³H (17,6 MeV pour 5 nucléons).",
          valeur("E_lib/nucléon", 0.73, "MeV/nucléon", "E_lib/236 = 173,4/236 = 0,73 MeV/nucléon"), ["E_lib/A", "236"], ["173,4/235"],
          corr([("5 : 173,4/236 = 0,73 MeV/nucléon < 17,6/5 = 3,5 MeV/nucléon : la fusion libère plus par nucléon.", "zéro virgule soixante-treize")],
               "cent soixante-treize virgule quatre sur deux cent trente-six، يعني zéro virgule soixante-treize méga électron volt par nucléon. la fusion، trois virgule cinq: كثر.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
