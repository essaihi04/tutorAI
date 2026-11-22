# Exercice SVT ch. 4 (relation gène – protéine), niveau difficile (« Supérieur ») : délétion d'un nucléotide (décalage du cadre
# de lecture, codon stop avancé) comparée à une délétion de trois nucléotides, mucoviscidose (protéine CFTR).
# Entraîne : ARNm et acides aminés depuis le brin TRANSCRIT ; trouver une délétion dans un extrait de même longueur (piège
# « même nombre de nucléotides = substitution ») ; nouvelle séquence et codon stop avancé ; longueur de la protéine (calcul) ;
# délétion de trois nucléotides sans décalage ; raisonnement critique : un seul acide aminé en moins suffit à rendre la protéine
# non fonctionnelle (document : la protéine mal formée n'atteint pas la membrane). Deux notions combinées (code génétique et
# relation protéine – caractère), document moins guidé.
# Sources comparées (lecture seule, rien de copié) :
# - exploration/relation_gene_proteine.json : origine_genetique (délétion 2017 N trois nucléotides, 2017 R un nucléotide,
#   2019 N stop prématuré, addition 2020 R), pièges (« croit qu'une délétion décale toujours », « compte les nucléotides et conclut
#   substitution » : Ouissam 38:56, AJIN9RAW 26:10-44:26), erreurs_examen (« appelle substitution un décalage »), insistances
#   (« une seule lettre perdue change toute la suite », « comparer jusqu'au bout »).
# - nationaux : 2017 N (caille, délétion d'un triplet), 2017 R, 2019 N, 2020 R : même gestes, autre situation et autres séquences.
# - séries en ligne : recherche faite (dyrassa série 7, alloschool, exercices PAH de l'université de Tours avec notation
#   « fsdelG ») ; PDF non ouverts (domaines bloqués par le réseau de la session) : titres et extraits seulement.
# Situation : la mucoviscidose n'est pas un sujet national 2016-2025 ; séquences et numéros inventés (simplifiés) ; la CFTR
# compte réellement 1480 acides aminés ; « protéine mal formée retenue dans la cellule » est donné par le document (pas de
# structure tertiaire, hors cadre).
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

# ── code génétique (vrai tableau) et outils ─────────────────────────────────────────────
_B = "UCAG"; _AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODE = {a + b + c: _AA[16 * i + 4 * j + k] for i, a in enumerate(_B) for j, b in enumerate(_B) for k, c in enumerate(_B)}
AB = {'F': 'Phe', 'L': 'Leu', 'S': 'Ser', 'Y': 'Tyr', '*': 'Stop', 'C': 'Cys', 'W': 'Trp', 'P': 'Pro', 'H': 'His', 'Q': 'Gln', 'R': 'Arg',
      'I': 'Ile', 'M': 'Met', 'T': 'Thr', 'N': 'Asn', 'K': 'Lys', 'V': 'Val', 'A': 'Ala', 'D': 'Asp', 'E': 'Glu', 'G': 'Gly'}
NOM = {'Phe': 'la phénylalanine', 'Leu': 'la leucine', 'Ser': 'la sérine', 'Tyr': 'la tyrosine', 'Cys': 'la cystéine', 'Trp': 'le tryptophane',
       'Pro': 'la proline', 'His': "l'histidine", 'Gln': 'la glutamine', 'Arg': "l'arginine", 'Ile': "l'isoleucine", 'Met': 'la méthionine',
       'Thr': 'la thréonine', 'Asn': "l'asparagine", 'Lys': 'la lysine', 'Val': 'la valine', 'Ala': "l'alanine", 'Asp': "l'acide aspartique",
       'Glu': "l'acide glutamique", 'Gly': 'la glycine'}
arn = lambda s: s.replace("T", "U")
cod = lambda s: [s[i:i + 3] for i in range(0, len(s) - len(s) % 3, 3)]
aa = lambda c: AB[CODE[arn(c)]]
L = lambda s: " ".join(s)                     # « GCT » → « G C T » (voix : lettres dites une à une)
assert CODE["AUG"] == "M" and CODE["UGG"] == "W" and CODE["UAG"] == "*" and CODE["GAG"] == "E" and CODE["CGA"] == "R" and CODE["CAA"] == "Q"


def fig_sequences(titre, debut, lignes, legende):
    """Tableau d'alignement dessiné : numéros des triplets, puis une ligne par séquence (étiquette, triplets)."""
    n = len(lignes[0][1]); x0, x1 = 30, 99; pas = (x1 - x0) / n; h = 8 * (len(lignes) + 1) + 2
    el = [{"f": "texte", "at": [1, h - 5], "t": "Triplets", "taille": "petit", "ancre": "gauche", "couleur": "faible"}]
    for j in range(n):
        el.append({"f": "texte", "at": [round(x0 + (j + .5) * pas, 2), h - 5], "t": str(debut + j), "taille": "petit", "couleur": "faible"})
    for i, (lab, trip, coul) in enumerate(lignes):
        y = h - 5 - 8 * (i + 1)
        el.append({"f": "ligne", "pts": [[0.5, y + 4], [99.5, y + 4]], "couleur": "faible"})
        el.append({"f": "texte", "at": [1, y], "t": lab, "taille": "petit", "ancre": "gauche", "couleur": "jaune"})
        for j, t in enumerate(trip):
            el.append({"f": "texte", "at": [round(x0 + (j + .5) * pas, 2), y], "t": t, "couleur": coul[j] if isinstance(coul, list) else coul})
    return {"type": "schema", "titre": titre, "cadre": {"l": 100, "h": h}, "legende": legende, "elements": el}



comp = lambda s: s.translate(str.maketrans("ATCG", "TAGC"))


def fig_tableau(titre, xs, entetes, lignes, legende):
    """Tableau dessiné (rect + texte) : colonnes aux abscisses xs, entêtes, une ligne par cas, cases sur 1 à 3 lignes."""
    hl = 4.2; hauteurs = [max(len(c) for c in l) * hl + 2 for l in lignes]
    h = 8 + sum(hauteurs); el = [{"f": "rect", "de": [0, h - 8], "a": [100, h], "couleur": "faible"}]
    for i, t in enumerate(entetes):
        el.append({"f": "texte", "at": [(xs[i] + xs[i + 1]) / 2, h - 4.6], "t": t, "taille": "petit", "couleur": "jaune"})
    y = h - 8
    for l, hh in zip(lignes, hauteurs):
        el.append({"f": "rect", "de": [0, y - hh], "a": [100, y], "couleur": "faible"})
        for i, cel in enumerate(l):
            for k, t in enumerate(cel):
                el.append({"f": "texte", "at": [(xs[i] + xs[i + 1]) / 2, round(y - 2.6 - k * hl, 2)], "t": t, "taille": "petit",
                           "couleur": "jaune" if i == 0 else "blanc"})
        y -= hh
    for x in xs[1:-1]:
        el.append({"f": "ligne", "pts": [[x, 0], [x, h]], "couleur": "faible"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 100, "h": round(h, 2)}, "legende": legende, "elements": el}


def traduire(nt):
    """Acides aminés depuis le 1er codon de l'extrait jusqu'au premier stop ; renvoie (liste, indice du stop ou None)."""
    out = []
    for i, c in enumerate(cod(nt)):
        if aa(c) == "Stop": return out, i
        out.append(aa(c))
    return out, None


def cas(debut, normal, p_del, j_trois, longueur, n_vu=9):
    """normal : triplets du brin NON transcrit (au moins n_vu + 1) ; p_del : rang (0-based, dans l'extrait) du nucléotide perdu par m1 ;
    j_trois : rang du triplet perdu par m2. Renvoie tout ce que l'énoncé, les réponses et les voix utilisent."""
    s = "".join(normal); n = 3 * n_vu
    m1, m2 = s[:p_del] + s[p_del + 1:], s[:3 * j_trois] + s[3 * j_trois + 3:]
    assert s[p_del - 1] != s[p_del] != s[p_del + 1]                       # délétion sans ambiguïté de position
    x = normal[j_trois]; assert s[3 * j_trois - 1] != x[2] and s[3 * j_trois + 3] != x[0]   # triplet perdu sans ambiguïté
    C = {"debut": debut, "N": cod(s[:n]), "M1": cod(m1[:n]), "M2": cod(m2[:n])}
    C["TN"], C["TM1"], C["TM2"] = ([comp(c) for c in C[k]] for k in ("N", "M1", "M2"))
    C["RN"], C["RM1"], C["RM2"] = ([arn(c) for c in C[k]] for k in ("N", "M1", "M2"))
    C["AN"], sN = traduire(s[:n]); assert sN is None and len(C["AN"]) == n_vu
    C["AM1"], C["stop1"] = traduire(m1); assert C["stop1"] is not None and C["stop1"] < n_vu
    C["AM2"], sM2 = traduire(m2[:n]); assert sM2 is None
    C["j_del"], C["rang_del"] = p_del // 3, p_del % 3
    assert C["AM1"][:C["j_del"]] == C["AN"][:C["j_del"]] and C["AM1"][C["j_del"]] != C["AN"][C["j_del"]]
    assert C["AM2"] == C["AN"][:j_trois] + C["AN"][j_trois + 1:] + [aa(normal[n_vu])]
    C["j_trois"], C["aa_perdu"] = j_trois, C["AN"][j_trois]
    C["t_del"], C["t_trois"], C["t_stop"] = debut + C["j_del"], debut + j_trois, debut + C["stop1"]
    C["base_del_tr"] = comp(s[p_del])                                     # nucléotide perdu, lu sur le brin transcrit
    C["long"], C["n1"], C["n2"] = longueur, debut + C["stop1"] - 1, longueur - 1
    C["pct1"] = round(C["n1"] / longueur * 100, 2)
    return C


A = cas(21, ["AAG", "CTG", "GAT", "CCA", "TGC", "TTT", "CTA", "AAG", "GTC", "CAG"], 7, 5, 1480)
assert A["TN"] == ["TTC", "GAC", "CTA", "GGT", "ACG", "AAA", "GAT", "TTC", "CAG"]
assert A["TM1"] == ["TTC", "GAC", "CAG", "GTA", "CGA", "AAG", "ATT", "TCC", "AGG"]
assert A["AN"] == ["Lys", "Leu", "Asp", "Pro", "Cys", "Phe", "Leu", "Lys", "Val"] and A["AM1"] == ["Lys", "Leu", "Val", "His", "Ala", "Phe"]
assert (A["t_del"], A["rang_del"], A["t_stop"], A["t_trois"], A["n1"], A["pct1"], A["base_del_tr"]) == (23, 1, 27, 26, 26, 1.76, "T")
B = cas(31, ["GGT", "ACC", "CAG", "TTC", "GAC", "AAA", "TTG", "ATC", "CGC", "TAC"], 7, 5, 1480)
assert B["AM1"] == ["Gly", "Thr", "Arg", "Ser", "Thr", "Asn"] and (B["t_del"], B["rang_del"], B["t_stop"], B["t_trois"], B["n1"], B["pct1"]) == (33, 1, 37, 36, 36, 2.43)
assert B["aa_perdu"] == "Lys" and A["aa_perdu"] == "Phe"

def extrait_code(C, plus):
    cs = []
    for c in C["RN"] + C["RM1"][:C["stop1"] + 1] + C["RM2"] + plus:
        if c not in cs: cs.append(c)
    return "Extrait du code génétique : " + " ; ".join(f"{c} : {AB[CODE[c]]}" for c in sorted(cs))

j = lambda xs: " ".join(xs)
tiret = lambda xs: " – ".join(xs)
RANG = ["1er", "2e", "3e"]; RANG_DIT = ["le premier", "le deuxième", "le troisième"]
FR = {21: "vingt et un", 23: "vingt-trois", 26: "vingt-six", 27: "vingt-sept", 29: "vingt-neuf", 31: "trente et un", 33: "trente-trois",
      36: "trente-six", 37: "trente-sept", 39: "trente-neuf"}

DOC = "/media/simulations/svt/relation_gene_proteine-tableau/"
TAB, MUT, SCH = DOC + "code_genetique.html?vue=tableau", DOC + "mutation.html?vue=mutation", DOC + "schema_bilan.html?vue=schema"

DOC2 = [[["personne saine", "(N et N)"], ["présente"], ["présente"], ["fluide"]],
        [["personne 1", "(m1 et m1)"], ["aucune protéine", "complète"], ["absente"], ["épais, bronches", "bouchées"]],
        [["personne 2", "(m2 et m2)"], ["présente, retenue", "dans le cytoplasme"], ["absente"], ["épais, bronches", "bouchées"]]]
XS2 = [0, 24, 50, 74, 100]


def enonce_fig(C):
    return [fig_sequences("Document 1 : brin transcrit (3′ → 5′)", C["debut"],
                          [("Allèle N", C["TN"], "blanc"), ("Allèle m1", C["TM1"], "blanc"), ("Allèle m2", C["TM2"], "blanc")],
                          "Extraits de même longueur du gène CFTR : allèle normal N et deux allèles mutés m1 et m2."),
            fig_tableau("Document 2 : la protéine CFTR chez trois personnes", XS2,
                        ["Personne", "CFTR dans la cellule", "CFTR dans la membrane", "Mucus"], DOC2,
                        "Chaque personne porte le même allèle sur les deux chromosomes de la paire.")]


def donnees(C, plus):
    d = C["debut"]
    return [f"Allèle N (brin transcrit, 3′ → 5′) : {j(C['TN'])}", f"Allèle m1 (brin transcrit, 3′ → 5′) : {j(C['TM1'])}",
            f"Allèle m2 (brin transcrit, 3′ → 5′) : {j(C['TM2'])}",
            f"Triplets {d} à {d + 8} ; le triplet 1 du gène correspond au codon AUG ; la protéine CFTR normale compte {C['long']} acides aminés.",
            "Une protéine dont la forme est anormale est retenue dans le cytoplasme et détruite : elle n'atteint pas la membrane.",
            extrait_code(C, plus)]


EX = {
  "id": "svt_ex_ch4_deletion_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "relation_gene_proteine", "cours": "svt_ch4_relation_gene_proteine",
  "titre": "La mucoviscidose : une lettre perdue ou un triplet perdu", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Écrire l'ARNm à partir du brin transcrit", "Repérer une délétion dans un extrait de même longueur",
                  "Expliquer le décalage du cadre de lecture et le codon stop avancé", "Calculer la longueur d'une protéine",
                  "Comparer une délétion d'un nucléotide et une délétion de trois nucléotides", "Relier la protéine au caractère"],
  "enonce": {
    "intro": ("La mucoviscidose est une maladie héréditaire : le mucus qui tapisse les bronches est épais et collant, les bronches se bouchent et s'infectent. "
              "La protéine CFTR est un canal situé dans la membrane des cellules des bronches : il laisse sortir des ions chlorure, ce qui rend le mucus fluide. "
              f"Document 1 : extraits du brin transcrit du gène CFTR (triplets {A['debut']} à {A['debut'] + 8}) de trois allèles : l'allèle normal N et deux allèles mutés m1 et m2 "
              "(séquences simplifiées pour l'exercice ; chaque extrait a la même longueur, celle de la fenêtre étudiée). "
              "Document 2 : la protéine CFTR et le mucus chez trois personnes."),
    "intro_dit": ("نقراو l'énoncé. la mucoviscidose هي maladie héréditaire: le mucus اللي ف les bronches كيولي غليظ وكيلصق، les bronches كيتسدو وكيتعفنو. "
                  "la protéine C F T R هي canal ف la membrane ديال les cellules ديال les bronches: كتخرج les ions chlorure، وهادشي كيخلي le mucus خفيف. "
                  "le document un: جزء من le brin transcrit ديال le gène، ل تلاتة ديال les allèles: l'allèle normal N، و جوج ديال les allèles mutés، m un و m deux. "
                  "كل جزء عندو نفس الطول. le document deux: la protéine C F T R و le mucus، عند تلاتة ديال الناس."),
    "figures": enonce_fig(A),
    "donnees": donnees(A, ["AUG", "UAG", "UGA"]),
    "questions": [
      {"id": "1", "texte": "Donner la séquence de l'ARNm et la séquence des acides aminés correspondant à l'extrait de l'allèle N.",
       "texte_dit": "la question un: عطي la séquence ديال l'A R N messager، و la séquence ديال les acides aminés، ديال l'allèle N.",
       "reponse": {"type": "phrase", "attendu": f"ARNm (allèle N) : {j(A['RN'])} ; acides aminés : {tiret(A['AN'])}."},
       "clavier": {"aides": ["ARNm :", "A → U", "T → A", "C → G", "G → C", "–"], "pieges": [j(arn(c) for c in A["TN"][:2]), "T"]},
       "aides": [
         {"texte": "Le document 1 donne le brin TRANSCRIT : l'ARNm est complémentaire, lettre par lettre, et n'a pas de T.",
          "dit": "le document un كيعطي le brin transcrit. l'A R N messager هو le complémentaire ديالو، حرف ب حرف، وما فيهش T."},
         {"texte": "Écris un codon sous chaque triplet, garde les numéros, puis cherche chaque codon dans l'extrait du code.",
          "dit": "كتب codon تحت كل triplet، خلي les numéros، ومن بعد قلب على كل codon ف le code génétique."}],
       "correction": {"lignes": [
           {"texte": f"1 : ARNm (allèle N) : {j(A['RN'])}", "mot": "l'A R N messager هو"},
           {"texte": f"acides aminés : {tiret(A['AN'])}", "mot": "les acides aminés"}],
         "parole": (f"la question un. le brin transcrit، إذن la complémentarité. l'A R N messager هو {'، '.join(L(c) for c in A['RN'])}. "
                    f"les acides aminés: {'، '.join(NOM[a] for a in A['AN'])}.")},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Comparer l'allèle m1 à l'allèle N : déterminer la mutation (type, nucléotide, triplet), donner la séquence des acides aminés de m1, puis expliquer pourquoi toute la séquence change après le triplet 23.",
       "texte_dit": "la question deux: قارن l'allèle m un مع l'allèle N. حدد la mutation، le type، le nucléotide، و le triplet. عطي les acides aminés ديال m un، ومن بعد فسر علاش la séquence كلها كتبدل من بعد le triplet vingt-trois.",
       "reponse": {"type": "phrase", "attendu": (f"Les deux extraits sont identiques jusqu'au 1er nucléotide du triplet 23 ; ensuite toutes les lettres de m1 sont décalées d'un rang vers la gauche. "
                                                 f"Le 2e nucléotide du triplet 23 du brin transcrit (T) a disparu : mutation par délétion d'un nucléotide. "
                                                 f"ARNm de m1 : {j(A['RM1'])} ; acides aminés : {tiret(A['AM1'])} (codon stop UAA au triplet 27 : arrêt de la traduction). "
                                                 "Les ribosomes lisent l'ARNm trois par trois depuis le début : la perte d'une lettre décale le cadre de lecture, "
                                                 "tous les codons après le triplet 23 changent et un codon stop apparaît plus tôt (triplet 27).")},
       "clavier": {"aides": ["délétion", "triplet 23", "décalage du cadre de lecture", "codon stop", "UAA", "arrêt de la traduction"], "pieges": ["plusieurs substitutions", "même nombre de nucléotides : substitution"]},
       "aides": [
         {"texte": "Les extraits ont la même longueur, mais ce n'est pas une preuve de substitution : compare lettre par lettre et cherche à partir d'où TOUT est décalé.",
          "dit": "نفس الطول، ولكن هادا ماشي دليل على substitution. قارن حرف ب حرف، وقلب على البلاصة اللي من بعدها كلشي تزحزح."},
         {"texte": "Si la suite de m1 est la suite de N décalée d'une lettre, une lettre a été perdue. Puis lis l'ARNm de m1 trois par trois depuis le début, jusqu'au premier stop.",
          "dit": "يلا la suite ديال m un هي la suite ديال N، متزحزحة ب حرف واحد، إذن حرف ضاع. ومن بعد قرا l'A R N messager ديال m un، تلاتة تلاتة، من البداية، حتى ل أول stop."}],
       "correction": {"lignes": [
           {"texte": "2 : délétion du 2e nucléotide (T) du triplet 23 du brin transcrit", "mot": "délétion ديال le deuxième nucléotide"},
           {"texte": f"ARNm m1 : {j(A['RM1'][:A['stop1'] + 1])}…", "mot": "l'A R N messager ديال m un"},
           {"texte": f"acides aminés : {tiret(A['AM1'])} (stop UAA au triplet 27)", "mot": "codon stop، U A A"},
           {"texte": "décalage du cadre de lecture : tous les codons changent après le triplet 23", "mot": "décalage du cadre de lecture"}],
         "parole": ("la question deux. الجوج بحال بحال حتى ل le triplet vingt-trois. من تما، كل الحروف ديال m un متزحزحين ب حرف واحد. "
                    "إذن délétion ديال le deuxième nucléotide، T، ف le triplet vingt-trois، du brin transcrit. "
                    f"l'A R N messager ديال m un: {'، '.join(L(c) for c in A['RM1'][:A['stop1'] + 1])}. "
                    f"les acides aminés: {'، '.join(NOM[a] for a in A['AM1'])}، ومن بعد codon stop، U A A، ف le triplet vingt-sept. "
                    "علاش؟ les ribosomes كيقراو تلاتة تلاتة من البداية. حرف واحد ضاع، كلشي من بعد كيتقرا غالط: هادا هو le décalage du cadre de lecture.")},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Calculer le nombre d'acides aminés de la protéine codée par m1, puis le pourcentage qu'il représente par rapport à la protéine CFTR normale.",
       "texte_dit": "la question trois: حسب شحال من acide aminé ف la protéine ديال m un، ومن بعد le pourcentage ديالها بالمقارنة مع la protéine C F T R normale.",
       "reponse": {"type": "valeur", "grandeur": "p", "valeur": A["pct1"], "unite": "%", "tolerance": 0.02,
                   "attendu": f"Stop au triplet 27 : n = 27 − 1 = 26 acides aminés ; p = 26/1480 × 100 ≈ {str(A['pct1']).replace('.', ',')} %"},
       "clavier": {"aides": ["n = 27 − 1", "26/1480 × 100", "%"], "pieges": ["n = 27", "1480/26"]},
       "aides": [
         {"texte": "Le triplet 1 (AUG) donne le 1er acide aminé ; chaque triplet jusqu'au triplet avant le stop en donne un ; le stop n'en donne aucun.",
          "dit": "le triplet un، A U G، كيعطي أول acide aminé. كل triplet حتى ل اللي قبل le stop كيعطي acide aminé. le stop ما كيعطي والو."},
         {"texte": "n = (triplet du stop) − 1, puis p = n / 1480 × 100.",
          "dit": "n égale le triplet ديال le stop moins un. ومن بعد p égale n sur mille quatre cent quatre-vingts، fois cent."}],
       "correction": {"lignes": [
           {"texte": "3 : stop au triplet 27 : n = 27 − 1 = 26 acides aminés", "mot": "n égale vingt-sept moins un"},
           {"texte": "p = 26/1480 × 100 ≈ 1,76 %", "mot": "p égale vingt-six sur mille quatre cent quatre-vingts"},
           {"texte": "la protéine m1 est presque entièrement absente : non fonctionnelle", "mot": "non fonctionnelle"}],
         "parole": ("la question trois. le stop ف le triplet vingt-sept. n égale vingt-sept moins un، égale vingt-six acides aminés. "
                    "p égale vingt-six sur mille quatre cent quatre-vingts، fois cent، environ un virgule sept six pour cent. "
                    "la protéine ديال m un ناقصاها تقريبا كلشي: non fonctionnelle.")},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Comparer l'allèle m2 à l'allèle N : nommer la mutation, donner sa conséquence sur la séquence et sur la longueur de la protéine, puis expliquer pourquoi, contrairement à m1, il n'y a pas de décalage du cadre de lecture.",
       "texte_dit": "la question quatre: قارن l'allèle m deux مع l'allèle N. سمي la mutation، عطي النتيجة ديالها على la séquence و على الطول ديال la protéine، ومن بعد فسر علاش، ماشي بحال m un، ما كاينش décalage du cadre de lecture.",
       "reponse": {"type": "phrase", "attendu": ("Le triplet 26 du brin transcrit (AAA, codon UUU, Phe) a disparu ; tous les autres triplets sont identiques : mutation par délétion de trois nucléotides. "
                                                 f"Acides aminés de m2 : {tiret(A['AM2'])} : seule la phénylalanine (26e acide aminé) manque, la suite est inchangée ; "
                                                 "la protéine compte 1480 − 1 = 1479 acides aminés. Pas de décalage : trois nucléotides forment un codon entier, "
                                                 "la lecture trois par trois des codons suivants n'est pas changée.")},
       "clavier": {"aides": ["délétion de trois nucléotides", "triplet 26", "Phe", "1479", "codon entier", "pas de décalage"], "pieges": ["décalage du cadre de lecture", "substitution"]},
       "aides": [
         {"texte": "Aligne m2 sous N : un triplet entier de N n'apparaît plus dans m2, et les triplets suivants arrivent à sa place. Lequel ?",
          "dit": "حط m deux تحت N. triplet كامل ديال N ما بقاش ف m deux، و les triplets اللي من بعدو جاو ف البلاصة ديالو. شمن واحد؟"},
         {"texte": "Trois lettres perdues = un codon perdu : un acide aminé en moins, mais le découpage en codons de la suite reste le même.",
          "dit": "trois lettres ضاعو، يعني codon واحد ضاع: acide aminé واحد ناقص، ولكن التقسيم ل des codons من بعد ما تبدلش."}],
       "correction": {"lignes": [
           {"texte": "4 : le triplet 26 (AAA, codon UUU, Phe) a disparu : délétion de trois nucléotides", "mot": "délétion de trois nucléotides"},
           {"texte": "seule la phénylalanine manque : 1480 − 1 = 1479 acides aminés", "mot": "mille quatre cent soixante-dix-neuf"},
           {"texte": "pas de décalage : trois nucléotides = un codon entier", "mot": "ما كاينش décalage"}],
         "parole": ("la question quatre. ف m deux، le triplet vingt-six كامل مشى: A A A، و le codon ديالو U U U، la phénylalanine. هادي délétion de trois nucléotides. "
                    "غير la phénylalanine اللي ناقصة، والباقي بحال بحال. la protéine فيها mille quatre cent quatre-vingts moins un، يعني mille quatre cent soixante-dix-neuf acides aminés. "
                    "ما كاينش décalage، حيت trois nucléotides هوما codon كامل: les codons اللي من بعد كيتقراو بحال قبل.")},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "En exploitant le document 2, expliquer pourquoi les personnes 1 et 2 sont toutes deux atteintes de mucoviscidose, alors que la protéine de m2 ne diffère de la protéine normale que par un seul acide aminé.",
       "texte_dit": "la question cinq: باستعمال le document deux، فسر علاش la personne un و la personne deux بجوج مراض ب la mucoviscidose، واخا la protéine ديال m deux ما فيها غير acide aminé واحد مختلف.",
       "reponse": {"type": "phrase", "attendu": ("Personne 1 : délétion d'un nucléotide → décalage du cadre de lecture → codon stop au triplet 27 → protéine de 26 acides aminés, non fonctionnelle (aucune CFTR complète). "
                                                 "Personne 2 : délétion de trois nucléotides → une phénylalanine en moins → la séquence d'acides aminés, qui donne sa forme à la protéine, est modifiée "
                                                 "→ CFTR mal formée, retenue dans le cytoplasme, absente de la membrane. "
                                                 "Dans les deux cas, pas de canal CFTR dans la membrane → les ions chlorure ne sortent pas → mucus épais → bronches bouchées : mucoviscidose. "
                                                 "Un seul acide aminé en moins peut donc suffire à rendre une protéine non fonctionnelle.")},
       "clavier": {"aides": ["décalage", "mal formée", "absente de la membrane", "ions chlorure", "mucus épais", "→"], "pieges": ["un acide aminé en moins ne change rien"]},
       "aides": [
         {"texte": "Regarde la colonne « CFTR dans la membrane » du document 2 : qu'ont en commun les personnes 1 et 2 ?",
          "dit": "شوف la colonne ديال C F T R ف la membrane، ف le document deux. شنو كيجمع la personne un و la personne deux؟"},
         {"texte": "Écris deux chaînes de flèches (m1 puis m2) qui se rejoignent : pas de CFTR dans la membrane → chlorure → mucus → maladie.",
          "dit": "كتب جوج ديال les chaînes ب des flèches، m un و m deux، كيتلاقاو ف: ما كايناش C F T R ف la membrane، من بعد les ions chlorure، le mucus، و la maladie."}],
       "correction": {"lignes": [
           {"texte": "5 : personne 1 : décalage → stop au triplet 27 → protéine de 26 acides aminés, non fonctionnelle", "mot": "عند la personne un"},
           {"texte": "personne 2 : une Phe en moins → protéine mal formée, retenue dans le cytoplasme", "mot": "عند la personne deux"},
           {"texte": "les deux : pas de CFTR dans la membrane → chlorure ne sort pas → mucus épais → mucoviscidose", "mot": "ف الجوج"},
           {"texte": "un seul acide aminé en moins peut suffire à rendre une protéine non fonctionnelle", "mot": "acide aminé واحد ناقص"}],
         "parole": ("la question cinq. عند la personne un، le décalage كيعطي codon stop ف le triplet vingt-sept: protéine قصيرة، non fonctionnelle. "
                    "عند la personne deux، la phénylalanine ناقصة. la séquence ديال les acides aminés هي اللي كتعطي الشكل ل la protéine: إذن la protéine كتخرج مشوهة، كتبقى ف le cytoplasme، و ما كتوصلش ل la membrane. "
                    "ف الجوج، ما كاينش canal C F T R ف la membrane، les ions chlorure ما كيخرجوش، le mucus كيولي غليظ، و les bronches كيتسدو: la mucoviscidose. "
                    "إذن حتى acide aminé واحد ناقص يقدر يخلي la protéine non fonctionnelle.")},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : codon par codon, avec le tableau du code",
     "screen_content": {"lead": "Brin transcrit → ARNm complémentaire ; un codon sous chaque triplet ; chaque codon lu dans le tableau."},
     "visual": {"kind": "simulation", "url": TAB, "caption": "Le tableau du code génétique"},
     "speech_text": {"mixed": ("أول حاجة: le brin transcrit، إذن l'A R N messager هو le complémentaire ديالو. "
                               f"مثلا {L(A['TN'][0])} كتولي {L(A['RN'][0])}. "
                               "من بعد، la méthode: قسم l'A R N messager ل des codons، codon تحت كل triplet. "
                               "قلب على كل codon ف le tableau: الحرف اللول ف اليسار، الثاني لفوق، الثالث ف اليمين. "
                               "كتب les acides aminés، بيناتهم tiret. "
                               f"هنا، le premier codon {L(A['RN'][0])} كيعطي la lysine.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": f"brin transcrit {A['TN'][0]} → codon {A['RN'][0]}", "mot": f"مثلا {L(A['TN'][0])}"},
                  {"texte": f"{A['RN'][0]} → Lys", "mot": "كيعطي la lysine"}],
       "pointage": [{"mot": "أول حاجة", "commande": "set_time", "parametres": {"time_s": 25.0}},
                    {"mot": f"مثلا {L(A['TN'][0])}", "cible": "centre:0"},
                    {"mot": "قسم l'A R N messager", "repere": "arnm"},
                    {"mot": "قلب على كل codon", "repere": "tableau"},
                    {"mot": "كتب les acides aminés", "repere": "sequence_acides_amines"},
                    {"mot": "كيعطي la lysine", "cible": "centre:1"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : une lettre perdue décale toute la lecture",
     "screen_content": {"lead": "Lecture trois par trois depuis le début : une lettre en moins, et tous les codons suivants changent."},
     "visual": {"kind": "simulation", "url": MUT, "caption": "Délétion d'un nucléotide : le cadre de lecture se décale"},
     "speech_text": {"mixed": ("شوف l'exemple ديال الدرس: nucléotide كيضيع، G ف le triplet trois. "
                               "l'A R N messager ديما كيتقرا تلاتة تلاتة، من البداية. "
                               "من البلاصة اللي ضاع فيها الحرف، جميع les codons كيتبدلو، و les acides aminés كيتبدلو. "
                               "هادا هو le décalage du cadre de lecture: الخط الحمر كيبين البلاصة. "
                               "ف التمرين ديالنا، نفس الشي: T ضاع ف le triplet vingt-trois، ومن بعد كلشي تبدل، حتى بان codon stop، U A A، ف le triplet vingt-sept.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "délétion d'un nucléotide → décalage du cadre de lecture", "mot": "هادا هو le décalage du cadre de lecture"},
                  {"texte": "m1 : T perdu au triplet 23 → stop UAA au triplet 27", "mot": "T ضاع ف le triplet vingt-trois"}],
       "pointage": [{"mot": "شوف l'exemple", "commande": "set_time", "parametres": {"time_s": 19.0}},
                    {"mot": "nucléotide كيضيع", "commande": "play_until", "parametres": {"moment": "deletion"}},
                    {"mot": "nucléotide كيضيع", "repere": "base_mutee"},
                    {"mot": "ديما كيتقرا تلاتة تلاتة", "repere": "arcs_lecture"},
                    {"mot": "جميع les codons كيتبدلو", "repere": "acide_amine_change"},
                    {"mot": "هادا هو le décalage du cadre de lecture", "commande": "play_until", "parametres": {"moment": "decalage"}},
                    {"mot": "الخط الحمر", "repere": "trait_decalage"},
                    {"mot": "هادا هو le décalage du cadre de lecture", "cible": "centre:0"},
                    {"mot": "T ضاع ف le triplet vingt-trois", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : du codon AUG jusqu'au codon stop",
     "screen_content": {"lead": "AUG (triplet 1) donne Met ; le codon stop ne donne rien : n = 27 − 1 = 26 ; p = 26/1480 × 100 ≈ 1,76 %."},
     "visual": {"kind": "simulation", "url": TAB, "caption": "Codon d'initiation et codons stop"},
     "speech_text": {"mixed": ("شوف: A U G، le codon d'initiation. هو le triplet un، وكيعطي أول acide aminé، la méthionine. "
                               "وهادو les codons stop: U A A، U A G، U G A. ما كيعطيو حتى acide aminé. "
                               "إذن، من le triplet un حتى ل le triplet vingt-six، كل triplet كيعطي acide aminé. "
                               "n égale vingt-sept moins un، égale vingt-six. "
                               "p égale vingt-six sur mille quatre cent quatre-vingts، fois cent، environ un virgule sept six pour cent.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "n = 27 − 1 = 26 acides aminés", "mot": "n égale vingt-sept moins un"},
                  {"texte": "p = 26/1480 × 100 ≈ 1,76 %", "mot": "environ un virgule sept six pour cent"}],
       "pointage": [{"mot": "شوف: A U G", "commande": "set_time", "parametres": {"time_s": 20.0}},
                    {"mot": "le codon d'initiation", "commande": "play_until", "parametres": {"moment": "initiation"}},
                    {"mot": "le codon d'initiation", "repere": "codon_initiation"},
                    {"mot": "وهادو les codons stop", "commande": "play_until", "parametres": {"moment": "codon_stop"}},
                    {"mot": "وهادو les codons stop", "repere": "cases_stop"},
                    {"mot": "n égale vingt-sept moins un", "cible": "centre:0"},
                    {"mot": "environ un virgule sept six pour cent", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : trois lettres perdues, un codon perdu, pas de décalage",
     "screen_content": {"lead": "Un triplet entier disparaît : un acide aminé en moins, la suite est lue comme avant."},
     "visual": {"kind": "simulation", "url": MUT, "caption": "Délétion de trois nucléotides"},
     "speech_text": {"mixed": ("ويلا مشاو trois nucléotides مرة وحدة؟ شوف: هنا le triplet trois كامل مشى. "
                               "l'A R N messager تبدل غير ف البلاصة ديالو، و la protéine ناقصاها غير acide aminé واحد. "
                               "ما كاينش décalage: trois nucléotides، هي codon كامل. "
                               "ف التمرين، le triplet vingt-six مشى: la phénylalanine ناقصة، و la protéine فيها mille quatre cent soixante-dix-neuf acides aminés.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "3 nucléotides = 1 codon : pas de décalage", "mot": "ما كاينش décalage"},
                  {"texte": "m2 : Phe (triplet 26) en moins → 1479 acides aminés", "mot": "le triplet vingt-six مشى"}],
       "pointage": [{"mot": "ويلا مشاو", "commande": "set_time", "parametres": {"time_s": 29.6}},
                    {"mot": "هنا le triplet trois", "commande": "play_until", "parametres": {"moment": "deletion_de_trois_evt"}},
                    {"mot": "كامل مشى", "repere": "base_mutee"},
                    {"mot": "l'A R N messager تبدل", "repere": "arnm_mute"},
                    {"mot": "ناقصاها غير acide aminé", "commande": "play_until", "parametres": {"moment": "deletion_de_trois"}},
                    {"mot": "ناقصاها غير acide aminé", "repere": "aa_mute"},
                    {"mot": "ما كاينش décalage", "commande": "play_until", "parametres": {"moment": "sans_decalage"}},
                    {"mot": "ما كاينش décalage", "repere": "accent_texte"},
                    {"mot": "ما كاينش décalage", "cible": "centre:0"},
                    {"mot": "le triplet vingt-six مشى", "cible": "centre:1"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : la protéine doit arriver au bon endroit",
     "screen_content": {"lead": "Pas de CFTR dans la membrane (absente ou mal formée) → chlorure retenu → mucus épais → maladie."},
     "visual": {"kind": "simulation", "url": SCH, "caption": "Du gène au caractère"},
     "speech_text": {"mixed": ("شوف la traduction ف le cytoplasme. le ribosome كيعطي la protéine. "
                               "la séquence ديال les acides aminés هي اللي كتعطي الشكل ل la protéine، والشكل كيعطي الخدمة ديالها. "
                               "عند m un، la protéine قصيرة بزاف. عند m deux، la protéine ناقصاها acide aminé واحد، كتخرج مشوهة، وكتبقى ف le cytoplasme. "
                               "ف الجوج، ما كاينش canal ف la membrane، le mucus كيولي غليظ: هادا هو le caractère. "
                               "le gène كيحدد la protéine، و la protéine كتحدد le caractère.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "m1 : protéine de 26 acides aminés ; m2 : protéine mal formée, retenue", "mot": "عند m un، la protéine قصيرة بزاف"},
                  {"texte": "pas de CFTR dans la membrane → mucus épais → mucoviscidose", "mot": "ما كاينش canal ف la membrane"}],
       "pointage": [{"mot": "شوف la traduction", "commande": "set_time", "parametres": {"time_s": 11.5}},
                    {"mot": "شوف la traduction", "commande": "play_until", "parametres": {"moment": "traduction"}},
                    {"mot": "شوف la traduction", "repere": "traduction"},
                    {"mot": "le ribosome كيعطي la protéine", "commande": "play_until", "parametres": {"moment": "proteine"}},
                    {"mot": "le ribosome كيعطي la protéine", "repere": "proteine"},
                    {"mot": "عند m un، la protéine قصيرة بزاف", "cible": "centre:0"},
                    {"mot": "ما كاينش canal ف la membrane", "cible": "centre:1"},
                    {"mot": "هادا هو le caractère", "commande": "play_until", "parametres": {"moment": "caractere"}},
                    {"mot": "هادا هو le caractère", "repere": "caractere"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : un codon depuis le brin transcrit", "سؤال ساهل: codon من le brin transcrit.",
      f"Brin transcrit : {A['TN'][2]}. Le codon de l'ARNm est…", [A["RN"][2], arn(A["TN"][2]), A["TN"][2]], 0, {
        "0": {"juste": rep(f"مزيان! le complémentaire: {L(A['TN'][2])} كتولي {L(A['RN'][2])}، و هو l'acide aspartique.", f"Juste : {A['TN'][2]} → {A['RN'][2]} (Asp).")},
        "1": {"1": rep("ما تقلقش. هادا le brin transcrit: خاصك la complémentarité، ماشي غير T كتولي U. عاود اختار.", "Brin transcrit : il faut la complémentarité. Réessaie."),
              "2": rep(f"الجواب هو {L(A['RN'][2])}: le complémentaire، حرف ب حرف.", f"Réponse : {A['RN'][2]}.")},
        "2": {"1": rep("قريب! نسيتي la complémentarité، و l'A R N ما فيهش T. عاود اختار.", "Pas de complémentarité, et l'ARN n'a pas de T. Réessaie."),
              "2": rep(f"الجواب هو {L(A['RN'][2])}.", f"Réponse : {A['RN'][2]}.")}},
      "Le brin transcrit est C T A. Quel est le codon de l'ARNm ?"),
    qcm_facile("fa_s2", "Plus facile : reconnaître une délétion", "سؤال ساهل: واش هادي délétion؟",
      "Normal : ATG GCA TTC CGA… ; muté : ATG GAT TCC GA… La mutation est…", ["une délétion d'un nucléotide (C perdu)", "trois substitutions", "une substitution faux-sens"], 0, {
        "0": {"juste": rep("برافو! C ديال G C A ضاع، و كلشي من بعد تزحزح ب حرف واحد: délétion.", "Juste : le C de GCA est perdu, tout est décalé d'une lettre : délétion.")},
        "1": {"1": rep("ما تقلقش. واش كاينين بزاف ديال les mutations، ولا الحروف غير تزحزحو؟ قارن حرف ب حرف. عاود اختار.", "Plusieurs mutations, ou des lettres simplement décalées ? Compare lettre par lettre. Réessaie."),
              "2": rep("الجواب هو délétion ديال nucléotide واحد: C ضاع، والباقي تزحزح. ف التمرين، mutation وحدة.", "Réponse : délétion d'un nucléotide (C) ; tout le reste est décalé.")},
        "2": {"1": rep("قريب! ف la substitution، غير حرف واحد كيتبدل، والباقي كيبقى ف البلاصة ديالو. هنا واش الباقي بقا؟ عاود اختار.", "En substitution, le reste ne bouge pas. Est-ce le cas ici ? Réessaie."),
              "2": rep("الجواب هو délétion ديال nucléotide واحد، حيت كلشي من بعد تزحزح.", "Réponse : délétion d'un nucléotide.")}},
      "A T G، G C A، T T C، C G A devient A T G، G A T، T C C، G A. Quel type de mutation ?"),
    qcm_facile("fa_s3", "Plus facile : compter les acides aminés", "سؤال ساهل: حسب les acides aminés.",
      "Le triplet 1 est AUG et le premier codon stop est au triplet 27. La protéine compte…", ["26 acides aminés", "27 acides aminés", "28 acides aminés"], 0, {
        "0": {"juste": rep("مزيان! vingt-sept moins un، égale vingt-six: le stop ما كيعطي والو.", "Juste : 27 − 1 = 26.")},
        "1": {"1": rep("ما تقلقش. واش le codon stop كيعطي acide aminé؟ عاود اختار.", "Le codon stop donne-t-il un acide aminé ? Réessaie."),
              "2": rep("الجواب هو vingt-six: vingt-sept moins un، حيت le stop ما كيتحسبش.", "Réponse : 26 (le stop ne compte pas).")},
        "2": {"1": rep("لا، ما كنزيدوش. le stop ما كيعطي والو. عاود اختار.", "On n'ajoute rien : le stop ne code rien. Réessaie."),
              "2": rep("الجواب هو vingt-six.", "Réponse : 26.")}},
      "Le premier codon stop est au triplet vingt-sept. Combien d'acides aminés ?"),
    vrai_faux("fa_s4", "Plus facile : un ou trois nucléotides perdus", "Vrai ou faux ?",
      "سؤال ساهل: صحيح ولا غالط؟", [
        ("La délétion d'un seul nucléotide décale le cadre de lecture.", True, "Vrai : tous les codons suivants changent."),
        ("Une délétion décale toujours le cadre de lecture.", False, "Faux : la perte de trois nucléotides (un codon entier) ne décale pas la lecture."),
        ("La délétion du triplet 26 enlève un seul acide aminé, la phénylalanine.", True, "Vrai : 1480 − 1 = 1479 acides aminés."),
        ("Après une délétion de trois nucléotides, tous les acides aminés suivants changent.", False, "Faux : la suite est lue comme dans l'allèle normal.")]),
    association("fa_s5", "Plus facile : de l'allèle à la protéine", "Relie chaque allèle à sa protéine CFTR.",
      "سؤال ساهل: ربط كل allèle مع la protéine ديالو.", "Relie chaque allèle à la protéine CFTR observée.",
      [("1", "Allèle N"), ("2", "Allèle m1"), ("3", "Allèle m2")],
      [("a", "CFTR normale, dans la membrane"), ("b", "Pas de CFTR complète (26 acides aminés)"), ("c", "CFTR mal formée, retenue dans le cytoplasme")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : l'allèle normal donne une CFTR fonctionnelle, dans la membrane.", "برافو: l'allèle normal كيعطي C F T R ف la membrane."),
       "1-b": (False, "L'allèle N n'a pas de codon stop dans l'extrait.", "لا، l'allèle N ما فيهش codon stop."),
       "1-c": (False, "L'allèle N a toute sa séquence : la protéine est bien formée.", "لا، l'allèle N كامل، la protéine مزيانة."),
       "2-a": (False, "m1 a un codon stop au triplet 27 : pas de protéine complète.", "لا، m un فيه codon stop ف le triplet vingt-sept."),
       "2-b": (True, "Oui : décalage puis stop au triplet 27 : 26 acides aminés.", "برافو: décalage، ومن بعد stop: vingt-six acides aminés."),
       "2-c": (False, "La protéine mal formée vient de m2 (une phénylalanine en moins).", "لا، la protéine المشوهة كتجي من m deux."),
       "3-a": (False, "Document 2 : la CFTR de la personne 2 est absente de la membrane.", "لا، عند la personne deux، ما كايناش ف la membrane."),
       "3-b": (False, "m2 n'a pas de codon stop avancé : la protéine est presque complète.", "لا، m deux ما فيهش stop بكري."),
       "3-c": (True, "Oui : une phénylalanine en moins, la protéine est mal formée et retenue.", "برافو: la phénylalanine ناقصة، la protéine مشوهة، وكتبقى ف le cytoplasme.")},
      ("(1 ; a) (2 ; b) (3 ; c).", "l'allèle N، protéine normale. m un، pas de protéine complète. m deux، protéine مشوهة."))
  ]}]},
  "similaire": {
    "id": "svt_ex_ch4_deletion_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Même étude sur un autre extrait du gène CFTR (mucoviscidose ; la CFTR normale compte 1480 acides aminés). "
                f"Document 1 : extraits du brin transcrit (triplets {B['debut']} à {B['debut'] + 8}) de l'allèle normal N et de deux allèles mutés m1 et m2, "
                "séquences simplifiées, de même longueur. Document 2 : identique (personne 1 : m1 et m1 ; personne 2 : m2 et m2)."),
      "intro_dit": "نفس الدراسة، ف جزء آخر من le gène C F T R. تلاتة ديال les allèles: N، m un، و m deux.",
      "figures": enonce_fig(B),
      "donnees": donnees(B, ["AUG", "UAA", "UAG"]),
      "questions": [
        {"id": "1", "texte": "Donner la séquence de l'ARNm et la séquence des acides aminés de l'allèle N.",
         "reponse": {"type": "phrase", "attendu": f"ARNm (allèle N) : {j(B['RN'])} ; acides aminés : {tiret(B['AN'])}."},
         "clavier": {"aides": ["ARNm :", "complémentarité", "–"], "pieges": ["T"]},
         "correction": {"lignes": [{"texte": f"1 : ARNm : {j(B['RN'])}", "mot": "l'A R N messager"},
                                   {"texte": f"acides aminés : {tiret(B['AN'])}", "mot": "les acides aminés"}],
                        "parole": f"la question un. l'A R N messager: {'، '.join(L(c) for c in B['RN'])}. les acides aminés: {'، '.join(NOM[a] for a in B['AN'])}."}},
        {"id": "2", "texte": "Comparer m1 à N : déterminer la mutation, donner les acides aminés de m1 et expliquer pourquoi la séquence change après le triplet 33.",
         "reponse": {"type": "phrase", "attendu": (f"Identiques jusqu'au 1er nucléotide du triplet 33, puis tout est décalé d'une lettre : délétion du 2e nucléotide (T) du triplet 33 du brin transcrit. "
                                                   f"ARNm de m1 : {j(B['RM1'])} ; acides aminés : {tiret(B['AM1'])} (codon stop UGA au triplet 37). "
                                                   "Lecture trois par trois depuis le début : décalage du cadre de lecture, tous les codons suivants changent, stop avancé.")},
         "clavier": {"aides": ["délétion", "triplet 33", "décalage du cadre de lecture", "UGA"], "pieges": ["substitution"]},
         "correction": {"lignes": [{"texte": "2 : délétion du T (2e nucléotide) du triplet 33 du brin transcrit", "mot": "délétion"},
                                   {"texte": f"{tiret(B['AM1'])} (stop UGA au triplet 37) : décalage du cadre de lecture", "mot": "décalage du cadre de lecture"}],
                        "parole": (f"la question deux. délétion ديال T، le deuxième nucléotide ديال le triplet trente-trois. les acides aminés: {'، '.join(NOM[a] for a in B['AM1'])}، "
                                   "ومن بعد codon stop، U G A، ف le triplet trente-sept. هادا هو le décalage du cadre de lecture.")}},
        {"id": "3", "texte": "Calculer le nombre d'acides aminés de la protéine de m1 et son pourcentage par rapport à la CFTR normale.",
         "reponse": {"type": "valeur", "grandeur": "p", "valeur": B["pct1"], "unite": "%", "tolerance": 0.02,
                     "attendu": f"n = 37 − 1 = 36 acides aminés ; p = 36/1480 × 100 ≈ {str(B['pct1']).replace('.', ',')} %"},
         "clavier": {"aides": ["n = 37 − 1", "36/1480 × 100"], "pieges": ["n = 37"]},
         "correction": {"lignes": [{"texte": "3 : n = 37 − 1 = 36 acides aminés", "mot": "n égale trente-sept moins un"},
                                   {"texte": "p = 36/1480 × 100 ≈ 2,43 %", "mot": "environ deux virgule quatre trois pour cent"}],
                        "parole": "la question trois. n égale trente-sept moins un، égale trente-six. p égale trente-six sur mille quatre cent quatre-vingts، fois cent، environ deux virgule quatre trois pour cent."}},
        {"id": "4", "texte": "Comparer m2 à N : nommer la mutation, sa conséquence sur la protéine, et expliquer l'absence de décalage.",
         "reponse": {"type": "phrase", "attendu": ("Le triplet 36 (TTT du brin transcrit, codon AAA, Lys) a disparu : délétion de trois nucléotides ; seule la lysine manque, la suite est inchangée : "
                                                   "1480 − 1 = 1479 acides aminés. Pas de décalage : trois nucléotides = un codon entier.")},
         "clavier": {"aides": ["délétion de trois nucléotides", "triplet 36", "Lys", "1479"], "pieges": ["décalage"]},
         "correction": {"lignes": [{"texte": "4 : triplet 36 perdu (codon AAA, Lys) : délétion de trois nucléotides, 1479 acides aminés", "mot": "délétion de trois nucléotides"},
                                   {"texte": "pas de décalage : un codon entier", "mot": "ما كاينش décalage"}],
                        "parole": "la question quatre. le triplet trente-six كامل مشى، la lysine ناقصة: délétion de trois nucléotides، mille quatre cent soixante-dix-neuf acides aminés. ما كاينش décalage، حيت codon كامل."}},
        {"id": "5", "texte": "En exploitant le document 2, expliquer pourquoi les personnes 1 et 2 sont toutes deux malades.",
         "reponse": {"type": "phrase", "attendu": ("Personne 1 : décalage → stop au triplet 37 → protéine de 36 acides aminés, non fonctionnelle. Personne 2 : une lysine en moins → protéine mal formée, retenue dans le cytoplasme. "
                                                   "Dans les deux cas, pas de CFTR dans la membrane → chlorure non sorti → mucus épais → mucoviscidose.")},
         "clavier": {"aides": ["mal formée", "absente de la membrane", "mucus épais"], "pieges": []},
         "correction": {"lignes": [{"texte": "5 : m1 : protéine courte ; m2 : protéine mal formée, retenue", "mot": "la protéine قصيرة"},
                                   {"texte": "pas de CFTR dans la membrane → mucus épais → mucoviscidose", "mot": "ما كاينش C F T R ف la membrane"}],
                        "parole": "la question cinq. عند m un، la protéine قصيرة. عند m deux، la protéine مشوهة وكتبقى ف le cytoplasme. ف الجوج، ما كاينش C F T R ف la membrane، و le mucus كيولي غليظ."}}
      ]}}
}
ecrire(EX, sys.argv[1])
