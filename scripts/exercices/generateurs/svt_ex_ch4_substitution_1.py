# Exercice SVT ch. 4 (relation gène – protéine), niveau moyen : substitution faux-sens, phénylcétonurie.
# Entraîne : décrire puis déduire (courbe), relation protéine – caractère, ARNm et acides aminés depuis le brin NON transcrit,
# comparer deux allèles et nommer la mutation, origine génétique en chaîne de flèches (cas_types arn_aa, origine_genetique,
# proteine_caractere de l'exploration).
# Sources comparées (lecture seule, rien de copié) :
# - exploration/relation_gene_proteine.json : cas_types (arn_aa 17/20 sessions, origine_genetique, proteine_caractere), pièges
#   (brin non transcrit, T → U, stop, tiret), erreurs_examen, insistances ; vidéos d'exercices (Driss DOTCOM 2025 N, Wessal,
#   Ouissam, Ikram, AJIN9RAW) résumées dans le même fichier.
# - nationaux : 2019 N (BRCA1, triplets 368-375, « déterminez la séquence… »), 2021 N, 2022 N, 2024 N, 2025 N (brin non transcrit,
#   substitution faux-sens, « expliquez l'origine génétique ») : mêmes verbes et même chaîne, situation différente.
# - séries en ligne : recherche faite (dyrassa « Notion de l'information génétique, série 7 », alloschool « Expression de
#   l'information génétique – exercices » N. Bahsina, série du lycée Naciri sur la rétinite pigmentaire, exercices PAH de
#   l'université de Tours) ; les PDF n'ont pas pu être ouverts (domaines bloqués par le réseau de la session) : seuls les
#   titres et extraits du moteur de recherche ont été lus.
# Situation : la phénylcétonurie (enzyme PAH) n'est pas un sujet national 2016-2025 ; séquences inventées (simplifiées).
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

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


def courbe_phe(saine, malade, ymax, titre):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": 8, "nom": "t", "unite": "h", "graduations": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
                     "y": {"min": 0, "max": ymax, "nom": "[Phe]", "unite": "mg/L", "graduations": list(range(0, ymax + 1, 50))}},
            "legende": "Concentration de la phénylalanine dans le sang ; repas riche en phénylalanine pris à t = 0.",
            "elements": [{"f": "ligne", "pts": saine, "couleur": "cyan"},
                         {"f": "texte", "at": [6.2, saine[-1][1] + 22], "t": "personne saine", "taille": "petit", "couleur": "cyan"},
                         {"f": "ligne", "pts": malade, "couleur": "orange"},
                         {"f": "texte", "at": [6.2, malade[-1][1] + 22], "t": "personne malade", "taille": "petit", "couleur": "orange"}]
                        + [{"f": "point", "at": p, "t": str(p[1]), "pos": "ne", "couleur": c} for p, c in
                           [(saine[0], "cyan"), (saine[1], "cyan"), (saine[4], "cyan"), (malade[0], "orange"), (malade[2], "orange")]]}


# ── données (une seule fois : tout le reste en découle) ─────────────────────────────────
D1, N1 = 47, ["GCT", "TTC", "CGA", "GAT", "CTC", "TAC", "GGA"]
M1 = N1[:2] + ["CAA"] + N1[3:]
J1 = 2                                                    # index du triplet muté (triplet 49)
AN1, AM1 = [aa(c) for c in N1], [aa(c) for c in M1]
assert AN1 == ["Ala", "Phe", "Arg", "Asp", "Leu", "Tyr", "Gly"] and AM1[J1] == "Gln" and AN1[:J1] + AN1[J1 + 1:] == AM1[:J1] + AM1[J1 + 1:]
assert [i for i in range(7) if N1[i] != M1[i]] == [J1] and sum(a != b for a, b in zip(N1[J1], M1[J1])) == 1
SAINE1 = [[0, 10], [1, 40], [2, 30], [4, 14], [6, 10], [8, 10]]
MALADE1 = [[0, 200], [1, 265], [2, 300], [4, 300], [6, 300], [8, 300]]
ARN_N1, ARN_M1 = " ".join(arn(c) for c in N1), " ".join(arn(c) for c in M1)
SEQ_N1, SEQ_M1 = " – ".join(AN1), " – ".join(AM1)

# similaire : autre extrait, autre substitution faux-sens
D2, N2 = 112, ["AAT", "GTC", "TAT", "CTG", "ACG", "GAG", "TTC"]
M2 = N2[:3] + ["CCG"] + N2[4:]
J2 = 3
AN2, AM2 = [aa(c) for c in N2], [aa(c) for c in M2]
assert AN2 == ["Asn", "Val", "Tyr", "Leu", "Thr", "Glu", "Phe"] and AM2[J2] == "Pro"
assert [i for i in range(7) if N2[i] != M2[i]] == [J2]
SAINE2 = [[0, 15], [1, 50], [2, 38], [4, 20], [6, 15], [8, 15]]
MALADE2 = [[0, 240], [1, 310], [2, 340], [4, 340], [6, 340], [8, 340]]
ARN_N2, ARN_M2 = " ".join(arn(c) for c in N2), " ".join(arn(c) for c in M2)
SEQ_N2, SEQ_M2 = " – ".join(AN2), " – ".join(AM2)

def extrait_code(codons):
    return "Extrait du code génétique : " + " ; ".join(f"{c} : {AB[CODE[c]]}" for c in codons)

CODE1 = extrait_code(["GCU", "UUC", "CGA", "AGA", "CAA", "CAG", "GAU", "GAC", "CUC", "UAC", "GGA", "UAA"])
CODE2 = extrait_code(["AAU", "GUC", "UAU", "CUG", "CCG", "CCA", "ACG", "GAG", "GAA", "UUC", "UAG"])
for c in ("CGA", "CAA", "GCU", "UUC", "GAU", "CUC", "UAC", "GGA"): assert c in CODE1
for c in [arn(x) for x in N2 + M2]: assert c in CODE2

DOC = "/media/simulations/svt/relation_gene_proteine-tableau/"
ALB, BRINS = DOC + "documents.html?vue=albinisme", DOC + "transcription.html?vue=brins"
MUT, ECH = DOC + "mutation.html?vue=mutation", DOC + "drepanocytose.html?vue=echelles"

triplets_ecrits = lambda d, n: f"triplets {d} à {d + n - 1}"

EX = {
  "id": "svt_ex_ch4_substitution_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "relation_gene_proteine", "cours": "svt_ch4_relation_gene_proteine",
  "titre": "La phénylcétonurie : une enzyme du foie et une substitution", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire une courbe puis déduire", "Montrer la relation protéine – caractère",
                  "Écrire l'ARNm et la séquence d'acides aminés à partir du brin non transcrit",
                  "Identifier une mutation par substitution faux-sens", "Expliquer l'origine génétique d'une maladie"],
  "enonce": {
    "intro": ("La phénylcétonurie (PCU) est une maladie héréditaire : non traitée, elle provoque des troubles du développement du système nerveux. "
              "Document 1 : une personne saine et une personne atteinte de PCU prennent à t = 0 un repas riche en phénylalanine (un acide aminé) ; "
              "on mesure ensuite la concentration de la phénylalanine [Phe] dans leur sang. "
              "Document 2 : dans les cellules du foie, une enzyme, la phénylalanine hydroxylase (PAH), transforme la phénylalanine en tyrosine. "
              "Chez la personne malade, la PAH est fabriquée mais elle est non fonctionnelle. "
              f"Document 3 : extrait du brin non transcrit du gène de la PAH ({triplets_ecrits(D1, 7)}), chez la personne saine et chez la personne malade "
              "(séquences simplifiées pour l'exercice)."),
    "intro_dit": ("نقراو l'énoncé. la phénylcétonurie هي maladie héréditaire. يلا ما تعالجاتش، كتدير مشاكل ف le développement ديال le système nerveux. "
                  "le document un: personne saine و personne malade كياكلو ماكلة فيها بزاف ديال la phénylalanine، و هي acide aminé. "
                  "من بعد، كنقيسو la concentration ديال la phénylalanine ف الدم ديالهم. "
                  "le document deux: ف les cellules ديال le foie، كاينة واحد l'enzyme، la P A H، كتحول la phénylalanine ل tyrosine. "
                  "عند la personne malade، la P A H كتصاوب، ولكن non fonctionnelle. "
                  "le document trois: جزء من le brin non transcrit ديال le gène ديال la P A H، عند la personne saine و عند la personne malade."),
    "figures": [courbe_phe(SAINE1, MALADE1, 350, "Document 1 : [Phe] dans le sang après le repas"),
                fig_sequences("Document 3 : brin non transcrit (5′ → 3′)", D1,
                              [("Allèle normal", N1, "blanc"), ("Allèle muté", M1, "blanc")],
                              "Gène de la PAH : allèle de la personne saine (normal) et allèle de la personne malade (muté).")],
    "donnees": [f"Allèle normal (brin non transcrit, 5′ → 3′) : {' '.join(N1)}",
                f"Allèle muté (brin non transcrit, 5′ → 3′) : {' '.join(M1)}",
                f"Les triplets sont numérotés de {D1} à {D1 + 6}.",
                CODE1,
                "La PAH (enzyme du foie) : phénylalanine → tyrosine."],
    "questions": [
      {"id": "1", "texte": "Décrire l'évolution de [Phe] chez la personne saine puis chez la personne malade (document 1), puis déduire ce que devient la phénylalanine chez chacune.",
       "texte_dit": "la question un: وصف l'évolution ديال la concentration ديال la phénylalanine، عند la personne saine، ومن بعد عند la personne malade. ومن بعد استنتج شنو كيوقع ل la phénylalanine عند كل وحدة.",
       "reponse": {"type": "phrase", "attendu": ("Personne saine : avant le repas, [Phe] = 10 mg/L ; après le repas, elle augmente jusqu'à 40 mg/L à 1 h, puis diminue et revient à 10 mg/L vers 6 h. "
                                                 "Personne malade : [Phe] est déjà élevée avant le repas (200 mg/L) ; elle augmente jusqu'à 300 mg/L à 2 h, puis reste constante à 300 mg/L jusqu'à 8 h. "
                                                 "On en déduit que la personne saine transforme (élimine) la phénylalanine du repas, alors que la personne malade ne la transforme pas : elle s'accumule dans son sang.")},
       "clavier": {"aides": ["augmente", "diminue", "reste constante", "mg/L", "On en déduit que", "s'accumule"], "pieges": ["la personne malade élimine la phénylalanine"]},
       "aides": [
         {"texte": "Lis chaque courbe en deux parties : la valeur à t = 0, puis ce qui se passe après le repas (monte, descend, reste constante), avec les valeurs.",
          "dit": "قرا كل courbe ف جوج ديال الأجزاء: la valeur ف t égale zéro، ومن بعد شنو كيوقع من بعد الماكلة، واش كتطلع، كتهبط، ولا كتبقى ثابتة، مع les valeurs."},
         {"texte": "Si la concentration redescend, la phénylalanine disparaît du sang (elle est transformée) ; si elle reste haute, elle n'est pas transformée.",
          "dit": "يلا la concentration رجعات هبطات، la phénylalanine كتمشي من الدم، يعني كتحول. يلا بقات طالعة، ما كتحولش."}],
       "correction": {"lignes": [
           {"texte": "1 : personne saine : 10 mg/L, augmente jusqu'à 40 mg/L à 1 h, puis revient à 10 mg/L vers 6 h", "mot": "عند la personne saine"},
           {"texte": "personne malade : 200 mg/L, augmente jusqu'à 300 mg/L à 2 h, puis reste constante à 300 mg/L", "mot": "عند la personne malade"},
           {"texte": "On en déduit que : la saine transforme la phénylalanine ; chez la malade, elle s'accumule dans le sang", "mot": "On en déduit que"}],
         "parole": ("la question un. عند la personne saine، قبل الماكلة، la concentration est de dix milligrammes par litre. من بعد الماكلة، كتزاد jusqu'à quarante milligrammes par litre، à une heure، "
                    "ومن بعد كتنقص، وكترجع à dix milligrammes par litre، vers six heures. "
                    "عند la personne malade، la concentration طالعة من البداية: elle est de deux cents milligrammes par litre. كتزاد jusqu'à trois cents milligrammes par litre، à deux heures، ومن بعد كتبقى ثابتة. "
                    "On en déduit que la personne saine كتحول la phénylalanine، أما la personne malade ما كتحولهاش، وكتجمع ف الدم ديالها.")},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "En exploitant les documents 1 et 2, montrer la relation protéine – caractère.",
       "texte_dit": "la question deux: باستعمال le document un و le document deux، بين la relation protéine caractère.",
       "reponse": {"type": "phrase", "attendu": ("Personne saine : PAH fonctionnelle → la phénylalanine est transformée en tyrosine → [Phe] reste faible dans le sang → développement nerveux normal (phénotype sain). "
                                                 "Personne malade : PAH non fonctionnelle → la phénylalanine n'est pas transformée → elle s'accumule dans le sang (300 mg/L) → troubles du système nerveux (phénylcétonurie). "
                                                 "D'où la relation protéine – caractère : le caractère dépend de la protéine (la PAH).")},
       "clavier": {"aides": ["PAH fonctionnelle", "PAH non fonctionnelle", "→", "tyrosine", "s'accumule", "D'où la relation protéine – caractère"], "pieges": ["la PAH est absente"]},
       "aides": [
         {"texte": "Écris deux lignes parallèles, personne saine et personne malade, en partant de la protéine (la PAH).",
          "dit": "كتب جوج ديال السطور، واحد ل la personne saine، و واحد ل la personne malade، وبدا ب la protéine، يعني la P A H."},
         {"texte": "Chaque ligne : état de la PAH → ce qu'elle fait (document 2) → [Phe] dans le sang (document 1) → phénotype.",
          "dit": "ف كل سطر: واش la P A H fonctionnelle، شنو كدير، شحال la phénylalanine ف الدم، ومن بعد le phénotype."}],
       "correction": {"lignes": [
           {"texte": "2 : saine : PAH fonctionnelle → Phe transformée en tyrosine → [Phe] faible → phénotype sain", "mot": "la P A H fonctionnelle"},
           {"texte": "malade : PAH non fonctionnelle → Phe non transformée → accumulation (300 mg/L) → troubles nerveux", "mot": "la P A H non fonctionnelle"},
           {"texte": "D'où la relation protéine – caractère", "mot": "D'où la relation protéine caractère"}],
         "parole": ("la question deux. عند la personne saine، la P A H fonctionnelle، كتحول la phénylalanine ل tyrosine، la concentration كتبقى قليلة، و le système nerveux كيتطور مزيان. "
                    "عند la personne malade، la P A H non fonctionnelle، la phénylalanine ما كتحولش، كتجمع ف الدم، jusqu'à trois cents milligrammes par litre، وكتجي les troubles ديال le système nerveux. "
                    "D'où la relation protéine caractère.")},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "En vous basant sur le document 3 et l'extrait du code génétique, donner la séquence de l'ARNm et la séquence des acides aminés correspondant à chaque allèle.",
       "texte_dit": "la question trois: باستعمال le document trois و le code génétique، عطي la séquence ديال l'A R N messager، و la séquence ديال les acides aminés، ل كل allèle.",
       "reponse": {"type": "phrase", "attendu": (f"Allèle normal : ARNm : {ARN_N1} ; acides aminés : {SEQ_N1}. "
                                                 f"Allèle muté : ARNm : {ARN_M1} ; acides aminés : {SEQ_M1}.")},
       "clavier": {"aides": ["ARNm :", "U", "–", "Arg", "Gln"], "pieges": [" ".join(c.translate(str.maketrans("ATCG", "UAGC")) for c in N1[:2]), "T"]},
       "aides": [
         {"texte": "Le document donne le brin NON transcrit : l'ARNm a les mêmes lettres, chaque T devient U.",
          "dit": "le document كيعطيك le brin non transcrit. l'A R N messager عندو نفس الحروف، غير كل T كتولي U. ما تديرش la complémentarité."},
         {"texte": "Écris un codon sous chaque triplet, cherche chaque codon dans l'extrait du code, et sépare les acides aminés par des tirets.",
          "dit": "كتب codon تحت كل triplet، قلب على كل codon ف le code génétique، وكتب les acides aminés بيناتهم tiret."}],
       "correction": {"lignes": [
           {"texte": f"3 : allèle normal : ARNm : {ARN_N1}", "mot": "l'allèle normal"},
           {"texte": f"acides aminés : {SEQ_N1}", "mot": NOM[AN1[0]] + "، " + NOM[AN1[1]]},
           {"texte": f"allèle muté : ARNm : {ARN_M1}", "mot": "l'allèle muté"},
           {"texte": f"acides aminés : {SEQ_M1}", "mot": "بلاصة l'arginine"}],
         "parole": (f"la question trois. le brin non transcrit، إذن نفس الحروف، و T كتولي U. l'allèle normal: l'A R N messager هو {'، '.join(L(arn(c)) for c in N1)}. "
                    f"les acides aminés: {'، '.join(NOM[a] for a in AN1)}. "
                    f"l'allèle muté: نفس الشي، غير le triplet quarante-neuf، l'A R N messager فيه {L(arn(M1[J1]))}. "
                    "إذن la glutamine ف بلاصة l'arginine، والباقي بحال بحال.")},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Comparer les deux allèles puis déduire le type de la mutation responsable de la PCU.",
       "texte_dit": "la question quatre: قارن الجوج ديال les allèles، ومن بعد استنتج le type ديال la mutation اللي كتسبب la maladie.",
       "reponse": {"type": "phrase", "attendu": ("Les deux allèles sont identiques sauf au triplet 49 : CGA (allèle normal) devient CAA (allèle muté), le 2e nucléotide G est remplacé par A. "
                                                 "Le codon CGA (Arg) devient CAA (Gln) : un acide aminé est remplacé par un autre. "
                                                 "On en déduit qu'il s'agit d'une mutation par substitution, de type faux-sens.")},
       "clavier": {"aides": ["triplet 49", "substitution", "faux-sens", "G remplacé par A", "Arg → Gln"], "pieges": ["délétion", "non-sens", "silencieuse"]},
       "aides": [
         {"texte": "Compare les deux allèles triplet par triplet, du premier au dernier : un seul triplet diffère. Lequel ? Quelle lettre a changé ?",
          "dit": "قارن triplet ب triplet، من اللول حتى ل اللخر. غير triplet واحد اللي مختلف. شمن واحد؟ وشمن حرف تبدل؟"},
         {"texte": "Même nombre de nucléotides et une seule lettre changée : substitution. Puis regarde l'acide aminé : même, autre, ou stop ?",
          "dit": "حرف واحد تبدل ب حرف آخر، بلا ما يتزاد ولا ينقص: هادي substitution. ومن بعد شوف l'acide aminé: واش نفسو، واش آخر، ولا stop؟"}],
       "correction": {"lignes": [
           {"texte": "4 : seul le triplet 49 diffère : CGA → CAA (G remplacé par A)", "mot": "غير le triplet quarante-neuf"},
           {"texte": "codon CGA (Arg) → CAA (Gln) : un acide aminé remplacé", "mot": "l'arginine تبدلات ب la glutamine"},
           {"texte": "donc mutation par substitution faux-sens", "mot": "substitution faux-sens"}],
         "parole": ("la question quatre. الجوج ديال les allèles بحال بحال، غير le triplet quarante-neuf: C G A ولات C A A. le nucléotide G تبدل ب A. "
                    "le codon C G A كان كيعطي l'arginine، و C A A كيعطي la glutamine: l'arginine تبدلات ب la glutamine. إذن هادي mutation par substitution faux-sens.")},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "À partir de ce qui précède, expliquer l'origine génétique de la phénylcétonurie.",
       "texte_dit": "la question cinq: من داكشي اللي فات، فسر l'origine génétique ديال la phénylcétonurie.",
       "reponse": {"type": "phrase", "attendu": ("Mutation par substitution du nucléotide G par A au triplet 49 du brin non transcrit du gène de la PAH → le codon CGA devient CAA "
                                                 "→ l'arginine est remplacée par la glutamine → PAH non fonctionnelle → la phénylalanine n'est plus transformée en tyrosine "
                                                 "→ elle s'accumule dans le sang → troubles du système nerveux : phénylcétonurie.")},
       "clavier": {"aides": ["substitution", "triplet 49", "brin non transcrit", "CGA → CAA", "Arg → Gln", "PAH non fonctionnelle", "→"], "pieges": ["mutation → maladie"]},
       "aides": [
         {"texte": "Fais une seule phrase avec des flèches, de l'ADN jusqu'à la maladie, sans sauter la protéine.",
          "dit": "دير جملة وحدة ب des flèches، من l'A D N حتى ل la maladie، وما تنساش la protéine ف الوسط."},
         {"texte": "Ordre : type de mutation, nucléotide, triplet, brin, gène → codon → acide aminé → PAH non fonctionnelle → [Phe] → maladie.",
          "dit": "الترتيب: le type ديال la mutation، le nucléotide، le triplet، le brin، le gène، من بعد le codon، من بعد l'acide aminé، من بعد la P A H non fonctionnelle، من بعد la phénylalanine ف الدم، ولخر حاجة la maladie."}],
       "correction": {"lignes": [
           {"texte": "5 : substitution de G par A au triplet 49 du brin non transcrit du gène de la PAH", "mot": "substitution du nucléotide G par A"},
           {"texte": "→ codon CGA → CAA → Arg remplacée par Gln", "mot": "le codon C G A ولا C A A"},
           {"texte": "→ PAH non fonctionnelle → Phe non transformée, accumulée dans le sang", "mot": "la P A H ولات non fonctionnelle"},
           {"texte": "→ troubles nerveux : phénylcétonurie", "mot": "هادي هي la phénylcétonurie"}],
         "parole": ("la question cinq. كنكتبو جملة وحدة، حلقة ب حلقة. mutation par substitution du nucléotide G par A، au triplet quarante-neuf، du brin non transcrit، du gène de la P A H. "
                    "إذن le codon C G A ولا C A A، و l'arginine تبدلات ب la glutamine. la P A H ولات non fonctionnelle، la phénylalanine ما بقاتش كتحول ل tyrosine، وكتجمع ف الدم. "
                    "le système nerveux ما كيتطورش مزيان: هادي هي la phénylcétonurie.")},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : une enzyme transforme une substance",
     "screen_content": {"lead": "Une concentration qui redescend : la substance est transformée. Une concentration qui reste haute : elle s'accumule."},
     "visual": {"kind": "simulation", "url": ALB, "caption": "Une enzyme transforme une substance en une autre"},
     "speech_text": {"mixed": ("قبل ما نقراو la courbe، نفهمو شنو كدير واحد l'enzyme. شوف هاد l'exemple ديال الدرس، l'albinisme. "
                               "l'enzyme هي protéine، كتحول substance ل substance أخرى: هنا la tyrosine كتولي mélanine. "
                               "ف التمرين ديالنا، نفس الفكرة: la P A H كتحول la phénylalanine ل tyrosine. "
                               "عند la personne saine، la concentration كتطلع من بعد الماكلة، ومن بعد كترجع à dix milligrammes par litre: la phénylalanine كتحول. "
                               "عند la personne malade، كتطلع jusqu'à trois cents milligrammes par litre، وكتبقى ثابتة: la phénylalanine ما كتحولش، كتجمع ف الدم.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "saine : 10 → 40 mg/L à 1 h → 10 mg/L : Phe transformée", "mot": "la phénylalanine كتحول."},
                  {"texte": "malade : 200 → 300 mg/L, puis constante : Phe accumulée", "mot": "كتجمع ف الدم"}],
       "pointage": [{"mot": "شوف هاد l'exemple", "commande": "play_until", "parametres": {"moment": "cellules"}},
                    {"mot": "l'enzyme هي protéine", "repere": "enzyme_saine"},
                    {"mot": "هنا la tyrosine كتولي mélanine", "commande": "play_until", "parametres": {"moment": "reaction"}},
                    {"mot": "هنا la tyrosine كتولي mélanine", "repere": "melanine"},
                    {"mot": "la phénylalanine كتحول.", "cible": "centre:0"},
                    {"mot": "كتجمع ف الدم", "cible": "centre:1"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : protéine fonctionnelle ou non, caractère normal ou modifié",
     "screen_content": {"lead": "Deux lignes : PAH fonctionnelle → Phe transformée → sain ; PAH non fonctionnelle → Phe accumulée → PCU."},
     "visual": {"kind": "simulation", "url": ALB, "caption": "Le tableau saine / malade : enzyme, substance, phénotype"},
     "speech_text": {"mixed": ("la relation protéine caractère كتكتب ف جوج ديال السطور، بحال هاد le tableau. "
                               "السطر اللول، l'enzyme: fonctionnelle عند la personne saine، non fonctionnelle عند la personne malade. "
                               "السطر الثاني، la substance: عند la personne saine، la phénylalanine كتحول ل tyrosine. عند la personne malade، كتجمع ف الدم. "
                               "السطر الثالث، le phénotype: système nerveux normal، ولا la phénylcétonurie. "
                               "إذن le caractère كيتبع la protéine: D'où la relation protéine caractère.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "PAH fonctionnelle → Phe → tyrosine → phénotype sain", "mot": "fonctionnelle عند la personne saine"},
                  {"texte": "PAH non fonctionnelle → Phe accumulée → PCU", "mot": "non fonctionnelle عند la personne malade"}],
       "pointage": [{"mot": "بحال هاد le tableau", "commande": "play_until", "parametres": {"moment": "reaction"}},
                    {"mot": "السطر اللول، l'enzyme:", "commande": "play_until", "parametres": {"moment": "ligne_enzyme"}},
                    {"mot": "fonctionnelle عند la personne saine", "cible": "centre:0"},
                    {"mot": "non fonctionnelle عند la personne malade", "repere": "enzyme_albinos"},
                    {"mot": "non fonctionnelle عند la personne malade", "cible": "centre:1"},
                    {"mot": "السطر الثاني، la substance:", "commande": "play_until", "parametres": {"moment": "ligne_pigment"}},
                    {"mot": "السطر الثالث، le phénotype:", "commande": "play_until", "parametres": {"moment": "ligne_phenotype"}},
                    {"mot": "D'où la relation", "commande": "play_until", "parametres": {"moment": "tableau"}},
                    {"mot": "D'où la relation", "repere": "tableau"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : du brin non transcrit à l'ARNm, puis aux acides aminés",
     "screen_content": {"lead": "Brin non transcrit : mêmes lettres, T → U. Puis un codon sous chaque triplet, et le tableau du code."},
     "visual": {"kind": "simulation", "url": BRINS, "caption": "Brin non transcrit, brin transcrit, ARNm"},
     "speech_text": {"mixed": ("شوف هاد تلاتة ديال السطور: لفوق le brin non transcrit، من بعد le brin transcrit، من بعد l'A R N messager. "
                               "l'A R N messager هو le complémentaire ديال le brin transcrit. "
                               "ولكن ملي كنحطوه تحت le brin non transcrit، كنلقاو نفس الحروف، غير كل T كتولي U. "
                               f"ف التمرين، le document كيعطي le brin non transcrit. إذن G C T كتولي {L(arn(N1[0]))}، و T T C كتولي U U C. "
                               "من بعد، كل codon كنقلبو عليه ف le code génétique، وكنكتبو l'acide aminé تحتو، وبين les acides aminés tiret.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "brin non transcrit → ARNm : mêmes lettres, T → U", "mot": "غير كل T كتولي U"},
                  {"texte": f"GCT → {arn(N1[0])} (Ala) ; TTC → UUC (Phe)", "mot": "و T T C كتولي U U C"}],
       "pointage": [{"mot": "شوف هاد تلاتة", "commande": "play_until", "parametres": {"moment": "trois_lignes"}},
                    {"mot": "لفوق le brin non transcrit", "repere": "ligne_non_transcrit"},
                    {"mot": "من بعد le brin transcrit", "repere": "ligne_transcrit"},
                    {"mot": "من بعد l'A R N messager", "repere": "ligne_arnm"},
                    {"mot": "هو le complémentaire", "commande": "play_until", "parametres": {"moment": "chemin_transcrit"}},
                    {"mot": "هو le complémentaire", "repere": "chemin_1"},
                    {"mot": "تحت le brin non transcrit", "commande": "play_until", "parametres": {"moment": "comparaison_non_transcrit"}},
                    {"mot": "تحت le brin non transcrit", "repere": "chemin_2"},
                    {"mot": "غير كل T كتولي U", "commande": "play_until", "parametres": {"moment": "t_devient_u"}},
                    {"mot": "غير كل T كتولي U", "repere": "t_entoures"},
                    {"mot": "غير كل T كتولي U", "cible": "centre:0"},
                    {"mot": "و T T C كتولي U U C", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : une lettre change, un acide aminé change : faux-sens",
     "screen_content": {"lead": "Comparer triplet par triplet ; une seule lettre remplacée : substitution ; un autre acide aminé : faux-sens."},
     "visual": {"kind": "simulation", "url": MUT, "caption": "Allèle normal et allèle muté alignés"},
     "speech_text": {"mixed": ("شوف l'exemple ديال الدرس. لفوق l'allèle normal، لتحت l'allèle muté. كنقارنو triplet ب triplet. "
                               "هنا G A G ولات G T G: حرف واحد تبدل. le codon G U G كيعطي la valine، ف البلاصة ديال l'acide glutamique. "
                               "هادي mutation faux-sens: substitution، و acide aminé تبدل ب واحد آخر. "
                               "ف التمرين ديالنا، نفس الشي: ف le triplet quarante-neuf، C G A ولات C A A، و l'arginine تبدلات ب la glutamine.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "une seule lettre remplacée : substitution", "mot": "حرف واحد تبدل"},
                  {"texte": "triplet 49 : CGA (Arg) → CAA (Gln) : faux-sens", "mot": "ف le triplet quarante-neuf"}],
       "pointage": [{"mot": "شوف l'exemple", "commande": "set_time", "parametres": {"time_s": 9.4}},
                    {"mot": "لفوق l'allèle normal", "repere": "allele_normal"},
                    {"mot": "لتحت l'allèle muté", "repere": "allele_mute"},
                    {"mot": "هنا G A G ولات G T G", "commande": "play_until", "parametres": {"moment": "faux_sens_evt"}},
                    {"mot": "حرف واحد تبدل", "repere": "codon_mute"},
                    {"mot": "حرف واحد تبدل", "cible": "centre:0"},
                    {"mot": "كيعطي la valine", "repere": "acide_amine_change"},
                    {"mot": "هادي mutation faux-sens", "commande": "play_until", "parametres": {"moment": "faux_sens"}},
                    {"mot": "هادي mutation faux-sens", "repere": "type_mutation"},
                    {"mot": "ف le triplet quarante-neuf", "cible": "centre:1"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : du gène au caractère, maillon par maillon",
     "screen_content": {"lead": "Allèle muté → codon → acide aminé → protéine non fonctionnelle → cellule → maladie."},
     "visual": {"kind": "simulation", "url": ECH, "caption": "Du gène au caractère : les échelles"},
     "speech_text": {"mixed": ("l'origine génétique كتمشي من لتحت ل الفوق، بحال هاد l'exemple ديال الدرس. "
                               "ف المستوى ديال le gène: la mutation، substitution ديال G ب A، ف le triplet quarante-neuf. "
                               "ف المستوى ديال la protéine: l'arginine تبدلات ب la glutamine، و la P A H ولات non fonctionnelle. "
                               "ف المستوى ديال la cellule: les cellules ديال le foie ما بقاوش كيحولو la phénylalanine. "
                               "ف المستوى ديال l'organisme: la phénylalanine كتجمع ف الدم، و le système nerveux كيتضرر. "
                               "allèle muté، protéine non fonctionnelle، caractère muté.")},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "substitution G → A (triplet 49) → CGA → CAA → Arg → Gln", "mot": "substitution ديال G ب A"},
                  {"texte": "→ PAH non fonctionnelle → Phe accumulée → PCU", "mot": "و la P A H ولات non fonctionnelle"}],
       "pointage": [{"mot": "ف المستوى ديال le gène", "commande": "play_until", "parametres": {"moment": "niveau_gene"}},
                    {"mot": "ف المستوى ديال le gène", "repere": "echelle_gene"},
                    {"mot": "substitution ديال G ب A", "cible": "centre:0"},
                    {"mot": "ف المستوى ديال la protéine", "commande": "play_until", "parametres": {"moment": "niveau_proteine"}},
                    {"mot": "ف المستوى ديال la protéine", "repere": "echelle_proteine"},
                    {"mot": "و la P A H ولات non fonctionnelle", "cible": "centre:1"},
                    {"mot": "ف المستوى ديال la cellule", "commande": "play_until", "parametres": {"moment": "niveau_cellule"}},
                    {"mot": "ف المستوى ديال la cellule", "repere": "echelle_cellule"},
                    {"mot": "ف المستوى ديال l'organisme", "commande": "play_until", "parametres": {"moment": "niveau_organisme"}},
                    {"mot": "ف المستوى ديال l'organisme", "repere": "echelle_organisme"},
                    {"mot": "allèle muté، protéine", "commande": "play_until", "parametres": {"moment": "maillon_mute"}},
                    {"mot": "allèle muté، protéine", "repere": "maillon_mute"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : lire la courbe de la personne malade", "نتمرنو بسؤال ساهل على la courbe ديال la personne malade.",
      "Chez la personne malade, après 2 h, [Phe]…", ["reste constante à 300 mg/L", "revient à 10 mg/L", "diminue jusqu'à 200 mg/L"], 0, {
        "0": {"juste": rep("مزيان! après deux heures، la concentration كتبقى ثابتة، à trois cents milligrammes par litre: la phénylalanine ما كتحولش.", "Juste : [Phe] reste constante à 300 mg/L ; elle n'est pas transformée.")},
        "1": {"1": rep("ما تقلقش. dix milligrammes par litre هي ديال la personne saine. شوف la courbe ديال la personne malade. عاود اختار.", "10 mg/L, c'est la personne saine. Regarde la courbe de la personne malade. Réessaie."),
              "2": rep("الجواب هو كتبقى ثابتة، à trois cents milligrammes par litre. اللي كترجع à dix milligrammes، هي la personne saine.", "Réponse : [Phe] reste constante à 300 mg/L.")},
        "2": {"1": rep("قريب! deux cents هي la valeur ف البداية. après deux heures، واش la courbe كتهبط؟ عاود اختار.", "200 mg/L, c'est la valeur de départ. Après 2 h, la courbe descend-elle ? Réessaie."),
              "2": rep("الجواب هو كتبقى ثابتة، à trois cents milligrammes par litre. la courbe ما كتهبطش.", "Réponse : elle reste constante à 300 mg/L.")}},
      "Chez la personne malade, après deux heures, la concentration de la phénylalanine ?"),
    vrai_faux("fa_s2", "Plus facile : protéine et caractère", "Vrai ou faux ?",
      "سؤال ساهل: قول واش هاد les phrases صحاح ولا غالطين.", [
        ("Chez la personne saine, la PAH transforme la phénylalanine en tyrosine.", True, "Vrai : c'est le rôle de la PAH (document 2)."),
        ("Chez la personne malade, la PAH est absente.", False, "Faux : elle est fabriquée, mais non fonctionnelle (document 2)."),
        ("La phénylalanine s'accumule dans le sang de la personne malade parce que la PAH ne la transforme pas.", True, "Vrai : PAH non fonctionnelle → [Phe] reste à 300 mg/L."),
        ("Le caractère (sain ou malade) dépend de l'état de la protéine PAH.", True, "Vrai : c'est la relation protéine – caractère.")]),
    qcm_facile("fa_s3", "Plus facile : le premier codon", "سؤال ساهل: le codon اللول.",
      f"Brin non transcrit : {N1[0]}. Le codon de l'ARNm est…", [arn(N1[0]), "CGA", N1[0]], 0, {
        "0": {"juste": rep("مزيان! le brin non transcrit: نفس الحروف، و T كتولي U. G C T كتولي G C U، و هو l'alanine.", f"Juste : {N1[0]} → {arn(N1[0])} (Ala).")},
        "1": {"1": rep("ما تقلقش. درتي la complémentarité، ولكن le brin non transcrit ما كنديروش ليه la complémentarité. عاود اختار.", "Tu as fait la complémentarité : pas pour le brin non transcrit. Réessaie."),
              "2": rep("الجواب هو G C U. le brin non transcrit: نفس الحروف، غير T كتولي U.", f"Réponse : {arn(N1[0])} (mêmes lettres, T → U).")},
        "2": {"1": rep("قريب! الحروف صحاح، ولكن l'A R N ما فيهش T. شنو كتولي T؟ عاود اختار.", "Les lettres sont bonnes, mais l'ARN n'a pas de T. Que devient T ? Réessaie."),
              "2": rep("الجواب هو G C U. نسيتي تبدل T ب U.", f"Réponse : {arn(N1[0])} (T devient U).")}},
      "Le brin non transcrit est G C T. Quel est le codon de l'ARNm ?"),
    qcm_facile("fa_s4", "Plus facile : nommer la mutation", "سؤال ساهل: سمي la mutation.",
      "CGA (Arg) devient CAA (Gln). C'est une mutation…", ["par substitution faux-sens", "par substitution silencieuse", "par délétion"], 0, {
        "0": {"juste": rep("برافو! حرف واحد تبدل، و l'acide aminé تبدل: substitution faux-sens.", "Juste : une lettre remplacée, un autre acide aminé : substitution faux-sens.")},
        "1": {"1": rep("ما تقلقش. silencieuse كتعني نفس l'acide aminé. واش l'arginine هي la glutamine؟ عاود اختار.", "Silencieuse = même acide aminé. Arg et Gln sont-ils pareils ? Réessaie."),
              "2": rep("الجواب هو substitution faux-sens: l'arginine تبدلات ب la glutamine، acide aminé آخر.", "Réponse : substitution faux-sens (Arg → Gln).")},
        "2": {"1": rep("قريب! ف la délétion، كيضيع nucléotide. هنا شحال ديال الحروف ف le triplet؟ عاود اختار.", "Délétion = un nucléotide perdu. Ici, le triplet a-t-il toujours trois lettres ? Réessaie."),
              "2": rep("الجواب هو substitution faux-sens: حرف تبدل ب حرف، ما ضاع والو.", "Réponse : substitution faux-sens (aucune lettre perdue).")}},
      "C G A, l'arginine, devient C A A, la glutamine. Quel type de mutation ?"),
    association("fa_s5", "Plus facile : remettre la chaîne dans l'ordre", "Relie chaque maillon à sa place dans la chaîne.",
      "سؤال ساهل: ربط كل حلقة مع البلاصة ديالها ف la chaîne.", "Relie chaque maillon (1 à 4) à ce qui se passe.",
      [("1", "1er maillon : le gène"), ("2", "2e maillon : l'ARNm"), ("3", "3e maillon : la protéine"), ("4", "4e maillon : le caractère")],
      [("a", "substitution G → A au triplet 49"), ("b", "codon CGA devenu CAA"), ("c", "PAH non fonctionnelle (Gln au lieu d'Arg)"), ("d", "Phe accumulée : phénylcétonurie")],
      {"1": "a", "2": "b", "3": "c", "4": "d"},
      {"1-a": (True, "Oui : la mutation est dans le gène (l'ADN).", "برافو: la mutation كاينة ف le gène."),
       "1-b": (False, "Le codon appartient à l'ARNm, pas au gène.", "لا، le codon كاين ف l'A R N messager، ماشي ف le gène."),
       "1-c": (False, "La PAH est la protéine, pas le gène.", "لا، la P A H هي la protéine."),
       "1-d": (False, "La maladie est le caractère, le dernier maillon.", "لا، la maladie هي le caractère، الحلقة اللخرة."),
       "2-a": (False, "La substitution touche l'ADN du gène ; l'ARNm en est la copie.", "لا، la substitution ف l'A D N. l'A R N messager غير نسخة."),
       "2-b": (True, "Oui : l'ARNm porte le codon modifié.", "برافو: l'A R N messager فيه le codon اللي تبدل."),
       "2-c": (False, "La PAH est la protéine, fabriquée après la lecture de l'ARNm.", "لا، la P A H هي la protéine، كتجي من بعد."),
       "2-d": (False, "L'accumulation de Phe, c'est le caractère.", "لا، هادا هو le caractère."),
       "3-a": (False, "La substitution est dans le gène.", "لا، la substitution ف le gène."),
       "3-b": (False, "Le codon est sur l'ARNm.", "لا، le codon ف l'A R N messager."),
       "3-c": (True, "Oui : la protéine PAH a la glutamine à la place de l'arginine : non fonctionnelle.", "برافو: la P A H فيها la glutamine ف بلاصة l'arginine، non fonctionnelle."),
       "3-d": (False, "C'est la conséquence sur l'organisme : le caractère.", "لا، هادي النتيجة على l'organisme، le caractère."),
       "4-a": (False, "La substitution est la cause, au début de la chaîne.", "لا، la substitution هي السبب، ف البداية."),
       "4-b": (False, "Le codon est un maillon du milieu.", "لا، le codon ف الوسط ديال la chaîne."),
       "4-c": (False, "La PAH est la protéine ; le caractère vient après.", "لا، la P A H هي la protéine، le caractère كيجي من بعد."),
       "4-d": (True, "Oui : l'accumulation de phénylalanine et les troubles nerveux, c'est le caractère.", "برافو: la phénylalanine كتجمع، هادا هو le caractère.")},
      ("(1 ; a) (2 ; b) (3 ; c) (4 ; d) : gène → ARNm → protéine → caractère.", "le gène، من بعد l'A R N messager، من بعد la protéine، ولخر حاجة le caractère."))
  ]}]},
  "similaire": {
    "id": "svt_ex_ch4_substitution_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Même étude chez une autre famille atteinte de phénylcétonurie. Document 1 : [Phe] dans le sang d'une personne saine et d'une personne malade après un repas riche en phénylalanine pris à t = 0. "
                "Document 2 : la PAH du foie transforme la phénylalanine en tyrosine ; chez la personne malade, elle est fabriquée mais non fonctionnelle. "
                f"Document 3 : extrait du brin non transcrit du gène de la PAH ({triplets_ecrits(D2, 7)}), séquences simplifiées."),
      "intro_dit": ("نفس الدراسة، عند عائلة أخرى. la courbe ديال la phénylalanine ف الدم، la P A H كتحول la phénylalanine ل tyrosine، و le brin non transcrit ديال le gène."),
      "figures": [courbe_phe(SAINE2, MALADE2, 400, "Document 1 : [Phe] dans le sang après le repas"),
                  fig_sequences("Document 3 : brin non transcrit (5′ → 3′)", D2,
                                [("Allèle normal", N2, "blanc"), ("Allèle muté", M2, "blanc")], "Gène de la PAH : allèle normal et allèle muté.")],
      "donnees": [f"Allèle normal (brin non transcrit, 5′ → 3′) : {' '.join(N2)}", f"Allèle muté (brin non transcrit, 5′ → 3′) : {' '.join(M2)}",
                  f"Les triplets sont numérotés de {D2} à {D2 + 6}.", CODE2],
      "questions": [
        {"id": "1", "texte": "Décrire l'évolution de [Phe] chez la personne saine puis chez la personne malade, puis déduire ce que devient la phénylalanine chez chacune.",
         "reponse": {"type": "phrase", "attendu": ("Personne saine : 15 mg/L avant le repas, augmente jusqu'à 50 mg/L à 1 h, puis revient à 15 mg/L vers 6 h. "
                                                   "Personne malade : 240 mg/L avant le repas, augmente jusqu'à 340 mg/L à 2 h, puis reste constante à 340 mg/L. "
                                                   "On en déduit que la personne saine transforme la phénylalanine, alors que chez la personne malade elle s'accumule dans le sang.")},
         "clavier": {"aides": ["augmente", "diminue", "reste constante", "On en déduit que"], "pieges": ["élimine"]},
         "correction": {"lignes": [{"texte": "1 : saine : 15 → 50 mg/L à 1 h → 15 mg/L vers 6 h", "mot": "la personne saine"},
                                   {"texte": "malade : 240 → 340 mg/L à 2 h, puis constante", "mot": "la personne malade"},
                                   {"texte": "On en déduit que : Phe transformée chez la saine, accumulée chez la malade", "mot": "On en déduit que"}],
                        "parole": ("la question un. la personne saine: quinze milligrammes par litre، كتزاد jusqu'à cinquante، à une heure، ومن بعد كترجع à quinze. "
                                   "la personne malade: deux cent quarante، كتزاد jusqu'à trois cent quarante، à deux heures، وكتبقى ثابتة. On en déduit que la phénylalanine كتجمع عند la personne malade.")}},
        {"id": "2", "texte": "Montrer la relation protéine – caractère.",
         "reponse": {"type": "phrase", "attendu": ("Saine : PAH fonctionnelle → phénylalanine transformée en tyrosine → [Phe] faible → phénotype sain. "
                                                   "Malade : PAH non fonctionnelle → phénylalanine non transformée → accumulée (340 mg/L) → troubles nerveux. D'où la relation protéine – caractère.")},
         "clavier": {"aides": ["PAH fonctionnelle", "PAH non fonctionnelle", "→"], "pieges": ["PAH absente"]},
         "correction": {"lignes": [{"texte": "2 : saine : PAH fonctionnelle → Phe → tyrosine → sain", "mot": "la P A H fonctionnelle"},
                                   {"texte": "malade : PAH non fonctionnelle → Phe accumulée → troubles nerveux", "mot": "la P A H non fonctionnelle"}],
                        "parole": "la question deux. عند la personne saine، la P A H fonctionnelle، la phénylalanine كتحول. عند la personne malade، la P A H non fonctionnelle، la phénylalanine كتجمع. D'où la relation protéine caractère."}},
        {"id": "3", "texte": "Donner la séquence de l'ARNm et la séquence des acides aminés correspondant à chaque allèle.",
         "reponse": {"type": "phrase", "attendu": f"Allèle normal : ARNm : {ARN_N2} ; acides aminés : {SEQ_N2}. Allèle muté : ARNm : {ARN_M2} ; acides aminés : {SEQ_M2}."},
         "clavier": {"aides": ["ARNm :", "U", "–"], "pieges": ["T"]},
         "correction": {"lignes": [{"texte": f"3 : normal : {ARN_N2} → {SEQ_N2}", "mot": "l'allèle normal"},
                                   {"texte": f"muté : {ARN_M2} → {SEQ_M2}", "mot": "l'allèle muté"}],
                        "parole": (f"la question trois. l'allèle normal: {'، '.join(L(arn(c)) for c in N2)}، و les acides aminés: {'، '.join(NOM[a] for a in AN2)}. "
                                   f"l'allèle muté: غير le triplet cent quinze، {L(arn(M2[J2]))}، اللي كيعطي la proline.")}},
        {"id": "4", "texte": "Comparer les deux allèles puis déduire le type de la mutation.",
         "reponse": {"type": "phrase", "attendu": "Seul le triplet 115 diffère : CTG devient CCG (le T est remplacé par C). Le codon CUG (Leu) devient CCG (Pro) : un acide aminé remplacé : mutation par substitution faux-sens."},
         "clavier": {"aides": ["triplet 115", "substitution", "faux-sens"], "pieges": ["silencieuse", "délétion"]},
         "correction": {"lignes": [{"texte": "4 : triplet 115 : CTG → CCG (T remplacé par C)", "mot": "le triplet cent quinze"},
                                   {"texte": "Leu → Pro : substitution faux-sens", "mot": "substitution faux-sens"}],
                        "parole": "la question quatre. غير le triplet cent quinze: C T G ولات C C G. la leucine تبدلات ب la proline. إذن mutation par substitution faux-sens."}},
        {"id": "5", "texte": "Expliquer l'origine génétique de la phénylcétonurie.",
         "reponse": {"type": "phrase", "attendu": ("Substitution du nucléotide T par C au triplet 115 du brin non transcrit du gène de la PAH → codon CUG devient CCG → la leucine est remplacée par la proline "
                                                   "→ PAH non fonctionnelle → phénylalanine non transformée, accumulée dans le sang → troubles nerveux : phénylcétonurie.")},
         "clavier": {"aides": ["substitution", "triplet 115", "→", "PAH non fonctionnelle"], "pieges": ["mutation → maladie"]},
         "correction": {"lignes": [{"texte": "5 : substitution T → C, triplet 115, brin non transcrit, gène de la PAH", "mot": "substitution du nucléotide T par C"},
                                   {"texte": "→ CUG → CCG → Leu remplacée par Pro → PAH non fonctionnelle → Phe accumulée → PCU", "mot": "la P A H non fonctionnelle"}],
                        "parole": ("la question cinq. mutation par substitution du nucléotide T par C، au triplet cent quinze، du brin non transcrit، du gène de la P A H. "
                                   "la leucine تبدلات ب la proline، la P A H non fonctionnelle، la phénylalanine كتجمع ف الدم: la phénylcétonurie.")}}
      ]}}
}
ecrire(EX, sys.argv[1])
