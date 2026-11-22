# Exercice SVT ch. 4 (relation gène – protéine), niveau difficile (« Supérieur ») : quatre allèles d'un même gène comparés
# (mutation silencieuse, deux faux-sens aux effets différents), couleur des pétales d'une plante.
# Entraîne : gène, allèle, locus sur une paire de chromosomes homologues ; ARNm et acides aminés de quatre allèles (brin non
# transcrit) ; nommer chaque mutation ; redondance du code (mutation silencieuse) ; exploiter un tableau d'activité de l'enzyme ;
# raisonnement critique (« une mutation change toujours le caractère » est faux, a_ne_pas_dire de l'exploration).
# Pas d'homozygote / hétérozygote ni de dominance (non enseignés dans ce cours) : chaque plante du document 2 porte le même
# allèle sur les deux chromosomes de la paire.
# Sources comparées (lecture seule, rien de copié) :
# - exploration/relation_gene_proteine.json : RGP1 (gène, allèle, locus), RGP6 (code redondant), RGP9 (silencieuse, faux-sens,
#   non-sens) ; pièges « dit qu'une mutation donne toujours une maladie », « prend une mutation silencieuse pour une mutation sans
#   changement de l'ADN » (AJIN9RAW 01:33:13), « confond gène et allèle » ; NC1 (gène, allèle, locus) ; restitution 2018 R.
# - nationaux : 2018 R (définir allèle et mutation), 2021 N, 2022 R, 2025 R (génotype → phénotype) : formes « comparez »,
#   « déduisez », « justifiez » ; aucun ne compare quatre allèles d'un gène de pigment.
# - séries en ligne : recherche faite (dyrassa série 7, alloschool N. Bahsina, moutamadris cours 2 bac), PDF non ouverts
#   (domaines bloqués par le réseau de la session) : titres et extraits seulement.
# Situation inventée (gène F d'une enzyme E du pigment rouge d'une plante à fleurs), séquences et activités inventées.
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




def fig_tableau(titre, xs, entetes, lignes, legende):
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


def cas(debut, f1, mutations, activites, couleurs):
    """f1 : triplets du brin non transcrit ; mutations : {"F2": (j, nouveau triplet), ...} (F2 silencieuse, F3 et F4 faux-sens)."""
    C = {"debut": debut, "seq": {"F1": f1}, "act": activites, "coul": couleurs}
    for k, (jj, t) in mutations.items():
        C["seq"][k] = f1[:jj] + [t] + f1[jj + 1:]
        assert sum(a != b for a, b in zip(f1[jj], t)) == 1
    C["arn"] = {k: [arn(c) for c in v] for k, v in C["seq"].items()}
    C["aa"] = {k: [aa(c) for c in v] for k, v in C["seq"].items()}
    for v in C["aa"].values(): assert "Stop" not in v
    C["j"] = {k: jj for k, (jj, t) in mutations.items()}
    C["pos"] = {k: next(i for i in range(3) if f1[jj][i] != t[i]) for k, (jj, t) in mutations.items()}
    assert C["aa"]["F2"] == C["aa"]["F1"]                                          # silencieuse
    for k in ("F3", "F4"):
        d = [i for i in range(len(f1)) if C["aa"][k][i] != C["aa"]["F1"][i]]; assert d == [C["j"][k]]   # faux-sens
    return C


A = cas(11, ["TCA", "GGA", "ACT", "TGG", "CAT", "GAA", "AAC"], {"F2": (2, "ACC"), "F3": (4, "CGT"), "F4": (5, "GAT")},
        {"F1": 100, "F2": 100, "F3": 0, "F4": 97}, {"F1": "rouge", "F2": "rouge", "F3": "blanche", "F4": "rouge"})
assert A["aa"]["F1"] == ["Ser", "Gly", "Thr", "Trp", "His", "Glu", "Asn"] and A["aa"]["F3"][4] == "Arg" and A["aa"]["F4"][5] == "Asp"
B = cas(21, ["GCC", "TTA", "GGT", "CAC", "AAG", "TCT", "GAC"], {"F2": (2, "GGA"), "F3": (5, "TTT"), "F4": (4, "AGG")},
        {"F1": 100, "F2": 100, "F3": 0, "F4": 95}, {"F1": "rouge", "F2": "rouge", "F3": "blanche", "F4": "rouge"})
assert B["aa"]["F1"] == ["Ala", "Leu", "Gly", "His", "Lys", "Ser", "Asp"] and B["aa"]["F3"][5] == "Phe" and B["aa"]["F4"][4] == "Arg"

j = lambda xs: " ".join(xs)
tiret = lambda xs: " – ".join(xs)
RANG = ["1er", "2e", "3e"]


def extrait_code(C, plus):
    cs = sorted({c for v in C["arn"].values() for c in v} | set(plus))
    return "Extrait du code génétique : " + " ; ".join(f"{c} : {AB[CODE[c]]}" for c in cs)


def figures(C):
    d = C["debut"]
    return [fig_sequences("Document 1 : brin non transcrit (5′ → 3′)", d, [(k, C["seq"][k], "blanc") for k in ("F1", "F2", "F3", "F4")],
                          "Quatre allèles du gène F (F1 : allèle de référence)."),
            fig_tableau("Document 2 : enzyme E et couleur des pétales", [0, 24, 62, 100], ["Allèle", "Activité de E", "Pétales"],
                        [[[k], [f"{C['act'][k]} % de F1"], [C["coul"][k]]] for k in ("F1", "F2", "F3", "F4")],
                        "Chaque plante porte le même allèle sur les deux chromosomes de la paire.")]


def donnees(C, plus):
    d = C["debut"]
    return [f"{k} (brin non transcrit, 5′ → 3′) : {j(C['seq'][k])}" for k in ("F1", "F2", "F3", "F4")] + [
            f"Triplets {d} à {d + 6}.", "L'enzyme E transforme une substance incolore en pigment rouge dans les cellules des pétales.", extrait_code(C, plus)]


def lignes_arn(C):
    return " ".join(f"{k} : ARNm {j(C['arn'][k])} → {tiret(C['aa'][k])}." for k in ("F1", "F2", "F3", "F4"))


def types(C):
    d = C["debut"]; s = C["seq"]; f1 = s["F1"]
    def un(k):
        jj = C["j"][k]; return f"{k} : triplet {d + jj} : {f1[jj]} → {s[k][jj]} ({RANG[C['pos'][k]]} nucléotide), codon {arn(f1[jj])} ({aa(f1[jj])}) → {arn(s[k][jj])} ({aa(s[k][jj])})"
    return f"{un('F2')} : substitution silencieuse. {un('F3')} : substitution faux-sens. {un('F4')} : substitution faux-sens."


DOC = "/media/simulations/svt/relation_gene_proteine-tableau/"
PAIRE, BRINS, MUT, PROP = DOC + "paire_homologues.html?vue=paire", DOC + "transcription.html?vue=brins", DOC + "mutation.html?vue=mutation", DOC + "code_genetique.html?vue=proprietes"
S = A["seq"]

EX = {
  "id": "svt_ex_ch4_alleles_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "relation_gene_proteine", "cours": "svt_ch4_relation_gene_proteine",
  "titre": "Quatre allèles pour la couleur d'une fleur", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Situer les allèles d'un gène sur une paire de chromosomes homologues", "Écrire l'ARNm et les acides aminés de plusieurs allèles",
                  "Nommer une mutation silencieuse ou faux-sens", "Expliquer la redondance du code génétique",
                  "Relier la séquence d'une protéine à son activité et au caractère", "Critiquer une affirmation à partir de résultats"],
  "enonce": {
    "intro": ("Chez une plante à fleurs, la couleur rouge des pétales est due à un pigment. Ce pigment est fabriqué par une enzyme E, codée par un gène F. "
              "On a trouvé quatre allèles de ce gène : F1 (allèle de référence), F2, F3 et F4. "
              f"Document 1 : extrait du brin non transcrit des quatre allèles (triplets {A['debut']} à {A['debut'] + 6} ; séquences simplifiées pour l'exercice). "
              "Document 2 : activité de l'enzyme E et couleur des pétales de plantes qui portent le même allèle sur les deux chromosomes de la paire."),
    "intro_dit": ("نقراو l'énoncé. عند واحد النبتة، اللون الحمر ديال les pétales جاي من un pigment. هاد le pigment كتصاوبو une enzyme E، و le gène ديالها هو le gène F. "
                  "لقاو les quatre allèles ديال هاد le gène: F un، F deux، F trois، و F quatre. "
                  "le document un: جزء من le brin non transcrit ديال les quatre allèles. "
                  "le document deux: l'activité ديال l'enzyme E، و اللون ديال les pétales، عند نباتات كل وحدة فيها نفس l'allèle ف les deux chromosomes ديال la paire."),
    "figures": figures(A),
    "donnees": donnees(A, ["AUG", "UAA", "CAC", "GAG"]),
    "questions": [
      {"id": "1", "texte": "Définir un allèle, puis préciser où sont situés les allèles F1 à F4 et combien d'allèles du gène F porte une cellule de cette plante. Justifier.",
       "texte_dit": "la question un: عرف l'allèle، ومن بعد قول فين كاينين les allèles، من F un حتى ل F quatre، و شحال من allèle ديال le gène F كاين ف خلية وحدة ديال هاد النبتة. برر.",
       "reponse": {"type": "phrase", "attendu": ("Un allèle est une des formes d'un même gène, située au même locus. F1, F2, F3 et F4 sont quatre formes du gène F : "
                                                 "ils occupent tous le même locus, sur une paire de chromosomes homologues. Une cellule porte deux chromosomes de cette paire "
                                                 "(l'un venu du père, l'autre de la mère), donc deux allèles du gène F seulement (identiques ou différents), jamais quatre.")},
       "clavier": {"aides": ["une des formes d'un même gène", "même locus", "chromosomes homologues", "deux allèles"], "pieges": ["un allèle est un caractère", "quatre allèles par cellule"]},
       "aides": [
         {"texte": "Allèle, gène, locus : relis la définition du cours. Le gène est une portion d'ADN à une place précise d'un chromosome.",
          "dit": "عاود قرا la définition ديال الدرس. le gène هو portion d'A D N، ف بلاصة محددة ف le chromosome."},
         {"texte": "Dans une cellule, combien de chromosomes de la même paire ? Chacun porte un allèle au locus du gène F.",
          "dit": "ف la cellule، شحال من chromosome ديال نفس la paire؟ كل واحد فيه allèle واحد ف le locus ديال le gène F."}],
       "correction": {"lignes": [
           {"texte": "1 : allèle : une des formes d'un même gène, au même locus", "mot": "une des formes d'un même gène"},
           {"texte": "F1 à F4 : même locus, sur une paire de chromosomes homologues", "mot": "نفس le locus"},
           {"texte": "une cellule : deux chromosomes de la paire → deux allèles seulement", "mot": "deux allèles"}],
         "parole": ("la question un. l'allèle: une des formes d'un même gène، au même locus. F un، F deux، F trois، و F quatre هوما les quatre formes ديال le gène F، إذن كلهم ف نفس le locus، ف une paire de chromosomes homologues. "
                    "ف la cellule، كاين جوج ديال les chromosomes ديال هاد la paire، واحد من الأب و واحد من الأم. إذن seulement deux allèles، يقدرو يكونو بحال بحال ولا مختلفين، jamais quatre.")},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "En vous basant sur le document 1 et l'extrait du code génétique, donner la séquence de l'ARNm et la séquence des acides aminés de chaque allèle.",
       "texte_dit": "la question deux: باستعمال le document un و le code génétique، عطي l'A R N messager و les acides aminés ديال كل allèle.",
       "reponse": {"type": "phrase", "attendu": lignes_arn(A)},
       "clavier": {"aides": ["ARNm", "U", "–", "Thr", "Arg", "Asp"], "pieges": [j(c.translate(str.maketrans("ATCG", "UAGC")) for c in S["F1"][:2]), "T"]},
       "aides": [
         {"texte": "Brin NON transcrit : l'ARNm a les mêmes lettres, T devient U. Fais F1 en entier, puis pour F2, F3, F4 change seulement ce qui diffère.",
          "dit": "le brin non transcrit: نفس الحروف، و T كتولي U. دير F un كامل، ومن بعد ف F deux، F trois، و F quatre، بدل غير اللي مختلف."},
         {"texte": "Cherche chaque codon dans l'extrait : deux codons différents peuvent donner le même acide aminé.",
          "dit": "قلب على كل codon ف le code. ردو البال: deux codons مختلفين يقدرو يعطيو نفس l'acide aminé."}],
       "correction": {"lignes": [
           {"texte": f"2 : F1 : {j(A['arn']['F1'])} → {tiret(A['aa']['F1'])}", "mot": "F un"},
           {"texte": f"F2 : {j(A['arn']['F2'])} → {tiret(A['aa']['F2'])}", "mot": "F deux"},
           {"texte": f"F3 : {j(A['arn']['F3'])} → {tiret(A['aa']['F3'])}", "mot": "F trois"},
           {"texte": f"F4 : {j(A['arn']['F4'])} → {tiret(A['aa']['F4'])}", "mot": "F quatre"}],
         "parole": (f"la question deux. F un: l'A R N messager هو {'، '.join(L(c) for c in A['arn']['F1'])}. les acides aminés: {'، '.join(NOM[a] for a in A['aa']['F1'])}. "
                    f"F deux: le triplet treize كيعطي {L(A['arn']['F2'][2])}، و هو حتى هو la thréonine: نفس les acides aminés. "
                    f"F trois: le triplet quinze كيعطي {L(A['arn']['F3'][4])}، l'arginine ف بلاصة l'histidine. "
                    f"F quatre: le triplet seize كيعطي {L(A['arn']['F4'][5])}، l'acide aspartique ف بلاصة l'acide glutamique.")},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Comparer chacun des allèles F2, F3 et F4 à l'allèle F1, puis nommer le type de chaque mutation.",
       "texte_dit": "la question trois: قارن F deux، F trois، و F quatre مع F un، ومن بعد سمي le type ديال كل mutation.",
       "reponse": {"type": "phrase", "attendu": types(A)},
       "clavier": {"aides": ["substitution", "silencieuse", "faux-sens", "triplet 13", "triplet 15", "triplet 16"], "pieges": ["non-sens", "délétion"]},
       "aides": [
         {"texte": "Pour chaque allèle, trouve le seul triplet qui diffère de F1 et la lettre changée.",
          "dit": "ل كل allèle، قلب على le triplet الوحيد اللي مختلف على F un، و الحرف اللي تبدل."},
         {"texte": "Une lettre remplacée = substitution. Même acide aminé : silencieuse ; autre acide aminé : faux-sens ; codon stop : non-sens.",
          "dit": "حرف تبدل ب حرف: substitution. نفس l'acide aminé: silencieuse. acide aminé آخر: faux-sens. codon stop: non-sens."}],
       "correction": {"lignes": [
           {"texte": "3 : F2 : triplet 13 ACT → ACC, ACU (Thr) → ACC (Thr) : substitution silencieuse", "mot": "substitution silencieuse"},
           {"texte": "F3 : triplet 15 CAT → CGT, CAU (His) → CGU (Arg) : substitution faux-sens", "mot": "F trois، le triplet quinze"},
           {"texte": "F4 : triplet 16 GAA → GAT, GAA (Glu) → GAU (Asp) : substitution faux-sens", "mot": "F quatre، le triplet seize"}],
         "parole": ("la question trois. F deux، le triplet treize: A C T ولات A C C. le codon A C U و A C C بجوج كيعطيو la thréonine: substitution silencieuse. "
                    "F trois، le triplet quinze: C A T ولات C G T. l'histidine تبدلات ب l'arginine: substitution faux-sens. "
                    "F quatre، le triplet seize: G A A ولات G A T. l'acide glutamique تبدل ب l'acide aspartique: حتى هي substitution faux-sens.")},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "En exploitant le document 2, préciser quels allèles donnent une enzyme E fonctionnelle et lesquels modifient le phénotype. Expliquer le cas de F2 et la différence entre F3 et F4.",
       "texte_dit": "la question quatre: باستعمال le document deux، قول شمن allèles كيعطيو enzyme E fonctionnelle، و شمن allèles كيبدلو le phénotype. فسر الحالة ديال F deux، و الفرق بين F trois و F quatre.",
       "reponse": {"type": "phrase", "attendu": ("F1, F2 et F4 donnent une enzyme E fonctionnelle (activité 100 %, 100 % et 97 %) : pétales rouges. Seul F3 modifie le phénotype : E inactive (0 %), pas de pigment, pétales blancs. "
                                                 "F2 : le code génétique est redondant : ACU et ACC codent tous deux la thréonine ; l'ADN a changé mais la protéine est identique. "
                                                 "F3 et F4 sont deux faux-sens : chez F3, l'histidine remplacée par l'arginine rend l'enzyme non fonctionnelle ; chez F4, l'acide aspartique "
                                                 "à la place de l'acide glutamique ne change presque pas son activité. Un acide aminé changé ne modifie donc pas toujours la fonction de la protéine.")},
       "clavier": {"aides": ["redondance du code", "même acide aminé", "enzyme fonctionnelle", "non fonctionnelle", "pétales blancs", "97 %"], "pieges": ["F2 ne change pas l'ADN", "tout faux-sens rend l'enzyme inactive"]},
       "aides": [
         {"texte": "Dans le document 2, classe les allèles : activité normale (pétales rouges) ou activité nulle (pétales blancs).",
          "dit": "ف le document deux، فرق les allèles: activité normale و les pétales حمرين، ولا activité zéro و les pétales بيض."},
         {"texte": "Relie à la question 3 : F2 garde la même séquence d'acides aminés (pourquoi ?) ; F3 et F4 changent chacun un acide aminé, mais pas avec le même effet.",
          "dit": "ربط مع la question trois: F deux عندو نفس les acides aminés، علاش؟ F trois و F quatre كل واحد بدل acide aminé، ولكن ماشي بنفس النتيجة."}],
       "correction": {"lignes": [
           {"texte": "4 : F1, F2, F4 : E fonctionnelle (100 %, 100 %, 97 %) → pétales rouges ; F3 : E inactive (0 %) → pétales blancs", "mot": "غير F trois"},
           {"texte": "F2 : redondance du code : ACU et ACC → Thr : même protéine", "mot": "la redondance du code"},
           {"texte": "F3 : His → Arg : E non fonctionnelle ; F4 : Glu → Asp : E encore fonctionnelle", "mot": "F quatre، l'enzyme مازال fonctionnelle"}],
         "parole": ("la question quatre. F un، F deux، و F quatre كيعطيو enzyme fonctionnelle: cent، cent، et quatre-vingt-dix-sept pour cent، و les pétales حمرين. "
                    "غير F trois اللي بدل le phénotype: l'activité zéro، ما كاينش le pigment، و les pétales بيض. "
                    "F deux: هادي la redondance du code. A C U و A C C بجوج كيعطيو la thréonine، إذن l'A D N تبدل، و la protéine بقات هي هي. "
                    "F trois: l'arginine ف بلاصة l'histidine، و l'enzyme ولات non fonctionnelle. F quatre، l'enzyme مازال fonctionnelle، واخا acide aminé تبدل.")},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Un élève affirme : « Toute mutation d'un gène modifie la protéine, donc le caractère. » Discuter cette affirmation à partir des résultats de l'exercice.",
       "texte_dit": "la question cinq: تلميذ كيقول: كل mutation ف le gène كتبدل la protéine، إذن كتبدل le caractère. ناقش هاد الكلام، بالنتائج ديال التمرين.",
       "reponse": {"type": "phrase", "attendu": ("L'affirmation est fausse. F2 est muté mais, grâce à la redondance du code, la protéine est identique : la mutation est silencieuse, le caractère ne change pas. "
                                                 "F4 change un acide aminé de la protéine, mais l'enzyme reste fonctionnelle (97 %) : le caractère ne change pas non plus. "
                                                 "Seul F3, dont la protéine est non fonctionnelle, modifie le caractère (pétales blancs). "
                                                 "Une mutation ne modifie le caractère que si elle rend la protéine non fonctionnelle.")},
       "clavier": {"aides": ["L'affirmation est fausse", "silencieuse", "F2", "F4", "F3", "protéine non fonctionnelle"], "pieges": ["L'affirmation est vraie"]},
       "aides": [
         {"texte": "Cherche dans l'exercice un allèle muté dont la protéine ne change pas, et un allèle muté dont la protéine change sans changer le caractère.",
          "dit": "قلب ف التمرين على allèle muté و la protéine ديالو ما تبدلاتش، و على allèle muté تبدلات la protéine ديالو، ولكن le caractère ما تبدلش."},
         {"texte": "Conclus par une phrase : à quelle condition une mutation modifie-t-elle le caractère ?",
          "dit": "سالي ب جملة: إمتى la mutation كتبدل le caractère؟"}],
       "correction": {"lignes": [
           {"texte": "5 : affirmation fausse", "mot": "هاد الكلام غالط"},
           {"texte": "F2 : silencieuse (redondance) → même protéine → même caractère", "mot": "F deux mutation silencieuse"},
           {"texte": "F4 : un acide aminé changé, mais E fonctionnelle (97 %) → pétales rouges", "mot": "F quatre"},
           {"texte": "seule une protéine non fonctionnelle (F3) modifie le caractère", "mot": "غير ملي la protéine كتولي non fonctionnelle"}],
         "parole": ("la question cinq. هاد الكلام غالط. F deux mutation silencieuse: بسبب la redondance du code، la protéine هي هي، و le caractère ما تبدلش. "
                    "F quatre: acide aminé تبدل ف la protéine، ولكن l'enzyme بقات fonctionnelle، و les pétales بقاو حمرين. "
                    "غير F trois اللي بدل le caractère. إذن la mutation كتبدل le caractère غير ملي la protéine كتولي non fonctionnelle.")},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : un gène, un locus, deux allèles par cellule",
     "screen_content": {"lead": "Paire de chromosomes homologues : même gène au même locus, un allèle sur chaque chromosome."},
     "visual": {"kind": "simulation", "url": PAIRE, "caption": "Une paire de chromosomes homologues"},
     "speech_text": {"mixed": ("شوف l'exemple ديال الدرس. ف la cellule، هادي la paire de chromosomes homologues: واحد جا من الأب، والآخر جا من الأم. "
                               "le gène كاين ف نفس البلاصة ف الجوج: هي le locus. "
                               "ف chromosome الأب، le gène مكتوب ب واحد la forme. وف chromosome الأم، ب forme أخرى. هادو هوما les allèles. "
                               "إذن ف كل cellule، deux allèles فقط ل كل gène. ف التمرين، F un حتى ل F quatre كلهم ف نفس le locus، ولكن la cellule كتهز seulement deux allèles.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "allèle : une des formes d'un même gène, au même locus", "mot": "هادو هوما les allèles"},
                  {"texte": "une cellule : 2 allèles du gène F (parmi F1, F2, F3, F4)", "mot": "deux allèles فقط"}],
       "pointage": [{"mot": "ف la cellule", "commande": "play_until", "parametres": {"moment": "paire"}},
                    {"mot": "واحد جا من الأب", "repere": "chromosome_pere"},
                    {"mot": "والآخر جا من الأم", "repere": "chromosome_mere"},
                    {"mot": "le gène كاين ف نفس البلاصة", "commande": "play_until", "parametres": {"moment": "locus"}},
                    {"mot": "هي le locus", "repere": "locus"},
                    {"mot": "ف chromosome الأب", "commande": "play_until", "parametres": {"moment": "allele_pere"}},
                    {"mot": "ف chromosome الأب", "repere": "allele_pere"},
                    {"mot": "وف chromosome الأم", "commande": "play_until", "parametres": {"moment": "allele_mere"}},
                    {"mot": "وف chromosome الأم", "repere": "allele_mere"},
                    {"mot": "هادو هوما les allèles", "cible": "centre:0"},
                    {"mot": "deux allèles فقط", "commande": "play_until", "parametres": {"moment": "deux_alleles_differents"}},
                    {"mot": "deux allèles فقط", "repere": "alleles_differents"},
                    {"mot": "deux allèles فقط", "cible": "centre:1"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : brin non transcrit → ARNm : T devient U",
     "screen_content": {"lead": "Mêmes lettres que le brin non transcrit, T → U ; puis le tableau du code, codon par codon."},
     "visual": {"kind": "simulation", "url": BRINS, "caption": "Brin non transcrit, brin transcrit, ARNm"},
     "speech_text": {"mixed": ("شوف هاد تلاتة ديال السطور: لفوق le brin non transcrit، من بعد le brin transcrit، من بعد l'A R N messager. "
                               "ملي كنحطو l'A R N messager تحت le brin non transcrit، كنلقاو نفس الحروف، غير كل T كتولي U. "
                               f"ف التمرين، {L(S['F1'][2])} كتولي {L(arn(S['F1'][2]))}، و {L(S['F2'][2])} كتولي {L(arn(S['F2'][2]))}. "
                               "من بعد، قلب على كل codon ف le code: غادي تلقى les deux codons مختلفين كيعطيو نفس l'acide aminé.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "brin non transcrit → ARNm : T → U", "mot": "غير كل T كتولي U"},
                  {"texte": f"F1 {S['F1'][2]} → {arn(S['F1'][2])} ; F2 {S['F2'][2]} → {arn(S['F2'][2])}", "mot": "ف التمرين"}],
       "pointage": [{"mot": "شوف هاد تلاتة", "commande": "play_until", "parametres": {"moment": "trois_lignes"}},
                    {"mot": "لفوق le brin non transcrit", "repere": "ligne_non_transcrit"},
                    {"mot": "من بعد l'A R N messager", "repere": "ligne_arnm"},
                    {"mot": "تحت le brin non transcrit", "commande": "play_until", "parametres": {"moment": "comparaison_non_transcrit"}},
                    {"mot": "تحت le brin non transcrit", "repere": "chemin_2"},
                    {"mot": "غير كل T كتولي U", "commande": "play_until", "parametres": {"moment": "t_devient_u"}},
                    {"mot": "غير كل T كتولي U", "repere": "t_entoures"},
                    {"mot": "غير كل T كتولي U", "cible": "centre:0"},
                    {"mot": "ف التمرين", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : silencieuse ou faux-sens ?",
     "screen_content": {"lead": "Une lettre remplacée : même acide aminé → silencieuse ; autre acide aminé → faux-sens."},
     "visual": {"kind": "simulation", "url": MUT, "caption": "Substitutions : silencieuse puis faux-sens"},
     "speech_text": {"mixed": ("شوف l'exemple ديال الدرس. nucléotide كيتبدل ب واحد آخر: هادي la substitution. "
                               "و codon واحد اللي تبدل. هنا le codon C U A مازال كيعطي la leucine: هادي mutation silencieuse. "
                               "دابا الحالة الثانية: G A G ولات G T G، و le codon G U G كيعطي la valine: acide aminé تبدل، هادي mutation faux-sens. "
                               "ف التمرين: F deux silencieuse، و F trois و F quatre faux-sens.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "même acide aminé : silencieuse (F2 : ACU, ACC → Thr)", "mot": "هادي mutation silencieuse"},
                  {"texte": "autre acide aminé : faux-sens (F3 : His → Arg ; F4 : Glu → Asp)", "mot": "هادي mutation faux-sens"}],
       "pointage": [{"mot": "شوف l'exemple", "commande": "set_time", "parametres": {"time_s": 4.6}},
                    {"mot": "nucléotide كيتبدل", "commande": "play_until", "parametres": {"moment": "substitution"}},
                    {"mot": "nucléotide كيتبدل", "repere": "base_mutee"},
                    {"mot": "و codon واحد اللي تبدل", "commande": "play_until", "parametres": {"moment": "codon_change"}},
                    {"mot": "و codon واحد اللي تبدل", "repere": "codon_mute"},
                    {"mot": "هادي mutation silencieuse", "commande": "play_until", "parametres": {"moment": "silencieuse"}},
                    {"mot": "هادي mutation silencieuse", "repere": "type_mutation"},
                    {"mot": "هادي mutation silencieuse", "cible": "centre:0"},
                    {"mot": "دابا الحالة الثانية", "commande": "play_until", "parametres": {"moment": "faux_sens_evt"}},
                    {"mot": "كيعطي la valine", "repere": "acide_amine_change"},
                    {"mot": "هادي mutation faux-sens", "commande": "play_until", "parametres": {"moment": "faux_sens"}},
                    {"mot": "هادي mutation faux-sens", "repere": "type_mutation"},
                    {"mot": "هادي mutation faux-sens", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : la redondance du code génétique",
     "screen_content": {"lead": "Plusieurs codons pour un même acide aminé : l'ADN change, la protéine peut rester la même."},
     "visual": {"kind": "simulation", "url": PROP, "caption": "Les propriétés du code : la redondance"},
     "speech_text": {"mixed": ("le code redondant: بزاف ديال les codons كيعطيو نفس l'acide aminé. "
                               "شوف: six cases ل la leucine. C U G و C U A، deux codons، نفس l'acide aminé. "
                               "ف التمرين، نفس الشي ل la thréonine: A C U و A C C. هادا علاش F deux كيعطي نفس la protéine، و les pétales حمرين. "
                               "أما F trois، l'enzyme non fonctionnelle، و les pétales بيض. و F quatre، acide aminé تبدل، ولكن l'enzyme بقات fonctionnelle.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "redondance : ACU et ACC → Thr : F2 = même protéine", "mot": "نفس الشي ل la thréonine"},
                  {"texte": "F3 : E inactive → blanc ; F4 : E active (97 %) → rouge", "mot": "أما F trois"}],
       "pointage": [{"mot": "le code redondant", "commande": "play_until", "parametres": {"moment": "redondance"}},
                    {"mot": "six cases ل la leucine", "repere": "codons_leu"},
                    {"mot": "C U G و C U A", "repere": "cug"},
                    {"mot": "deux codons، نفس l'acide aminé", "repere": "cua"},
                    {"mot": "نفس الشي ل la thréonine", "cible": "centre:0"},
                    {"mot": "أما F trois", "cible": "centre:1"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : une mutation ne change pas toujours le caractère",
     "screen_content": {"lead": "Silencieuse : rien ne change. Faux-sens : la protéine change, sa fonction pas toujours."},
     "visual": {"kind": "simulation", "url": MUT, "caption": "Le bilan des mutations"},
     "speech_text": {"mixed": ("نجمعو. la substitution تقدر تكون silencieuse، faux-sens، ولا non-sens. "
                               "وعقل: le caractère ما كيتبدلش ديما. "
                               "ف التمرين، F deux silencieuse، و F quatre faux-sens ولكن l'enzyme fonctionnelle: le caractère ما تبدلش. "
                               "غير F trois، la protéine non fonctionnelle، و les pétales بيض. إذن كلام التلميذ غالط.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "F2 et F4 : mutés, pétales rouges", "mot": "le caractère ما تبدلش"},
                  {"texte": "seule une protéine non fonctionnelle (F3) change le caractère", "mot": "غير F trois"}],
       "pointage": [{"mot": "نجمعو", "commande": "set_time", "parametres": {"time_s": 34.4}},
                    {"mot": "نجمعو", "commande": "play_until", "parametres": {"moment": "bilan"}},
                    {"mot": "la substitution تقدر", "commande": "play_until", "parametres": {"moment": "bilan_substitution"}},
                    {"mot": "la substitution تقدر", "repere": "bilan_1"},
                    {"mot": "le caractère ما كيتبدلش ديما", "commande": "play_until", "parametres": {"moment": "bilan_caractere"}},
                    {"mot": "le caractère ما كيتبدلش ديما", "repere": "bilan_4"},
                    {"mot": "le caractère ما تبدلش", "cible": "centre:0"},
                    {"mot": "غير F trois", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : combien d'allèles par cellule ?", "سؤال ساهل: شحال من allèle ف la cellule؟",
      "Une cellule de la plante porte, pour le gène F…", ["deux allèles", "quatre allèles", "un seul allèle"], 0, {
        "0": {"juste": rep("برافو! deux chromosomes ف la paire، ف كل واحد allèle: deux allèles.", "Juste : un allèle sur chaque chromosome de la paire.")},
        "1": {"1": rep("ما تقلقش. quatre allèles كاينين ف النباتات، ولكن la cellule شحال فيها من chromosome ديال la paire؟ عاود اختار.", "Quatre allèles existent dans l'espèce ; mais combien de chromosomes de la paire par cellule ? Réessaie."),
              "2": rep("الجواب: c'est deux allèles. واحد ف كل chromosome ديال la paire.", "Réponse : deux allèles.")},
        "2": {"1": rep("قريب! la paire فيها جوج ديال les chromosomes، و كل واحد فيه le gène F. عاود اختار.", "La paire a deux chromosomes, chacun porte le gène F. Réessaie."),
              "2": rep("الجواب: c'est deux allèles. واحد من الأب و واحد من الأم.", "Réponse : deux allèles.")}},
      "Combien d'allèles du gène F dans une cellule ?"),
    qcm_facile("fa_s2", "Plus facile : le codon du triplet 13 de F2", "سؤال ساهل: le codon ديال F deux.",
      f"Brin non transcrit de F2, triplet 13 : {S['F2'][2]}. Le codon et l'acide aminé sont…",
      [f"{arn(S['F2'][2])} : Thr", f"{S['F2'][2].translate(str.maketrans('ATCG', 'UAGC'))} : Trp", f"{S['F2'][2]} : Thr"], 0, {
        "0": {"juste": rep("مزيان! A C C كتولي A C C، و هو la thréonine، بحال F un.", f"Juste : {arn(S['F2'][2])} → Thr.")},
        "1": {"1": rep("ما تقلقش. le brin non transcrit ما كنديروش ليه la complémentarité. عاود اختار.", "Pas de complémentarité pour le brin non transcrit. Réessaie."),
              "2": rep("الجواب هو A C C، la thréonine. نفس الحروف، T كتولي U.", "Réponse : ACC (Thr).")},
        "2": {"1": rep("قريب! l'acide aminé صحيح، ولكن le codon ديال l'A R N ما فيهش T. عاود اختار.", "Acide aminé juste, mais un codon d'ARN n'a pas de T. Réessaie."),
              "2": rep("الجواب هو A C C: le codon فيه غير A، U، C، G.", "Réponse : ACC (pas de T dans l'ARN).")}},
      "Le triplet A C C du brin non transcrit donne quel codon et quel acide aminé ?"),
    association("fa_s3", "Plus facile : chaque allèle, sa mutation", "Relie chaque allèle au type de mutation.",
      "سؤال ساهل: ربط كل allèle مع le type ديال la mutation ديالو.", "Relie chaque allèle au type de sa mutation.",
      [("1", "F2 : ACU (Thr) → ACC (Thr)"), ("2", "F3 : CAU (His) → CGU (Arg)"), ("3", "F4 : GAA (Glu) → GAU (Asp)")],
      [("a", "Substitution silencieuse"), ("b", "Substitution faux-sens"), ("c", "Substitution non-sens")],
      {"1": "a", "2": "b", "3": "b"},
      {"1-a": (True, "Oui : même acide aminé, la thréonine : silencieuse.", "برافو: نفس l'acide aminé: silencieuse."),
       "1-b": (False, "Faux-sens = autre acide aminé ; ici Thr reste Thr.", "لا، faux-sens كتعني acide aminé آخر. هنا la thréonine بقات."),
       "1-c": (False, "Non-sens = codon stop ; ACC code Thr.", "لا، non-sens كتعني codon stop."),
       "2-a": (False, "His et Arg sont deux acides aminés différents.", "لا، l'histidine و l'arginine مختلفين."),
       "2-b": (True, "Oui : His remplacée par Arg : faux-sens.", "برافو: l'histidine تبدلات ب l'arginine: faux-sens."),
       "2-c": (False, "CGU n'est pas un codon stop.", "لا، C G U ماشي codon stop."),
       "3-a": (False, "Glu et Asp sont deux acides aminés différents, même si l'enzyme reste active.", "لا، l'acide glutamique و l'acide aspartique مختلفين."),
       "3-b": (True, "Oui : Glu remplacé par Asp : faux-sens (l'enzyme reste pourtant active).", "برافو: faux-sens، واخا l'enzyme بقات fonctionnelle."),
       "3-c": (False, "GAU code Asp, ce n'est pas un stop.", "لا، G A U كيعطي l'acide aspartique.")},
      ("(1 ; a) (2 ; b) (3 ; b) : la lettre c (non-sens) est en trop.", "F deux silencieuse، F trois و F quatre faux-sens، و non-sens ما كايناش هنا.")),
    vrai_faux("fa_s4", "Plus facile : document 2", "Vrai ou faux ?",
      "سؤال ساهل: صحيح ولا غالط؟", [
        ("La mutation de F2 ne change pas l'ADN.", False, "Faux : l'ADN change (ACT → ACC), mais pas l'acide aminé (redondance du code)."),
        ("ACU et ACC codent le même acide aminé : le code génétique est redondant.", True, "Vrai : les deux codent la thréonine."),
        ("F3 donne une enzyme E inactive : les pétales sont blancs.", True, "Vrai : activité 0 %, pas de pigment."),
        ("Tout changement d'acide aminé rend une enzyme inactive.", False, "Faux : F4 change un acide aminé et garde 97 % d'activité.")]),
    qcm_facile("fa_s5", "Plus facile : à quelle condition le caractère change ?", "سؤال ساهل: إمتى le caractère كيتبدل؟",
      "Une mutation modifie le caractère…", ["seulement si la protéine devient non fonctionnelle", "toujours", "seulement si elle est silencieuse"], 0, {
        "0": {"juste": rep("برافو! غير ملي la protéine كتولي non fonctionnelle، بحال F trois.", "Juste : seulement si la protéine devient non fonctionnelle (F3).")},
        "1": {"1": rep("ما تقلقش. شوف F deux و F quatre: mutés، ولكن شنو اللون ديال les pétales؟ عاود اختار.", "Regarde F2 et F4 : mutés, mais quelle couleur ? Réessaie."),
              "2": rep("الجواب: غير ملي la protéine كتولي non fonctionnelle. F deux و F quatre حمرين.", "Réponse : seulement si la protéine devient non fonctionnelle.")},
        "2": {"1": rep("لا، silencieuse كتعني la protéine ما تبدلاتش، إذن le caractère ما كيتبدلش. عاود اختار.", "Silencieuse = protéine inchangée, donc caractère inchangé. Réessaie."),
              "2": rep("الجواب: غير ملي la protéine كتولي non fonctionnelle.", "Réponse : seulement si la protéine devient non fonctionnelle.")}},
      "Une mutation modifie le caractère dans quel cas ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch4_alleles_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Même plante, même gène F (enzyme E du pigment rouge), quatre autres allèles F1 à F4. "
                f"Document 1 : brin non transcrit (triplets {B['debut']} à {B['debut'] + 6}, séquences simplifiées). Document 2 : activité de E et couleur des pétales "
                "(chaque plante porte le même allèle sur les deux chromosomes de la paire)."),
      "intro_dit": "نفس النبتة، نفس le gène F، quatre allèles آخرين.",
      "figures": figures(B),
      "donnees": donnees(B, ["AUG", "UAG", "GGC", "UCC"]),
      "questions": [
        {"id": "1", "texte": "Définir un allèle, puis préciser où sont situés F1 à F4 et combien d'allèles du gène F porte une cellule. Justifier.",
         "reponse": {"type": "phrase", "attendu": "Un allèle est une des formes d'un même gène, au même locus. F1 à F4 occupent le même locus sur une paire de chromosomes homologues ; une cellule porte deux chromosomes de la paire, donc deux allèles du gène F."},
         "clavier": {"aides": ["même locus", "chromosomes homologues", "deux allèles"], "pieges": ["quatre allèles"]},
         "correction": {"lignes": [{"texte": "1 : allèle : une des formes d'un même gène, au même locus", "mot": "une des formes d'un même gène"},
                                   {"texte": "même locus ; deux allèles par cellule", "mot": "deux allèles"}],
                        "parole": "la question un. l'allèle: une des formes d'un même gène، au même locus. كلهم ف نفس le locus، و la cellule فيها seulement deux allèles."}},
        {"id": "2", "texte": "Donner la séquence de l'ARNm et la séquence des acides aminés de chaque allèle.",
         "reponse": {"type": "phrase", "attendu": lignes_arn(B)},
         "clavier": {"aides": ["ARNm", "U", "–"], "pieges": ["T"]},
         "correction": {"lignes": [{"texte": f"2 : F1 : {j(B['arn']['F1'])} → {tiret(B['aa']['F1'])}", "mot": "F un"},
                                   {"texte": f"F2 : → {tiret(B['aa']['F2'])} ; F3 : → {tiret(B['aa']['F3'])} ; F4 : → {tiret(B['aa']['F4'])}", "mot": "F deux"}],
                        "parole": (f"la question deux. F un: {'، '.join(L(c) for c in B['arn']['F1'])}، و les acides aminés: {'، '.join(NOM[a] for a in B['aa']['F1'])}. "
                                   "F deux: نفس les acides aminés. F trois: la phénylalanine ف بلاصة la sérine. F quatre: l'arginine ف بلاصة la lysine.")}},
        {"id": "3", "texte": "Comparer F2, F3 et F4 à F1, puis nommer le type de chaque mutation.",
         "reponse": {"type": "phrase", "attendu": types(B)},
         "clavier": {"aides": ["silencieuse", "faux-sens"], "pieges": ["non-sens"]},
         "correction": {"lignes": [{"texte": "3 : F2 : triplet 23 GGT → GGA, Gly → Gly : silencieuse", "mot": "silencieuse"},
                                   {"texte": "F3 : triplet 26 TCT → TTT, Ser → Phe ; F4 : triplet 25 AAG → AGG, Lys → Arg : faux-sens", "mot": "faux-sens"}],
                        "parole": "la question trois. F deux، le triplet vingt-trois: la glycine بقات: silencieuse. F trois و F quatre: acide aminé تبدل: faux-sens."}},
        {"id": "4", "texte": "En exploitant le document 2, préciser quels allèles donnent une enzyme fonctionnelle et lesquels modifient le phénotype ; expliquer F2 et la différence entre F3 et F4.",
         "reponse": {"type": "phrase", "attendu": ("F1, F2 et F4 : E fonctionnelle (100 %, 100 %, 95 %), pétales rouges ; F3 : E inactive (0 %), pétales blancs. "
                                                   "F2 : redondance du code (GGU et GGA codent la glycine) : même protéine. F3 : sérine remplacée par phénylalanine, enzyme non fonctionnelle ; "
                                                   "F4 : lysine remplacée par arginine, enzyme encore fonctionnelle.")},
         "clavier": {"aides": ["redondance du code", "95 %"], "pieges": ["tout faux-sens rend l'enzyme inactive"]},
         "correction": {"lignes": [{"texte": "4 : seul F3 : E inactive → pétales blancs", "mot": "غير F trois"},
                                   {"texte": "F2 : redondance ; F4 : faux-sens sans perte de fonction", "mot": "la redondance du code"}],
                        "parole": "la question quatre. غير F trois اللي كيعطي les pétales بيض. F deux: la redondance du code. F quatre: acide aminé تبدل، ولكن l'enzyme بقات fonctionnelle."}},
        {"id": "5", "texte": "Un élève affirme : « Toute mutation d'un gène modifie la protéine, donc le caractère. » Discuter cette affirmation.",
         "reponse": {"type": "phrase", "attendu": "Fausse : F2 (silencieuse) ne change pas la protéine ; F4 change un acide aminé sans changer la fonction ; seul F3, protéine non fonctionnelle, change le caractère."},
         "clavier": {"aides": ["L'affirmation est fausse", "silencieuse"], "pieges": ["L'affirmation est vraie"]},
         "correction": {"lignes": [{"texte": "5 : fausse : F2 et F4 mutés, pétales rouges", "mot": "هاد الكلام غالط"},
                                   {"texte": "seule une protéine non fonctionnelle (F3) change le caractère", "mot": "غير F trois"}],
                        "parole": "la question cinq. هاد الكلام غالط: F deux و F quatre mutés، و les pétales حمرين. غير F trois اللي بدل le caractère."}}
      ]}}
}
ecrire(EX, sys.argv[1])
