# Exercice de SVT (ch. 4, relation gène – protéine) : expériences de marquage, niveau moyen (niveau du national).
# Ce qu'il entraîne : justifier le choix d'un précurseur radioactif (uracile = base propre à l'ARN), « Décrire… puis déduire »
# une courbe de radioactivité noyau / cytoplasme (une ligne par période, valeurs lues), lire un tableau (leucine radioactive),
# proposer une hypothèse (un intermédiaire, l'ARNm, porte l'information du noyau aux ribosomes), nommer et situer
# transcription et traduction. Pas de mutation (autres exercices du cours).
# Le cours et la simulation parlent d'« uracile radioactif » (pas d'uridine) : on garde ce mot (professeur règle 27).
# Sources comparées :
# - exploration relation_gene_proteine.json : capacité RGP4 (« exploiter des expériences de marquage : uracile radioactif,
#   acides aminés radioactifs, autoradiographie »), piège « pense que l'ADN sort du noyau » (simulation marquage),
#   cas_type « hypothese_verification » (forme « proposez une hypothèse »), redaction « Décrire puis déduire ».
# - vidéos des profs (exploration) : Faress (analogie livre / photocopie), Ikram et Driss (« l'ADN ne sort jamais du noyau »).
# - nationaux : expériences de marquage à la thymidine radioactive (2017 R, 2019 R, 2021 R : réplication, autre chapitre ; on
#   n'en reprend ni la situation ni les données) ; formes « Décrivez… puis déduisez », « proposez une hypothèse ».
# - séries en ligne : recherche faite (dyrassa, moutamadris, documents d'autoradiographie à l'uracile) mais lecture impossible
#   (réseau de la session refusé).
# Données originales ; courbes calculées ci-dessous (fonctions noyau / cytoplasme), radioactivité conservée après le transfert.
import sys
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/relation_gene_proteine-tableau/"
URA = BASE + "marquage.html?vue=uracile"
ACI = BASE + "marquage.html?vue=acides_amines"
BILAN = BASE + "schema_bilan.html?vue=schema"

# ── Données (exercice principal, puis semblable) : pic du noyau, durée du marquage, début de la sortie, pente ──
class Courbe:
    def __init__(s, pic, t_marq, t_sortie, pente):
        s.pic, s.tm, s.ts, s.p = pic, t_marq, t_sortie, pente
    def noyau(s, t):
        if t <= s.tm: return s.pic * t / s.tm
        if t <= s.ts: return s.pic
        return s.pic - s.p * (t - s.ts)
    def cyto(s, t):
        return 0 if t <= s.ts else s.p * (t - s.ts)
    def exprs(s):
        a = s.pic / s.tm
        return (f"{a}*x", f"{s.pic}", f"{s.pic}-{s.p}*(x-{s.ts})", f"{s.p}*(x-{s.ts})")

A = Courbe(80, 5, 10, 2.5)
B = Courbe(60, 5, 8, 2)
# vérifications des valeurs dites dans les réponses
assert (A.noyau(5), A.noyau(10), A.noyau(30), A.cyto(30), A.noyau(20), A.cyto(20)) == (80, 80, 30, 50, 55, 25)
assert (B.noyau(5), B.noyau(8), B.noyau(30), B.cyto(30)) == (60, 60, 16, 44)
for C in (A, B):
    for t in range(C.ts, 31): assert abs(C.noyau(t) + C.cyto(t) - C.pic) < 1e-9   # conservation après le transfert
TAB_A = {"5 min": (0, 40), "30 min": (0, 90)}
TAB_B = {"5 min": (0, 30), "30 min": (0, 75)}

def fv(v):
    return str(int(v)) if float(v).is_integer() else str(v).replace(".", ",")

def fig_courbe(C, titre):
    e1, e2, e3, e4 = C.exprs()
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": 30, "nom": "t", "unite": "min", "graduations": [0, 5, 10, 15, 20, 25, 30]},
                     "y": {"min": 0, "max": 100, "nom": "radioactivité", "unite": "u.a.", "graduations": [0, 20, 40, 60, 80, 100]}},
            "legende": f"Expérience 1 : uracile radioactif pendant {C.tm} min, puis milieu non radioactif. Radioactivité du noyau (violet) et du cytoplasme (orange).",
            "elements": [
              {"f": "courbe", "expr": e1, "de": 0, "a": C.tm, "couleur": "violet"},
              {"f": "courbe", "expr": e2, "de": C.tm, "a": C.ts, "couleur": "violet"},
              {"f": "courbe", "expr": e3, "de": C.ts, "a": 30, "couleur": "violet", "texte": "noyau", "texte_x": 26, "pos": "n"},
              {"f": "courbe", "expr": "0", "de": 0, "a": C.ts, "couleur": "orange"},
              {"f": "courbe", "expr": e4, "de": C.ts, "a": 30, "couleur": "orange", "texte": "cytoplasme", "texte_x": 26, "pos": "n"},
              {"f": "fleche", "de": [C.tm, 97], "a": [C.tm, C.pic + 3], "couleur": "jaune", "texte": "transfert en milieu non radioactif", "pos": "e"},
              {"f": "repere", "x": C.ts, "y": C.pic, "couleur": "faible"}]}

def fig_tableau(tab, titre):
    els = [{"f": "rect", "de": [0.2, 0.2], "a": [9.8, 3.4], "couleur": "faible"},
           {"f": "ligne", "pts": [[0.2, 2.4], [9.8, 2.4]], "couleur": "faible"},
           {"f": "ligne", "pts": [[0.2, 1.3], [9.8, 1.3]], "couleur": "faible"},
           {"f": "ligne", "pts": [[5.0, 0.2], [5.0, 3.4]], "couleur": "faible"},
           {"f": "ligne", "pts": [[7.4, 0.2], [7.4, 3.4]], "couleur": "faible"},
           {"f": "texte", "at": [2.6, 2.9], "t": "radioactivité (u.a.)", "couleur": "cyan", "taille": "petit"},
           {"f": "texte", "at": [2.6, 1.85], "t": "noyau", "couleur": "violet"},
           {"f": "texte", "at": [2.6, 0.75], "t": "cytoplasme (ribosomes)", "couleur": "orange", "taille": "petit"}]
    for (temps, (n, c)), x in zip(tab.items(), (6.2, 8.6)):
        els += [{"f": "texte", "at": [x, 2.9], "t": temps, "couleur": "cyan"},
                {"f": "texte", "at": [x, 1.85], "t": str(n), "couleur": "blanc"},
                {"f": "texte", "at": [x, 0.75], "t": str(c), "couleur": "blanc"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": 3.6},
            "legende": "Expérience 2 : leucine radioactive (un acide aminé). Radioactivité mesurée par autoradiographie.", "elements": els}

def intro(C, cellules):
    return (f"Pour savoir où sont fabriqués l'ARN et les protéines, on réalise deux expériences sur des {cellules} en culture. "
            f"Expérience 1 : on place les cellules pendant {C.tm} min dans un milieu contenant de l'uracile radioactif, puis on les lave "
            "et on les transfère dans un milieu non radioactif. On mesure, par autoradiographie, la radioactivité du noyau et celle du "
            "cytoplasme au cours du temps (document 1). Expérience 2 : d'autres cellules sont placées dans un milieu contenant de la "
            "leucine radioactive, un acide aminé ; la radioactivité est mesurée à 5 min et à 30 min (document 2).")

def att2(C):
    return (f"De 0 à {C.tm} min, la radioactivité du noyau augmente de 0 à {fv(C.pic)} u.a. alors que celle du cytoplasme reste nulle. "
            f"De {C.tm} à {C.ts} min, la radioactivité du noyau reste constante ({fv(C.pic)} u.a.) et celle du cytoplasme reste nulle. "
            f"De {C.ts} à 30 min, la radioactivité du noyau diminue de {fv(C.pic)} à {fv(C.noyau(30))} u.a. tandis que celle du cytoplasme "
            f"augmente de 0 à {fv(C.cyto(30))} u.a. On en déduit que l'ARN est synthétisé dans le noyau, puis qu'il migre du noyau vers le cytoplasme.")

def corr2(C):
    return {"lignes": [
        {"texte": f"2 : de 0 à {C.tm} min : noyau ↑ de 0 à {fv(C.pic)} u.a. ; cytoplasme nul", "mot": "la radioactivité ديال le noyau كتزاد"},
        {"texte": f"de {C.tm} à {C.ts} min : noyau constant ({fv(C.pic)} u.a.) ; cytoplasme nul", "mot": "كتبقى ثابتة"},
        {"texte": f"de {C.ts} à 30 min : noyau ↓ de {fv(C.pic)} à {fv(C.noyau(30))} u.a. ; cytoplasme ↑ de 0 à {fv(C.cyto(30))} u.a.", "mot": "و la radioactivité ديال le cytoplasme كتزاد"},
        {"texte": "on en déduit : l'ARN est synthétisé dans le noyau, puis migre vers le cytoplasme", "mot": "on en déduit"}],
        "parole": (f"question deux. de zéro à {nb(C.tm)} minutes، la radioactivité ديال le noyau كتزاد، de zéro à {nb(C.pic)} unités arbitraires، "
                   f"و le cytoplasme ما فيه والو. de {nb(C.tm)} à {nb(C.ts)} minutes، la radioactivité ديال le noyau كتبقى ثابتة، à {nb(C.pic)} unités arbitraires. "
                   f"de {nb(C.ts)} à trente minutes، la radioactivité ديال le noyau كتنقص، de {nb(C.pic)} à {nb(C.noyau(30))}، "
                   f"و la radioactivité ديال le cytoplasme كتزاد، de zéro à {nb(C.cyto(30))} unités arbitraires. "
                   "on en déduit que l'A R N كيتصاوب ف le noyau، ومن بعد كيدوز ل le cytoplasme.")}

NB = {5: "cinq", 8: "huit", 10: "dix", 16: "seize", 30: "trente", 44: "quarante-quatre", 50: "cinquante", 60: "soixante", 80: "quatre-vingts",
      40: "quarante", 90: "quatre-vingt-dix", 75: "soixante-quinze"}
def nb(v):
    return NB[int(v)]

def att3(tab):
    (t1, (n1, c1)), (t2, (n2, c2)) = tab.items()
    return (f"La radioactivité est nulle dans le noyau à {t1} et à {t2} ; elle est présente seulement dans le cytoplasme, au niveau des ribosomes, "
            f"et y augmente de {c1} u.a. à {t1} à {c2} u.a. à {t2}. La leucine radioactive est incorporée dans les protéines : on en déduit que "
            "les protéines sont synthétisées dans le cytoplasme, au niveau des ribosomes.")

def corr3(tab):
    (t1, (n1, c1)), (t2, (n2, c2)) = tab.items()
    return {"lignes": [
        {"texte": "3 : noyau : radioactivité nulle (0 u.a.) à 5 min et à 30 min", "mot": "le noyau ما فيه حتى radioactivité"},
        {"texte": f"cytoplasme (ribosomes) : {c1} u.a. à 5 min, {c2} u.a. à 30 min", "mot": "ف le cytoplasme، ف les ribosomes"},
        {"texte": "on en déduit : les protéines sont synthétisées dans le cytoplasme, sur les ribosomes", "mot": "on en déduit"}],
        "parole": (f"question trois. le noyau ما فيه حتى radioactivité، à cinq minutes et à trente minutes. la radioactivité كاينة غير ف le cytoplasme، ف les ribosomes: "
                   f"{nb(c1)} unités arbitraires à cinq minutes، et {nb(c2)} à trente minutes. la leucine كتدخل ف les protéines، "
                   "إذن on en déduit que les protéines كيتصاوبو ف le cytoplasme، ف les ribosomes.")}

ATT1 = "L'uracile (U) est une base qui existe dans l'ARN et jamais dans l'ADN : l'uracile radioactif est incorporé seulement dans l'ARN fabriqué par la cellule. La radioactivité permet donc de suivre l'ARN (où il est fabriqué, où il va), sans marquer l'ADN."
CLAV1 = {"aides": ["uracile (U)", "base propre à l'ARN", "thymine (T)", "incorporé", "suivre l'ARN"], "pieges": ["l'uracile est dans l'ADN", "acide aminé"]}
CORR1 = {"lignes": [
    {"texte": "1 : l'uracile est une base de l'ARN, absente de l'ADN (qui contient T)", "mot": "base كاينة غير ف l'A R N"},
    {"texte": "l'uracile radioactif est incorporé seulement dans l'ARN fabriqué", "mot": "كتدخل غير ف l'A R N"},
    {"texte": "la radioactivité permet de suivre l'ARN, sans marquer l'ADN", "mot": "كنتبعو l'A R N"}],
    "parole": "question un. l'uracile هي base كاينة غير ف l'A R N، و l'A D N فيه la thymine ف البلاصة ديالها. إذن l'uracile radioactif كتدخل غير ف l'A R N اللي كيتصاوب. إذن la radioactivité كتبين غير l'A R N، ماشي l'A D N، وكنتبعو l'A R N: فين كيتصاوب، و فين كيمشي."}
ATT4 = "Hypothèse : dans le noyau, l'information génétique d'un gène est copiée sous forme d'un ARN, l'ARN messager (ARNm) ; cet ARNm sort du noyau par les pores nucléaires et porte l'information jusqu'aux ribosomes du cytoplasme, où elle est utilisée pour fabriquer la protéine. L'ARNm est donc l'intermédiaire entre l'ADN et la protéine."
CLAV4 = {"aides": ["intermédiaire", "copie", "ARN messager (ARNm)", "pores nucléaires", "ribosomes"], "pieges": ["l'ADN sort du noyau", "les ribosomes entrent dans le noyau"]}
CORR4 = {"lignes": [
    {"texte": "4 : hypothèse : l'information d'un gène est copiée dans le noyau sous forme d'ARN messager (ARNm)", "mot": "كتنسخ ف le noyau"},
    {"texte": "l'ARNm sort par les pores nucléaires et porte l'information aux ribosomes du cytoplasme", "mot": "كيخرج من les pores"},
    {"texte": "l'ARNm est l'intermédiaire entre l'ADN (noyau) et la protéine (cytoplasme)", "mot": "هو l'intermédiaire"}],
    "parole": "question quatre. l'A D N ما كيخرجش من le noyau. إذن l'hypothèse: l'information ديال le gène كتنسخ ف le noyau، ف واحد l'A R N: l'A R N messager. هاد l'A R N messager كيخرج من les pores، وكيهز l'information حتى ل les ribosomes ف le cytoplasme. إذن l'A R N messager هو l'intermédiaire بين l'A D N و la protéine."}
ATT5 = "Transcription : synthèse de l'ARNm à partir de l'ADN (brin transcrit d'un gène), dans le noyau. Traduction : synthèse de la protéine (chaîne d'acides aminés) à partir de l'ARNm, dans le cytoplasme, sur les ribosomes. Bilan : ADN → (transcription, noyau) → ARNm → (traduction, cytoplasme) → protéine."
CLAV5 = {"aides": ["transcription", "traduction", "noyau", "cytoplasme", "ribosomes", "ADN → ARNm → protéine"], "pieges": ["réplication", "traduction dans le noyau"]}
CORR5 = {"lignes": [
    {"texte": "5 : transcription : ADN → ARNm, dans le noyau", "mot": "la transcription"},
    {"texte": "traduction : ARNm → protéine, dans le cytoplasme, sur les ribosomes", "mot": "la traduction"},
    {"texte": "ADN → (transcription) → ARNm → (traduction) → protéine", "mot": "l'A D N، ومن بعد l'A R N messager"}],
    "parole": "question cinq. المرحلة اللولة هي la transcription: كتصاوب l'A R N messager من l'A D N، ف le noyau. المرحلة الثانية هي la traduction: كتصاوب la protéine من l'A R N messager، ف le cytoplasme، ف les ribosomes. إذن: l'A D N، ومن بعد l'A R N messager، ومن بعد la protéine."}

Q1_T = "Expliquer pourquoi on utilise de l'uracile radioactif pour suivre la synthèse de l'ARN."
Q2_T = "Décrire l'évolution de la radioactivité dans le noyau et dans le cytoplasme (document 1), puis déduire le lieu de synthèse de l'ARN et son devenir."
Q3_T = "Décrire la répartition de la radioactivité dans la cellule (document 2), puis déduire le lieu de synthèse des protéines."
Q4_T = "Sachant que l'ADN, support de l'information génétique, ne quitte jamais le noyau, proposer une hypothèse expliquant comment l'information génétique parvient aux ribosomes du cytoplasme."
Q5_T = "Nommer les deux étapes de l'expression de l'information génétique mises en évidence par ces expériences, et préciser le lieu de chacune."

EX = {
  "id": "svt_ex_ch4_marquage_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "relation_gene_proteine", "cours": "svt_ch4_relation_gene_proteine",
  "titre": "Uracile et leucine radioactifs : où se fabriquent l'ARN et les protéines ?", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Exploiter des expériences de marquage radioactif", "Décrire une courbe puis déduire", "Proposer une hypothèse sur l'ARNm intermédiaire", "Situer la transcription et la traduction"],
  "enonce": {
    "intro": intro(A, "cellules animales"),
    "intro_dit": "نقراو l'énoncé. باش نعرفو فين كيتصاوب l'A R N و فين كيتصاوبو les protéines، on a réalisé deux expériences، على des cellules. l'expérience un: حطينا les cellules، pendant cinq minutes، ف milieu فيه l'uracile radioactif. من بعد غسلناهم، وحطيناهم ف milieu non radioactif. وقسنا la radioactivité ديال le noyau و ديال le cytoplasme، ب l'autoradiographie: هادا le document un. l'expérience deux: cellules أخرين، ف milieu فيه la leucine radioactive، وهي un acide aminé. قسنا la radioactivité، à cinq minutes et à trente minutes: هادا le document deux.",
    "figures": [fig_courbe(A, "Document 1 : radioactivité du noyau et du cytoplasme (uracile radioactif)"),
                fig_tableau(TAB_A, "Document 2 : répartition de la radioactivité (leucine radioactive)")],
    "donnees": ["u.a. : unité arbitraire", f"Expérience 1 : uracile radioactif de 0 à {A.tm} min, puis milieu non radioactif",
                "Expérience 2 : leucine radioactive (acide aminé), mesures à 5 min et à 30 min"],
    "questions": [
      {"id": "1", "texte": Q1_T,
       "texte_dit": "question un: فسر علاش كنستعملو l'uracile radioactif، باش نتبعو la synthèse ديال l'A R N.",
       "reponse": {"type": "phrase", "attendu": ATT1}, "clavier": CLAV1,
       "aides": [
         {"texte": "Compare les bases de l'ADN et celles de l'ARN : laquelle est dans l'ARN seulement ?",
          "dit": "قارن les bases ديال l'A D N مع les bases ديال l'A R N: شمن base كاينة غير ف l'A R N؟"},
         {"texte": "Une molécule radioactive marque la molécule dans laquelle elle entre. Dans quelle molécule l'uracile entre-t-il, et dans laquelle jamais ?",
          "dit": "la radioactivité كتبقى ف la molécule اللي دخلات فيها. l'uracile فين كتدخل، وفين عمرها ما كتدخل؟"}],
       "correction": CORR1, "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": Q2_T,
       "texte_dit": "question deux: وصف l'évolution ديال la radioactivité ف le noyau و ف le cytoplasme، ف le document un، ومن بعد استنتج فين كيتصاوب l'A R N، وشنو كيوقع ليه.",
       "reponse": {"type": "phrase", "attendu": att2(A)},
       "clavier": {"aides": ["De 0 à 5 min", "augmente", "reste constante", "diminue", "u.a.", "On en déduit que"], "pieges": ["l'ARN est synthétisé dans le cytoplasme"]},
       "aides": [
         {"texte": f"Découpe le temps en trois périodes : de 0 à {A.tm} min, de {A.tm} à {A.ts} min, de {A.ts} à 30 min. Pour chacune, lis les deux courbes.",
          "dit": f"قسم le temps en trois périodes: de zéro à cinq minutes، de cinq à dix minutes، و de dix à trente minutes. ف كل période، قرا les deux courbes."},
         {"texte": "Une ligne par période : « De … à … min, la radioactivité du noyau augmente / reste constante / diminue de … à … u.a., celle du cytoplasme … ». Puis : « On en déduit que l'ARN… ».",
          "dit": "سطر لكل période: la radioactivité ديال le noyau كتزاد، ولا ثابتة، ولا كتنقص، مع les valeurs، ونفس الشي ل le cytoplasme. ومن بعد: on en déduit que l'A R N، وكمل."}],
       "correction": corr2(A), "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": Q3_T,
       "texte_dit": "question trois: وصف فين كاينة la radioactivité ف la cellule، ف le document deux، ومن بعد استنتج فين كيتصاوبو les protéines.",
       "reponse": {"type": "phrase", "attendu": att3(TAB_A)},
       "clavier": {"aides": ["nulle dans le noyau", "cytoplasme", "ribosomes", "augmente", "On en déduit que"], "pieges": ["protéines synthétisées dans le noyau"]},
       "aides": [
         {"texte": "Lis la ligne « noyau » puis la ligne « cytoplasme », à 5 min et à 30 min.",
          "dit": "قرا السطر ديال le noyau، ومن بعد السطر ديال le cytoplasme، à cinq minutes et à trente minutes."},
         {"texte": "La leucine est un acide aminé : dans quelle molécule entre-t-elle ? Là où est la radioactivité, cette molécule est fabriquée.",
          "dit": "la leucine هي un acide aminé: ف شمن molécule كتدخل؟ فين كاينة la radioactivité، تما كتتصاوب هاد la molécule."}],
       "correction": corr3(TAB_A), "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": Q4_T,
       "texte_dit": "question quatre: عارفين بلي l'A D N، اللي فيه l'information génétique، عمرو ما كيخرج من le noyau. اقترح une hypothèse: كيفاش كتوصل l'information génétique ل les ribosomes ف le cytoplasme؟",
       "reponse": {"type": "phrase", "attendu": ATT4}, "clavier": CLAV4,
       "aides": [
         {"texte": "Relie tes deux déductions : une molécule est fabriquée dans le noyau puis passe dans le cytoplasme, où sont fabriquées les protéines.",
          "dit": "ربط les deux déductions ديالك: كاينة molécule كتتصاوب ف le noyau، ومن بعد كتدوز ل le cytoplasme، فين كيتصاوبو les protéines."},
         {"texte": "Le livre (l'ADN) reste à la bibliothèque (le noyau) : qu'est-ce qui sort à sa place ? Donne son nom et son rôle.",
          "dit": "le livre، يعني l'A D N، كيبقى ف la bibliothèque، يعني le noyau. شنو اللي كيخرج ف البلاصة ديالو؟ عطي السمية ديالو و الدور ديالو."}],
       "correction": CORR4, "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": Q5_T,
       "texte_dit": "question cinq: سمي les deux étapes ديال l'expression ديال l'information génétique، اللي بانو ف هاد les expériences، وحدد فين كتوقع كل وحدة.",
       "reponse": {"type": "phrase", "attendu": ATT5}, "clavier": CLAV5,
       "aides": [
         {"texte": "Première étape : de l'ADN à l'ARNm. Deuxième étape : de l'ARNm à la protéine. Quels sont leurs noms ?",
          "dit": "المرحلة اللولة: من l'A D N ل l'A R N messager. المرحلة الثانية: من l'A R N messager ل la protéine. شنو السمية ديالهم؟"},
         {"texte": "Reprends tes déductions des questions 2 et 3 pour donner le lieu de chacune.",
          "dit": "رجع ل les déductions ديال question deux و question trois، باش تعطي البلاصة ديال كل وحدة."}],
       "correction": CORR5, "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : pourquoi l'uracile ?",
     "screen_content": {"lead": "L'uracile est une base propre à l'ARN : elle ne marque que l'ARN."},
     "visual": {"kind": "simulation", "url": URA, "caption": "La cellule, le noyau avec l'ADN, les ribosomes du cytoplasme"},
     "speech_text": {"mixed": "شوف la cellule: ف le noyau كاين l'A D N، وف le cytoplasme كاينين les ribosomes. دابا كنعطيو l'uracile radioactif. علاش l'uracile؟ حيت هي base كاينة غير ف l'A R N، و l'A D N فيه la thymine ف البلاصة ديالها. إذن la radioactivité كتدخل غير ف l'A R N الجديد، وما كتدخلش ف l'A D N."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "uracile (U) : base propre à l'ARN", "mot": "حيت هي base كاينة غير ف l'A R N"},
                  {"texte": "la radioactivité marque l'ARN, pas l'ADN", "mot": "وما كتدخلش ف l'A D N"}],
       "pointage": [{"mot": "شوف la cellule", "commande": "play_until", "parametres": {"moment": "cellule"}},
                    {"mot": "ف le noyau كاين l'A D N", "repere": "adn"},
                    {"mot": "دابا كنعطيو l'uracile radioactif", "commande": "play_until", "parametres": {"moment": "uracile_apporte"}},
                    {"mot": "حيت هي base كاينة غير ف l'A R N", "repere": "uracile_radioactif"},
                    {"mot": "حيت هي base كاينة غير ف l'A R N", "cible": "centre:0"},
                    {"mot": "وما كتدخلش ف l'A D N", "cible": "centre:1"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : d'abord le noyau, puis le cytoplasme",
     "screen_content": {"lead": "Grains d'abord dans le noyau, puis dans le cytoplasme : l'ARN est fabriqué dans le noyau, puis il en sort."},
     "visual": {"kind": "simulation", "url": URA, "caption": "Les grains noirs d'autoradiographie au fil du temps"},
     "speech_text": {"mixed": "كل نقطة كحلة كتبين la radioactivité. à cinq minutes، النقط الكحلين كاينين ف le noyau: l'A R N كيتصاوب تما. من بعد، les cellules ف milieu non radioactif: ما بقاش كيدخل uracile radioactif جديد. à quinze minutes، l'A R N radioactif كيخرج من les pores. à trente minutes، le cytoplasme ولا فيه النقط الكحلين، و le noyau نقصات فيه la radioactivité. هادشي بحال la courbe ديال le document un: le noyau كيطلع اللول، ومن بعد كينقص ملي le cytoplasme كيطلع. on en déduit que l'A R N كيتصاوب ف le noyau، ومن بعد كيدوز ل le cytoplasme."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "d'abord : noyau marqué", "mot": "كاينين ف le noyau"},
                  {"texte": "ensuite : noyau ↓, cytoplasme ↑", "mot": "و le noyau نقصات فيه la radioactivité"},
                  {"texte": "l'ARN est fabriqué dans le noyau, puis passe dans le cytoplasme", "mot": "on en déduit"}],
       "pointage": [{"mot": "كل نقطة كحلة", "commande": "set_time", "parametres": {"time_s": 5.5}},
                    {"mot": "كاينين ف le noyau", "commande": "play_until", "parametres": {"moment": "noyau_marque"}},
                    {"mot": "كاينين ف le noyau", "repere": "grains_noyau"},
                    {"mot": "كاينين ف le noyau", "cible": "centre:0"},
                    {"mot": "كيخرج من les pores", "commande": "play_until", "parametres": {"moment": "arn_sort_pores"}},
                    {"mot": "كيخرج من les pores", "repere": "pore"},
                    {"mot": "le cytoplasme ولا فيه النقط الكحلين", "commande": "play_until", "parametres": {"moment": "cytoplasme_marque"}},
                    {"mot": "و le noyau نقصات فيه la radioactivité", "cible": "centre:1"},
                    {"mot": "on en déduit", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                    {"mot": "on en déduit", "cible": "centre:2"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la leucine marque les ribosomes",
     "screen_content": {"lead": "Leucine radioactive : grains sur les ribosomes du cytoplasme, noyau non marqué."},
     "visual": {"kind": "simulation", "url": ACI, "caption": "Leucine radioactive : où sont les grains ?"},
     "speech_text": {"mixed": "هاد المرة، كنعطيو la leucine radioactive، وهي un acide aminé: منها كيتصاوبو les protéines. فين كيبانو النقط الكحلين؟ ف le cytoplasme، ف les ribosomes. أما le noyau، ما فيه والو. on en déduit que les protéines كيتصاوبو ف le cytoplasme، ف les ribosomes."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "noyau : pas de radioactivité", "mot": "ما فيه والو"},
                  {"texte": "cytoplasme : grains sur les ribosomes", "mot": "ف le cytoplasme، ف les ribosomes"},
                  {"texte": "protéines synthétisées sur les ribosomes", "mot": "on en déduit"}],
       "pointage": [{"mot": "كنعطيو la leucine radioactive", "commande": "play_until", "parametres": {"moment": "acides_amines_apportes"}},
                    {"mot": "ف le cytoplasme، ف les ribosomes", "commande": "play_until", "parametres": {"moment": "ribosomes_marques"}},
                    {"mot": "ف le cytoplasme، ف les ribosomes", "repere": "grains_ribosomes"},
                    {"mot": "ف le cytoplasme، ف les ribosomes", "cible": "centre:1"},
                    {"mot": "ما فيه والو", "cible": "centre:0"},
                    {"mot": "on en déduit", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                    {"mot": "on en déduit", "cible": "centre:2"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le livre reste, la photocopie sort",
     "screen_content": {"lead": "L'ADN reste dans le noyau ; une copie, l'ARNm, porte l'information aux ribosomes."},
     "visual": {"kind": "simulation", "url": URA, "caption": "Comment l'information passe-t-elle du noyau aux ribosomes ?"},
     "speech_text": {"mixed": "l'A D N ف le noyau، و les protéines كيتصاوبو ف le cytoplasme. كيفاش كتدوز l'information؟ فكر ف واحد le livre ف la bibliothèque: ما كيخرجش، ولكن كنخرجو une photocopie. l'A D N هو le livre، كيبقى ف le noyau. و la photocopie هي l'A R N messager: كيتصاوب ف le noyau، كيخرج من les pores، وكيهز l'information ل les ribosomes. هادي هي l'hypothèse: l'A R N messager هو l'intermédiaire."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ADN = livre : reste dans le noyau", "mot": "l'A D N هو le livre"},
                  {"texte": "ARNm = photocopie : sort par les pores vers les ribosomes", "mot": "و la photocopie هي l'A R N messager"},
                  {"texte": "hypothèse : l'ARNm est l'intermédiaire ADN → protéine", "mot": "هادي هي l'hypothèse"}],
       "pointage": [{"mot": "كيفاش كتدوز l'information؟", "commande": "play_until", "parametres": {"moment": "question"}},
                    {"mot": "une photocopie", "commande": "play_until", "parametres": {"moment": "photocopie"}},
                    {"mot": "l'A D N هو le livre", "repere": "adn"},
                    {"mot": "l'A D N هو le livre", "cible": "centre:0"},
                    {"mot": "كيخرج من les pores", "commande": "play_until", "parametres": {"moment": "arn_sort_pores"}},
                    {"mot": "و la photocopie هي l'A R N messager", "cible": "centre:1"},
                    {"mot": "هادي هي l'hypothèse", "cible": "centre:2"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : transcription dans le noyau, traduction dans le cytoplasme",
     "screen_content": {"lead": "ADN → (transcription, noyau) → ARNm → (traduction, cytoplasme) → protéine."},
     "visual": {"kind": "simulation", "url": BILAN, "caption": "Du gène à la protéine, dans la cellule"},
     "speech_text": {"mixed": "هادا le gène، ف l'A D N، ف le noyau. المرحلة اللولة هي la transcription: كتصاوب l'A R N messager، ف le noyau. l'A R N messager كيخرج من un pore. المرحلة الثانية هي la traduction: ف le cytoplasme، les ribosomes كيقراو l'A R N messager، وكيصاوبو la protéine."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "transcription : ADN → ARNm, dans le noyau", "mot": "المرحلة اللولة هي la transcription"},
                  {"texte": "traduction : ARNm → protéine, dans le cytoplasme (ribosomes)", "mot": "المرحلة الثانية هي la traduction"}],
       "pointage": [{"mot": "هادا le gène", "commande": "play_until", "parametres": {"moment": "gene"}},
                    {"mot": "المرحلة اللولة هي la transcription", "commande": "play_until", "parametres": {"moment": "transcription"}},
                    {"mot": "المرحلة اللولة هي la transcription", "cible": "centre:0"},
                    {"mot": "كيخرج من un pore", "commande": "play_until", "parametres": {"moment": "pore"}},
                    {"mot": "المرحلة الثانية هي la traduction", "commande": "play_until", "parametres": {"moment": "traduction"}},
                    {"mot": "المرحلة الثانية هي la traduction", "cible": "centre:1"},
                    {"mot": "وكيصاوبو la protéine", "commande": "play_until", "parametres": {"moment": "proteine"}}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : le choix de l'uracile", "نتمرنو بسؤال ساهل على l'uracile.",
      "On utilise de l'uracile radioactif parce que…", ["l'uracile est un acide aminé des protéines", "l'uracile est une base propre à l'ARN", "l'uracile est une base présente dans l'ADN et dans l'ARN"], 1, {
        "1": {"juste": rep("برافو! l'uracile كاينة غير ف l'A R N: إذن la radioactivité كتكون غير ف l'A R N.", "Juste : base propre à l'ARN, elle ne marque que l'ARN.")},
        "0": {"1": rep("لا، l'uracile ماشي acide aminé، هي base. فين كاينة هاد la base؟ عاود اختار.", "L'uracile n'est pas un acide aminé, c'est une base. Dans quelle molécule ? Réessaie."),
              "2": rep("الجواب: l'uracile هي base كاينة غير ف l'A R N. l'acide aminé ف التجربة هو la leucine.", "Réponse : l'uracile est une base propre à l'ARN ; l'acide aminé de l'expérience 2 est la leucine.")},
        "2": {"1": rep("قريب! ولكن l'A D N فيه la thymine، ماشي l'uracile. عاود اختار.", "Presque : l'ADN contient la thymine, pas l'uracile. Réessaie."),
              "2": rep("الجواب: l'uracile كاينة غير ف l'A R N. يلا كانت حتى ف l'A D N، ما نعرفوش شمن molécule فيها la radioactivité.", "Réponse : base propre à l'ARN ; si elle était aussi dans l'ADN, on ne saurait pas quelle molécule est marquée.")}},
      "علاش كنستعملو l'uracile radioactif؟"),
    vrai_faux("fa_s2", "Plus facile : lire le document 1", "Vrai ou faux : lis les deux courbes du document 1.",
      "سؤال ساهل: قرا les deux courbes، وقول صحيح ولا خطأ.", [
        (f"À {A.tm} min, la radioactivité est dans le noyau et le cytoplasme n'est pas radioactif.", True, f"Vrai : à {A.tm} min, noyau {fv(A.pic)} u.a., cytoplasme 0."),
        ("Le cytoplasme est radioactif dès le début de l'expérience.", False, f"Faux : il reste à 0 jusqu'à {A.ts} min."),
        (f"Après {A.ts} min, la radioactivité du noyau diminue pendant que celle du cytoplasme augmente.", True, f"Vrai : noyau de {fv(A.pic)} à {fv(A.noyau(30))} u.a., cytoplasme de 0 à {fv(A.cyto(30))} u.a."),
        ("On en déduit que l'ARN est fabriqué dans le cytoplasme.", False, "Faux : il est d'abord dans le noyau : il y est fabriqué, puis il passe dans le cytoplasme.")]),
    qcm_facile("fa_s3", "Plus facile : où sont fabriquées les protéines ?", "سؤال ساهل على la leucine.",
      "Avec la leucine radioactive, la radioactivité est seulement dans le cytoplasme. Les protéines sont donc fabriquées…", ["dans le noyau", "dans les pores du noyau", "dans le cytoplasme, sur les ribosomes"], 2, {
        "2": {"juste": rep("برافو! la radioactivité ف les ribosomes: تما كيتصاوبو les protéines.", "Juste : dans le cytoplasme, sur les ribosomes.")},
        "0": {"1": rep("لا، le noyau ما فيه حتى radioactivité ف le document deux. فين كاينة؟ عاود اختار.", "Le noyau n'est pas radioactif dans le document 2. Où est la radioactivité ? Réessaie."),
              "2": rep("الجواب هو ف le cytoplasme، ف les ribosomes: le noyau بقا à zéro.", "Réponse : dans le cytoplasme, sur les ribosomes (noyau à 0).")},
        "1": {"1": rep("لا، les pores غير كيدوز منهم l'A R N. la leucine فين كاينة؟ عاود اختار.", "Les pores laissent seulement passer l'ARN. Où est la leucine ? Réessaie."),
              "2": rep("الجواب هو ف le cytoplasme، ف les ribosomes. les pores غير طريق.", "Réponse : dans le cytoplasme, sur les ribosomes ; les pores ne sont qu'un passage.")}},
      "les protéines فين كيتصاوبو؟"),
    qcm_facile("fa_s4", "Plus facile : l'hypothèse", "سؤال ساهل: اختار l'hypothèse الصحيحة.",
      "L'ADN reste dans le noyau. Comment l'information arrive-t-elle aux ribosomes ?", ["L'ADN sort du noyau par les pores.", "Les ribosomes entrent dans le noyau pour lire l'ADN.", "Une copie en ARN, l'ARNm, sort du noyau et porte l'information aux ribosomes."], 2, {
        "2": {"juste": rep("برافو! l'A R N messager هو la photocopie: كيخرج، وكيهز l'information ل les ribosomes.", "Juste : l'ARNm, copie de l'information, sort du noyau et va aux ribosomes.")},
        "0": {"1": rep("لا، l'A D N عمرو ما كيخرج من le noyau. شنو اللي كيخرج ف البلاصة ديالو؟ عاود اختار.", "L'ADN ne quitte jamais le noyau. Qu'est-ce qui sort à sa place ? Réessaie."),
              "2": rep("الجواب: l'A R N messager هو اللي كيخرج. l'A D N كيبقى ف le noyau، بحال le livre ف la bibliothèque.", "Réponse : c'est l'ARNm qui sort ; l'ADN reste dans le noyau.")},
        "1": {"1": rep("لا، les ribosomes كيبقاو ف le cytoplasme: la leucine ما عطات حتى radioactivité ف le noyau. عاود اختار.", "Les ribosomes restent dans le cytoplasme (noyau non marqué par la leucine). Réessaie."),
              "2": rep("الجواب: l'A R N messager كيخرج من le noyau، وكيمشي ل les ribosomes.", "Réponse : l'ARNm sort du noyau et va aux ribosomes.")}},
      "كيفاش كتوصل l'information ل les ribosomes؟"),
    association("fa_s5", "Plus facile : deux étapes, deux lieux", "Relie chaque étape à ce qu'elle fait et où.",
      "سؤال ساهل: ربط كل مرحلة مع شنو كتدير و فين.", "Relie chaque étape de l'expression de l'information génétique à sa description.",
      [("1", "Transcription"), ("2", "Traduction")],
      [("a", "Dans le noyau : ADN → ARNm"), ("b", "Dans le cytoplasme, sur les ribosomes : ARNm → protéine"), ("c", "Dans le noyau : copie des deux brins de l'ADN")],
      {"1": "a", "2": "b"},
      {"1-a": (True, "Oui : la transcription fabrique l'ARNm à partir de l'ADN, dans le noyau.", "برافو: la transcription كتصاوب l'A R N messager من l'A D N، ف le noyau."),
       "1-b": (False, "Fabriquer une protéine sur les ribosomes, c'est la traduction.", "لا، تصاوب la protéine ف les ribosomes هي la traduction."),
       "1-c": (False, "Copier les deux brins de l'ADN, c'est la réplication, pas la transcription.", "لا، نسخ les deux brins ديال l'A D N هي la réplication."),
       "2-a": (False, "Fabriquer l'ARNm dans le noyau, c'est la transcription.", "لا، تصاوب l'A R N messager ف le noyau هي la transcription."),
       "2-b": (True, "Oui : la traduction fabrique la protéine à partir de l'ARNm, sur les ribosomes.", "برافو: la traduction كتصاوب la protéine من l'A R N messager، ف les ribosomes."),
       "2-c": (False, "La traduction se fait dans le cytoplasme et donne une protéine, pas de l'ADN.", "لا، la traduction ف le cytoplasme، وكتعطي la protéine، ماشي l'A D N.")},
      ("(1 ; a) (2 ; b) : transcription dans le noyau, traduction sur les ribosomes du cytoplasme. La copie des deux brins est la réplication.",
       "la transcription ف le noyau، و la traduction ف les ribosomes ديال le cytoplasme. أما نسخ les deux brins، هي la réplication."))
  ]}]},
  "similaire": {
    "id": "svt_ex_ch4_marquage_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": intro(B, "cellules de pancréas"),
      "intro_dit": "نفس التمرين، ب des cellules ديال le pancréas وقيم أخرى. l'expérience un: l'uracile radioactif pendant cinq minutes، ومن بعد milieu non radioactif: le document un. l'expérience deux: la leucine radioactive: le document deux.",
      "figures": [fig_courbe(B, "Document 1 : radioactivité du noyau et du cytoplasme (uracile radioactif)"),
                  fig_tableau(TAB_B, "Document 2 : répartition de la radioactivité (leucine radioactive)")],
      "donnees": ["u.a. : unité arbitraire", f"Expérience 1 : uracile radioactif de 0 à {B.tm} min, puis milieu non radioactif",
                  "Expérience 2 : leucine radioactive (acide aminé), mesures à 5 min et à 30 min"],
      "questions": [
        {"id": "1", "texte": Q1_T, "reponse": {"type": "phrase", "attendu": ATT1}, "clavier": CLAV1, "correction": CORR1},
        {"id": "2", "texte": Q2_T, "reponse": {"type": "phrase", "attendu": att2(B)},
         "clavier": {"aides": ["augmente", "reste constante", "diminue", "u.a.", "On en déduit que"], "pieges": ["l'ARN est synthétisé dans le cytoplasme"]}, "correction": corr2(B)},
        {"id": "3", "texte": Q3_T, "reponse": {"type": "phrase", "attendu": att3(TAB_B)},
         "clavier": {"aides": ["nulle dans le noyau", "ribosomes", "On en déduit que"], "pieges": ["protéines synthétisées dans le noyau"]}, "correction": corr3(TAB_B)},
        {"id": "4", "texte": Q4_T, "reponse": {"type": "phrase", "attendu": ATT4}, "clavier": CLAV4, "correction": CORR4},
        {"id": "5", "texte": Q5_T, "reponse": {"type": "phrase", "attendu": ATT5}, "clavier": CLAV5, "correction": CORR5}
      ]}}
}
ecrire(EX, sys.argv[1])
