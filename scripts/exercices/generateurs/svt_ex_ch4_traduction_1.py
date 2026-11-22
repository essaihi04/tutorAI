# Exercice de SVT (ch. 4, relation gène – protéine) : la traduction, niveau facile.
# Ce qu'il entraîne : lire l'extrait du tableau du code génétique (1re lettre, 2e, 3e) codon par codon, s'arrêter au codon stop
# (sans tiret ni « Stop » comme acide aminé), nommer le codon d'initiation (AUG, Met) et le codon stop, trouver l'anticodon d'un
# ARNt (complémentaire du codon ; piège : chercher l'anticodon dans le tableau — l'extrait contient exprès le codon égal à
# l'anticodon), dire le rôle des ribosomes et des ARNt et le lieu de la traduction. Pas de mutation (autres exercices du cours).
# Sources comparées :
# - exploration relation_gene_proteine.json : cas_type « arn_aa » (méthode : codons, tableau, arrêt au stop), « etapes_traduction »
#   (2018 R), pièges « continue après le stop », « tiret après le dernier acide aminé », « cherche l'anticodon dans le tableau »,
#   « lit le tableau dans le mauvais ordre » ; valeurs repères (64 codons, 3 stop, AUG = Met).
# - vidéos des profs (exploration) : Faress (AUG CGC AGU … UAG, trois étapes), Elbrahimi (trois ribosomes), Mousstaid (exemples),
#   AJIN9RAW (ordre de lecture du tableau, national 2014).
# - nationaux : « déterminez la séquence de l'ARNm et la séquence d'acides aminés… en vous basant sur le tableau du code génétique »
#   (17 sessions sur 20), 2018 R (étapes de la traduction), 2022 N (sous-unités du ribosome).
# - séries en ligne : recherche faite (dyrassa, moutamadris) mais lecture impossible (réseau de la session refusé).
# Séquences originales ; acides aminés et anticodons calculés ci-dessous avec le code génétique complet.
import sys
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/relation_gene_proteine-tableau/"
TABLEAU = BASE + "code_genetique.html?vue=tableau"
TRAD = BASE + "traduction.html?vue=traduction"

L4 = "UCAG"
AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
ABR = {'F': 'Phe', 'L': 'Leu', 'S': 'Ser', 'Y': 'Tyr', '*': 'Stop', 'C': 'Cys', 'W': 'Trp', 'P': 'Pro', 'H': 'His', 'Q': 'Gln',
       'R': 'Arg', 'I': 'Ile', 'M': 'Met', 'T': 'Thr', 'N': 'Asn', 'K': 'Lys', 'V': 'Val', 'A': 'Ala', 'D': 'Asp', 'E': 'Glu', 'G': 'Gly'}
CODE = {a + b + c: ABR[AA[16 * i + 4 * j + k]] for i, a in enumerate(L4) for j, b in enumerate(L4) for k, c in enumerate(L4)}
NOMS = {'Met': 'méthionine', 'Phe': 'phénylalanine', 'Gly': 'glycine', 'His': 'histidine', 'Lys': 'lysine', 'Trp': 'tryptophane',
        'Pro': 'proline', 'Asp': 'acide aspartique', 'Leu': 'leucine', 'Thr': 'thréonine', 'Glu': 'acide glutamique',
        'Gln': 'glutamine', 'Cys': 'cystéine', 'Val': 'valine'}
CA = {'A': 'U', 'U': 'A', 'C': 'G', 'G': 'C'}
anticodon = lambda c: "".join(CA[b] for b in c)
def traduire(arn):
    out = []
    for c in arn.split():
        a = CODE[c]
        if a == 'Stop': return out, c
        out.append(a)
    raise ValueError("pas de codon stop")
epele = lambda seq: "، ".join(" ".join(t) for t in seq.split())

# ── Données de l'exercice ──
ARN = "AUG UUC GGA CAU AAA UGG UAG"
EXTRAIT = "AUG UUC UUU GGA GGC CAU CAA AAA AAG UGG UGU GUA UAG UAA UGA"
AA_ARN, STOP = traduire(ARN)
assert AA_ARN == ['Met', 'Phe', 'Gly', 'His', 'Lys', 'Trp'] and STOP == "UAG"
AA_Q3 = 'His'; COD_Q3 = "CAU"; ANTI = anticodon(COD_Q3)
assert CODE[COD_Q3] == AA_Q3 and ANTI == "GUA" and ANTI in EXTRAIT.split()      # piège voulu : GUA (Val) est dans l'extrait

ARN_B = "AUG CCA GAC UUA ACU GAG UGA"
EXTRAIT_B = "AUG CCA CCU GAC GAU UUA CUG ACU GAG GAA CAG UGA UAA UAG"
AA_B, STOP_B = traduire(ARN_B)
assert AA_B == ['Met', 'Pro', 'Asp', 'Leu', 'Thr', 'Glu'] and STOP_B == "UGA"
AA_Q3B = 'Asp'; COD_Q3B = "GAC"; ANTI_B = anticodon(COD_Q3B)
assert CODE[COD_Q3B] == AA_Q3B and ANTI_B == "CUG" and ANTI_B in EXTRAIT_B.split()
for c in ARN.split(): assert c in EXTRAIT.split()
for c in ARN_B.split(): assert c in EXTRAIT_B.split()

def chaine(aas): return " – ".join(aas)
def noms_dits(aas): return "، ".join(NOMS[a] for a in aas)


def fig_arnm(arn, titre):
    cods = arn.split(); n = len(cods)
    xs = [2.5 + 1.08 * j for j in range(n)]
    els = [{"f": "texte", "at": [0.1, 2.0], "t": "codons", "couleur": "faible", "taille": "petit", "ancre": "gauche"}]
    for j, x in enumerate(xs):
        els.append({"f": "texte", "at": [x, 2.0], "t": str(j + 1), "couleur": "blanc", "taille": "petit"})
        els.append({"f": "texte", "at": [x, 1.1], "t": cods[j], "couleur": "blanc"})
    els += [{"f": "texte", "at": [0.1, 1.1], "t": "ARNm", "couleur": "orange", "taille": "petit", "ancre": "gauche"},
            {"f": "texte", "at": [1.75, 1.1], "t": "5′", "couleur": "vert"},
            {"f": "texte", "at": [xs[-1] + 0.75, 1.1], "t": "3′", "couleur": "vert"},
            {"f": "rect", "de": [1.95, 0.7], "a": [xs[-1] + 0.55, 1.5], "couleur": "orange", "arrondi": True},
            {"f": "fleche", "de": [2.0, 0.3], "a": [xs[-1] + 0.5, 0.3], "couleur": "jaune", "texte": "sens de lecture", "pos": "s"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 10.4, "h": 2.6},
            "legende": "Fragment d'ARNm cytoplasmique, orienté de 5′ vers 3′, découpé en codons numérotés.", "elements": els}

def fig_code(extrait, titre):
    cods = extrait.split(); n = len(cods); par = (n + 1) // 2
    h = par * 0.6 + 1.0
    els = []
    for col in range(2):
        x0 = 0.3 + col * 5.1
        els += [{"f": "rect", "de": [x0, 0.2], "a": [x0 + 4.7, h - 0.2], "couleur": "faible"},
                {"f": "texte", "at": [x0 + 1.0, h - 0.55], "t": "codon", "couleur": "cyan", "taille": "petit"},
                {"f": "texte", "at": [x0 + 3.2, h - 0.55], "t": "acide aminé", "couleur": "cyan", "taille": "petit"},
                {"f": "ligne", "pts": [[x0, h - 0.85], [x0 + 4.7, h - 0.85]], "couleur": "faible"},
                {"f": "ligne", "pts": [[x0 + 2.0, 0.2], [x0 + 2.0, h - 0.2]], "couleur": "faible"}]
    for i, c in enumerate(cods):
        col, r = divmod(i, par); x0 = 0.3 + col * 5.1; y = h - 1.2 - r * 0.6
        a = CODE[c]
        els.append({"f": "texte", "at": [x0 + 1.0, y], "t": c, "couleur": "blanc"})
        els.append({"f": "texte", "at": [x0 + 3.2, y], "t": "codon stop" if a == 'Stop' else a, "couleur": "rouge" if a == 'Stop' else "vert"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 10.4, "h": round(h, 2)},
            "legende": "Extrait du tableau du code génétique : codons de l'ARNm et acides aminés correspondants.", "elements": els}

def donnees(arn, extrait):
    lignes = [f"ARNm : 5′ {arn} 3′"]
    lignes.append("Extrait du code génétique : " + " ; ".join(f"{c} : {'codon stop' if CODE[c] == 'Stop' else CODE[c]}" for c in extrait.split()))
    noms = sorted({CODE[c] for c in extrait.split() if CODE[c] != 'Stop'})
    lignes.append("Abréviations : " + " ; ".join(f"{a} = {NOMS[a]}" for a in noms))
    return lignes

MOTS = {"1": "un", "2": "deux", "3": "trois", "4": "quatre"}

def q1(arn, aas, stop):
    att = f"Codons : {arn}. Séquence d'acides aminés : {chaine(aas)} ; {stop} est un codon stop : arrêt de la traduction (aucun acide aminé)."
    corr = {"lignes": [
        {"texte": f"1 : codons : {arn}", "mot": "كنقسمو l'A R N messager"},
        {"texte": f"acides aminés : {chaine(aas)}", "mot": "كتعطي"},
        {"texte": f"{stop} : codon stop, arrêt de la traduction", "mot": "ما كيعطي حتى acide aminé"}],
        "parole": f"question un. كنقسمو l'A R N messager ل des codons، à partir de cinq prime: {epele(arn)}. كل codon، كنقلبو عليه ف le tableau. la séquence كتعطي: {noms_dits(aas)}. والأخير، {' '.join(stop)}، هو codon stop: ما كيعطي حتى acide aminé، و la traduction كتحبس."}
    return att, corr

def q2(stop):
    att = f"Le premier codon AUG est le codon d'initiation : il code la méthionine (Met) et marque le début de la traduction. Le dernier codon {stop} est un codon stop (non-sens) : il ne code aucun acide aminé et marque la fin de la traduction (la chaîne d'acides aminés est libérée)."
    corr = {"lignes": [
        {"texte": "2 : AUG : codon d'initiation, code la méthionine (Met), début de la traduction", "mot": "le codon d'initiation"},
        {"texte": f"{stop} : codon stop (non-sens), aucun acide aminé", "mot": "codon stop"},
        {"texte": "fin de la traduction : la chaîne est libérée", "mot": "la chaîne كتخرج"}],
        "parole": f"question deux. A U G هو le codon d'initiation: كيعطي la méthionine، و منو كتبدا la traduction. {' '.join(stop)} هو un codon stop: ما كيعطي حتى acide aminé. تما كتسالي la traduction، و la chaîne كتخرج من le ribosome."}
    return att, corr

def q3(aa, cod, anti):
    att = f"L'{NOMS[aa]} ({aa}) correspond au codon {cod} de l'ARNm. L'anticodon de l'ARNt qui l'apporte est complémentaire de ce codon : {anti}."
    corr = {"lignes": [
        {"texte": f"3 : {aa} ← codon {cod} de l'ARNm", "mot": f"le codon ديال l'{NOMS[aa]}"},
        {"texte": "l'anticodon est complémentaire du codon (A–U, C–G)", "mot": "l'anticodon complémentaire"},
        {"texte": f"anticodon : {anti}", "mot": f"إذن l'anticodon هو {' '.join(anti)}"}],
        "parole": f"question trois. le codon ديال l'{NOMS[aa]} ف l'A R N messager هو {' '.join(cod)}. l'anticodon complémentaire مع le codon: قدام A، U. قدام U، A. قدام C، G. قدام G، C. إذن l'anticodon هو {' '.join(anti)}. ماشي باش نقلبو عليه ف le tableau."}
    return att, corr

ATT4 = "La traduction a lieu dans le cytoplasme, sur les ribosomes. Le ribosome se fixe sur l'ARNm au codon AUG puis avance codon par codon, de 5′ vers 3′ ; il lie les acides aminés les uns aux autres par des liaisons peptidiques. Chaque ARNt apporte un acide aminé précis et le place en face du bon codon grâce à son anticodon, complémentaire du codon."
CLAV4 = {"aides": ["cytoplasme", "ribosome", "codon par codon", "liaison peptidique", "ARNt", "anticodon"], "pieges": ["noyau", "ARN polymérase"]}
CORR4 = {"lignes": [
    {"texte": "4 : lieu : le cytoplasme, sur les ribosomes", "mot": "ف le cytoplasme"},
    {"texte": "ribosome : lit l'ARNm codon par codon (5′ → 3′) et lie les acides aminés (liaisons peptidiques)", "mot": "le ribosome كيقرا l'A R N messager"},
    {"texte": "ARNt : apporte un acide aminé précis, placé grâce à son anticodon", "mot": "l'A R N de transfert كيجيب"}],
    "parole": "question quatre. la traduction كتوقع ف le cytoplasme، ف les ribosomes. le ribosome كيقرا l'A R N messager، codon par codon، de cinq prime vers trois prime، وكيربط les acides aminés ب des liaisons peptidiques. l'A R N de transfert كيجيب un acide aminé، وكيحطو قدام le codon الصحيح، ب l'anticodon ديالو."}

Q1_T = "En vous basant sur l'extrait du code génétique, donner la séquence des acides aminés correspondant à ce fragment d'ARNm."
Q2_T = "Nommer le premier codon et le dernier codon de ce fragment, puis préciser le rôle de chacun dans la traduction."
Q3_T = lambda aa: f"L'{NOMS[aa]} est apportée au ribosome par un ARNt. Donner l'anticodon de cet ARNt. Justifier."
Q4_T = "Préciser le lieu de la traduction dans la cellule, puis le rôle des ribosomes et celui des ARNt."

A1, C1 = q1(ARN, AA_ARN, STOP); A2, C2 = q2(STOP); A3, C3 = q3(AA_Q3, COD_Q3, ANTI)
A1b, C1b = q1(ARN_B, AA_B, STOP_B); A2b, C2b = q2(STOP_B); A3b, C3b = q3(AA_Q3B, COD_Q3B, ANTI_B)

EX = {
  "id": "svt_ex_ch4_traduction_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "relation_gene_proteine", "cours": "svt_ch4_relation_gene_proteine",
  "titre": "De l'ARNm à la chaîne d'acides aminés : la traduction", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Utiliser le tableau du code génétique", "Reconnaître le codon d'initiation et le codon stop", "Expliquer le rôle des ribosomes et des ARNt"],
  "enonce": {
    "intro": "Un ARNm est sorti du noyau d'une cellule et se trouve dans le cytoplasme. Le document 1 représente un fragment de cet ARNm, orienté de 5′ vers 3′ et découpé en codons. Le document 2 donne un extrait du tableau du code génétique.",
    "intro_dit": "نقراو l'énoncé. un A R N messager خرج من le noyau، ودابا كاين ف le cytoplasme. le document un فيه un fragment ديال هاد l'A R N messager، de cinq prime vers trois prime، مقسوم ل des codons. و le document deux فيه جزء من le tableau du code génétique.",
    "figures": [fig_arnm(ARN, "Document 1 : fragment d'ARNm"), fig_code(EXTRAIT, "Document 2 : extrait du code génétique")],
    "donnees": donnees(ARN, EXTRAIT),
    "questions": [
      {"id": "1", "texte": Q1_T,
       "texte_dit": "question un: اعتمد على le tableau du code génétique، وعطي la séquence ديال les acides aminés اللي كتقابل هاد le fragment ديال l'A R N messager.",
       "reponse": {"type": "phrase", "attendu": A1},
       "clavier": {"aides": ["Met", "–", "codon stop", "arrêt de la traduction", "Phe", "Gly"], "pieges": ["– Stop", "Val"]},
       "aides": [
         {"texte": "Les codons sont déjà séparés. Cherche chaque codon de l'ARNm, un par un, dans le document 2.",
          "dit": "les codons مفرقين. قلب على كل codon ديال l'A R N messager، واحد ب واحد، ف le document deux."},
         {"texte": "Écris l'acide aminé sous chaque codon, reliés par des tirets. Au codon stop, n'écris pas d'acide aminé : écris « arrêt de la traduction ».",
          "dit": "كتب l'acide aminé تحت كل codon، وربطهم ب des tirets. ملي توصل ل le codon stop، ما تكتب حتى acide aminé: كتب arrêt de la traduction."}],
       "correction": C1, "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": Q2_T,
       "texte_dit": "question deux: سمي le premier codon و le dernier codon ديال هاد le fragment، ومن بعد قول شنو الدور ديال كل واحد ف la traduction.",
       "reponse": {"type": "phrase", "attendu": A2},
       "clavier": {"aides": ["codon d'initiation", "méthionine (Met)", "codon stop", "non-sens", "aucun acide aminé"], "pieges": ["Stop est un acide aminé"]},
       "aides": [
         {"texte": "Le premier codon est AUG, le dernier est UAG. Que lis-tu en face de chacun dans le document 2 ?",
          "dit": "le premier codon هو A U G، و le dernier هو U A G. شنو كتقرا قدام كل واحد ف le document deux؟"},
         {"texte": "Un codon commence toujours la traduction et donne la méthionine ; un autre ne donne aucun acide aminé et l'arrête. Donne leurs noms.",
          "dit": "كاين codon ديما كتبدا بيه la traduction، وكيعطي la méthionine. وكاين codon ما كيعطي حتى acide aminé، وكيحبسها. عطي السمية ديال كل واحد."}],
       "correction": C2, "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": Q3_T(AA_Q3),
       "texte_dit": f"question trois: l'{NOMS[AA_Q3]} كيجيبها ل le ribosome un A R N de transfert. عطي l'anticodon ديال هاد l'A R N de transfert، وبرر.",
       "reponse": {"type": "phrase", "attendu": A3},
       "clavier": {"aides": ["codon", "anticodon", "complémentaire", "A–U", "C–G"], "pieges": ["chercher l'anticodon dans le tableau", "T"]},
       "aides": [
         {"texte": f"Trouve d'abord le codon de l'ARNm qui donne l'{NOMS[AA_Q3]} ({AA_Q3}) dans le document 1.",
          "dit": f"قلب اللول على le codon ديال l'A R N messager اللي كيعطي l'{NOMS[AA_Q3]}، ف le document un."},
         {"texte": "L'anticodon est complémentaire du codon : A en face de U, U en face de A, C en face de G, G en face de C. Ne le cherche pas dans le tableau.",
          "dit": "l'anticodon complémentaire مع le codon: A قدام U، U قدام A، C قدام G، و G قدام C. ما تقلبش عليه ف le tableau."}],
       "correction": C3, "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": Q4_T,
       "texte_dit": "question quatre: حدد فين كتوقع la traduction ف la cellule، ومن بعد الدور ديال les ribosomes، والدور ديال les A R N de transfert.",
       "reponse": {"type": "phrase", "attendu": ATT4}, "clavier": CLAV4,
       "aides": [
         {"texte": "L'ARNm est sorti du noyau : où sont les organites qui le lisent ?",
          "dit": "l'A R N messager خرج من le noyau: فين كاينين les organites اللي كيقراوه؟"},
         {"texte": "Ribosome : que fait-il le long de l'ARNm, et que fait-il avec les acides aminés ? ARNt : qu'apporte-t-il, et comment trouve-t-il le bon codon ?",
          "dit": "le ribosome: شنو كيدير على طول l'A R N messager، وشنو كيدير ب les acides aminés؟ l'A R N de transfert: شنو كيجيب، وكيفاش كيلقى le codon الصحيح؟"}],
       "correction": CORR4, "explication": "ex_s4", "facile": "fa_s4"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : lire le tableau, codon par codon",
     "screen_content": {"lead": f"5′ {ARN} 3′ → {chaine(AA_ARN)}, puis arrêt."},
     "visual": {"kind": "simulation", "url": TABLEAU, "caption": "L'ARNm de l'exercice et le tableau du code génétique"},
     "speech_text": {"mixed": f"هادا l'A R N messager ديالنا، و هادا le tableau du code génétique. ناخدو le premier codon، A U G. الحرف اللول كيعطي السطر. الحرف الثاني كيعطي العمود. والحرف الثالث كيعطي la case. ف la case، كنقراو la méthionine، وكنكتبوها تحت le codon. les codons اللي من بعد كيتقراو بنفس الطريقة: {noms_dits(AA_ARN[1:])}. والأخير، U A G، codon stop: ما كيعطي حتى acide aminé، وكنكتبو arrêt."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "1re lettre : ligne ; 2e : colonne ; 3e : case", "mot": "والحرف الثالث كيعطي la case"},
                  {"texte": chaine(AA_ARN), "mot": "بنفس الطريقة"},
                  {"texte": f"{STOP} : codon stop → arrêt", "mot": "ما كيعطي حتى acide aminé"}],
       "pointage": [{"mot": "هادا l'A R N messager ديالنا", "commande": "set_parameters", "parametres": {"arnm": ARN}},
                    {"mot": "هادا l'A R N messager ديالنا", "repere": "arnm"},
                    {"mot": "و هادا le tableau du code génétique", "commande": "play_until", "parametres": {"moment": "tableau"}},
                    {"mot": "ناخدو le premier codon", "commande": "play_until", "parametres": {"moment": "premier_codon"}},
                    {"mot": "الحرف اللول كيعطي السطر", "commande": "play_until", "parametres": {"moment": "ligne"}},
                    {"mot": "الحرف الثاني كيعطي العمود", "commande": "play_until", "parametres": {"moment": "colonne"}},
                    {"mot": "والحرف الثالث كيعطي la case", "commande": "play_until", "parametres": {"moment": "case"}},
                    {"mot": "والحرف الثالث كيعطي la case", "cible": "centre:0"},
                    {"mot": "كنقراو la méthionine", "commande": "play_until", "parametres": {"moment": "acide_amine_ecrit"}},
                    {"mot": "بنفس الطريقة", "commande": "play_until", "parametres": {"moment": "codons_suivants"}},
                    {"mot": "بنفس الطريقة", "cible": "centre:1"},
                    {"mot": "codon stop", "commande": "play_until", "parametres": {"moment": "codon_stop"}},
                    {"mot": "ما كيعطي حتى acide aminé", "cible": "centre:2"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : le codon d'initiation et le codon stop",
     "screen_content": {"lead": f"AUG : début, méthionine. {STOP} : codon stop, aucun acide aminé."},
     "visual": {"kind": "simulation", "url": TABLEAU, "caption": "AUG au début, le codon stop à la fin"},
     "speech_text": {"mixed": f"شوف le premier codon: A U G. هو le codon d'initiation: كيعطي la méthionine، و منو كتبدا la traduction. دابا شوف le dernier: U A G. ف le tableau، la case ديالو مكتوب فيها stop. ما كيعطي حتى acide aminé: هو un codon stop، أو codon non-sens. تما كتحبس la traduction. عقل: les codons stop هوما U A A، U A G، و U G A."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "AUG : codon d'initiation (Met)", "mot": "هو le codon d'initiation"},
                  {"texte": f"{STOP} : codon stop, aucun acide aminé", "mot": "هو un codon stop"},
                  {"texte": "codons stop : UAA, UAG, UGA", "mot": "les codons stop هوما"}],
       "pointage": [{"mot": "شوف le premier codon", "commande": "set_parameters", "parametres": {"arnm": ARN}},
                    {"mot": "شوف le premier codon", "commande": "set_time", "parametres": {"time_s": 20.0}},
                    {"mot": "هو le codon d'initiation", "commande": "play_until", "parametres": {"moment": "initiation"}},
                    {"mot": "هو le codon d'initiation", "cible": "centre:0"},
                    {"mot": "دابا شوف le dernier", "commande": "play_until", "parametres": {"moment": "codon_stop"}},
                    {"mot": "هو un codon stop", "cible": "centre:1"},
                    {"mot": "les codons stop هوما", "cible": "centre:2"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : l'anticodon, complémentaire du codon",
     "screen_content": {"lead": f"Codon {COD_Q3} ({AA_Q3}) → anticodon {ANTI}."},
     "visual": {"kind": "simulation", "url": TRAD, "caption": "L'ARNt : un acide aminé en haut, l'anticodon en bas"},
     "speech_text": {"mixed": f"شوف l'A R N de transfert. لفوق، كيهز un acide aminé. لتحت، كاينين les trois bases ديال l'anticodon. l'anticodon كيتحط قدام le codon، وهو complémentaire معاه. هنا، قدام le codon C G C، كيجي l'anticodon G C G، وكيجيب l'arginine. ف التمرين ديالنا، le codon ديال l'{NOMS[AA_Q3]} هو {' '.join(COD_Q3)}. إذن l'anticodon هو {' '.join(ANTI)}. le tableau فيه غير les codons ديال l'A R N messager، ماشي les anticodons."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "anticodon = complémentaire du codon", "mot": "وهو complémentaire معاه"},
                  {"texte": f"codon {COD_Q3} ({AA_Q3}) → anticodon {ANTI}", "mot": f"إذن l'anticodon هو {' '.join(ANTI)}"},
                  {"texte": "le tableau donne des codons, pas des anticodons", "mot": "ماشي les anticodons"}],
       "pointage": [{"mot": "شوف l'A R N de transfert", "commande": "play_until", "parametres": {"moment": "acteurs"}},
                    {"mot": "وهو complémentaire معاه", "cible": "centre:0"},
                    {"mot": "قدام le codon C G C", "commande": "set_time", "parametres": {"time_s": 11.9}},
                    {"mot": "قدام le codon C G C", "commande": "play_until", "parametres": {"moment": "arnt_2_arrive"}},
                    {"mot": f"إذن l'anticodon هو {' '.join(ANTI)}", "cible": "centre:1"},
                    {"mot": "ماشي les anticodons", "cible": "centre:2"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le ribosome et les ARNt au travail",
     "screen_content": {"lead": "Dans le cytoplasme : le ribosome avance codon par codon, les ARNt apportent les acides aminés."},
     "visual": {"kind": "simulation", "url": TRAD, "caption": "Initiation, élongation, terminaison"},
     "speech_text": {"mixed": "حنا ف le cytoplasme. la petite sous-unité ديال le ribosome كتشد ف l'A R N messager، ف le codon A U G. كيجي l'A R N de transfert ديال la méthionine، ومن بعد la grande sous-unité. من بعد كيجي l'A R N de transfert الثاني، وكتكون la liaison peptidique بين les deux acides aminés. le ribosome كيتقدم، codon par codon، vers trois prime، وكنعاودو. ملي كيوصل ل un codon stop، la chaîne كتخرج، و les deux sous-unités كيتفرقو."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "lieu : cytoplasme, ribosomes", "mot": "حنا ف le cytoplasme"},
                  {"texte": "ARNt : apporte l'acide aminé (anticodon)", "mot": "كيجي l'A R N de transfert الثاني"},
                  {"texte": "ribosome : avance codon par codon, liaisons peptidiques", "mot": "le ribosome كيتقدم"}],
       "pointage": [{"mot": "حنا ف le cytoplasme", "commande": "set_time", "parametres": {"time_s": 5.2}},
                    {"mot": "حنا ف le cytoplasme", "cible": "centre:0"},
                    {"mot": "la petite sous-unité", "commande": "play_until", "parametres": {"moment": "petite_sous_unite"}},
                    {"mot": "ديال la méthionine", "commande": "play_until", "parametres": {"moment": "arnt_met"}},
                    {"mot": "la grande sous-unité", "commande": "play_until", "parametres": {"moment": "grande_sous_unite"}},
                    {"mot": "كيجي l'A R N de transfert الثاني", "commande": "play_until", "parametres": {"moment": "arnt_2_arrive"}},
                    {"mot": "كيجي l'A R N de transfert الثاني", "cible": "centre:1"},
                    {"mot": "وكتكون la liaison peptidique", "commande": "play_until", "parametres": {"moment": "liaison_peptidique"}},
                    {"mot": "le ribosome كيتقدم", "commande": "play_until", "parametres": {"moment": "avance_codon"}},
                    {"mot": "le ribosome كيتقدم", "cible": "centre:2"},
                    {"mot": "ملي كيوصل ل un codon stop", "commande": "play_until", "parametres": {"moment": "codon_stop"}},
                    {"mot": "la chaîne كتخرج", "commande": "play_until", "parametres": {"moment": "chaine_liberee"}},
                    {"mot": "كيتفرقو", "commande": "play_until", "parametres": {"moment": "dissociation"}}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : un ARNm court", "نتمرنو ب A R N messager قصير.",
      "Avec l'extrait du document 2, l'ARNm 5′ AUG GGA AAA UAG 3′ donne…", ["Met – Gly – Lys – Stop", "Met – Gly – Lys, puis arrêt", "Met – Gly – Lys – Leu"], 1, {
        "1": {"juste": rep("برافو! la méthionine، la glycine، la lysine، ومن بعد U A G codon stop: ما كيعطي حتى acide aminé.", "Juste : Met – Gly – Lys, puis UAG : arrêt de la traduction.")},
        "0": {"1": rep("قريب! ولكن stop ماشي acide aminé. واش كنكتبوه ف la chaîne؟ عاود اختار.", "Presque : « Stop » n'est pas un acide aminé. L'écrit-on dans la chaîne ? Réessaie."),
              "2": rep("الجواب هو Met، Gly، Lys، ومن بعد arrêt. le codon stop ما كيعطي حتى acide aminé، إذن ما كنكتبوش stop ف la chaîne.", "Réponse : Met – Gly – Lys, puis arrêt ; le codon stop ne donne aucun acide aminé.")},
        "2": {"1": rep("لا، U A G ما كاينش ف السطر ديال la leucine. شوف le document deux: شنو مكتوب قدام U A G؟ عاود اختار.", "UAG ne code pas Leu. Que lis-tu en face de UAG dans le document 2 ? Réessaie."),
              "2": rep("الجواب هو Met، Gly، Lys، ومن بعد arrêt. U A G هو codon stop.", "Réponse : Met – Gly – Lys, puis arrêt : UAG est un codon stop.")}},
      "l'A R N messager، A U G، G G A، A A A، U A G، كيعطي شنو؟"),
    association("fa_s2", "Plus facile : chaque codon et son rôle", "Relie chaque codon à son rôle.",
      "سؤال ساهل: ربط كل codon مع الدور ديالو.", "Relie chaque codon de l'ARNm à ce qu'il fait pendant la traduction.",
      [("1", "AUG"), ("2", STOP), ("3", COD_Q3)],
      [("a", "Codon d'initiation : méthionine"), ("b", "Codon stop : aucun acide aminé"), ("c", f"Code l'{NOMS[AA_Q3]} ({AA_Q3})"), ("d", "Code la valine (Val)")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : AUG commence la traduction et donne Met.", "برافو: A U G كتبدا بيه la traduction، وكيعطي la méthionine."),
       "1-b": (False, "AUG donne un acide aminé, la méthionine : ce n'est pas un stop.", "لا، A U G كيعطي la méthionine. ماشي stop."),
       "1-c": (False, f"AUG ne code pas l'{NOMS[AA_Q3]} : regarde sa ligne dans le tableau.", "لا، شوف السطر ديال A U G ف le tableau."),
       "1-d": (False, "AUG ne code pas la valine : regarde le tableau.", "لا، A U G ما كيعطيش la valine. شوف le tableau."),
       "2-a": (False, f"{STOP} ne donne pas la méthionine : regarde ce qui est écrit en face de lui.", "لا، شوف شنو مكتوب قدامو ف le tableau."),
       "2-b": (True, f"Oui : {STOP} est un codon stop, la traduction s'arrête.", "برافو: هادا codon stop، la traduction كتحبس."),
       "2-c": (False, f"{STOP} ne code aucun acide aminé.", "لا، هادا ما كيعطي حتى acide aminé."),
       "2-d": (False, f"{STOP} ne code aucun acide aminé, pas même la valine.", "لا، هادا ما كيعطي حتى acide aminé."),
       "3-a": (False, f"{COD_Q3} n'est pas le codon d'initiation : c'est AUG.", "لا، le codon d'initiation هو A U G."),
       "3-b": (False, f"{COD_Q3} donne un acide aminé : ce n'est pas un stop.", "لا، هادا كيعطي acide aminé. ماشي stop."),
       "3-c": (True, f"Oui : {COD_Q3} code l'{NOMS[AA_Q3]}.", f"برافو: هادا le codon ديال l'{NOMS[AA_Q3]}."),
       "3-d": (False, f"La valine est codée par {ANTI} dans l'extrait, pas par {COD_Q3} : tu as peut-être pensé à l'anticodon.", "لا، la valine عندها codon آخر. يمكن خلطتي مع l'anticodon.")},
      (f"(1 ; a) (2 ; b) (3 ; c) : AUG début (Met), {STOP} fin, {COD_Q3} = {AA_Q3}.",
       f"A U G le début، {' '.join(STOP)} la fin، و {' '.join(COD_Q3)} كيعطي l'{NOMS[AA_Q3]}.")),
    qcm_facile("fa_s3", "Plus facile : l'anticodon", "سؤال ساهل على l'anticodon.",
      f"Le codon {COD_Q3} est lu par un ARNt dont l'anticodon est…", [ANTI, COD_Q3, "GTA"], 0, {
        "0": {"juste": rep(f"برافو! l'anticodon complémentaire مع le codon: {' '.join(ANTI)}.", f"Juste : l'anticodon {ANTI} est complémentaire du codon {COD_Q3}.")},
        "1": {"1": rep("لا، هادا هو le codon براسو. l'anticodon خاصو يكون complémentaire معاه. عاود اختار.", "C'est le codon lui-même ; l'anticodon lui est complémentaire. Réessaie."),
              "2": rep(f"الجواب هو {' '.join(ANTI)}: قدام C، G. قدام A، U. قدام U، A.", f"Réponse : {ANTI} (complémentaire de {COD_Q3}).")},
        "2": {"1": rep("قريب! ولكن l'A R N de transfert هو A R N: واش فيه T؟ عاود اختار.", "Presque : un ARNt est un ARN ; contient-il des T ? Réessaie."),
              "2": rep(f"الجواب هو {' '.join(ANTI)}. l'A R N de transfert ما فيه حتى T، فيه U.", f"Réponse : {ANTI} ; pas de T dans un ARN.")}},
      f"le codon {' '.join(COD_Q3)}، شنو هو l'anticodon ديالو؟"),
    vrai_faux("fa_s4", "Plus facile : qui fait quoi ?", "Vrai ou faux : la traduction.",
      "سؤال ساهل: صحيح ولا خطأ، على la traduction.", [
        ("La traduction a lieu dans le noyau.", False, "Faux : elle a lieu dans le cytoplasme, sur les ribosomes."),
        ("Le ribosome lit l'ARNm codon par codon, de 5′ vers 3′.", True, "Vrai : il avance d'un codon à la fois vers 3′."),
        ("Chaque ARNt apporte un acide aminé précis.", True, "Vrai : l'ARNt porte l'acide aminé qui correspond à son anticodon."),
        ("L'ARN polymérase lie les acides aminés entre eux.", False, "Faux : l'ARN polymérase agit dans la transcription ; les acides aminés sont liés sur le ribosome (liaisons peptidiques).")])
  ]}]},
  "similaire": {
    "id": "svt_ex_ch4_traduction_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Un autre ARNm se trouve dans le cytoplasme. Le document 1 représente un fragment de cet ARNm, orienté de 5′ vers 3′ et découpé en codons ; le document 2 donne un extrait du tableau du code génétique.",
      "intro_dit": "نفس التمرين، ب A R N messager آخر. le document un فيه le fragment، و le document deux فيه جزء من le tableau du code génétique.",
      "figures": [fig_arnm(ARN_B, "Document 1 : fragment d'ARNm"), fig_code(EXTRAIT_B, "Document 2 : extrait du code génétique")],
      "donnees": donnees(ARN_B, EXTRAIT_B),
      "questions": [
        {"id": "1", "texte": Q1_T, "reponse": {"type": "phrase", "attendu": A1b},
         "clavier": {"aides": ["Met", "–", "codon stop", "arrêt de la traduction"], "pieges": ["– Stop"]}, "correction": C1b},
        {"id": "2", "texte": Q2_T, "reponse": {"type": "phrase", "attendu": A2b},
         "clavier": {"aides": ["codon d'initiation", "méthionine (Met)", "codon stop", "aucun acide aminé"], "pieges": ["Stop est un acide aminé"]}, "correction": C2b},
        {"id": "3", "texte": Q3_T(AA_Q3B), "reponse": {"type": "phrase", "attendu": A3b},
         "clavier": {"aides": ["codon", "anticodon", "complémentaire"], "pieges": ["chercher l'anticodon dans le tableau"]}, "correction": C3b},
        {"id": "4", "texte": Q4_T, "reponse": {"type": "phrase", "attendu": ATT4}, "clavier": CLAV4, "correction": CORR4}
      ]}}
}
ecrire(EX, sys.argv[1])
