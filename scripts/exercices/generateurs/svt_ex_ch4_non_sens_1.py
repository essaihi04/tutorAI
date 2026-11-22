# Exercice SVT ch. 4 (relation gène – protéine), niveau moyen : substitution non-sens, myopathie de Duchenne.
# Entraîne : comparer un phénotype aux trois niveaux (moléculaire, cellulaire, macroscopique) puis déduire la relation
# protéine – caractère ; ARNm et acides aminés depuis le brin TRANSCRIT (complémentarité) ; reconnaître un codon stop
# prématuré (non-sens) ; calculer la longueur d'une protéine raccourcie ; relation gène – protéine – caractère.
# Sources comparées (lecture seule, rien de copié) :
# - exploration/relation_gene_proteine.json : cas_types (arn_aa, origine_genetique, relation_gpc), pièges (« continue après le
#   stop », « stop écrit comme un acide aminé », « cherche le triplet de l'ADN dans le tableau »), NC2 (trois échelles), vidéos
#   d'exercices des profs (Ouissam, Wessal, Driss, AJIN9RAW : phrase à flèches, stop « arrêt de la traduction »).
# - nationaux : non-sens 2018 N, 2023 N (récepteur LDL), 2024 R ; brin transcrit 2018 N, 2019 R, 2020 R, 2024 R : même forme de
#   questions (« donnez l'ARNm et la séquence d'acides aminés », « montrez la relation gène – protéine – caractère »), autre situation.
# - séries en ligne : recherche faite (dyrassa série 7, alloschool N. Bahsina, série Naciri), PDF non ouverts (domaines bloqués
#   par le réseau de la session) : titres et extraits seulement.
# Situation : la myopathie de Duchenne (dystrophine) n'est pas un sujet national 2016-2025 ; séquences inventées (simplifiées) ;
# la longueur de la dystrophine (3685 acides aminés) est la valeur réelle.
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


def fig_tableau(titre, entetes, lignes, legende):
    """Tableau à trois colonnes dessiné (rect + texte) : entêtes, puis une ligne par niveau, chaque case sur 1 à 3 lignes."""
    xs = [0, 22, 61, 100]; hl = 4.2; hauteurs = [max(len(c) for c in l) * hl + 2 for l in lignes]
    h = 8 + sum(hauteurs); el = []; y = h
    el.append({"f": "rect", "de": [0, h - 8], "a": [100, h], "couleur": "faible"})
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


NIVEAUX = [
    [["moléculaire"], ["dystrophine présente", "sous la membrane", "des fibres musculaires"], ["dystrophine absente", "des fibres musculaires"]],
    [["cellulaire"], ["fibres musculaires", "intactes après", "les contractions"], ["membrane fragile : les", "fibres se déchirent", "et meurent"]],
    [["macroscopique"], ["marche, course et", "escaliers normaux"], ["faiblesse musculaire,", "chutes fréquentes"]]]

# ── données ────────────────────────────────────────────────────────────────────────────
D1, NT1 = 36, ["GCA", "AAC", "TTG", "CAG", "GAA", "ATC", "CGT"]          # brin NON transcrit (sert au calcul)
MT1 = NT1[:3] + ["TAG"] + NT1[4:]; J1 = 3
TN1, TM1 = [comp(c) for c in NT1], [comp(c) for c in MT1]                 # brin transcrit, donné dans l'énoncé
assert TN1 == ["CGT", "TTG", "AAC", "GTC", "CTT", "TAG", "GCA"] and TM1[J1] == "ATC"
RN1, RM1 = [arn(c) for c in NT1], [arn(c) for c in MT1]
AN1 = [aa(c) for c in NT1]
AM1 = []
for c in MT1:
    if aa(c) == "Stop": break
    AM1.append(aa(c))
assert AN1 == ["Ala", "Asn", "Leu", "Gln", "Glu", "Ile", "Arg"] and AM1 == ["Ala", "Asn", "Leu"] and aa(MT1[J1]) == "Stop"
assert [i for i in range(7) if TN1[i] != TM1[i]] == [J1]
LONG = 3685
N_MUTE1 = D1 + J1 - 1                       # triplet 1 = AUG (Met) ; le stop (triplet 39) ne code rien → 38 acides aminés
assert N_MUTE1 == 38
ARN_N1, ARN_M1 = " ".join(RN1), " ".join(RM1)
SEQ_N1, SEQ_M1 = " – ".join(AN1), " – ".join(AM1) + " (codon stop UAG : arrêt de la traduction)"

D2, NT2 = 51, ["TCA", "GGC", "AAT", "CGA", "TTG", "GAC", "CTT"]
MT2 = NT2[:3] + ["TGA"] + NT2[4:]; J2 = 3
TN2, TM2 = [comp(c) for c in NT2], [comp(c) for c in MT2]
assert TN2 == ["AGT", "CCG", "TTA", "GCT", "AAC", "CTG", "GAA"] and TM2[J2] == "ACT"
RN2, RM2 = [arn(c) for c in NT2], [arn(c) for c in MT2]
AN2 = [aa(c) for c in NT2]; AM2 = AN2[:J2]
assert AN2 == ["Ser", "Gly", "Asn", "Arg", "Leu", "Asp", "Leu"] and aa(MT2[J2]) == "Stop"
N_MUTE2 = D2 + J2 - 1; assert N_MUTE2 == 53
ARN_N2, ARN_M2 = " ".join(RN2), " ".join(RM2)
SEQ_N2, SEQ_M2 = " – ".join(AN2), " – ".join(AM2) + " (codon stop UGA : arrêt de la traduction)"

def extrait_code(codons):
    return "Extrait du code génétique : " + " ; ".join(f"{c} : {AB[CODE[c]]}" for c in codons)
CODE1 = extrait_code(["GCA", "AAC", "UUG", "CAG", "GAA", "AUC", "CGU", "UAG", "UAA", "AUG", "GUC", "CUU"])
CODE2 = extrait_code(["UCA", "GGC", "AAU", "CGA", "UUG", "GAC", "CUU", "UGA", "UAA", "AGU", "CCG"])
for c in RN1 + RM1: assert c in CODE1
for c in RN2 + RM2: assert c in CODE2

DOC = "/media/simulations/svt/relation_gene_proteine-tableau/"
ECH, BRINS, MUT = DOC + "drepanocytose.html?vue=echelles", DOC + "transcription.html?vue=brins", DOC + "mutation.html?vue=mutation"
TRAD, SCH = DOC + "traduction.html?vue=traduction", DOC + "schema_bilan.html?vue=schema"

def seqs_fig(titre, d, tn, tm, leg):
    return fig_sequences(titre, d, [("Allèle normal", tn, "blanc"), ("Allèle muté", tm, "blanc")], leg)

EX = {
  "id": "svt_ex_ch4_non_sens_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "relation_gene_proteine", "cours": "svt_ch4_relation_gene_proteine",
  "titre": "La myopathie de Duchenne : un codon stop trop tôt", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Comparer un phénotype aux trois niveaux", "Montrer la relation protéine – caractère",
                  "Écrire l'ARNm à partir du brin transcrit", "Reconnaître une mutation non-sens (codon stop prématuré)",
                  "Calculer la longueur d'une protéine", "Montrer la relation gène – protéine – caractère"],
  "enonce": {
    "intro": ("La myopathie de Duchenne est une maladie héréditaire qui touche surtout les garçons. "
              "La dystrophine est une protéine placée sous la membrane des fibres musculaires : elle rend cette membrane solide pendant les contractions. "
              "Document 1 : comparaison d'un garçon sain et d'un garçon malade aux trois niveaux. "
              f"Document 2 : extrait du brin transcrit du gène de la dystrophine (triplets {D1} à {D1 + 6}), allèle normal du garçon sain et allèle muté du garçon malade "
              "(séquences simplifiées pour l'exercice). Le triplet 1 du gène correspond au codon d'initiation AUG ; la dystrophine normale compte 3685 acides aminés."),
    "intro_dit": ("نقراو l'énoncé. la myopathie de Duchenne هي maladie héréditaire، كتصيب بزاف les garçons. "
                  "la dystrophine هي protéine، كاينة تحت la membrane ديال les fibres musculaires، وكتخلي la membrane قوية ملي كتنقبض la fibre. "
                  "le document un كيقارن garçon sain و garçon malade، ف تلاتة ديال المستويات. "
                  "le document deux: جزء من le brin transcrit ديال le gène ديال la dystrophine، l'allèle normal و l'allèle muté. "
                  "le triplet un ديال le gène هو le codon d'initiation، A U G. و la dystrophine normale compte trois mille six cent quatre-vingt-cinq acides aminés."),
    "figures": [fig_tableau("Document 1 : le phénotype aux trois niveaux", ["Niveau", "Garçon sain", "Garçon malade"], NIVEAUX,
                            "Le même caractère observé à l'échelle de la molécule, de la cellule et de l'organisme."),
                seqs_fig("Document 2 : brin transcrit (3′ → 5′)", D1, TN1, TM1, "Gène de la dystrophine : allèle normal et allèle muté.")],
    "donnees": [f"Allèle normal (brin transcrit, 3′ → 5′) : {' '.join(TN1)}",
                f"Allèle muté (brin transcrit, 3′ → 5′) : {' '.join(TM1)}",
                f"Les triplets sont numérotés de {D1} à {D1 + 6} ; le triplet 1 correspond au codon AUG.",
                "Dystrophine normale : 3685 acides aminés.", CODE1],
    "questions": [
      {"id": "1", "texte": "Comparer le phénotype des deux garçons aux niveaux moléculaire, cellulaire et macroscopique (document 1), puis déduire la relation protéine – caractère.",
       "texte_dit": "la question un: قارن le phénotype ديال الجوج ديال les garçons، ف le niveau moléculaire، cellulaire، و macroscopique، ومن بعد استنتج la relation protéine caractère.",
       "reponse": {"type": "phrase", "attendu": ("Niveau moléculaire : la dystrophine est présente sous la membrane des fibres chez le garçon sain, absente chez le garçon malade. "
                                                 "Niveau cellulaire : les fibres restent intactes chez le sain ; chez le malade, leur membrane est fragile, elles se déchirent et meurent. "
                                                 "Niveau macroscopique : marche et course normales chez le sain ; faiblesse musculaire et chutes chez le malade. "
                                                 "On en déduit que l'absence de la dystrophine (protéine) entraîne la maladie (caractère) : le caractère dépend de la protéine.")},
       "clavier": {"aides": ["niveau moléculaire", "niveau cellulaire", "niveau macroscopique", "dystrophine absente", "On en déduit que"], "pieges": ["la fibre est absente"]},
       "aides": [
         {"texte": "Lis le document 1 ligne par ligne : pour chaque niveau, une phrase qui compare le garçon sain et le garçon malade.",
          "dit": "قرا le document un سطر ب سطر. ف كل niveau، جملة كتقارن le garçon sain و le garçon malade."},
         {"texte": "Pour déduire, relie le niveau moléculaire (la protéine) au niveau macroscopique (le caractère), en passant par la cellule.",
          "dit": "باش تستنتج، ربط le niveau moléculaire، يعني la protéine، مع le niveau macroscopique، يعني le caractère، و دوز من la cellule."}],
       "correction": {"lignes": [
           {"texte": "1 : moléculaire : dystrophine présente (sain) / absente (malade)", "mot": "ف le niveau moléculaire"},
           {"texte": "cellulaire : fibres intactes / membrane fragile, fibres déchirées qui meurent", "mot": "ف le niveau cellulaire"},
           {"texte": "macroscopique : mouvements normaux / faiblesse musculaire, chutes", "mot": "ف le niveau macroscopique"},
           {"texte": "On en déduit que : sans dystrophine (protéine) → maladie (caractère)", "mot": "On en déduit que"}],
         "parole": ("la question un. ف le niveau moléculaire، la dystrophine كاينة عند le garçon sain، و ما كايناش عند le garçon malade. "
                    "ف le niveau cellulaire، les fibres ديال le garçon sain كيبقاو سالمين، و عند le garçon malade، la membrane ضعيفة، les fibres كيتقطعو وكيموتو. "
                    "ف le niveau macroscopique، le garçon sain كيمشي وكيجري عادي، و le garçon malade عندو faiblesse musculaire وكيطيح بزاف. "
                    "On en déduit que le caractère كيتبع la protéine: بلا dystrophine، كتجي la maladie.")},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "En vous basant sur le document 2 et l'extrait du code génétique, donner la séquence de l'ARNm et la séquence des acides aminés de chaque allèle.",
       "texte_dit": "la question deux: باستعمال le document deux و le code génétique، عطي la séquence ديال l'A R N messager، و la séquence ديال les acides aminés، ل كل allèle.",
       "reponse": {"type": "phrase", "attendu": (f"Allèle normal : ARNm : {ARN_N1} ; acides aminés : {SEQ_N1}. "
                                                 f"Allèle muté : ARNm : {ARN_M1} ; acides aminés : {SEQ_M1}.")},
       "clavier": {"aides": ["ARNm :", "A → U", "T → A", "C → G", "G → C", "arrêt de la traduction"], "pieges": [" ".join(arn(c) for c in TN1[:2]), "Stop"]},
       "aides": [
         {"texte": "Le document donne le brin TRANSCRIT : l'ARNm est son complémentaire (A → U, T → A, C → G, G → C).",
          "dit": "le document كيعطيك le brin transcrit. l'A R N messager هو le complémentaire ديالو: A كتولي U، T كتولي A، C كتولي G، و G كتولي C."},
         {"texte": "Traduis codon par codon avec l'extrait ; au premier codon stop, écris « arrêt de la traduction » et ne traduis plus rien après.",
          "dit": "ترجم codon ب codon. ف أول codon stop، كتب arrêt de la traduction، و ما تترجم والو من بعد."}],
       "correction": {"lignes": [
           {"texte": f"2 : allèle normal : ARNm : {ARN_N1}", "mot": "l'allèle normal"},
           {"texte": f"acides aminés : {SEQ_N1}", "mot": "les acides aminés"},
           {"texte": f"allèle muté : ARNm : {ARN_M1}", "mot": "l'allèle muté"},
           {"texte": f"acides aminés : {SEQ_M1}", "mot": "arrêt de la traduction"}],
         "parole": (f"la question deux. le brin transcrit، إذن la complémentarité. l'allèle normal: l'A R N messager هو {'، '.join(L(c) for c in RN1)}. "
                    f"les acides aminés: {'، '.join(NOM[a] for a in AN1)}. "
                    f"l'allèle muté: ف le triplet trente-neuf، le codon ولا {L(RM1[J1])}، و هو codon stop. "
                    f"إذن غير {'، '.join(NOM[a] for a in AM1)}، ومن بعد arrêt de la traduction.")},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Déterminer la mutation (type, nucléotide, triplet) et nommer sa conséquence sur la traduction. Justifier.",
       "texte_dit": "la question trois: حدد la mutation، le type ديالها، le nucléotide و le triplet، وسمي النتيجة ديالها على la traduction. برر.",
       "reponse": {"type": "phrase", "attendu": ("Seul le triplet 39 diffère : GTC (allèle normal) devient ATC (allèle muté) sur le brin transcrit : substitution du 1er nucléotide G par A. "
                                                 "Le codon CAG (Gln) devient UAG, un codon stop : la traduction s'arrête au triplet 39. "
                                                 "C'est une mutation par substitution non-sens (codon stop prématuré).")},
       "clavier": {"aides": ["triplet 39", "substitution", "non-sens", "codon stop", "UAG", "G remplacé par A"], "pieges": ["faux-sens", "délétion", "TAG est un codon stop"]},
       "aides": [
         {"texte": "Compare les deux brins triplet par triplet : un seul triplet change. Puis regarde son codon d'ARNm, pas le triplet de l'ADN.",
          "dit": "قارن triplet ب triplet: غير triplet واحد اللي تبدل. ومن بعد شوف le codon ديال l'A R N messager، ماشي le triplet ديال l'A D N."},
         {"texte": "Une lettre remplacée : substitution. Si le nouveau codon est UAA, UAG ou UGA : non-sens.",
          "dit": "حرف تبدل ب حرف: substitution. يلا le codon الجديد هو U A A، ولا U A G، ولا U G A، هادي non-sens."}],
       "correction": {"lignes": [
           {"texte": "3 : triplet 39 du brin transcrit : GTC → ATC (G remplacé par A)", "mot": "غير le triplet trente-neuf"},
           {"texte": "codon CAG (Gln) → UAG : codon stop, la traduction s'arrête", "mot": "U A G، codon stop"},
           {"texte": "donc mutation par substitution non-sens", "mot": "substitution non-sens"}],
         "parole": ("la question trois. غير le triplet trente-neuf اللي تبدل: G T C ولات A T C. le nucléotide G تبدل ب A. "
                    "le codon C A G، اللي كان كيعطي la glutamine، ولا U A G، codon stop. la traduction كتحبس بكري. هادي mutation par substitution non-sens. "
                    "ردو البال: T A G ف le triplet quarante et un هو triplet ديال l'A D N، ماشي codon. le codon ديالو هو A U C.")},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Calculer le nombre d'acides aminés de la protéine fabriquée à partir de l'allèle muté, puis expliquer pourquoi elle est non fonctionnelle.",
       "texte_dit": "la question quatre: حسب شحال من acide aminé ف la protéine اللي كتجي من l'allèle muté، ومن بعد فسر علاش هي non fonctionnelle.",
       "reponse": {"type": "valeur", "grandeur": "n", "valeur": N_MUTE1, "unite": "acides aminés", "tolerance": 0.02,
                   "attendu": "Le triplet 1 (AUG) donne le 1er acide aminé ; le codon stop du triplet 39 ne code aucun acide aminé : n = 39 − 1 = 38 acides aminés (au lieu de 3685) : protéine très raccourcie, non fonctionnelle."},
       "clavier": {"aides": ["n = 39 − 1", "triplet 1 = AUG", "acides aminés", "3685"], "pieges": ["n = 39", "n = 3685 − 39"]},
       "aides": [
         {"texte": "Chaque triplet, du triplet 1 (AUG) jusqu'au triplet juste avant le stop, donne un acide aminé. Où est le stop ?",
          "dit": "كل triplet، من le triplet un، A U G، حتى ل le triplet اللي قبل le stop، كيعطي acide aminé. فين كاين le stop؟"},
         {"texte": "Le codon stop ne code aucun acide aminé : n = (numéro du triplet du stop) − 1. Compare avec 3685.",
          "dit": "le codon stop ما كيعطي حتى acide aminé. إذن n égale le numéro ديال le triplet ديال le stop moins un. ومن بعد قارن avec trois mille six cent quatre-vingt-cinq."}],
       "correction": {"lignes": [
           {"texte": "4 : triplets 1 à 38 → un acide aminé chacun ; triplet 39 : stop", "mot": "من le triplet un حتى ل le triplet trente-huit"},
           {"texte": "n = 39 − 1 = 38 acides aminés (au lieu de 3685)", "mot": "n égale trente-neuf moins un"},
           {"texte": "protéine très raccourcie, il lui manque presque toute la chaîne : non fonctionnelle", "mot": "non fonctionnelle"}],
         "parole": ("la question quatre. من le triplet un حتى ل le triplet trente-huit، كل triplet كيعطي acide aminé. le triplet trente-neuf هو le stop، ما كيعطي والو. "
                    "n égale trente-neuf moins un، égale trente-huit acides aminés، au lieu de trois mille six cent quatre-vingt-cinq. "
                    "la protéine قصيرة بزاف، ناقصاها تقريبا la chaîne كاملة، إذن non fonctionnelle.")},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "À partir de ce qui précède, montrer la relation gène – protéine – caractère chez le garçon malade.",
       "texte_dit": "la question cinq: من داكشي اللي فات، بين la relation gène protéine caractère عند le garçon malade.",
       "reponse": {"type": "phrase", "attendu": ("Allèle muté (substitution non-sens au triplet 39) → codon stop UAG prématuré → dystrophine raccourcie (38 acides aminés), non fonctionnelle "
                                                 "→ membrane des fibres musculaires fragile, les fibres se déchirent et meurent → faiblesse musculaire : myopathie de Duchenne. "
                                                 "Chez le garçon sain : allèle normal → dystrophine fonctionnelle → fibres intactes → muscles normaux. "
                                                 "Le gène détermine la protéine, qui détermine le caractère.")},
       "clavier": {"aides": ["allèle muté", "codon stop", "dystrophine non fonctionnelle", "fibres", "→", "Le gène détermine la protéine"], "pieges": ["allèle muté → maladie"]},
       "aides": [
         {"texte": "Écris la chaîne gène → protéine → cellule → organisme, pour le garçon malade (et, en face, pour le sain).",
          "dit": "كتب la chaîne: le gène، la protéine، la cellule، l'organisme، ل le garçon malade، و قدامها ل le garçon sain."},
         {"texte": "Reprends tes réponses : 3 pour le gène, 4 pour la protéine, document 1 pour la cellule et l'organisme.",
          "dit": "رجع ل الأجوبة ديالك: la question trois ل le gène، la question quatre ل la protéine، و le document un ل la cellule و l'organisme."}],
       "correction": {"lignes": [
           {"texte": "5 : allèle muté (non-sens, triplet 39) → codon stop UAG", "mot": "l'allèle muté فيه substitution non-sens"},
           {"texte": "→ dystrophine de 38 acides aminés, non fonctionnelle", "mot": "la dystrophine قصيرة"},
           {"texte": "→ fibres fragiles qui se déchirent → faiblesse musculaire : myopathie", "mot": "les fibres كيتقطعو"},
           {"texte": "Le gène détermine la protéine, qui détermine le caractère", "mot": "le gène كيحدد la protéine"}],
         "parole": ("la question cinq. عند le garçon malade، l'allèle muté فيه substitution non-sens، ف le triplet trente-neuf، إذن codon stop U A G بكري. "
                    "la dystrophine قصيرة، seulement trente-huit acides aminés، non fonctionnelle. la membrane كتولي ضعيفة، les fibres كيتقطعو وكيموتو، وكتجي faiblesse musculaire: la myopathie de Duchenne. "
                    "عند le garçon sain، allèle normal، dystrophine fonctionnelle، و les muscles عاديين. إذن le gène كيحدد la protéine، و la protéine كتحدد le caractère.")},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : le même caractère à trois échelles",
     "screen_content": {"lead": "Molécule (la protéine), cellule (la fibre), organisme (les mouvements) : on compare à chaque niveau."},
     "visual": {"kind": "simulation", "url": ECH, "caption": "Du gène au caractère : les échelles"},
     "speech_text": {"mixed": ("le caractère كيتشاف ف بزاف ديال les niveaux، بحال هاد l'exemple ديال الدرس. "
                               "ف le niveau moléculaire، كنشوفو la protéine: هنا la dystrophine، كاينة عند le sain، و ما كايناش عند le malade. "
                               "ف le niveau cellulaire، كنشوفو la cellule: la fibre musculaire سالمة، ولا la fibre كتقطع وكتموت. "
                               "ف le niveau macroscopique، كنشوفو l'organisme: كيمشي عادي، ولا faiblesse musculaire. "
                               "إذن la protéine هي السبب ديال le caractère.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "moléculaire : dystrophine présente / absente", "mot": "هنا la dystrophine"},
                  {"texte": "cellulaire : fibre intacte / fibre déchirée", "mot": "la fibre musculaire سالمة"},
                  {"texte": "macroscopique : mouvements normaux / faiblesse musculaire", "mot": "ولا faiblesse musculaire"}],
       "pointage": [{"mot": "بحال هاد l'exemple", "commande": "play_until", "parametres": {"moment": "niveau_gene"}},
                    {"mot": "ف le niveau moléculaire", "commande": "play_until", "parametres": {"moment": "niveau_proteine"}},
                    {"mot": "ف le niveau moléculaire", "repere": "echelle_proteine"},
                    {"mot": "هنا la dystrophine", "cible": "centre:0"},
                    {"mot": "ف le niveau cellulaire", "commande": "play_until", "parametres": {"moment": "niveau_cellule"}},
                    {"mot": "ف le niveau cellulaire", "repere": "echelle_cellule"},
                    {"mot": "la fibre musculaire سالمة", "cible": "centre:1"},
                    {"mot": "ف le niveau macroscopique", "commande": "play_until", "parametres": {"moment": "niveau_organisme"}},
                    {"mot": "ف le niveau macroscopique", "repere": "echelle_organisme"},
                    {"mot": "ولا faiblesse musculaire", "cible": "centre:2"},
                    {"mot": "إذن la protéine هي السبب", "commande": "play_until", "parametres": {"moment": "relation"}},
                    {"mot": "إذن la protéine هي السبب", "repere": "relation"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : depuis le brin transcrit, on fait la complémentarité",
     "screen_content": {"lead": "Brin transcrit → ARNm complémentaire (A → U, T → A, C → G, G → C) ; on traduit jusqu'au stop."},
     "visual": {"kind": "simulation", "url": BRINS, "caption": "Brin non transcrit, brin transcrit, ARNm"},
     "speech_text": {"mixed": ("شوف هاد تلاتة ديال السطور: لفوق le brin non transcrit، من بعد le brin transcrit، من بعد l'A R N messager. "
                               "هنا، le document كيعطيك le brin transcrit. الطريق هو: l'A R N messager هو le complémentaire ديال le brin transcrit. "
                               f"A كتولي U، T كتولي A، C كتولي G، و G كتولي C. مثلا {L(TN1[0])} كتولي {L(RN1[0])}. "
                               "من بعد كنترجمو codon ب codon. وف أول codon stop، كنكتبو arrêt de la traduction، وكنحبسو.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "brin transcrit → ARNm : A → U, T → A, C → G, G → C", "mot": "A كتولي U، T كتولي A"},
                  {"texte": f"{TN1[0]} → {RN1[0]}", "mot": f"مثلا {L(TN1[0])}"}],
       "pointage": [{"mot": "شوف هاد تلاتة", "commande": "play_until", "parametres": {"moment": "trois_lignes"}},
                    {"mot": "لفوق le brin non transcrit", "repere": "ligne_non_transcrit"},
                    {"mot": "من بعد le brin transcrit", "repere": "ligne_transcrit"},
                    {"mot": "من بعد l'A R N messager", "repere": "ligne_arnm"},
                    {"mot": "الطريق هو", "commande": "play_until", "parametres": {"moment": "chemin_transcrit"}},
                    {"mot": "هو le complémentaire", "repere": "chemin_1"},
                    {"mot": "A كتولي U، T كتولي A", "cible": "centre:0"},
                    {"mot": f"مثلا {L(TN1[0])}", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : un codon devient stop : non-sens",
     "screen_content": {"lead": "Une lettre remplacée et le codon devient UAA, UAG ou UGA : la traduction s'arrête trop tôt."},
     "visual": {"kind": "simulation", "url": MUT, "caption": "Allèle normal et allèle muté alignés"},
     "speech_text": {"mixed": ("شوف l'exemple ديال الدرس: T G G ولات T A G. حرف واحد تبدل. "
                               "le codon U G G، اللي كان كيعطي le tryptophane، ولا U A G: un codon stop. la traduction كتحبس بكري، و la protéine كتولي قصيرة. "
                               "هادي mutation non-sens. ف التمرين ديالنا، نفس الشي: ف le triplet trente-neuf، le codon C A G ولا U A G.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "un codon devient UAA, UAG ou UGA : arrêt de la traduction", "mot": "un codon stop"},
                  {"texte": "triplet 39 : CAG (Gln) → UAG (stop) : non-sens", "mot": "ف le triplet trente-neuf"}],
       "pointage": [{"mot": "شوف l'exemple", "commande": "set_time", "parametres": {"time_s": 14.2}},
                    {"mot": "T G G ولات T A G", "commande": "play_until", "parametres": {"moment": "non_sens_evt"}},
                    {"mot": "حرف واحد تبدل", "repere": "base_mutee"},
                    {"mot": "un codon stop", "repere": "codon_stop"},
                    {"mot": "un codon stop", "cible": "centre:0"},
                    {"mot": "la protéine كتولي قصيرة", "repere": "aa_mute"},
                    {"mot": "هادي mutation non-sens", "commande": "play_until", "parametres": {"moment": "non_sens"}},
                    {"mot": "هادي mutation non-sens", "repere": "type_mutation"},
                    {"mot": "ف le triplet trente-neuf", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : au codon stop, la chaîne est libérée",
     "screen_content": {"lead": "Un acide aminé par codon, du AUG jusqu'au codon avant le stop : n = 39 − 1 = 38."},
     "visual": {"kind": "simulation", "url": TRAD, "caption": "La terminaison : le ribosome arrive au codon stop"},
     "speech_text": {"mixed": ("شوف le ribosome. كيقرا codon ب codon، وكل codon كيزيد acide aminé. "
                               "ملي كيوصل ل un codon stop، ما كيجي حتى A R N de transfert، و la chaîne كتخرج. "
                               "إذن la chaîne فيها acide aminé ل كل codon، من A U G حتى ل le codon اللي قبل le stop. "
                               "ف التمرين، le stop ف le triplet trente-neuf: n égale trente-neuf moins un، égale trente-huit acides aminés، au lieu de trois mille six cent quatre-vingt-cinq.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "codon stop : aucun acide aminé, la chaîne est libérée", "mot": "و la chaîne كتخرج"},
                  {"texte": "n = 39 − 1 = 38 acides aminés (au lieu de 3685)", "mot": "n égale trente-neuf moins un"}],
       "pointage": [{"mot": "شوف le ribosome", "commande": "set_time", "parametres": {"time_s": 25.8}},
                    {"mot": "ملي كيوصل ل un codon stop", "commande": "play_until", "parametres": {"moment": "codon_stop"}},
                    {"mot": "ملي كيوصل ل un codon stop", "repere": "codon_stop"},
                    {"mot": "و la chaîne كتخرج", "commande": "play_until", "parametres": {"moment": "chaine_liberee"}},
                    {"mot": "و la chaîne كتخرج", "repere": "chaine"},
                    {"mot": "و la chaîne كتخرج", "cible": "centre:0"},
                    {"mot": "n égale trente-neuf moins un", "cible": "centre:1"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : gène → ARNm → protéine → caractère",
     "screen_content": {"lead": "Le gène est transcrit en ARNm, traduit en protéine ; la protéine fait le caractère."},
     "visual": {"kind": "simulation", "url": SCH, "caption": "Du gène au caractère"},
     "speech_text": {"mixed": ("ف le noyau، le gène ديال la dystrophine كاين ف l'A D N. la transcription كتعطي l'A R N messager. "
                               "كيخرج من un pore nucléaire. ف le cytoplasme، la traduction كتعطي la protéine. "
                               "عند le garçon malade، l'A R N messager فيه codon stop بكري: la protéine قصيرة، non fonctionnelle. "
                               "les fibres كيتقطعو، وكتجي la faiblesse musculaire: هادا هو le caractère. "
                               "le gène كيحدد la protéine، و la protéine كتحدد le caractère.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "allèle muté → ARNm avec stop précoce → dystrophine non fonctionnelle", "mot": "la protéine قصيرة، non fonctionnelle"},
                  {"texte": "→ fibres déchirées → faiblesse musculaire", "mot": "وكتجي la faiblesse musculaire"}],
       "pointage": [{"mot": "ف le noyau", "commande": "play_until", "parametres": {"moment": "gene"}},
                    {"mot": "كاين ف l'A D N", "repere": "gene"},
                    {"mot": "la transcription كتعطي", "commande": "play_until", "parametres": {"moment": "arnm"}},
                    {"mot": "la transcription كتعطي", "repere": "arnm"},
                    {"mot": "كيخرج من un pore nucléaire", "commande": "play_until", "parametres": {"moment": "pore"}},
                    {"mot": "كيخرج من un pore nucléaire", "repere": "pore"},
                    {"mot": "la traduction كتعطي la protéine", "commande": "play_until", "parametres": {"moment": "proteine"}},
                    {"mot": "la traduction كتعطي la protéine", "repere": "proteine"},
                    {"mot": "la protéine قصيرة، non fonctionnelle", "cible": "centre:0"},
                    {"mot": "هادا هو le caractère", "commande": "play_until", "parametres": {"moment": "caractere"}},
                    {"mot": "هادا هو le caractère", "repere": "caractere"},
                    {"mot": "وكتجي la faiblesse musculaire", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    association("fa_s1", "Plus facile : un niveau, une observation", "Relie chaque niveau à ce qu'on observe chez le garçon malade.",
      "سؤال ساهل: ربط كل niveau مع داكشي اللي كنشوفو عند le garçon malade.", "Relie chaque niveau à l'observation du garçon malade.",
      [("1", "Niveau moléculaire"), ("2", "Niveau cellulaire"), ("3", "Niveau macroscopique")],
      [("a", "Dystrophine absente"), ("b", "Fibres musculaires qui se déchirent"), ("c", "Faiblesse musculaire, chutes")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : la dystrophine est une molécule (protéine).", "برافو: la dystrophine هي molécule، protéine."),
       "1-b": (False, "La fibre est une cellule, pas une molécule.", "لا، la fibre هي cellule، ماشي molécule."),
       "1-c": (False, "Les chutes se voient sur tout l'organisme.", "لا، كيطيح: هادشي كيتشاف ف l'organisme كامل."),
       "2-a": (False, "La dystrophine est une molécule, plus petite qu'une cellule.", "لا، la dystrophine هي molécule، صغر من la cellule."),
       "2-b": (True, "Oui : la fibre musculaire est une cellule.", "برافو: la fibre musculaire هي cellule."),
       "2-c": (False, "La faiblesse se voit à l'échelle de l'organisme.", "لا، la faiblesse كتشاف ف l'organisme."),
       "3-a": (False, "Une protéine ne se voit pas à l'œil nu.", "لا، la protéine ما كتشافش بالعين."),
       "3-b": (False, "Une fibre se voit au microscope : niveau cellulaire.", "لا، la fibre كتشاف ب le microscope: niveau cellulaire."),
       "3-c": (True, "Oui : la faiblesse musculaire se voit sur l'organisme entier.", "برافو: la faiblesse musculaire كتشاف ف l'organisme.")},
      ("(1 ; a) (2 ; b) (3 ; c) : molécule, cellule, organisme.", "molécule، cellule، organisme.")),
    qcm_facile("fa_s2", "Plus facile : le codon depuis le brin transcrit", "سؤال ساهل: le codon من le brin transcrit.",
      f"Brin transcrit : {TN1[0]}. Le codon de l'ARNm est…", [RN1[0], arn(TN1[0]), TN1[0][::-1].translate(str.maketrans("ATCG", "UAGC"))], 0, {
        "0": {"juste": rep(f"مزيان! le complémentaire: {L(TN1[0])} كتولي {L(RN1[0])}.", f"Juste : {TN1[0]} → {RN1[0]}.")},
        "1": {"1": rep("ما تقلقش. هنا le brin transcrit: خاصك la complémentarité، ماشي غير T كتولي U. عاود اختار.", "Brin transcrit : il faut la complémentarité, pas seulement T → U. Réessaie."),
              "2": rep(f"الجواب هو {L(RN1[0])}: le complémentaire ديال le brin transcrit.", f"Réponse : {RN1[0]} (complémentaire).")},
        "2": {"1": rep("قريب! la complémentarité صحيحة، ولكن قلبتي الترتيب ديال الحروف. خلي نفس الترتيب. عاود اختار.", "Complémentarité juste, mais lettres inversées : garde l'ordre. Réessaie."),
              "2": rep(f"الجواب هو {L(RN1[0])}. كل حرف تحت الحرف ديالو، بنفس الترتيب.", f"Réponse : {RN1[0]}.")}},
      "Le brin transcrit est C G T. Quel est le codon de l'ARNm ?"),
    qcm_facile("fa_s3", "Plus facile : reconnaître le codon stop", "سؤال ساهل: شمن واحد هو codon stop؟",
      "Lequel de ces codons de l'ARNm est un codon stop ?", ["UAG", "CAG", "AUG"], 0, {
        "0": {"juste": rep("برافو! U A G هو codon stop، ما كيعطي حتى acide aminé.", "Juste : UAG est un codon stop.")},
        "1": {"1": rep("ما تقلقش. C A G كيعطي la glutamine. les codons stop هوما U A A، U A G، U G A. عاود اختار.", "CAG donne Gln. Les stops : UAA, UAG, UGA. Réessaie."),
              "2": rep("الجواب هو U A G. C A G كيعطي la glutamine.", "Réponse : UAG (CAG = Gln).")},
        "2": {"1": rep("قريب! A U G هو le codon d'initiation، كيعطي la méthionine. عاود اختار.", "AUG est le codon d'initiation (Met). Réessaie."),
              "2": rep("الجواب هو U A G. A U G هو le codon d'initiation.", "Réponse : UAG (AUG = initiation).")}},
      "Lequel est un codon stop : U A G، C A G، ou A U G ?"),
    qcm_facile("fa_s4", "Plus facile : compter les acides aminés", "سؤال ساهل: حسب les acides aminés.",
      "Un ARNm commence par AUG (triplet 1) et a son premier codon stop au triplet 5. La protéine compte…", ["4 acides aminés", "5 acides aminés", "3 acides aminés"], 0, {
        "0": {"juste": rep("مزيان! من le triplet un حتى ل le triplet quatre: quatre acides aminés. le stop ما كيعطي والو.", "Juste : triplets 1 à 4 → 4 acides aminés.")},
        "1": {"1": rep("ما تقلقش. واش le codon stop كيعطي acide aminé؟ عاود اختار.", "Le codon stop donne-t-il un acide aminé ? Réessaie."),
              "2": rep("الجواب: c'est quatre، cinq moins un، حيت le stop ما كيعطي حتى acide aminé.", "Réponse : 4 (= 5 − 1).")},
        "2": {"1": rep("قريب! A U G حتى هو كيعطي acide aminé، la méthionine. عاود اختار.", "AUG donne aussi un acide aminé (Met). Réessaie."),
              "2": rep("الجواب: c'est quatre. A U G كيتحسب، و le stop ما كيتحسبش.", "Réponse : 4 (AUG compte, le stop non).")}},
      "le premier codon stop est au triplet cinq. Combien d'acides aminés ?"),
    vrai_faux("fa_s5", "Plus facile : gène, protéine, caractère", "Vrai ou faux ?",
      "سؤال ساهل: صحيح ولا غالط؟", [
        ("L'allèle muté donne une dystrophine raccourcie, non fonctionnelle.", True, "Vrai : le codon stop arrête la traduction au triplet 39."),
        ("La mutation agit directement sur les muscles sans passer par la protéine.", False, "Faux : gène → protéine → cellule → organisme ; la protéine est un maillon obligatoire."),
        ("Sans dystrophine fonctionnelle, la membrane des fibres musculaires devient fragile.", True, "Vrai : document 1, niveau cellulaire."),
        ("Le gène détermine la protéine, qui détermine le caractère.", True, "Vrai : c'est la relation gène – protéine – caractère.")])
  ]}]},
  "similaire": {
    "id": "svt_ex_ch4_non_sens_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Même étude chez un autre garçon atteint de myopathie de Duchenne (document 1 identique). "
                f"Document 2 : extrait du brin transcrit du gène de la dystrophine (triplets {D2} à {D2 + 6}), séquences simplifiées. "
                "Le triplet 1 correspond au codon AUG ; la dystrophine normale compte 3685 acides aminés."),
      "intro_dit": "نفس الدراسة، عند garçon آخر. جزء آخر من le brin transcrit ديال le gène ديال la dystrophine.",
      "figures": [fig_tableau("Document 1 : le phénotype aux trois niveaux", ["Niveau", "Garçon sain", "Garçon malade"], NIVEAUX,
                              "Le même caractère observé à l'échelle de la molécule, de la cellule et de l'organisme."),
                  seqs_fig("Document 2 : brin transcrit (3′ → 5′)", D2, TN2, TM2, "Gène de la dystrophine : allèle normal et allèle muté.")],
      "donnees": [f"Allèle normal (brin transcrit, 3′ → 5′) : {' '.join(TN2)}", f"Allèle muté (brin transcrit, 3′ → 5′) : {' '.join(TM2)}",
                  f"Les triplets sont numérotés de {D2} à {D2 + 6} ; le triplet 1 correspond au codon AUG.", "Dystrophine normale : 3685 acides aminés.", CODE2],
      "questions": [
        {"id": "1", "texte": "Comparer le phénotype des deux garçons aux trois niveaux, puis déduire la relation protéine – caractère.",
         "reponse": {"type": "phrase", "attendu": ("Moléculaire : dystrophine présente / absente. Cellulaire : fibres intactes / fibres fragiles qui se déchirent et meurent. "
                                                   "Macroscopique : mouvements normaux / faiblesse musculaire. On en déduit que l'absence de la protéine entraîne le caractère malade.")},
         "clavier": {"aides": ["moléculaire", "cellulaire", "macroscopique", "On en déduit que"], "pieges": []},
         "correction": {"lignes": [{"texte": "1 : dystrophine absente → fibres fragiles → faiblesse musculaire", "mot": "ما كايناش la dystrophine"},
                                   {"texte": "On en déduit que le caractère dépend de la protéine", "mot": "On en déduit que"}],
                        "parole": "la question un. عند le garçon malade، ما كايناش la dystrophine، les fibres كيتقطعو، وكاينة faiblesse musculaire. On en déduit que le caractère كيتبع la protéine."}},
        {"id": "2", "texte": "Donner la séquence de l'ARNm et la séquence des acides aminés de chaque allèle.",
         "reponse": {"type": "phrase", "attendu": f"Allèle normal : ARNm : {ARN_N2} ; acides aminés : {SEQ_N2}. Allèle muté : ARNm : {ARN_M2} ; acides aminés : {SEQ_M2}."},
         "clavier": {"aides": ["ARNm :", "complémentarité", "arrêt de la traduction"], "pieges": ["Stop"]},
         "correction": {"lignes": [{"texte": f"2 : normal : {ARN_N2} → {SEQ_N2}", "mot": "l'allèle normal"},
                                   {"texte": f"muté : {ARN_M2} → {SEQ_M2}", "mot": "arrêt de la traduction"}],
                        "parole": (f"la question deux. l'allèle normal: {'، '.join(L(c) for c in RN2)}، و les acides aminés: {'، '.join(NOM[a] for a in AN2)}. "
                                   f"l'allèle muté: le triplet cinquante-quatre كيعطي {L(RM2[J2])}، codon stop: {'، '.join(NOM[a] for a in AM2)}، ومن بعد arrêt de la traduction.")}},
        {"id": "3", "texte": "Déterminer la mutation (type, nucléotide, triplet) et nommer sa conséquence sur la traduction. Justifier.",
         "reponse": {"type": "phrase", "attendu": "Seul le triplet 54 diffère : GCT devient ACT sur le brin transcrit (G remplacé par A). Le codon CGA (Arg) devient UGA, un codon stop : substitution non-sens."},
         "clavier": {"aides": ["triplet 54", "substitution", "non-sens", "UGA"], "pieges": ["faux-sens"]},
         "correction": {"lignes": [{"texte": "3 : triplet 54 : GCT → ACT (G remplacé par A)", "mot": "le triplet cinquante-quatre"},
                                   {"texte": "CGA (Arg) → UGA (stop) : substitution non-sens", "mot": "substitution non-sens"}],
                        "parole": "la question trois. le triplet cinquante-quatre: G C T ولات A C T. le codon C G A ولا U G A، codon stop. هادي substitution non-sens."}},
        {"id": "4", "texte": "Calculer le nombre d'acides aminés de la protéine de l'allèle muté, puis expliquer pourquoi elle est non fonctionnelle.",
         "reponse": {"type": "valeur", "grandeur": "n", "valeur": N_MUTE2, "unite": "acides aminés", "tolerance": 0.02,
                     "attendu": "Stop au triplet 54 : n = 54 − 1 = 53 acides aminés (au lieu de 3685) : protéine très raccourcie, non fonctionnelle."},
         "clavier": {"aides": ["n = 54 − 1", "acides aminés"], "pieges": ["n = 54"]},
         "correction": {"lignes": [{"texte": "4 : n = 54 − 1 = 53 acides aminés", "mot": "n égale cinquante-quatre moins un"},
                                   {"texte": "au lieu de 3685 : non fonctionnelle", "mot": "non fonctionnelle"}],
                        "parole": "la question quatre. n égale cinquante-quatre moins un، égale cinquante-trois acides aminés، au lieu de trois mille six cent quatre-vingt-cinq: la protéine non fonctionnelle."}},
        {"id": "5", "texte": "Montrer la relation gène – protéine – caractère chez le garçon malade.",
         "reponse": {"type": "phrase", "attendu": ("Allèle muté (non-sens au triplet 54) → codon stop UGA prématuré → dystrophine de 53 acides aminés, non fonctionnelle → fibres fragiles qui se déchirent "
                                                   "→ faiblesse musculaire : myopathie. Le gène détermine la protéine, qui détermine le caractère.")},
         "clavier": {"aides": ["allèle muté", "codon stop", "→"], "pieges": []},
         "correction": {"lignes": [{"texte": "5 : allèle muté → stop UGA → dystrophine non fonctionnelle → fibres déchirées → myopathie", "mot": "l'allèle muté"},
                                   {"texte": "Le gène détermine la protéine, qui détermine le caractère", "mot": "le gène كيحدد la protéine"}],
                        "parole": "la question cinq. l'allèle muté، codon stop U G A، la dystrophine non fonctionnelle، les fibres كيتقطعو، faiblesse musculaire. إذن le gène كيحدد la protéine، و la protéine كتحدد le caractère."}}
      ]}}
}
ecrire(EX, sys.argv[1])
