# Exercice SVT ch. 3 (notion de l'information génétique), niveau moyen : composition en bases de l'ADN de quatre espèces
# (données inventées, réalistes), rapports A/T et C/G, (A + G)/(T + C), pourcentage manquant, brin complémentaire,
# structure de l'ADN.
# Entraîne : calculer des rapports, « Décrire… puis déduire » (une ligne de valeurs, « On en déduit que »), la
# complémentarité A–T / C–G, le calcul d'un pourcentage par complémentarité (sans oublier T), l'écriture tête-bêche du
# brin complémentaire (extrémités 5' et 3' d'abord), la double hélice à brins antiparallèles et liaisons hydrogène.
# Les rapports sont écrits A/T et C/G comme dans le cours et la simulation adn.html (vue chargaff).
# Sources comparées (lues, rien copié) :
# - exploration notion_information_genetique.json : cas_types « chargaff » (calculer A/T, C/G, (A+G)/(C+T), constater ≈ 1,
#   déduire la complémentarité ; contrôles, pas au national PC 2016-2025) ; pieges (brin complémentaire écrit dans le
#   même sens ; A avec G) ; insistances (A–T deux liaisons, C–G trois ; brins antiparallèles) ; valeurs_reperes (Chargaff
#   homme) ; a_ne_pas_dire (pas de numéros de carbone, pas d'histones comptées).
# - nationaux PC : aucun calcul de Chargaff 2016-2025 ; 2018 R QCM (chromatide = deux brins d'ADN), 2019 N (écriture d'une
#   séquence complémentaire, chapitre suivant) : formes d'écriture des séquences reprises.
# - séries en ligne (recherche du 22/11/2026 : dyrassa « Notion de l'information génétique, série d'exercices » (quantité
#   d'ADN et bases chez plusieurs espèces), dreamjob.ma « notion information génétique, exercices corrigés » (règle de
#   Chargaff, pourcentage manquant), TD universitaires de Guelma et M'sila (rapports A/T, C/G)) : titres et résumés
#   seulement, le réseau du conteneur refuse ces sites. Le tableau, les espèces et les nombres sont écrits ici.
import sys
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

ADN = "/media/simulations/svt/notion_information_genetique-tableau/adn.html"
COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}


def fr(x, n=1):
    return f"{x:.{n}f}".replace(".", ",")


def comp(seq):
    return "".join(COMP[b] for b in seq)


def tableau(especes, titre):
    """Tableau dessiné : Espèce | % A | % T | % G | % C."""
    n = len(especes); h = 0.9; H = h * (n + 1); xs = [0, 3.0, 4.75, 6.5, 8.25, 10]
    el = [{"f": "rect", "de": [0, 0], "a": [10, H], "couleur": "blanc"}]
    for x in xs[1:-1]:
        el.append({"f": "ligne", "pts": [[x, 0], [x, H]], "couleur": "faible"})
    for i in range(1, n + 1):
        el.append({"f": "ligne", "pts": [[0, round(H - i * h, 3)], [10, round(H - i * h, 3)]], "couleur": "blanc" if i == 1 else "faible"})
    entetes = ["Espèce", "% A", "% T", "% G", "% C"]; coul = [None, "rouge", "jaune", "vert", "bleu"]
    for j, t in enumerate(entetes):
        e = {"f": "texte", "at": [round((xs[j] + xs[j + 1]) / 2, 3), round(H - h / 2, 3)], "t": t}
        if coul[j]: e["couleur"] = coul[j]
        el.append(e)
    for i, (nom, *v) in enumerate(especes):
        y = round(H - (i + 1.5) * h, 3)
        el.append({"f": "texte", "at": [1.5, y], "t": nom})
        for j, val in enumerate(v):
            el.append({"f": "texte", "at": [round((xs[j + 1] + xs[j + 2]) / 2, 3), y], "t": fr(val)})
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": round(H, 3)},
            "legende": "Pourcentage de chaque base azotée parmi toutes les bases de l'ADN extrait (A : adénine, T : thymine, G : guanine, C : cytosine).",
            "elements": el}


def rapports(especes):
    out = []
    for nom, a, t, g, c in especes:
        assert abs(a + t + g + c - 100) < 1e-9, nom
        out.append((nom, fr(a / t, 2), fr(c / g, 2), a, t, g, c))
    return out


# ── Données (inventées, réalistes) ───────────────────────────────────────────────────────────────────────────────
ESP = [("Bœuf", 28.7, 28.9, 21.3, 21.1), ("Blé", 27.3, 27.1, 22.6, 23.0), ("Oursin", 32.4, 32.7, 17.6, 17.3), ("Bactérie", 24.9, 24.6, 25.1, 25.4)]
ESP_B = [("Porc", 29.4, 29.7, 20.6, 20.3), ("Maïs", 26.8, 27.2, 23.1, 22.9), ("Criquet", 29.3, 29.0, 20.5, 21.2), ("Levure", 31.6, 32.2, 18.3, 17.9)]
R, R_B = rapports(ESP), rapports(ESP_B)
assert [(r[1], r[2]) for r in R] == [("0,99", "0,99"), ("1,01", "1,02"), ("0,99", "0,98"), ("1,01", "1,01")]
assert [(r[1], r[2]) for r in R_B] == [("0,99", "0,99"), ("0,99", "0,99"), ("1,01", "1,03"), ("0,98", "0,98")]
# (A + G)/(T + C) chez le blé (similaire : le maïs)
AG, TC = 27.3 + 22.6, 27.1 + 23.0; assert (fr(AG), fr(TC), fr(AG / TC, 2)) == ("49,9", "50,1", "1,00")
AGb, TCb = 26.8 + 23.1, 27.2 + 22.9; assert (fr(AGb), fr(TCb), fr(AGb / TCb, 2)) == ("49,9", "50,1", "1,00")
# Espèce Z : A = 21 % → G = 29 % (similaire : A = 18 % → G = 32 %)
assert (100 - 2 * 21) / 2 == 29 and (100 - 2 * 18) / 2 == 32
SEQ, SEQ_B = "ACGTTGC", "TGACCTA"
assert comp(SEQ) == "TGCAACG" and comp(SEQ)[::-1] == "GCAACGT"
assert comp(SEQ_B) == "ACTGGAT" and comp(SEQ_B)[::-1] == "TAGGTCA"


def ligne_rapports(r):
    return " ; ".join(f"{nom} : A/T = {fr(a)}/{fr(t)} ≈ {at}, C/G = {fr(c)}/{fr(g)} ≈ {cg}" for nom, at, cg, a, t, g, c in r)


def assoc_bases(sid):
    gauche = [("1", "A (adénine)"), ("2", "T (thymine)"), ("3", "C (cytosine)"), ("4", "G (guanine)")]
    droite = [("a", "T"), ("b", "A"), ("c", "G"), ("d", "C")]
    couples = {"1": "a", "2": "b", "3": "c", "4": "d"}
    lettre = {"1": "A", "2": "T", "3": "C", "4": "G"}; dl = {"a": "T", "b": "A", "c": "G", "d": "C"}
    nom = {"A": "l'adénine", "T": "la thymine", "C": "la cytosine", "G": "la guanine"}
    retours = {}
    for g, _ in gauche:
        for d, _ in droite:
            x, y = lettre[g], dl[d]
            if couples[g] == d:
                nb = "deux" if x in "AT" else "trois"
                retours[f"{g}-{d}"] = (True, f"Oui : {x} en face de {y}, reliées par {nb} liaisons hydrogène.",
                                       f"برافو. {nom[x]} مقابلها {nom[y]}، avec {nb} liaisons hydrogène.")
            elif x == y:
                retours[f"{g}-{d}"] = (False, "Non : une base ne s'associe jamais à elle-même. Rappelle-toi : A–T et C–G.",
                                       f"لا. {nom[x]} ما كتجمعش مع راسها. تفكر: A مع T، و C مع G.")
            else:
                retours[f"{g}-{d}"] = (False, f"Non : {x} ne s'associe pas à {y}. Rappelle-toi : A–T et C–G.",
                                       f"لا. {nom[x]} ما كتجمعش مع {nom[y]}. تفكر: A مع T، و C مع G.")
    return association(sid, "Plus facile : les bases complémentaires", "Relie chaque base à sa base complémentaire.",
                       "سؤال ساهل: ربط كل base مع la base complémentaire ديالها.", "Relie chaque base du brin donné à la base posée en face.",
                       gauche, droite, couples, retours,
                       ("(A ; T) (T ; A) (C ; G) (G ; C) : A–T par deux liaisons hydrogène, C–G par trois.",
                        "A مقابلها T، و C مقابلها G. A و T، avec deux liaisons hydrogène. C و G، avec trois liaisons hydrogène."))


def questions(esp, r, idx_ag, ag, tc, aZ, seq, avec_tout):
    """Les six questions ; avec_tout = False pour l'exercice semblable (sans aides, explication, facile)."""
    nom_ag = esp[idx_ag][0].lower(); gZ = (100 - 2 * aZ) // 2
    amin = min(esp, key=lambda e: e[1]); amax = max(esp, key=lambda e: e[1])
    gmin = min(esp, key=lambda e: e[3]); gmax = max(esp, key=lambda e: e[3])
    qs = [
      {"id": "1", "texte": "Calculer les rapports A/T et C/G pour chaque espèce (arrondir à 0,01).",
       "reponse": {"type": "phrase", "attendu": ligne_rapports(r) + "."},
       "clavier": {"aides": ["A/T", "C/G", "≈", "0,99", "1,01"], "pieges": ["A/G", "T/A"]},
       "correction": {"lignes": [{"texte": "1 : " + ligne_rapports(r[:2]), "mot": "A sur T"},
                                 {"texte": ligne_rapports(r[2:]), "mot": "كل les rapports"}],
         "parole": "السؤال un. A sur T، هو le pourcentage ديال A، sur le pourcentage ديال T. و C sur G، هو le pourcentage ديال C، sur le pourcentage ديال G. مثلا، chez le " + ("bœuf" if avec_tout else "porc") + "، A sur T، environ zéro virgule quatre-vingt-dix-neuf. كل les rapports، entre zéro virgule quatre-vingt-dix-huit et un virgule zéro trois: كاملين environ un."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Décrire les résultats du tableau et des rapports calculés, puis déduire la relation entre les bases de l'ADN.",
       "reponse": {"type": "phrase", "attendu": f"Les pourcentages des bases varient d'une espèce à l'autre (A : de {fr(amin[1])} % chez {amin[0].lower()} à {fr(amax[1])} % chez {amax[0].lower()} ; G : de {fr(gmin[3])} % chez {gmin[0].lower()} à {fr(gmax[3])} % chez {gmax[0].lower()}). Mais chez toutes les espèces, A/T ≈ 1 et C/G ≈ 1 : % A ≈ % T et % C ≈ % G. On en déduit que, dans l'ADN, l'adénine (A) est associée à la thymine (T) et la cytosine (C) à la guanine (G) : les bases sont complémentaires (A–T, C–G)."},
       "clavier": {"aides": ["varient d'une espèce à l'autre", "A/T ≈ 1", "C/G ≈ 1", "On en déduit que", "complémentaires"], "pieges": ["A avec G", "identiques chez toutes les espèces"]},
       "correction": {"lignes": [{"texte": f"2 : les % varient selon l'espèce (A de {fr(amin[1])} à {fr(amax[1])} %)", "mot": "كيتبدلو من espèce لأخرى"},
                                 {"texte": "mais A/T ≈ 1 et C/G ≈ 1 chez toutes les espèces : % A ≈ % T, % C ≈ % G", "mot": "ديما environ un"},
                                 {"texte": "On en déduit : A s'associe à T, C s'associe à G (complémentarité des bases)", "mot": "On en déduit"}],
         "parole": f"السؤال deux. les pourcentages ديال les bases كيتبدلو من espèce لأخرى: A، de {DIT[amin[1]]} à {DIT[amax[1]]} pour cent. ولكن A sur T و C sur G، ديما environ un، عند جميع les espèces: autant de A que de T، و autant de C que de G. On en déduit: A كتجمع مع T، و C كتجمع مع G. هادي la complémentarité des bases."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": f"Montrer que, chez le {nom_ag}, le rapport (A + G)/(T + C) est voisin de 1.",
       "reponse": {"type": "valeur", "grandeur": "(A + G)/(T + C)", "valeur": 1.0, "unite": "", "tolerance": 0.02,
                   "attendu": f"(A + G)/(T + C) = ({fr(esp[idx_ag][1])} + {fr(esp[idx_ag][3])})/({fr(esp[idx_ag][2])} + {fr(esp[idx_ag][4])}) = {fr(ag)}/{fr(tc)} ≈ {fr(ag / tc, 2)}"},
       "clavier": {"aides": ["A + G", "T + C", "≈ 1"], "pieges": ["(A + T)/(G + C)"]},
       "correction": {"lignes": [{"texte": f"3 : A + G = {fr(esp[idx_ag][1])} + {fr(esp[idx_ag][3])} = {fr(ag)} ; T + C = {fr(esp[idx_ag][2])} + {fr(esp[idx_ag][4])} = {fr(tc)}", "mot": f"A plus G، égale {DIT[ag]}"},
                                 {"texte": f"(A + G)/(T + C) = {fr(ag)}/{fr(tc)} ≈ {fr(ag / tc, 2)} ≈ 1", "mot": "environ un"}],
         "parole": f"السؤال trois. chez le {nom_ag}، A plus G، égale {DIT[ag]}. T plus C، égale {DIT[tc]}. A plus G، sur T plus C، égale {DIT[ag]} sur {DIT[tc]}، environ un. وهادا منطقي: حيت A égale T، و G égale C."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": f"Chez une espèce Z, l'adénine représente {aZ} % des bases de l'ADN. Calculer le pourcentage de guanine.",
       "reponse": {"type": "valeur", "grandeur": "% G", "valeur": gZ, "unite": "%", "tolerance": 0.02,
                   "attendu": f"T = A = {aZ} % ; G + C = 100 − ({aZ} + {aZ}) = {100 - 2 * aZ} % ; G = C = {100 - 2 * aZ}/2 = {gZ} %"},
       "clavier": {"aides": ["T = A", "G = C", "100 −", "/2", "%"], "pieges": [f"{100 - aZ} %", f"{100 - 2 * aZ} %"]},
       "correction": {"lignes": [{"texte": f"4 : T = A = {aZ} %", "mot": "T égale A"},
                                 {"texte": f"G + C = 100 − ({aZ} + {aZ}) = {100 - 2 * aZ} %", "mot": "G plus C، égale cent moins"},
                                 {"texte": f"G = C = {100 - 2 * aZ}/2 = {gZ} %", "mot": f"G égale {DIT[gZ]} pour cent"}],
         "parole": f"السؤال quatre. T égale A، {DIT[aZ]} pour cent. G plus C، égale cent moins {DIT[2 * aZ]}، égale {DIT[100 - 2 * aZ]} pour cent. وحيت G égale C، G égale {DIT[gZ]} pour cent."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": f"Un fragment de l'un des deux brins de l'ADN a la séquence : 5' {seq} 3'. Écrire la séquence du brin complémentaire, en précisant ses extrémités.",
       "reponse": {"type": "phrase", "attendu": f"Brin complémentaire : 3' {comp(seq)} 5' (lu de 5' vers 3' : 5' {comp(seq)[::-1]} 3')."},
       "clavier": {"aides": ["3'", "5'", "A", "T", "C", "G"], "pieges": [f"5' {comp(seq)} 3'"]},
       "correction": {"lignes": [{"texte": f"5 : brin donné : 5' {seq} 3'", "mot": "le brin donné"},
                                 {"texte": f"brin complémentaire : 3' {comp(seq)} 5'", "mot": "trois prime، " + " ".join(comp(seq))}],
         "parole": f"السؤال cinq. le brin donné: cinq prime، {' '.join(seq)}، trois prime. مقابل كل A، T. مقابل كل C، G. وle brin complémentaire كيبدا par trois prime: trois prime، {' '.join(comp(seq))}، cinq prime."},
       "explication": "ex_s5", "facile": "fa_s5"},
      {"id": "6", "texte": "En exploitant les résultats précédents, décrire la structure de la molécule d'ADN.",
       "reponse": {"type": "phrase", "attendu": "La molécule d'ADN est formée de deux brins de nucléotides enroulés en double hélice. Les deux brins sont antiparallèles (5'→3' en face de 3'→5'). Les bases des deux brins sont complémentaires : A en face de T (deux liaisons hydrogène), C en face de G (trois liaisons hydrogène). C'est pourquoi % A = % T et % C = % G dans l'ADN."},
       "clavier": {"aides": ["deux brins", "double hélice", "antiparallèles", "liaisons hydrogène", "A–T", "C–G"], "pieges": ["un seul brin", "même sens"]},
       "correction": {"lignes": [{"texte": "6 : deux brins de nucléotides en double hélice", "mot": "deux brins de nucléotides"},
                                 {"texte": "brins antiparallèles (5'→3' en face de 3'→5')", "mot": "antiparallèles"},
                                 {"texte": "A–T (deux liaisons hydrogène), C–G (trois liaisons hydrogène) : d'où % A = % T, % C = % G", "mot": "avec trois liaisons hydrogène"}],
         "parole": "السؤال six. l'A D N: deux brins de nucléotides، ملويين على بعضهم: la double hélice. les deux brins antiparallèles: cinq prime مقابل trois prime. les bases complémentaires: A en face de T، avec deux liaisons hydrogène. C en face de G، avec trois liaisons hydrogène. هادشي علاش autant de A que de T، و autant de C que de G."},
       "explication": "ex_s6", "facile": "fa_s6"}]
    if not avec_tout:
        for q in qs:
            for k in ("explication", "facile"): q.pop(k)
    return qs


DIT = {24.9: "vingt-quatre virgule neuf", 32.4: "trente-deux virgule quatre", 26.8: "vingt-six virgule huit", 31.6: "trente et un virgule six",
       49.9: "quarante-neuf virgule neuf", 50.1: "cinquante virgule un", 21: "vingt et un", 42: "quarante-deux", 58: "cinquante-huit",
       29: "vingt-neuf", 18: "dix-huit", 36: "trente-six", 64: "soixante-quatre", 32: "trente-deux"}
DIT[AG] = DIT[49.9]; DIT[TC] = DIT[50.1]; DIT[AGb] = DIT[49.9]; DIT[TCb] = DIT[50.1]

QS = questions(ESP, R, 1, AG, TC, 21, SEQ, True)
TD = {
  "1": ("السؤال un: حسب les rapports A sur T، و C sur G، عند كل espèce.",
        [("Le rapport A/T, c'est le pourcentage de A divisé par le pourcentage de T, lus sur la même ligne du tableau.",
          "A sur T، هو le pourcentage ديال A، sur le pourcentage ديال T، فنفس السطر ديال le tableau."),
         ("Exemple de méthode : A/T = % A / % T, puis arrondis à deux chiffres après la virgule ; fais de même pour C/G.",
          "قسم، ومن بعد قرب لزوج ديال الأرقام من بعد la virgule. ودير نفس الشي ل C sur G.")]),
  "2": ("السؤال deux: وصف les résultats ديال le tableau وles rapports، ومن بعد استنتج la relation بين les bases.",
        [("Compare d'abord les pourcentages d'une espèce à l'autre, puis compare les rapports calculés : que remarques-tu ?",
          "قارن الأول les pourcentages من espèce لأخرى، ومن بعد قارن les rapports. شنو لاحظتي؟"),
         ("Décris avec des valeurs (« varient de … à … », « A/T ≈ … »), puis écris « On en déduit que… » : quelles bases sont en quantités égales ?",
          "وصف بles valeurs، ومن بعد كتب: On en déduit que. شمن les bases عندهم نفس الكمية؟")]),
  "3": ("السؤال trois: بين أن chez le blé، le rapport A plus G، sur T plus C، قريب بزاف من un.",
        [("Lis les quatre pourcentages du blé dans le tableau.", "قرا les quatre pourcentages ديال le blé فle tableau."),
         ("Calcule A + G, puis T + C, puis divise le premier résultat par le second.", "حسب A plus G، ومن بعد T plus C، ومن بعد قسم الأول على الثاني.")]),
  "4": ("السؤال quatre: عند واحد l'espèce Z، l'adénine هي vingt et un pour cent ديال les bases. حسب le pourcentage ديال la guanine.",
        [("Utilise la complémentarité trouvée à la question 2 : quelle base a le même pourcentage que A ? et que G ?",
          "خدم بla complémentarité ديال السؤال deux: شمن base عندها نفس le pourcentage ديال A؟ وديال G؟"),
         ("Les quatre bases font 100 % : retire A et T, puis partage ce qui reste entre G et C, qui sont égales.",
          "les quatre bases كيعطيو cent pour cent. حيد A و T، ومن بعد قسم الباقي par deux، حيت G égale C.")]),
  "5": ("السؤال cinq: كتب le brin complémentaire ديال cinq prime، A C G T T G C، trois prime، وحدد les extrémités ديالو.",
        [("En face de chaque base, pose sa base complémentaire : A en face de T, C en face de G.",
          "مقابل كل base، حط la base complémentaire ديالها: A مقابل T، و C مقابل G."),
         ("Les brins sont antiparallèles : écris d'abord les extrémités, 3' à gauche sous le 5' du brin donné.",
          "les brins antiparallèles: كتب الأول les extrémités. trois prime على اليسار، تحت cinq prime ديال le brin donné.")]),
  "6": ("السؤال six: استغل الأجوبة اللي فاتو، ووصف la structure ديال la molécule d'A D N.",
        [("Combien de brins ? Dans quel sens est chaque brin ? Comment sont reliées les bases d'en face ?",
          "شحال من brin؟ كيفاش موجه كل brin؟ وكيفاش مربوطين les bases اللي مقابلين بعضهم؟"),
         ("Pense aux mots du cours : nucléotides, double hélice, antiparallèles, complémentaires, liaisons hydrogène (deux ou trois).",
          "تفكر الكلمات ديال le cours: nucléotides، double hélice، antiparallèles، complémentaires، liaisons hydrogène.")]),
}
for q in QS:
    td, aides = TD[q["id"]]
    q["texte_dit"] = td
    q["aides"] = [{"texte": t, "dit": d} for t, d in aides]
# ordre des champs comme les pilotes
QS = [{k: q[k] for k in ("id", "texte", "texte_dit", "reponse", "clavier", "aides", "correction", "explication", "facile")} for q in QS]

QS_B = questions(ESP_B, R_B, 1, AGb, TCb, 18, SEQ_B, False)

EX = {
  "id": "svt_ex_ch3_bases_adn_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "La composition en bases de l'ADN et sa structure", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer et exploiter les rapports de bases (Chargaff)", "Déduire la complémentarité des bases",
                  "Calculer un pourcentage de base par complémentarité", "Écrire un brin complémentaire avec ses extrémités",
                  "Décrire la structure de l'ADN"],
  "enonce": {
    "intro": "On extrait l'ADN des cellules de quatre espèces, puis on détermine le pourcentage de chacune des quatre bases azotées (adénine A, thymine T, guanine G, cytosine C) parmi toutes les bases de cet ADN. Le tableau présente les résultats.",
    "intro_dit": "دابا نقراو l'énoncé. خرجنا l'A D N من les cellules ديال quatre espèces. ومن بعد حسبنا le pourcentage ديال كل base azotée: l'adénine، la thymine، la guanine و la cytosine. le tableau فيه les résultats.",
    "figures": [tableau(ESP, "Composition en bases de l'ADN de quatre espèces (en %)")],
    "donnees": ["Pourcentages en % du nombre total de bases de l'ADN", "Arrondir les rapports à 0,01",
                "Bases azotées : adénine (A), thymine (T), guanine (G), cytosine (C)"],
    "questions": QS
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : calculer A/T et C/G",
     "screen_content": {"lead": "A/T = % A / % T ; C/G = % C / % G, sur la même ligne du tableau."},
     "visual": {"kind": "simulation", "url": ADN + "?vue=chargaff", "caption": "On compte les bases de l'ADN, puis on calcule les rapports"},
     "speech_text": {"mixed": "Chargaff حسب les pourcentages ديال les bases فl'A D N. مثلا عند l'homme: A trente virgule neuf pour cent، T vingt-neuf virgule quatre pour cent. شوف: les bocaux ديال A و T طالعين لنفس المستوى. A sur T: trente virgule neuf sur vingt-neuf virgule quatre، environ un virgule zéro cinq. و C sur G: dix-neuf virgule huit sur dix-neuf virgule neuf، environ zéro virgule quatre-vingt-dix-neuf. فl'exercice ديالك، دير نفس القسمة لكل espèce."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "A/T = % A / % T", "mot": "A sur T: trente"}, {"texte": "C/G = % C / % G", "mot": "و C sur G"}],
       "pointage": [{"mot": "Chargaff حسب", "commande": "play_until", "parametres": {"moment": "homme"}},
                    {"mot": "مثلا عند l'homme", "repere": "tube_homme"},
                    {"mot": "les bocaux ديال A و T", "repere": "paire_at"},
                    {"mot": "A sur T: trente", "commande": "play_until", "parametres": {"moment": "rapport_at"}},
                    {"mot": "A sur T: trente", "repere": "rapport_at"},
                    {"mot": "A sur T: trente", "cible": "centre:0"},
                    {"mot": "و C sur G", "commande": "play_until", "parametres": {"moment": "rapport_cg"}},
                    {"mot": "و C sur G", "repere": "rapport_cg"},
                    {"mot": "و C sur G", "cible": "centre:1"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : décrire, puis déduire la complémentarité",
     "screen_content": {"lead": "Les % varient selon l'espèce, mais A/T ≈ 1 et C/G ≈ 1 : A s'associe à T, C à G."},
     "visual": {"kind": "simulation", "url": ADN + "?vue=chargaff&diapo=ex_deduire", "caption": "Le tableau de Chargaff et sa conclusion"},
     "speech_text": {"mixed": "عند le mouton و le poulet، نفس الشي: A قريبة بزاف من T، و G قريبة من C. شوف le tableau: les pourcentages كيتبدلو من espèce لأخرى. ولكن A sur T ديما environ un، و C sur G ديما environ un. يعني autant de A que de T، و autant de C que de G. On en déduit: A كتجمع مع T، و C كتجمع مع G. هادي la complémentarité des bases."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "les % varient d'une espèce à l'autre", "mot": "كيتبدلو من espèce لأخرى"}, {"texte": "A/T ≈ 1 et C/G ≈ 1 → A–T, C–G", "mot": "On en déduit"}],
       "pointage": [{"mot": "عند le mouton", "commande": "set_time", "parametres": {"time_s": 15.0}},
                    {"mot": "عند le mouton", "commande": "play_until", "parametres": {"moment": "especes"}},
                    {"mot": "شوف le tableau", "commande": "play_until", "parametres": {"moment": "tableau"}},
                    {"mot": "شوف le tableau", "repere": "tableau"},
                    {"mot": "كيتبدلو من espèce لأخرى", "cible": "centre:0"},
                    {"mot": "A sur T ديما", "repere": "colonne_at"},
                    {"mot": "C sur G ديما", "repere": "colonne_cg"},
                    {"mot": "On en déduit", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                    {"mot": "On en déduit", "repere": "conclusion"},
                    {"mot": "On en déduit", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : si A = T et G = C, alors A + G = T + C",
     "screen_content": {"lead": "(A + G)/(T + C) ≈ 1 chez toutes les espèces."},
     "visual": {"kind": "simulation", "url": ADN + "?vue=chargaff&diapo=ex_somme", "caption": "La conclusion de Chargaff"},
     "speech_text": {"mixed": "شوف la conclusion: autant de A que de T، و autant de C que de G. يلا A égale T، و G égale C، إذن A plus G égale T plus C. يعني le rapport A plus G، sur T plus C، كيكون environ un، عند جميع les espèces. فl'exercice، جمع A و G ديال le blé، ومن بعد قسم على T plus C."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "A = T et G = C → A + G = T + C", "mot": "إذن A plus G égale T plus C"}, {"texte": "(A + G)/(T + C) ≈ 1", "mot": "كيكون environ un"}],
       "pointage": [{"mot": "شوف la conclusion", "commande": "set_time", "parametres": {"time_s": 20.4}},
                    {"mot": "شوف la conclusion", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                    {"mot": "شوف la conclusion", "repere": "conclusion"},
                    {"mot": "إذن A plus G égale T plus C", "cible": "centre:0"},
                    {"mot": "كيكون environ un", "repere": "tableau"},
                    {"mot": "كيكون environ un", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : un pourcentage manquant, par complémentarité",
     "screen_content": {"lead": "T = A ; G + C = 100 − (A + T) ; G = C = (G + C)/2."},
     "visual": {"kind": "simulation", "url": ADN + "?vue=construire&diapo=ex_pourcentage", "caption": "Les deux brins : A en face de T, C en face de G"},
     "speech_text": {"mixed": "فl'A D N، كل A مقابلها T، وكل G مقابلها C. إذن le pourcentage ديال T، هو نفس le pourcentage ديال A. هادي الخطوة الأولى: T égale A. والباقي: G plus C، égale cent moins A moins T. وحيت G égale C، كنقسمو هاد الباقي par deux. ما تنساش T، حيت بزاف ديال التلاميذ كيحيدو غير A."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "T = A", "mot": "T égale A"}, {"texte": "G + C = 100 − (A + T)", "mot": "G plus C، égale cent moins A moins T"}, {"texte": "G = C = (G + C)/2", "mot": "كنقسمو هاد الباقي par deux"}],
       "pointage": [{"mot": "كل A مقابلها T", "commande": "set_time", "parametres": {"time_s": 14.8}},
                    {"mot": "كل A مقابلها T", "commande": "play_until", "parametres": {"moment": "appariement"}},
                    {"mot": "كل A مقابلها T", "repere": "paire_at"},
                    {"mot": "وكل G مقابلها C", "repere": "paire_cg"},
                    {"mot": "T égale A", "cible": "centre:0"},
                    {"mot": "G plus C، égale cent moins A moins T", "cible": "centre:1"},
                    {"mot": "كنقسمو هاد الباقي par deux", "cible": "centre:2"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : le brin complémentaire, tête-bêche",
     "screen_content": {"lead": f"5' {SEQ} 3' → 3' {comp(SEQ)} 5'."},
     "visual": {"kind": "simulation", "url": ADN + "?vue=complementaire", "caption": "On pose en face de chaque base sa base complémentaire"},
     "speech_text": {"mixed": f"هادا le brin: cinq prime، {' '.join(SEQ)}، trois prime. مقابل A، كنحطو T. مقابل C، G. مقابل G، C. مقابل T، A. ورد البال ل les extrémités: le brin complémentaire كيبدا par trois prime. إذن: trois prime، {' '.join(comp(SEQ))}، cinq prime. جوج ديال القواعد: نبدلو les bases، ونقلبو les extrémités."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": f"3' {comp(SEQ)} 5'", "mot": "إذن: trois prime"}],
       "pointage": [{"mot": "هادا le brin:", "commande": "set_parameters", "parametres": {"sequence": SEQ}},
                    {"mot": "هادا le brin:", "commande": "play_until", "parametres": {"moment": "brin_donne"}},
                    {"mot": "هادا le brin:", "repere": "brin_donne"},
                    {"mot": "مقابل A، كنحطو T", "commande": "play_until", "parametres": {"moment": "premiere_base"}},
                    {"mot": "مقابل C، G.", "commande": "play_until", "parametres": {"moment": "bases_posees"}},
                    {"mot": "مقابل C، G.", "repere": "reserve"},
                    {"mot": "ورد البال ل les extrémités", "commande": "play_until", "parametres": {"moment": "extremites"}},
                    {"mot": "إذن: trois prime", "repere": "resultat"},
                    {"mot": "إذن: trois prime", "cible": "centre:0"}]}},
    {"id": "ex_s6", "slide_type": "simulation", "title": "Question 6 : la double hélice",
     "screen_content": {"lead": "Deux brins antiparallèles, A–T (2 liaisons H), C–G (3 liaisons H), enroulés en double hélice."},
     "visual": {"kind": "simulation", "url": ADN + "?vue=construire&diapo=ex_structure", "caption": "Deux brins, tête-bêche, appariés, puis enroulés"},
     "speech_text": {"mixed": "l'A D N: deux brins de nucléotides. le deuxième brin مقلوب: tête-bêche. كل brin عندو extrémité cinq prime و extrémité trois prime: les brins sont antiparallèles. A en face de T، avec deux liaisons hydrogène. C en face de G، avec trois liaisons hydrogène. ومن بعد les deux brins كيتلواو: la double hélice. هادشي علاش autant de A que de T، و autant de C que de G."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "deux brins antiparallèles", "mot": "les brins sont antiparallèles"}, {"texte": "A–T : 2 liaisons H ; C–G : 3 liaisons H", "mot": "avec trois liaisons hydrogène"}, {"texte": "double hélice", "mot": "la double hélice"}],
       "pointage": [{"mot": "l'A D N: deux brins", "commande": "set_time", "parametres": {"time_s": 8.6}},
                    {"mot": "l'A D N: deux brins", "commande": "play_until", "parametres": {"moment": "deux_brins"}},
                    {"mot": "l'A D N: deux brins", "repere": "brin_2"},
                    {"mot": "le deuxième brin مقلوب", "commande": "play_until", "parametres": {"moment": "tete_beche"}},
                    {"mot": "كل brin عندو", "commande": "play_until", "parametres": {"moment": "antiparalleles"}},
                    {"mot": "كل brin عندو", "repere": "extremite_5"},
                    {"mot": "les brins sont antiparallèles", "cible": "centre:0"},
                    {"mot": "A en face de T", "commande": "play_until", "parametres": {"moment": "appariement"}},
                    {"mot": "A en face de T", "repere": "paire_at"},
                    {"mot": "avec deux liaisons hydrogène", "commande": "play_until", "parametres": {"moment": "liaisons_hydrogene"}},
                    {"mot": "avec deux liaisons hydrogène", "repere": "liaisons"},
                    {"mot": "avec trois liaisons hydrogène", "cible": "centre:1"},
                    {"mot": "كيتلواو", "commande": "play_until", "parametres": {"moment": "torsion_helice"}},
                    {"mot": "la double hélice", "repere": "helice"},
                    {"mot": "la double hélice", "cible": "centre:2"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : le rapport A/T", "سؤال ساهل: كيفاش كنحسبو A sur T؟",
      "Le rapport A/T se calcule en divisant :", ["le % de A par le % de G", "le % de A par le % de T", "la somme A + T par 100"], 1, {
        "1": {"juste": rep("برافو! A sur T، هو le pourcentage ديال A، sur le pourcentage ديال T.", "Juste : A/T = % A / % T.")},
        "0": {"1": rep("قريب! شوف الحروف ديال le rapport: A sur شنو؟ عاود اختار.", "Regarde les lettres du rapport : A divisé par quoi ? Réessaie."),
              "2": rep("الجواب هو: le pourcentage ديال A، sur le pourcentage ديال T. ماشي G.", "Réponse : A/T = % A / % T, pas % A / % G.")},
        "2": {"1": rep("ما تقلقش. le rapport A sur T، قسمة ديال جوج pourcentages: A فوق، و T لتحت. عاود اختار.", "Le rapport A/T divise deux pourcentages : A en haut, T en bas. Réessaie."),
              "2": rep("الجواب هو: le pourcentage ديال A، sur le pourcentage ديال T.", "Réponse : A/T = % A / % T.")}},
      "le rapport A sur T، كيفاش كيتحسب؟"),
    vrai_faux("fa_s2", "Plus facile : ce que montre le tableau", "Vrai ou faux : ce que montrent les résultats.",
      "سؤال ساهل: vrai ولا faux، على les résultats ديال le tableau.", [
        ("Chez toutes les espèces du tableau, % A ≈ % T.", True, "Vrai : A/T est voisin de 1 chez les quatre espèces."),
        ("Les pourcentages des bases sont les mêmes chez toutes les espèces.", False, "Faux : ils varient d'une espèce à l'autre ; seuls les rapports A/T et C/G restent voisins de 1."),
        ("A/T ≈ 1 et C/G ≈ 1 montrent que A s'associe à T et C à G.", True, "Vrai : c'est la complémentarité des bases."),
        ("L'adénine s'associe à la guanine.", False, "Faux : l'adénine s'associe à la thymine, la guanine à la cytosine.")]),
    qcm_facile("fa_s3", "Plus facile : (A + G)/(T + C)", "سؤال ساهل على le rapport A plus G، sur T plus C.",
      "Si % A = % T et % G = % C, alors (A + G)/(T + C) vaut :", ["2", "0,5", "1"], 2, {
        "2": {"juste": rep("برافو! A plus G égale T plus C، إذن le rapport égale un.", "Juste : A + G = T + C, donc le rapport vaut 1.")},
        "0": {"1": rep("قريب! عوض A ب T، و G ب C: الفوق واللتحت، شنو كيوليو؟ عاود اختار.", "Remplace A par T et G par C : que deviennent le haut et le bas ? Réessaie."),
              "2": rep("الجواب هو: un. الفوق واللتحت متساويين: A plus G égale T plus C.", "Réponse : 1, car A + G = T + C.")},
        "1": {"1": rep("ما تقلقش. الفوق ماشي النص ديال اللتحت. عوض A ب T، و G ب C. عاود اختار.", "Le haut n'est pas la moitié du bas. Remplace A par T et G par C. Réessaie."),
              "2": rep("الجواب هو: un، حيت A plus G égale T plus C.", "Réponse : 1, car A + G = T + C.")}},
      "يلا A égale T، و G égale C، le rapport A plus G، sur T plus C، شحال كيساوي؟"),
    qcm_facile("fa_s4", "Plus facile : le pourcentage manquant", "سؤال ساهل: نحسبو le pourcentage ديال G.",
      "Chez l'espèce Z, A = 21 %. Le pourcentage de G est :", ["21 %", "29 %", "58 %"], 1, {
        "1": {"juste": rep("برافو! T égale vingt et un، G plus C égale cinquante-huit، و G égale vingt-neuf pour cent.", "Juste : T = 21 %, G + C = 58 %, G = 29 %.")},
        "0": {"1": rep("قريب! vingt et un pour cent، هو A وهو T. ولكن G ماشي مقابلة A. عاود اختار.", "21 %, c'est A et T ; G n'est pas en face de A. Réessaie."),
              "2": rep("الجواب هو vingt-neuf pour cent: cent moins quarante-deux، égale cinquante-huit، و cinquante-huit sur deux، égale vingt-neuf.", "Réponse : G = (100 − 42)/2 = 29 %.")},
        "2": {"1": rep("قريب! cinquante-huit هو G plus C. و G égale C. عاود اختار.", "58 %, c'est G + C ; or G = C. Réessaie."),
              "2": rep("الجواب هو vingt-neuf pour cent: cinquante-huit sur deux، حيت G égale C.", "Réponse : G = 58/2 = 29 %, car G = C.")}},
      "عند l'espèce Z، A égale vingt et un pour cent. شحال هو le pourcentage ديال G؟"),
    assoc_bases("fa_s5"),
    vrai_faux("fa_s6", "Plus facile : la structure de l'ADN", "Vrai ou faux : la structure de l'ADN.",
      "سؤال ساهل: vrai ولا faux، على la structure ديال l'A D N.", [
        ("L'ADN est formé de deux brins enroulés en double hélice.", True, "Vrai : deux brins de nucléotides, en double hélice."),
        ("Les deux brins sont orientés dans le même sens.", False, "Faux : ils sont antiparallèles : 5'→3' en face de 3'→5'."),
        ("A et T sont reliées par deux liaisons hydrogène, C et G par trois.", True, "Vrai : A–T deux liaisons, C–G trois liaisons."),
        ("Le brin complémentaire de 5' ACG 3' s'écrit 5' TGC 3'.", False, "Faux : il s'écrit 3' TGC 5' : les extrémités sont inversées.")])
  ]}]},
  "similaire": {
    "id": "svt_ex_ch3_bases_adn_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On détermine de la même façon le pourcentage de chaque base azotée (A, T, G, C) dans l'ADN de quatre autres espèces. Le tableau présente les résultats.",
      "intro_dit": "نفس التجربة مع quatre espèces أخرى: حسبنا le pourcentage ديال كل base فl'A D N. le tableau فيه les résultats.",
      "figures": [tableau(ESP_B, "Composition en bases de l'ADN de quatre espèces (en %)")],
      "donnees": ["Pourcentages en % du nombre total de bases de l'ADN", "Arrondir les rapports à 0,01",
                  "Bases azotées : adénine (A), thymine (T), guanine (G), cytosine (C)"],
      "questions": [{k: q[k] for k in ("id", "texte", "reponse", "clavier", "correction")} for q in QS_B]
    }}
}
ecrire(EX, sys.argv[1])
