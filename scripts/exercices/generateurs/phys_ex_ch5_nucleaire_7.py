# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau difficile n° 7 : la désintégration α du radium 226 lue
# sur un diagramme énergétique en valeurs absolues (sans flèche donnée) — équation, E_ℓ(Ra) et Δm en kg, E_lib,
# E_ℓ(Rn) déduite du diagramme, stabilité comparée et lecture critique (pourquoi Ra se désintègre).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration energie_nucleaire.json : cas_types « diagramme énergétique » (nommer les niveaux ; flèche = arrivée −
#    départ), « défaut de masse en kg » (Δm = E_ℓ/931,5 puis × 1,66·10⁻²⁷, Bazhar), « comparer la stabilité » ; pièges
#    « E_lib négative », « Δm en u multiplié par 9·10¹⁶ », « stabilité comparée avec E_ℓ » ; conseil « E_lib d'une
#    désintégration : quelques MeV ».
#  - nationaux : 2020 N (diagramme du polonium 210 en 10⁵ MeV : E_lib et Δm en kg), 2019 N (radon 222 : stabilité par
#    E_ℓ/A), 2024 R (E_lib d'une désintégration α) : ici un autre noyau (radium 226), un diagramme sans flèches, et deux
#    étapes de plus (E_ℓ du noyau fils déduite du diagramme, lecture critique de la stabilité) : au-dessus du national.
#  - séries en ligne (désintégration α du radium, diagramme d'énergie) : extraits de recherche lus ; pages non
#    joignables depuis cette session.
#  - cours : diagramme.html?vue=polonium (1,971820·10⁵ ; 1,955372·10⁵ ; 1,955318·10⁵ MeV ; −5,4 MeV),
#    reactions.html?vue=spontanee (²¹⁰Po → ²⁰⁶Pb + α), figures.html?fig=fig_defaut (Δm en kg), fig_stabilite
#    (8,78 > 8,64) : l'explication dit les valeurs de la simulation, puis applique la méthode à nos données.
#  Données : masses des noyaux (masses atomiques tabulées moins Z × 0,00055 u), mêmes m_p, m_n, 931,5 que le cours ;
#  niveaux du diagramme = masses × 931,5, arrondis au 0,1 MeV près (7 chiffres significatifs, comme au national 2020 N).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_7"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
MP, MN, U, KG = 1.00728, 1.00866, 931.5, 1.66e-27


def niveaux_abs(titre, haut, milieu, bas, vh, vm, vb):
    """Diagramme en valeurs absolues (10⁵ MeV) : trois paliers, valeurs à gauche, noms à droite ; aucune flèche."""
    els = [{"f": "fleche", "de": [2.2, 0.3], "a": [2.2, 4.1], "couleur": "blanc"},
           {"f": "texte", "at": [2.45, 4.0], "t": "E (MeV)", "ancre": "gauche"}]
    for y, nom, v, c in ((3.5, haut, vh, "cyan"), (1.6, milieu, vm, "jaune"), (0.9, bas, vb, "vert")):
        els.append({"f": "ligne", "pts": [[2.2, y], [6.2, y]], "couleur": c, "epais": True})
        els.append({"f": "texte", "at": [2.05, y - 0.1], "t": v, "couleur": c, "ancre": "droite", "taille": "petit"})
        els.append({"f": "texte", "at": [6.35, y - 0.1], "t": nom, "couleur": c, "ancre": "gauche"})
    els.append({"f": "texte", "at": [9.3, 0.3], "t": "échelle non respectée", "couleur": "faible", "ancre": "droite", "taille": "petit"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 9.4, "h": 4.3}, "elements": els,
            "legende": "Chaque palier : énergie du système au repos (nucléons séparés, noyau père, produits)."}


# ---------------------------------------------------------------- calculs (énoncé : radium 226)
def niveaux(Z, A, m, m_fils):
    r = lambda x: round(x / 1e5, 6) * 1e5
    return r((Z * MP + (A - Z) * MN) * U), r(m * U), r((m_fils + 4.00150) * U)
EN, EP, EF = niveaux(88, 226, 225.97710, 221.97036)
assert (round(EN / 1e5, 6), round(EP / 1e5, 6), round(EF / 1e5, 6)) == (2.12229, 2.104977, 2.104928)
EL_RA = EN - EP                          # 1731,3 MeV
DM_KG = EL_RA / U * KG                   # 3,09·10⁻²⁷ kg
DE = EF - EP                             # −4,9 MeV
EL_RN = EN - EF - 28.30                  # 1707,9 MeV
assert round(EL_RA, 1) == 1731.3 and abs(DM_KG - 3.0853e-27) < 1e-30 and round(DE, 1) == -4.9 and round(EL_RN, 1) == 1707.9
assert round(EL_RA / 226, 2) == 7.66 and round(EL_RN / 222, 2) == 7.69
# cohérence avec les masses : Q = 4,88 MeV
assert round((221.97036 + 4.00150 - 225.97710) * U, 2) == -4.88
# semblable : thorium 230 → radium 226 + α
EN2, EP2, EF2 = niveaux(90, 230, 229.98372, 225.97710)
assert (round(EN2 / 1e5, 6), round(EP2 / 1e5, 6), round(EF2 / 1e5, 6)) == (2.159847, 2.142298, 2.142251)
EL_TH = EN2 - EP2                        # 1754,9
DM_KG2 = EL_TH / U * KG                  # 3,13·10⁻²⁷
DE2 = EF2 - EP2                          # −4,7
EL_RA2 = EN2 - EF2 - 28.30               # 1731,3
assert round(EL_TH, 1) == 1754.9 and abs(DM_KG2 - 3.1274e-27) < 1e-30 and round(DE2, 1) == -4.7 and round(EL_RA2, 1) == 1731.3
assert round(EL_TH / 230, 2) == 7.63

DIAG = SIMD + "diagramme.html?vue=polonium"

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "Le radium 226 : un diagramme énergétique à exploiter", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire l'équation d'une désintégration α", "Lire une énergie de liaison sur un diagramme et la convertir en défaut de masse (kg)",
                  "Calculer E_lib à partir d'un diagramme", "Déduire l'énergie de liaison d'un produit", "Comparer la stabilité et critiquer un résultat"],
  "enonce": {
    "intro": "Le radium ²²⁶₈₈Ra, découvert par Marie et Pierre Curie, est radioactif α : il donne un isotope du radon Rn. La figure représente le diagramme énergétique de cette désintégration (énergies des systèmes au repos, échelle non respectée).",
    "intro_dit": "دابا نقراو l'énoncé. le radium deux cent vingt-six radioactif alpha: كيعطي l'isotope ديال le radon. la figure هي le diagramme énergétique ديال هاد la désintégration، و l'échelle ماشي محترمة.",
    "figures": [niveaux_abs("Figure : diagramme énergétique (radium 226)",
                            "88 ¹₁p + 138 ¹₀n", "²²⁶₈₈Ra", "Rn + ⁴₂He", "2,122290·10⁵", "2,104977·10⁵", "2,104928·10⁵")],
    "donnees": ["E_ℓ(⁴₂He) = 28,30 MeV", "1 u = 931,5 MeV/c² = 1,66·10⁻²⁷ kg", "Extrait du tableau périodique : ₈₄Po, ₈₅At, ₈₆Rn, ₈₇Fr, ₈₈Ra"],
    "questions": [
      question("1", "Écrire l'équation de la désintégration du radium 226, en précisant les lois utilisées.",
        "السؤال un: كتب l'équation ديال la désintégration ديال le radium deux cent vingt-six، وذكر les lois اللي استعملتي.",
        phrase("²²⁶₈₈Ra → ᴬ_ZRn + ⁴₂He ; conservation du nombre de nucléons : 226 = A + 4, donc A = 222 ; conservation du nombre de charge : 88 = Z + 2, donc Z = 86 : ²²⁶₈₈Ra → ²²²₈₆Rn + ⁴₂He (lois de Soddy)."),
        ["⁴₂He", "conservation de A", "conservation de Z", "²²²₈₆Rn"], ["⁰₋₁e", "Z = 90"],
        [aide("Une particule α est un noyau d'hélium ⁴₂He. Écris l'équation avec un noyau ᴬ_ZRn inconnu.",
              "la particule alpha هي noyau d'hélium quatre. كتب l'équation مع le radon، A و Z ما عارفينهمش."),
         aide("Conservation de A : 226 = A + 4 ; conservation de Z : 88 = Z + 2.",
              "la conservation ديال A: deux cent vingt-six égale A plus quatre. la conservation ديال Z: quatre-vingt-huit égale Z plus deux.")],
        corr([("1 : ²²⁶₈₈Ra → ᴬ_ZRn + ⁴₂He", "le radium كيعطي le radon et l'hélium"),
              ("A : 226 = A + 4 ⇒ A = 222 ; Z : 88 = Z + 2 ⇒ Z = 86", "A égale deux cent vingt-deux"),
              ("²²⁶₈₈Ra → ²²²₈₆Rn + ⁴₂He", "l'équation كاملة")],
             "السؤال un. le radium كيعطي le radon et l'hélium quatre. la conservation ديال A: deux cent vingt-six égale A plus quatre، إذن A égale deux cent vingt-deux. la conservation ديال Z: quatre-vingt-huit égale Z plus deux، إذن Z égale quatre-vingt-six. ونكتبو l'équation كاملة."),
        "ex_n7_1", "fa_n7_1"),
      question("2", "À l'aide du diagramme, déterminer l'énergie de liaison E_ℓ du noyau ²²⁶₈₈Ra, puis en déduire son défaut de masse Δm en kilogramme.",
        "السؤال deux: بالاستعانة ب le diagramme، حدد l'énergie de liaison ديال le radium، ومن بعد استنتج le défaut de masse ديالو ب kilogramme.",
        valeur("Δm", 3.09e-27, "kg", "E_ℓ = 2,122290·10⁵ − 2,104977·10⁵ = 1731,3 MeV ; Δm = E_ℓ/c² = 1731,3/931,5 u = 1,8586 u = 1,8586 × 1,66·10⁻²⁷ = 3,09·10⁻²⁷ kg"),
        ["E_ℓ = E(nucléons) − E(noyau)", "Δm = E_ℓ/c²", "÷ 931,5", "× 1,66·10⁻²⁷"], ["Δm = 1731,3 × 1,66·10⁻²⁷", "Δm = 1731,3/9·10¹⁶"],
        [aide("L'énergie de liaison est l'énergie qu'il faut fournir pour passer du noyau au repos aux nucléons séparés au repos : quels paliers ?",
              "l'énergie de liaison هي l'énergie اللي خاصنا نعطيو باش نمشيو من النواة واقفة ل les nucléons بعاد. أشمن paliers؟"),
         aide("E_ℓ = E(haut) − E(radium). Puis Δm = E_ℓ/931,5 en u, et × 1,66·10⁻²⁷ pour les kg.",
              "E l égale E الفوق moins E ديال le radium. ومن بعد delta m égale E l sur neuf cent trente et un virgule cinq، ب u، ومن بعد fois un virgule soixante-six fois dix puissance moins vingt-sept.")],
        corr([("2 : E_ℓ(Ra) = E(88 p + 138 n) − E(Ra) = 2,122290·10⁵ − 2,104977·10⁵ = 1731,3 MeV", "E l égale mille sept cent trente et un virgule trois"),
              ("Δm = E_ℓ/c² = 1731,3 MeV/c² = 1731,3/931,5 u = 1,8586 u", "un virgule huit mille cinq cent quatre-vingt-six u"),
              ("Δm = 1,8586 × 1,66·10⁻²⁷ = 3,09·10⁻²⁷ kg", "trois virgule zéro neuf fois dix puissance moins vingt-sept kilogramme")],
             "السؤال deux. E l du radium égale l'énergie des nucléons séparés moins l'énergie du noyau: deux virgule un deux deux deux neuf zéro fois dix puissance cinq، moins deux virgule un zéro quatre neuf sept sept fois dix puissance cinq. E l égale mille sept cent trente et un virgule trois méga électron volt. delta m égale E l sur c au carré، يعني mille sept cent trente et un virgule trois sur neuf cent trente et un virgule cinq: un virgule huit mille cinq cent quatre-vingt-six u. fois un virgule soixante-six fois dix puissance moins vingt-sept: delta m égale trois virgule zéro neuf fois dix puissance moins vingt-sept kilogramme."),
        "ex_n7_2", "fa_n7_2"),
      question("3", "Déterminer la variation d'énergie ΔE de la désintégration et l'énergie libérée E_lib.",
        "السؤال trois: حدد delta E ديال la désintégration، و l'énergie libérée.",
        valeur("E_lib", 4.9, "MeV", "ΔE = E_f − E_i = 2,104928·10⁵ − 2,104977·10⁵ = −4,9 MeV ; E_lib = |ΔE| = 4,9 MeV"),
        ["ΔE = E_f − E_i", "E_lib = |ΔE|", "MeV"], ["ΔE = E_i − E_f", "E_lib = −4,9 MeV"],
        [aide("L'état initial est le radium au repos ; l'état final, les produits au repos. Lis ces deux paliers.",
              "la حالة اللولة هي le radium واقف، والحالة الأخيرة هي les produits واقفين. قرا هاد les deux paliers."),
         aide("ΔE = E_f − E_i (arrivée − départ) ; ΔE < 0, donc E_lib = |ΔE|. Attention aux puissances de dix : soustrais les nombres complets.",
              "delta E égale E f moins E i، l'arrivée moins le départ. delta E négatif، إذن E libérée égale la valeur absolue. رد البال ل les puissances de dix.")],
        corr([("3 : ΔE = E_f − E_i = E(Rn + He) − E(Ra)", "delta E égale E f moins E i"),
              ("ΔE = 2,104928·10⁵ − 2,104977·10⁵ = −4,9 MeV", "delta E égale moins quatre virgule neuf"),
              ("ΔE < 0 : E_lib = |ΔE| = 4,9 MeV", "E libérée égale quatre virgule neuf méga électron volt")],
             "السؤال trois. delta E égale E f moins E i، يعني l'énergie des produits moins l'énergie du radium: deux virgule un zéro quatre neuf deux huit fois dix puissance cinq، moins deux virgule un zéro quatre neuf sept sept fois dix puissance cinq. delta E égale moins quatre virgule neuf méga électron volt. négatif، إذن E libérée égale quatre virgule neuf méga électron volt."),
        "ex_n7_3", "fa_n7_3"),
      question("4", "En exploitant le diagramme et la donnée E_ℓ(⁴₂He), déterminer l'énergie de liaison du noyau de radon produit.",
        "السؤال quatre: بالاستعانة ب le diagramme و E l ديال l'hélium، حدد l'énergie de liaison ديال le radon.",
        valeur("E_ℓ(Rn)", 1707.9, "MeV", "E_ℓ(Rn) + E_ℓ(He) = 2,122290·10⁵ − 2,104928·10⁵ = 1736,2 MeV ; E_ℓ(Rn) = 1736,2 − 28,30 = 1707,9 MeV"),
        ["E(nucléons) − E(produits) = E_ℓ(Rn) + E_ℓ(He)", "28,30"], ["E_ℓ(Rn) = 1736,2 MeV", "E_ℓ(Rn) = 1731,3 − 28,30"],
        [aide("Du palier des produits (Rn + He) au palier des nucléons séparés, il faut casser deux noyaux. Quelle énergie faut-il fournir ?",
              "من palier ديال les produits ل palier ديال les nucléons بعاد، خاصنا نهرسو les deux noyaux: le radon و l'hélium. شحال خاصنا نعطيو؟"),
         aide("E(haut) − E(Rn + He) = E_ℓ(Rn) + E_ℓ(He) ; retranche ensuite E_ℓ(He) = 28,30 MeV.",
              "E الفوق moins E ديال les produits égale E l du radon plus E l de l'hélium. ومن بعد نقص، moins vingt-huit virgule trente.")],
        corr([("4 : E(nucléons) − E(Rn + He) = E_ℓ(Rn) + E_ℓ(⁴He)", "E l du radon plus E l de l'hélium"),
              ("E_ℓ(Rn) + E_ℓ(He) = 2,122290·10⁵ − 2,104928·10⁵ = 1736,2 MeV", "mille sept cent trente-six virgule deux"),
              ("E_ℓ(Rn) = 1736,2 − 28,30 = 1707,9 MeV", "E l du radon égale mille sept cent sept virgule neuf")],
             "السؤال quatre. من les produits ل les nucléons بعاد، كنهرسو les deux noyaux: l'énergie هي E l du radon plus E l de l'hélium. deux virgule un deux deux deux neuf zéro fois dix puissance cinq، moins deux virgule un zéro quatre neuf deux huit fois dix puissance cinq، يعني mille sept cent trente-six virgule deux. كنقصو، moins vingt-huit virgule trente: E l du radon égale mille sept cent sept virgule neuf méga électron volt."),
        "ex_n7_4", "fa_n7_4"),
      question("5", "Comparer la stabilité des noyaux ²²⁶Ra et ²²²Rn. Ce résultat est-il cohérent avec le fait que le radium se désintègre spontanément ? Justifier.",
        "السؤال cinq: قارن la stabilité ديال le radium و le radon. واش هاد النتيجة متفقة مع كون le radium كيتفكك بوحدو؟ علل.",
        phrase("E_ℓ/A(Ra) = 1731,3/226 = 7,66 MeV/nucléon ; E_ℓ/A(Rn) = 1707,9/222 = 7,69 MeV/nucléon. 7,69 > 7,66 : le radon est plus stable que le radium (alors que E_ℓ(Ra) > E_ℓ(Rn) : on compare E_ℓ/A, pas E_ℓ). C'est cohérent : un noyau se désintègre spontanément pour donner un noyau plus stable, et ΔE < 0 (4,9 MeV libérés)."),
        ["E_ℓ/A", "7,66", "7,69", "plus stable"], ["comparer E_ℓ", "E_ℓ(Ra) > E_ℓ(Rn) donc Ra plus stable"],
        [aide("Calcule l'énergie de liaison par nucléon de chaque noyau : A = 226 et A = 222.",
              "حسب E l sur A ديال كل نواة: A égale deux cent vingt-six، و A égale deux cent vingt-deux."),
         aide("Le plus stable a la plus grande E_ℓ/A. Une désintégration spontanée va-t-elle vers un noyau plus ou moins stable ?",
              "le plus stable عندو E l sur A الكبيرة. la désintégration spontanée كتمشي نحو noyau plus stable ولا moins stable؟")],
        corr([("5 : E_ℓ/A(Ra) = 1731,3/226 = 7,66 MeV/nucléon ; E_ℓ/A(Rn) = 1707,9/222 = 7,69 MeV/nucléon", "sept virgule soixante-six"),
              ("7,69 > 7,66 : ²²²Rn est plus stable que ²²⁶Ra (on compare E_ℓ/A, pas E_ℓ)", "le radon plus stable"),
              ("Cohérent : la désintégration spontanée donne un noyau plus stable et libère de l'énergie (ΔE < 0).", "متفقة")],
             "السؤال cinq. E l sur A du radium égale mille sept cent trente et un virgule trois sur deux cent vingt-six، يعني sept virgule soixante-six. E l sur A du radon égale mille sept cent sept virgule neuf sur deux cent vingt-deux، يعني sept virgule soixante-neuf. sept virgule soixante-neuf plus grand، إذن le radon plus stable، واخا E l ديالو صغيرة. النتيجة متفقة: le noyau كيتفكك بوحدو باش يعطي noyau plus stable، وكتخرج l'énergie."),
        "ex_n7_5", "fa_n7_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n7_1", "Question 1 : l'équation de la désintégration α", "²²⁶₈₈Ra → ²²²₈₆Rn + ⁴₂He",
      SIMD + "reactions.html?vue=spontanee", "Une réaction spontanée : un noyau émet seul une particule α (exemple du cours : le polonium 210)",
      "شوف le noyau ديال le polonium بوحدو، حتى حاجة ما ضرباتو. كيخرج منو la particule alpha، noyau d'hélium quatre. وكيبقى le plomb. l'équation كتكتب ب les lois de Soddy. فالتمرين ديالنا: deux cent vingt-six égale A plus quatre، إذن A égale deux cent vingt-deux. quatre-vingt-huit égale Z plus deux، إذن Z égale quatre-vingt-six: le radon.",
      centre=[("226 = A + 4 ⇒ A = 222", "إذن A égale deux cent vingt-deux"), ("88 = Z + 2 ⇒ Z = 86 : ²²²₈₆Rn", "إذن Z égale quatre-vingt-six")],
      pointage=[{"mot": "شوف le noyau", "commande": "play_until", "parametres": {"moment": "noyau_seul"}},
                {"mot": "كيخرج منو la particule alpha", "commande": "play_until", "parametres": {"moment": "emission"}},
                {"mot": "وكيبقى le plomb", "commande": "play_until", "parametres": {"moment": "produits"}},
                {"mot": "l'équation كتكتب", "commande": "play_until", "parametres": {"moment": "legende"}}]),
    diapo_sim("ex_n7_2", "Question 2 : E_ℓ lue sur le diagramme, puis Δm en kg", "E_ℓ(Ra) = 2,122290·10⁵ − 2,104977·10⁵ = 1731,3 MeV ; Δm = 1,8586 u = 3,09·10⁻²⁷ kg",
      DIAG, "Le diagramme du cours (polonium 210, national 2020 N) : nucléons séparés, noyau, produits",
      "شوف le diagramme ديال le cours. الفوق: les nucléons بعاد، un virgule neuf sept un huit deux zéro fois dix puissance cinq. تحتو: le noyau ديال le polonium، un virgule neuf cinq cinq trois sept deux fois dix puissance cinq. الفرق بيناتهم هو l'énergie de liaison: mille six cent quarante-quatre virgule huit méga électron volt. فالتمرين ديالنا: E l du radium égale mille sept cent trente et un virgule trois. باش نوصلو ل delta m: كنقسمو sur neuf cent trente et un virgule cinq، يعني un virgule huit mille cinq cent quatre-vingt-six u، ومن بعد fois un virgule soixante-six fois dix puissance moins vingt-sept: trois virgule zéro neuf fois dix puissance moins vingt-sept kilogramme.",
      centre=[("E_ℓ(Ra) = 1731,3 MeV", "E l du radium égale mille"), ("Δm = 1731,3/931,5 = 1,8586 u = 3,09·10⁻²⁷ kg", "trois virgule zéro neuf fois dix puissance moins vingt-sept kilogramme")],
      pointage=[{"mot": "الفوق: les nucléons", "commande": "play_until", "parametres": {"moment": "niveau_nucleons"}},
                {"mot": "تحتو: le noyau", "commande": "play_until", "parametres": {"moment": "niveau_reactifs"}},
                {"mot": "الفرق بيناتهم", "repere": "niveau_reactifs"}]),
    diapo_sim("ex_n7_3", "Question 3 : ΔE = E_f − E_i", "ΔE = 2,104928·10⁵ − 2,104977·10⁵ = −4,9 MeV ; E_lib = 4,9 MeV",
      DIAG, "La flèche ΔE : du noyau père aux produits",
      "شوف palier ديال les produits، تحت le noyau. la flèche delta E كتمشي من le noyau ل les produits: delta E égale E f moins E i. فle cours: moins cinq virgule quatre méga électron volt. فالتمرين ديالنا: deux virgule un zéro quatre neuf deux huit fois dix puissance cinq، moins deux virgule un zéro quatre neuf sept sept fois dix puissance cinq، يعني moins quatre virgule neuf méga électron volt. E libérée égale quatre virgule neuf méga électron volt.",
      centre=[("ΔE = E_f − E_i", "delta E égale E f moins E i"), ("ΔE = −4,9 MeV ; E_lib = |ΔE| = 4,9 MeV", "E libérée égale quatre virgule neuf")],
      pointage=[{"mot": "شوف palier ديال les produits", "commande": "play_until", "parametres": {"moment": "niveau_produits"}},
                {"mot": "la flèche delta E", "commande": "play_until", "parametres": {"moment": "fleche_delta_E"}},
                {"mot": "فle cours: moins cinq", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_n7_4", "Question 4 : l'énergie de liaison du radon", "E_ℓ(Rn) + E_ℓ(He) = 1736,2 MeV ; E_ℓ(Rn) = 1736,2 − 28,30 = 1707,9 MeV",
      DIAG, "Du palier des produits au palier des nucléons : on casse les deux noyaux",
      "شوف من جديد les paliers. من les produits ل les nucléons بعاد، خاصنا نهرسو les deux noyaux: le radon و l'hélium. إذن هاد الفرق égale E l du radon plus E l de l'hélium. فالتمرين ديالنا: deux virgule un deux deux deux neuf zéro fois dix puissance cinq، moins deux virgule un zéro quatre neuf deux huit fois dix puissance cinq، يعني mille sept cent trente-six virgule deux. كنقصو E l de l'hélium، vingt-huit virgule trente: E l du radon égale mille sept cent sept virgule neuf méga électron volt.",
      centre=[("E(nucléons) − E(Rn + He) = E_ℓ(Rn) + E_ℓ(He) = 1736,2 MeV", "إذن هاد الفرق égale E l du radon"), ("E_ℓ(Rn) = 1736,2 − 28,30 = 1707,9 MeV", "E l du radon égale mille sept cent sept")],
      pointage=[{"mot": "شوف من جديد les paliers", "commande": "play_until", "parametres": {"moment": "niveau_produits"}},
                {"mot": "من les produits ل les nucléons", "repere": "niveau_produits"},
                {"mot": "les nucléons بعاد، خاصنا", "repere": "niveau_nucleons"}]),
    diapo_sim("ex_n7_5", "Question 5 : le plus stable", "E_ℓ/A(Ra) = 7,66 < E_ℓ/A(Rn) = 7,69 MeV/nucléon : le radon est plus stable",
      SIMD + "figures.html?fig=fig_stabilite", "Comparer la stabilité : la plus grande E_ℓ/A (exemple du cours : ⁶⁰Ni et ⁵⁶Ni)",
      "شوف l'exemple ديال le cours: le nickel soixante، huit virgule soixante-dix-huit، و le nickel cinquante-six، huit virgule soixante-quatre. huit virgule soixante-dix-huit plus grand: le nickel soixante plus stable. فالتمرين ديالنا: le radium، sept virgule soixante-six، و le radon، sept virgule soixante-neuf. إذن le radon plus stable، واخا E l ديالو صغيرة. رد البال: كنقارنو E l sur A، ماشي E l. ومتفقة: le radium كيتفكك بوحدو باش يولي noyau plus stable.",
      centre=[("E_ℓ/A(Ra) = 1731,3/226 = 7,66", "le radium، sept virgule soixante-six"), ("E_ℓ/A(Rn) = 1707,9/222 = 7,69 : Rn plus stable", "le radon، sept virgule soixante-neuf")],
      pointage=[{"mot": "شوف l'exemple", "commande": "play_until", "parametres": {"moment": "calcul"}},
                {"mot": "huit virgule soixante-dix-huit plus grand", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                {"mot": "رد البال", "commande": "play_until", "parametres": {"moment": "piege"}}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n7_1", "Plus facile : la particule α", "نتمرنو على la particule alpha.",
      "Lors d'une désintégration α, le noyau émet :",
      ["un électron ⁰₋₁e", "un noyau d'hélium ⁴₂He", "un neutron ¹₀n"], 1, {
        "1": {"juste": rep("برافو! la particule alpha هي noyau d'hélium quatre: A كينقص de quatre، et Z de deux.", "Juste : α = ⁴₂He (A − 4, Z − 2).")},
        "0": {"1": rep("ما تقلقش. l'électron ديال la radioactivité bêta moins. و alpha؟ عاود اختار.", "L'électron, c'est β⁻. Et α ? Réessaie."),
              "2": rep("الجواب: noyau d'hélium quatre.", "Réponse : ⁴₂He.")},
        "2": {"1": rep("لا، le neutron كيخرج ف la fission. عاود اختار.", "Le neutron sort lors d'une fission. Réessaie."),
              "2": rep("الجواب: noyau d'hélium quatre.", "Réponse : ⁴₂He.")}},
      "Lors d'une désintégration alpha, le noyau émet quoi ?"),
    qcm_facile("fa_n7_2", "Plus facile : de MeV à kg", "سؤال ساهل: من l'énergie ل la masse.",
      "Une énergie de liaison de 931,5 MeV correspond à un défaut de masse de :",
      ["1 u = 1,66·10⁻²⁷ kg", "931,5 u", "931,5 × 1,66·10⁻²⁷ kg"], 0, {
        "0": {"juste": rep("برافو! neuf cent trente et un virgule cinq méga électron volt sur c au carré، هي la valeur de un u.", "Juste : 931,5 MeV/c² = 1 u = 1,66·10⁻²⁷ kg.")},
        "1": {"1": rep("ما تقلقش. la valeur de un u كتقابل، neuf cent trente et un virgule cinq méga électron volt. واش نقسمو ولا نضربو؟ عاود اختار.", "1 u ↔ 931,5 MeV : faut-il diviser ? Réessaie."),
              "2": rep("الجواب: un u، يعني un virgule soixante-six fois dix puissance moins vingt-sept kilogramme.", "Réponse : 1 u = 1,66·10⁻²⁷ kg.")},
        "2": {"1": rep("قريب، ولكن خاصك اللول تقسم sur neuf cent trente et un virgule cinq باش تلقى u. عاود اختار.", "Divise d'abord par 931,5 pour avoir des u. Réessaie."),
              "2": rep("الجواب: un u، يعني un virgule soixante-six fois dix puissance moins vingt-sept kilogramme.", "Réponse : 1 u = 1,66·10⁻²⁷ kg.")}},
      "Une énergie de liaison de neuf cent trente et un virgule cinq méga électron volt correspond à quel défaut de masse ?"),
    vrai_faux_facile("fa_n7_3", "Plus facile : vrai ou faux", "سؤال ساهل على le diagramme.",
      "Diagramme : E(Ra) = 2,104977·10⁵ MeV ; E(Rn + He) = 2,104928·10⁵ MeV.",
      [("ΔE = E(Rn + He) − E(Ra) = −4,9 MeV.", True, "ΔE = E_f − E_i : arrivée moins départ."),
       ("L'énergie libérée est E_lib = −4,9 MeV.", False, "E_lib = |ΔE| = 4,9 MeV, toujours positive."),
       ("On peut calculer ΔE avec seulement 2,104928 − 2,104977, sans les puissances de dix.", False, "Le résultat serait −0,0000049 : il faut multiplier par 10⁵ (−4,9 MeV).")]),
    association_facile("fa_n7_4", "Plus facile : lire les écarts du diagramme", "سؤال ساهل: ربط كل فرق ديال les paliers بالمعنى ديالو.",
      "Relie chaque écart entre paliers à ce qu'il représente.", "Associer chaque écart à son énergie.",
      [("1", "E(nucléons) − E(Ra)"), ("2", "E(nucléons) − E(Rn + He)"), ("3", "E(Rn + He) − E(Ra)")],
      [("a", "ΔE de la désintégration"), ("b", "E_ℓ(Ra)"), ("c", "E_ℓ(Rn) + E_ℓ(He)")],
      {"1": "b", "2": "c", "3": "a"},
      {"1-b": (True, "Oui : séparer le radium en ses nucléons coûte E_ℓ(Ra).", "صحيح. باش نفرقو le radium خاصنا E l du radium."),
       "1-c": (False, "Cet écart part du radium, pas des produits : il ne concerne qu'un seul noyau.", "هاد الفرق كيبدا من le radium، ماشي من les produits."),
       "1-a": (False, "ΔE relie le radium aux produits, pas aux nucléons séparés.", "delta E كتربط le radium ب les produits، ماشي ب les nucléons."),
       "2-c": (True, "Oui : il faut casser les deux noyaux produits.", "صحيح. خاصنا نهرسو les deux noyaux: le radon و l'hélium."),
       "2-b": (False, "Cet écart part des produits (Rn + He), pas du radium.", "هاد الفرق كيبدا من les produits، ماشي من le radium."),
       "2-a": (False, "ΔE ne passe pas par les nucléons séparés.", "delta E ما كتفوتش من les nucléons بعاد."),
       "3-a": (True, "Oui : ΔE = E_f − E_i = −4,9 MeV.", "صحيح. delta E égale E f moins E i."),
       "3-b": (False, "Cet écart ne fait pas intervenir les nucléons séparés : ce n'est pas une énergie de liaison.", "هاد الفرق ما فيهش les nucléons بعاد: ماشي énergie de liaison."),
       "3-c": (False, "Cet écart relie le radium aux produits : c'est le bilan de la réaction.", "هاد الفرق كيربط le radium ب les produits: هادي الحصيلة.")},
      "(1 ; b) (2 ; c) (3 ; a).",
      "الأزواج: un avec b، deux avec c، trois avec a."),
    qcm_facile("fa_n7_5", "Plus facile : le plus stable", "سؤال ساهل على la stabilité.",
      "E_ℓ(Ra) = 1731,3 MeV (A = 226) ; E_ℓ(Rn) = 1707,9 MeV (A = 222). Le plus stable est :",
      ["le radium, car E_ℓ(Ra) > E_ℓ(Rn)", "le radon, car E_ℓ/A(Rn) > E_ℓ/A(Ra)", "les deux sont aussi stables"], 1, {
        "1": {"juste": rep("برافو! sept virgule soixante-neuf plus grand que sept virgule soixante-six: le radon plus stable.", "Juste : 7,69 > 7,66 MeV/nucléon.")},
        "0": {"1": rep("هادا هو الفخ. واش كنقارنو E l ولا E l sur A؟ عاود اختار.", "Compare-t-on E_ℓ ou E_ℓ/A ? Réessaie."),
              "2": rep("الجواب: le radon، حيت E l sur A ديالو كبر: sept virgule soixante-neuf contre sept virgule soixante-six.", "Réponse : le radon (7,69 > 7,66).")},
        "2": {"1": rep("لا، حسب E l sur A ديال كل واحد، وغادي تلقى فرق صغير ولكن كاين. عاود اختار.", "Calcule E_ℓ/A : il y a une petite différence. Réessaie."),
              "2": rep("الجواب: le radon، sept virgule soixante-neuf contre sept virgule soixante-six.", "Réponse : le radon.")}},
      "Énergies de liaison du radium et du radon données. Le plus stable est lequel ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, un autre noyau : le thorium 230",
    "enonce": {
      "intro": "Le thorium ²³⁰₉₀Th est radioactif α et donne un isotope du radium Ra. La figure représente le diagramme énergétique de cette désintégration.",
      "intro_dit": "le thorium deux cent trente radioactif alpha، وكيعطي l'isotope ديال le radium.",
      "figures": [niveaux_abs("Figure : diagramme énergétique (thorium 230)",
                              "90 ¹₁p + 140 ¹₀n", "²³⁰₉₀Th", "Ra + ⁴₂He", "2,159847·10⁵", "2,142298·10⁵", "2,142251·10⁵")],
      "donnees": ["E_ℓ(⁴₂He) = 28,30 MeV", "1 u = 931,5 MeV/c² = 1,66·10⁻²⁷ kg", "Extrait du tableau périodique : ₈₆Rn, ₈₇Fr, ₈₈Ra, ₈₉Ac, ₉₀Th"],
      "questions": [
        question_semblable("1", "Écrire l'équation de la désintégration du thorium 230, en précisant les lois utilisées.",
          phrase("²³⁰₉₀Th → ²²⁶₈₈Ra + ⁴₂He : conservation de A (230 = A + 4, A = 226) et de Z (90 = Z + 2, Z = 88)."),
          ["⁴₂He", "conservation de A", "conservation de Z"], ["⁰₋₁e"],
          corr([("1 : ²³⁰₉₀Th → ²²⁶₈₈Ra + ⁴₂He (A = 230 − 4 ; Z = 90 − 2)", "le thorium كيعطي le radium")],
               "le thorium كيعطي le radium deux cent vingt-six et l'hélium quatre.")),
        question_semblable("2", "Déterminer E_ℓ(²³⁰Th) à l'aide du diagramme, puis son défaut de masse Δm en kilogramme.",
          valeur("Δm", 3.13e-27, "kg", "E_ℓ = 2,159847·10⁵ − 2,142298·10⁵ = 1754,9 MeV ; Δm = 1754,9/931,5 = 1,8840 u = 1,8840 × 1,66·10⁻²⁷ = 3,13·10⁻²⁷ kg"),
          ["Δm = E_ℓ/c²", "÷ 931,5"], ["Δm = 1754,9 × 1,66·10⁻²⁷"],
          corr([("2 : E_ℓ(Th) = 1754,9 MeV ; Δm = 1,8840 u = 3,13·10⁻²⁷ kg", "trois virgule treize fois dix puissance moins vingt-sept kilogramme")],
               "E l du thorium égale mille sept cent cinquante-quatre virgule neuf. delta m égale un virgule quatre-vingt-huit mille quatre cent quarante u، يعني trois virgule treize fois dix puissance moins vingt-sept kilogramme.")),
        question_semblable("3", "Déterminer ΔE et l'énergie libérée E_lib.",
          valeur("E_lib", 4.7, "MeV", "ΔE = 2,142251·10⁵ − 2,142298·10⁵ = −4,7 MeV ; E_lib = 4,7 MeV"), ["ΔE = E_f − E_i"], ["ΔE = E_i − E_f"],
          corr([("3 : ΔE = E_f − E_i = −4,7 MeV ; E_lib = |ΔE| = 4,7 MeV", "quatre virgule sept")],
               "delta E égale E f moins E i، يعني moins quatre virgule sept، و E libérée égale quatre virgule sept méga électron volt.")),
        question_semblable("4", "Déterminer l'énergie de liaison du noyau de radium produit.",
          valeur("E_ℓ(Ra)", 1731.3, "MeV", "E_ℓ(Ra) + E_ℓ(He) = 2,159847·10⁵ − 2,142251·10⁵ = 1759,6 MeV ; E_ℓ(Ra) = 1759,6 − 28,30 = 1731,3 MeV"),
          ["E_ℓ(Ra) + E_ℓ(He)", "28,30"], ["E_ℓ(Ra) = 1759,6 MeV"],
          corr([("4 : E_ℓ(Ra) + E_ℓ(He) = 1759,6 MeV ; E_ℓ(Ra) = 1759,6 − 28,30 = 1731,3 MeV", "mille sept cent trente et un virgule trois")],
               "E l du radium plus E l de l'hélium égale mille sept cent cinquante-neuf virgule six. كنقصو، moins vingt-huit virgule trente: mille sept cent trente et un virgule trois méga électron volt.")),
        question_semblable("5", "Comparer la stabilité de ²³⁰Th et ²²⁶Ra. Est-ce cohérent avec la désintégration spontanée du thorium ?",
          phrase("E_ℓ/A(Th) = 1754,9/230 = 7,63 MeV/nucléon < E_ℓ/A(Ra) = 1731,3/226 = 7,66 MeV/nucléon : le radium est plus stable ; cohérent, la désintégration spontanée donne un noyau plus stable."),
          ["E_ℓ/A", "plus stable"], ["comparer E_ℓ"],
          corr([("5 : 7,63 < 7,66 MeV/nucléon : ²²⁶Ra est plus stable que ²³⁰Th ; cohérent avec la désintégration spontanée.", "le radium plus stable")],
               "E l sur A du thorium égale sept virgule soixante-trois، و du radium sept virgule soixante-six. إذن le radium plus stable، ومتفقة مع la désintégration.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
