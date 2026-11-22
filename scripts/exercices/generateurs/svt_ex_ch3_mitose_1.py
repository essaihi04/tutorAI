# Exercice SVT ch. 3 (notion de l'information génétique), niveau facile : quatre croquis de cellules animales en mitose
# (2n = 4), à identifier en justifiant, à ranger dans l'ordre, puis compter chromosomes et chromatides.
# Entraîne : « nom de la phase + car + critère visible » (Ikram, Driss), l'ordre P, M, A, T, le comptage des chromatides
# en métaphase (une chromatide = une molécule d'ADN ; chromosome à deux chromatides), l'anaphase (une chromatide de chaque
# chromosome vers chaque pôle, même nombre aux deux pôles), deux cellules filles 2n = 4 génétiquement identiques.
# Sources comparées (lues, rien copié) :
# - exploration notion_information_genetique.json : cas_types « identifier_phase », « caracteriser_phase »,
#   « schematiser » ; pieges (« chromatide » pour un chromosome à une chromatide, « même pôle », fuseau disparu en
#   anaphase) ; erreurs_examen « schéma d'une phase » (même nombre de chromatides aux deux pôles) et « anaphase 2018 R » ;
#   insistances (quatre phases P, M, A, T avec leurs phrases ; chromatides vers les pôles OPPOSÉS).
# - nationaux PC : 2018 R restitution (deux caractéristiques des chromosomes à l'anaphase de la mitose : une chromatide
#   par chromosome après clivage du centromère, migration vers les pôles opposés) ; QCM 2018 R métaphase (deux
#   chromatides de deux brins) ; 2024 N association (centromère) — formes de question seulement.
# - séries en ligne (recherche du 22/11/2026 : dreamjob.ma « mitose, cours et exercices corrigés », dyrassa séries
#   « Notion de l'information génétique », moutamadris activités 2 Bac SP, alloschool) : titres et résumés seulement, le
#   réseau du conteneur refuse ces sites ; la situation « figures a, b, c, d à identifier et ordonner, 2n = 4 » y est
#   classique. Les croquis sont dessinés ici en code.
import math, sys
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

MITOSE = "/media/simulations/svt/notion_information_genetique-tableau/mitose.html"

# ── Dessin des croquis (cadre 10 × 10 : quatre cases de 5 × 5) ────────────────────────────────────────────────────
def _r(v): return round(v, 3)


def bichromatidien(cx, cy, L, ang, coul):
    """Chromosome à deux chromatides : deux bâtonnets parallèles reliés par le centromère."""
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang)); nx, ny = -uy, ux; e = 0.07
    el = []
    for s in (-1, 1):
        x0, y0 = cx + s * e * nx, cy + s * e * ny
        el.append({"f": "ligne", "pts": [[_r(x0 - ux * L / 2), _r(y0 - uy * L / 2)], [_r(x0 + ux * L / 2), _r(y0 + uy * L / 2)]], "couleur": coul, "epais": True})
    el.append({"f": "cercle", "c": [_r(cx), _r(cy)], "r": 0.07, "remplir": "jaune", "couleur": "jaune"})
    return el


def aster(x, y):
    el = [{"f": "cercle", "c": [_r(x), _r(y)], "r": 0.1, "remplir": "jaune", "couleur": "jaune"}]
    for a in range(0, 360, 45):
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        el.append({"f": "ligne", "pts": [[_r(x + 0.16 * ux), _r(y + 0.16 * uy)], [_r(x + 0.36 * ux), _r(y + 0.36 * uy)]], "couleur": "jaune"})
    return el


def prophase(cx, cy, chrom):
    el = [{"f": "cercle", "c": [cx, cy], "r": 1.9}, {"f": "cercle", "c": [cx, cy], "r": 1.15, "trait": "pointille", "couleur": "faible"}]
    places = [(-0.45, 0.35, 30), (0.4, 0.45, -50), (-0.3, -0.45, 100), (0.45, -0.3, 15), (0.0, 0.0, 70), (-0.65, -0.05, -20)]
    for (L, coul), (dx, dy, a) in zip(chrom, places):
        el += bichromatidien(cx + dx, cy + dy, L, a, coul)
    return el + aster(cx - 1.5, cy) + aster(cx + 1.5, cy)


def metaphase(cx, cy, chrom):
    ax, bx = cx - 1.65, cx + 1.65
    el = [{"f": "ellipse", "c": [cx, cy], "rx": 2.05, "ry": 1.75}]
    n = len(chrom); ys = [cy + 1.3 - 2.6 * (i + 0.5) / n for i in range(n)]
    for y in ys:
        el.append({"f": "ligne", "pts": [[ax, cy], [cx, _r(y)], [bx, cy]], "couleur": "faible"})
    for (L, coul), y in zip(chrom, ys):
        el += bichromatidien(cx, y, L * 0.48, 90, coul)
    return el + aster(ax, cy) + aster(bx, cy)


def anaphase(cx, cy, chrom):
    ax, bx = cx - 1.75, cx + 1.75
    el = [{"f": "ellipse", "c": [cx, cy], "rx": 2.15, "ry": 1.6}]
    n = len(chrom); ys = [cy + 1.1 - 2.2 * (i + 0.5) / n for i in range(n)]; h = 0.13 if n <= 4 else 0.1
    for s, xp in ((-1, cx - 0.95), (1, cx + 0.95)):
        for (L, coul), y in zip(chrom, ys):
            a = L * 0.75
            el.append({"f": "ligne", "pts": [[_r(xp - s * a), _r(y + h)], [_r(xp), _r(y)], [_r(xp - s * a), _r(y - h)]], "couleur": coul, "epais": True})
            el.append({"f": "ligne", "pts": [[ax if s < 0 else bx, cy], [_r(xp), _r(y)]], "couleur": "faible"})
    return el + aster(ax, cy) + aster(bx, cy)


def telophase(cx, cy, chrom):
    contour = [(-2.1, 0), (-1.75, 1.15), (-0.9, 1.45), (0, 0.55), (0.9, 1.45), (1.75, 1.15), (2.1, 0),
               (1.75, -1.15), (0.9, -1.45), (0, -0.55), (-0.9, -1.45), (-1.75, -1.15)]   # cellule étranglée au milieu
    el = [{"f": "ligne", "pts": [[_r(cx + a), _r(cy + b)] for a, b in contour], "ferme": True, "lisse": True, "couleur": "blanc"}]
    for x in (cx - 1.0, cx + 1.0):
        el.append({"f": "cercle", "c": [x, cy], "r": 0.6, "couleur": "faible"})
        for i, (L, coul) in enumerate(chrom):
            y = cy + 0.35 - 0.7 * (i + 0.5) / len(chrom)
            el.append({"f": "ligne", "pts": [[_r(x - 0.3), _r(y)], [_r(x - 0.1), _r(y + 0.06)], [_r(x + 0.1), _r(y - 0.06)], [_r(x + 0.3), _r(y)]], "lisse": True, "couleur": coul})
    return el


DESSIN = {"prophase": prophase, "métaphase": metaphase, "anaphase": anaphase, "télophase": telophase}
CASES = {1: (2.5, 7.3), 2: (7.5, 7.3), 3: (2.5, 2.3), 4: (7.5, 2.3)}


def planche(ordre, chrom, n2):
    """ordre : {numéro de figure: phase}. chrom : [(longueur, couleur)] des 2n chromosomes."""
    el = []
    for num, ph in ordre.items():
        cx, cy = CASES[num]
        el += DESSIN[ph](cx, cy, chrom)
        el.append({"f": "texte", "at": [cx - 2.3, cy + 2.35], "t": f"Figure {num}", "couleur": "jaune", "ancre": "gauche"})
    return {"type": "croquis", "titre": f"Cellules animales en division (2n = {n2})", "cadre": {"l": 10, "h": 10},
            "legende": "Croquis d'observations au microscope : jaune = centromères et asters ; traits fins = fibres du fuseau ; cercle pointillé = enveloppe nucléaire.",
            "elements": el}


CHROM4 = [(0.9, "cyan"), (0.9, "rose"), (0.55, "cyan"), (0.55, "rose")]
CHROM6 = [(0.9, "cyan"), (0.9, "rose"), (0.7, "cyan"), (0.7, "rose"), (0.5, "cyan"), (0.5, "rose")]
ORDRE = {1: "anaphase", 2: "prophase", 3: "télophase", 4: "métaphase"}      # chronologie : 2, 4, 1, 3
ORDRE_B = {1: "métaphase", 2: "télophase", 3: "prophase", 4: "anaphase"}    # chronologie : 3, 1, 4, 2
assert [k for p in ("prophase", "métaphase", "anaphase", "télophase") for k, v in ORDRE.items() if v == p] == [2, 4, 1, 3]
assert [k for p in ("prophase", "métaphase", "anaphase", "télophase") for k, v in ORDRE_B.items() if v == p] == [3, 1, 4, 2]
assert 4 * 2 == 8 and 6 * 2 == 12


def assoc_criteres(sid):
    gauche = [("1", "Chromosomes alignés par leur centromère au milieu de la cellule"),
              ("2", "Chromatides qui migrent vers les deux pôles"),
              ("3", "Cellule étranglée au milieu, deux noyaux"),
              ("4", "Chromosomes qui se condensent, enveloppe nucléaire qui disparaît")]
    droite = [("a", "Prophase"), ("b", "Métaphase"), ("c", "Anaphase"), ("d", "Télophase")]
    couples = {"1": "b", "2": "c", "3": "d", "4": "a"}
    g_dit = {"1": "les chromosomes متصفين فالوسط ديال la cellule", "2": "les chromatides كيمشيو نحو les pôles",
             "3": "la cellule كتضيق فالوسط، وكاينين les deux noyaux", "4": "les chromosomes كيتجمعو، وl'enveloppe nucléaire كتختفي"}
    d_txt = {"a": "la prophase : condensation, disparition de l'enveloppe nucléaire, formation du fuseau",
             "b": "la métaphase : chromosomes alignés sur la plaque équatoriale",
             "c": "l'anaphase : clivage du centromère, chromatides vers les pôles opposés",
             "d": "la télophase : étranglement et reformation de deux noyaux"}
    d_dit = {"a": "la prophase هي فين les chromosomes كيتجمعو، وl'enveloppe كتختفي",
             "b": "la métaphase هي فين les chromosomes كيتصفو على la plaque équatoriale",
             "c": "l'anaphase هي فين les chromatides كيمشيو نحو les pôles opposés",
             "d": "la télophase هي فين la cellule كتضيق، وكيرجعو les noyaux"}
    retours = {}
    for g, gt in gauche:
        for d, dn in droite:
            if couples[g] == d:
                retours[f"{g}-{d}"] = (True, f"Oui : {gt.lower()} : c'est {d_txt[d].split(' :')[0]}.", f"برافو. {g_dit[g]}: هادي {d_dit[d].split(' هي')[0]}.")
            else:
                retours[f"{g}-{d}"] = (False, f"Non : {d_txt[d]}. Ce critère correspond à une autre phase.",
                                       f"لا. {d_dit[d]}. وهنا {g_dit[g]}. قلب على phase أخرى.")
    return association(sid, "Plus facile : critère → phase", "Relie chaque critère à sa phase.",
                       "سؤال ساهل: ربط كل دليل مع la phase ديالو.", "Relie chaque critère observé à la phase de la mitose.",
                       gauche, droite, couples, retours,
                       ("(1 ; métaphase) (2 ; anaphase) (3 ; télophase) (4 ; prophase).",
                        "متصفين فالوسط: la métaphase. كيمشيو نحو les pôles: l'anaphase. كتضيق وكاينين les deux noyaux: la télophase. كيتجمعو: la prophase."))


EX = {
  "id": "svt_ex_ch3_mitose_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "Reconnaître et ordonner les phases de la mitose", "niveau": "facile", "duree_min": 20,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Identifier une phase de la mitose en justifiant", "Ordonner les phases de la mitose",
                  "Compter chromosomes et chromatides (2n = 4)", "Dire le rôle de la mitose"],
  "enonce": {
    "intro": "On observe au microscope des cellules animales en division, dont la formule chromosomique est 2n = 4. Les figures 1 à 4 sont les croquis de quatre de ces cellules, chacune à une phase différente de la mitose.",
    "intro_dit": "دابا نقراو l'énoncé. شفنا فle microscope des cellules animales اللي كيتقسمو. la formule chromosomique ديالهم: deux n égale quatre. les figures، de un à quatre، هوما les croquis de quatre cellules، وكل وحدة فphase مختلفة ديال la mitose.",
    "figures": [planche(ORDRE, CHROM4, 4)],
    "donnees": ["Cellule animale, 2n = 4 (deux paires de chromosomes : une longue, une courte)",
                "Jaune : centromères et asters ; traits fins : fibres du fuseau"],
    "questions": [
      {"id": "1", "texte": "Identifier la phase de la mitose représentée par chacune des figures 1 à 4, en justifiant par un critère visible.",
       "texte_dit": "السؤال un: عرف la phase ديال la mitose فكل figure، وبرر بدليل اللي كيبان فالرسم.",
       "reponse": {"type": "phrase", "attendu": "Figure 1 : anaphase, car les chromatides sœurs se sont séparées et migrent vers les pôles opposés (4 chromatides de chaque côté). Figure 2 : prophase, car les chromosomes condensés à deux chromatides apparaissent et l'enveloppe nucléaire disparaît ; les asters se placent aux pôles. Figure 3 : télophase, car la cellule s'étrangle au milieu et deux noyaux se reforment. Figure 4 : métaphase, car les chromosomes à deux chromatides sont alignés par leur centromère sur la plaque équatoriale."},
       "clavier": {"aides": ["car", "prophase", "métaphase", "anaphase", "télophase", "plaque équatoriale", "pôles opposés", "étranglement"], "pieges": ["interphase", "chromosomes homologues"]},
       "aides": [
         {"texte": "Pour chaque figure, regarde où sont les chromosomes : dans un noyau qui disparaît, alignés au milieu, en deux lots vers les pôles, ou dans deux noyaux.",
          "dit": "فكل figure، شوف فين كاينين les chromosomes: وسط noyau اللي كيختفي، ولا متصفين فالوسط، ولا مقسومين نحو les pôles، ولا فles deux noyaux."},
         {"texte": "Écris : nom de la phase + « car » + le critère vu sur le croquis (plaque équatoriale, migration vers les pôles opposés, étranglement…).",
          "dit": "كتب: اسم la phase، من بعد car، من بعد الدليل اللي شفتي فالرسم: la plaque équatoriale، ولا la migration نحو les pôles opposés، ولا l'étranglement."}],
       "correction": {"lignes": [
           {"texte": "1 : figure 1 : anaphase, car les chromatides migrent vers les pôles opposés", "mot": "figure un: l'anaphase"},
           {"texte": "figure 2 : prophase, car chromosomes condensés et enveloppe nucléaire qui disparaît", "mot": "figure deux: la prophase"},
           {"texte": "figure 3 : télophase, car étranglement et deux noyaux", "mot": "figure trois: la télophase"},
           {"texte": "figure 4 : métaphase, car chromosomes alignés sur la plaque équatoriale", "mot": "figure quatre: la métaphase"}],
         "parole": "السؤال un. figure un: l'anaphase، car les chromatides sœurs كيمشيو نحو les pôles opposés. figure deux: la prophase، car les chromosomes condensés كيبانو، وl'enveloppe nucléaire كتختفي. figure trois: la télophase، car la cellule كتضيق فالوسط، et deux noyaux se forment. figure quatre: la métaphase، car les chromosomes متصفين على la plaque équatoriale."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Classer les figures 1 à 4 dans l'ordre chronologique de la mitose.",
       "texte_dit": "السؤال deux: رتب les figures حسب الترتيب ديال la mitose فالوقت.",
       "reponse": {"type": "phrase", "attendu": "2 (prophase) → 4 (métaphase) → 1 (anaphase) → 3 (télophase)."},
       "clavier": {"aides": ["→", "prophase", "métaphase", "anaphase", "télophase"], "pieges": ["1 → 2 → 3 → 4"]},
       "aides": [
         {"texte": "Utilise tes réponses à la question 1 : quelle figure montre la première phase de la mitose ?",
          "dit": "خدم بالأجوبة ديال السؤال un: شمن figure فيها la première phase ديال la mitose؟"},
         {"texte": "L'ordre des phases est toujours prophase, métaphase, anaphase, télophase (P, M, A, T).",
          "dit": "الترتيب ديما هو: prophase، métaphase، anaphase، télophase. P، M، A، T."}],
       "correction": {"lignes": [
           {"texte": "2 : 2 (prophase) → 4 (métaphase) → 1 (anaphase) → 3 (télophase)", "mot": "figure deux، من بعد figure quatre"}],
         "parole": "السؤال deux. الترتيب هو: figure deux، من بعد figure quatre، من بعد figure un، وفاللخر figure trois. يعني prophase، métaphase، anaphase، télophase."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Calculer le nombre de chromatides contenues dans la cellule de la figure 4.",
       "texte_dit": "السؤال trois: حسب شحال ديال les chromatides كاينين فla cellule ديال la figure quatre.",
       "reponse": {"type": "valeur", "grandeur": "chromatides", "valeur": 8, "unite": "chromatides", "tolerance": 0.02,
                   "attendu": "2n = 4 chromosomes à deux chromatides : 4 × 2 = 8 chromatides"},
       "clavier": {"aides": ["2n = 4", "× 2", "chromatides"], "pieges": ["4 chromatides", "16"]},
       "aides": [
         {"texte": "Compte les chromosomes de la figure 4 : combien y en a-t-il, et combien de chromatides a chacun ?",
          "dit": "حسب les chromosomes ف la figure quatre. شحال كاين؟ وكل chromosome، شحال فيه ديال les chromatides؟"},
         {"texte": "En métaphase, chaque chromosome a deux chromatides : nombre de chromatides = nombre de chromosomes × 2.",
          "dit": "فla métaphase، كل chromosome، deux chromatides. إذن le nombre de chromatides égale le nombre de chromosomes، fois deux."}],
       "correction": {"lignes": [
           {"texte": "3 : figure 4 (métaphase) : 2n = 4 chromosomes à deux chromatides", "mot": "quatre chromosomes à deux chromatides"},
           {"texte": "4 × 2 = 8 chromatides", "mot": "quatre fois deux، égale huit chromatides"}],
         "parole": "السؤال trois. فla figure quatre، la métaphase، il y a quatre chromosomes à deux chromatides. quatre fois deux، égale huit chromatides."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Indiquer le nombre de chromatides qui arrivent à chaque pôle dans la figure 1, puis le nombre et l'état des chromosomes de chaque cellule fille. Conclure sur le rôle de la mitose.",
       "texte_dit": "السؤال quatre: قول شحال ديال les chromatides كيوصلو لكل pôle فla figure un. من بعد، شحال ديال les chromosomes فكل cellule fille، وكيف دايرين. واستنتج le rôle ديال la mitose.",
       "reponse": {"type": "phrase", "attendu": "Dans la figure 1 (anaphase), 4 chromatides arrivent à chaque pôle : une chromatide de chaque chromosome. Chaque cellule fille reçoit donc 4 chromosomes à une chromatide (2n = 4), comme la cellule mère. La mitose donne deux cellules filles génétiquement identiques entre elles et à la cellule mère : c'est une reproduction conforme."},
       "clavier": {"aides": ["4 chromatides", "à chaque pôle", "chromosomes à une chromatide", "2n = 4", "génétiquement identiques"], "pieges": ["8 chromatides à chaque pôle", "n = 2"]},
       "aides": [
         {"texte": "Compte les chromatides d'un seul pôle dans la figure 1. D'où vient chacune ?",
          "dit": "حسب les chromatides ديال واحد le pôle فla figure un. كل chromatide، من أشمن chromosome جات؟"},
         {"texte": "Chaque chromatide arrivée à un pôle devient un chromosome à une chromatide du noyau fils. Compare avec la cellule mère.",
          "dit": "كل chromatide اللي وصلات لpôle، كتولي chromosome à une chromatide فle noyau الجديد. قارن مع la cellule mère."}],
       "correction": {"lignes": [
           {"texte": "4 : anaphase : 4 chromatides à chaque pôle (une de chaque chromosome)", "mot": "quatre chromatides"},
           {"texte": "chaque cellule fille : 4 chromosomes à une chromatide (2n = 4)", "mot": "quatre chromosomes à une chromatide"},
           {"texte": "deux cellules filles génétiquement identiques : reproduction conforme", "mot": "la reproduction conforme"}],
         "parole": "السؤال quatre. فla figure un، فكل pôle، quatre chromatides: وحدة من كل chromosome. كل cellule fille: quatre chromosomes à une chromatide، deux n égale quatre، بحال la cellule mère. إذن la mitose donne deux cellules filles génétiquement identiques: هادي la reproduction conforme."},
       "explication": "ex_s4", "facile": "fa_s4"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : chaque phase et son critère",
     "screen_content": {"lead": "Nom de la phase + car + critère visible."},
     "visual": {"kind": "simulation", "url": MITOSE + "?vue=animale", "caption": "La mitose d'une cellule animale (2n = 4), phase par phase"},
     "speech_text": {"mixed": "نشوفو la mitose، phase par phase. la prophase: la chromatine كتجمع، وكيبانو des chromosomes à deux chromatides. l'enveloppe nucléaire كتختفي، وle fuseau كيتكون، entre deux asters. la métaphase: les chromosomes كيتصفو على la plaque équatoriale. l'anaphase: le centromère كيتقسم، و les chromatides كيمشيو نحو les pôles opposés. la télophase: la cellule كتضيق فالوسط، وكيرجعو les noyaux. فكل figure، قول اسم la phase، من بعد car، والدليل اللي كتشوف."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "nom de la phase + car + critère visible", "mot": "قول اسم la phase"}],
       "pointage": [{"mot": "la chromatine كتجمع", "commande": "play_until", "parametres": {"moment": "condensation"}},
                    {"mot": "des chromosomes à deux chromatides", "repere": "chromosomes"},
                    {"mot": "l'enveloppe nucléaire كتختفي", "commande": "play_until", "parametres": {"moment": "enveloppe_disparait"}},
                    {"mot": "وle fuseau كيتكون", "commande": "play_until", "parametres": {"moment": "asters_fuseau"}},
                    {"mot": "وle fuseau كيتكون", "repere": "fuseau"},
                    {"mot": "la métaphase:", "commande": "play_until", "parametres": {"moment": "plaque_equatoriale"}},
                    {"mot": "على la plaque équatoriale", "repere": "plaque"},
                    {"mot": "l'anaphase:", "commande": "play_until", "parametres": {"moment": "clivage_centromere"}},
                    {"mot": "نحو les pôles opposés", "commande": "play_until", "parametres": {"moment": "migration"}},
                    {"mot": "نحو les pôles opposés", "repere": "chromatides"},
                    {"mot": "la télophase:", "commande": "play_until", "parametres": {"moment": "etranglement"}},
                    {"mot": "la cellule كتضيق فالوسط", "repere": "etranglement"},
                    {"mot": "وكيرجعو les noyaux", "commande": "play_until", "parametres": {"moment": "deux_noyaux"}},
                    {"mot": "وكيرجعو les noyaux", "repere": "noyaux_fils"},
                    {"mot": "قول اسم la phase", "cible": "centre:0"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : toujours P, M, A, T",
     "screen_content": {"lead": "Prophase → métaphase → anaphase → télophase."},
     "visual": {"kind": "simulation", "url": MITOSE + "?vue=animale&apercu=1", "caption": "La mitose d'un coup d'œil"},
     "speech_text": {"mixed": "الترتيب ديال la mitose ديما هو: prophase، métaphase، anaphase، télophase. باش تتفكرو: P، M، A، T. فالأول les chromosomes كيتجمعو. من بعد كيتصفو فالوسط. من بعد les chromatides كيتفارقو. وفاللخر، la cellule كتقسم، et deux cellules filles se forment."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "prophase → métaphase → anaphase → télophase (P, M, A, T)", "mot": "ديما هو"}],
       "pointage": [{"mot": "ديما هو", "cible": "centre:0"},
                    {"mot": "فالأول les chromosomes كيتجمعو", "commande": "play_until", "parametres": {"moment": "condensation"}},
                    {"mot": "من بعد كيتصفو فالوسط", "commande": "play_until", "parametres": {"moment": "plaque_equatoriale"}},
                    {"mot": "les chromatides كيتفارقو", "commande": "play_until", "parametres": {"moment": "migration"}},
                    {"mot": "وفاللخر، la cellule كتقسم", "commande": "play_until", "parametres": {"moment": "fin"}},
                    {"mot": "et deux cellules filles se forment", "repere": "noyaux_fils"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : en métaphase, 4 chromosomes × 2 chromatides",
     "screen_content": {"lead": "2n = 4 chromosomes, chacun à deux chromatides : 8 chromatides."},
     "visual": {"kind": "simulation", "url": MITOSE + "?vue=animale&diapo=ex_metaphase", "caption": "La métaphase : les chromosomes sur la plaque équatoriale"},
     "speech_text": {"mixed": "فla métaphase، les chromosomes متصفين على la plaque équatoriale. شوف واحد le chromosome: deux chromatides، مربوطين بle centromère. deux n égale quatre: quatre chromosomes. وكل chromosome، deux chromatides. donc quatre fois deux، égale huit chromatides."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "2n = 4 chromosomes à deux chromatides", "mot": "deux n égale quatre"}, {"texte": "4 × 2 = 8 chromatides", "mot": "égale huit chromatides"}],
       "pointage": [{"mot": "فla métaphase", "commande": "set_time", "parametres": {"time_s": 10.2}},
                    {"mot": "متصفين على la plaque équatoriale", "commande": "play_until", "parametres": {"moment": "plaque_equatoriale"}},
                    {"mot": "متصفين على la plaque équatoriale", "repere": "plaque"},
                    {"mot": "مربوطين بle centromère", "repere": "centromere"},
                    {"mot": "deux n égale quatre", "cible": "centre:0"},
                    {"mot": "égale huit chromatides", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : 4 chromatides à chaque pôle, deux cellules filles 2n = 4",
     "screen_content": {"lead": "Une chromatide de chaque chromosome à chaque pôle : deux cellules filles identiques."},
     "visual": {"kind": "simulation", "url": MITOSE + "?vue=animale&diapo=ex_anaphase", "caption": "L'anaphase, la télophase et les deux cellules filles"},
     "speech_text": {"mixed": "فl'anaphase، le centromère كيتقسم. كل chromosome كيعطي chromatide لكل pôle. شوف: فكل pôle، quatre chromatides. ودابا كل chromatide ولات chromosome à une chromatide. فla télophase، كيتكونو les noyaux. كل cellule fille: quatre chromosomes à une chromatide، deux n égale quatre، بحال la cellule mère. إذن la mitose donne deux cellules filles génétiquement identiques: la reproduction conforme."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "anaphase : 4 chromatides à chaque pôle", "mot": "فكل pôle، quatre chromatides"},
                  {"texte": "chaque cellule fille : 2n = 4 chromosomes à une chromatide", "mot": "كل cellule fille:"},
                  {"texte": "deux cellules filles génétiquement identiques", "mot": "la reproduction conforme"}],
       "pointage": [{"mot": "فl'anaphase", "commande": "set_time", "parametres": {"time_s": 13.2}},
                    {"mot": "le centromère كيتقسم", "commande": "play_until", "parametres": {"moment": "clivage_centromere"}},
                    {"mot": "كل chromosome كيعطي chromatide", "commande": "play_until", "parametres": {"moment": "migration"}},
                    {"mot": "فكل pôle، quatre chromatides", "repere": "chromatides"},
                    {"mot": "فكل pôle، quatre chromatides", "cible": "centre:0"},
                    {"mot": "فla télophase", "commande": "play_until", "parametres": {"moment": "deux_noyaux"}},
                    {"mot": "كيتكونو les noyaux", "repere": "noyaux_fils"},
                    {"mot": "كل cellule fille:", "commande": "play_until", "parametres": {"moment": "fin"}},
                    {"mot": "كل cellule fille:", "cible": "centre:1"},
                    {"mot": "la reproduction conforme", "cible": "centre:2"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    assoc_criteres("fa_s1"),
    qcm_facile("fa_s2", "Plus facile : l'ordre des phases", "سؤال ساهل: شنو هو الترتيب ديال les phases؟",
      "L'ordre des phases de la mitose est :", ["prophase → anaphase → métaphase → télophase", "prophase → métaphase → anaphase → télophase",
                                                 "métaphase → prophase → anaphase → télophase"], 1, {
        "1": {"juste": rep("برافو! prophase، métaphase، anaphase، télophase: P، M، A، T.", "Juste : prophase → métaphase → anaphase → télophase.")},
        "0": {"1": rep("قريب! les chromatides ما يمكنش يتفارقو قبل ما les chromosomes يتصفو فالوسط. عاود اختار.", "Les chromatides ne se séparent qu'après l'alignement des chromosomes au milieu. Réessaie."),
              "2": rep("الجواب هو prophase، métaphase، anaphase، télophase. la métaphase كتجي قبل l'anaphase.", "Réponse : prophase → métaphase → anaphase → télophase ; la métaphase vient avant l'anaphase.")},
        "2": {"1": rep("ما تقلقش. باش يتصفو les chromosomes، خاصهم يتجمعو الأول. شمن phase فيها كيتجمعو؟ عاود اختار.", "Pour s'aligner, les chromosomes doivent d'abord se condenser. Dans quelle phase ? Réessaie."),
              "2": rep("الجواب هو prophase، métaphase، anaphase، télophase. la prophase هي الأولى.", "Réponse : prophase → métaphase → anaphase → télophase ; la prophase est la première.")}},
      "شنو هو الترتيب ديال les phases ديال la mitose؟"),
    qcm_facile("fa_s3", "Plus facile : compter les chromatides", "سؤال ساهل: نحسبو les chromatides.",
      "Une cellule 2n = 4 en métaphase contient :", ["4 chromatides", "2 chromatides", "8 chromatides"], 2, {
        "2": {"juste": rep("برافو! quatre chromosomes، وكل chromosome، deux chromatides: quatre fois deux، égale huit chromatides.", "Juste : 4 chromosomes × 2 chromatides = 8 chromatides.")},
        "0": {"1": rep("قريب! quatre هو le nombre ديال les chromosomes. وكل chromosome فla métaphase، شحال فيه ديال les chromatides؟ عاود اختار.", "4, c'est le nombre de chromosomes. Combien de chromatides a chacun en métaphase ? Réessaie."),
              "2": rep("الجواب هو: huit chromatides: quatre chromosomes، fois deux chromatides.", "Réponse : 8 chromatides (4 chromosomes × 2).")},
        "1": {"1": rep("ما تقلقش. deux هو عدد les chromatides ديال واحد le chromosome. و la cellule a quatre chromosomes. عاود اختار.", "2, ce sont les chromatides d'un seul chromosome ; la cellule en a 4. Réessaie."),
              "2": rep("الجواب هو: huit chromatides: quatre fois deux.", "Réponse : 8 chromatides (4 × 2).")}},
      "cellule، deux n égale quatre، فla métaphase: شحال فيها ديال les chromatides؟"),
    vrai_faux("fa_s4", "Plus facile : l'anaphase et les cellules filles", "Vrai ou faux : anaphase et cellules filles (2n = 4).",
      "سؤال ساهل: vrai ولا faux، على l'anaphase وles cellules filles.", [
        ("À l'anaphase, chaque pôle reçoit une chromatide de chaque chromosome.", True, "Vrai : les chromatides sœurs partent vers les pôles opposés."),
        ("À l'anaphase d'une cellule 2n = 4, 8 chromatides arrivent à chaque pôle.", False, "Faux : 4 à chaque pôle, 8 au total."),
        ("Chaque cellule fille a 4 chromosomes, comme la cellule mère.", True, "Vrai : 2n = 4 chromosomes à une chromatide."),
        ("Les deux cellules filles ont des informations génétiques différentes.", False, "Faux : elles sont génétiquement identiques (reproduction conforme).")])
  ]}]},
  "similaire": {
    "id": "svt_ex_ch3_mitose_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On observe au microscope des cellules animales d'une autre espèce, de formule chromosomique 2n = 6. Les figures 1 à 4 sont les croquis de quatre de ces cellules, chacune à une phase différente de la mitose.",
      "intro_dit": "نفس التمرين، مع espèce أخرى: deux n égale six. les figures، de un à quatre، هوما les croquis de quatre cellules، وكل وحدة فphase مختلفة ديال la mitose.",
      "figures": [planche(ORDRE_B, CHROM6, 6)],
      "donnees": ["Cellule animale, 2n = 6 (trois paires de chromosomes)", "Jaune : centromères et asters ; traits fins : fibres du fuseau"],
      "questions": [
        {"id": "1", "texte": "Identifier la phase de la mitose représentée par chacune des figures 1 à 4, en justifiant par un critère visible.",
         "reponse": {"type": "phrase", "attendu": "Figure 1 : métaphase, car les chromosomes à deux chromatides sont alignés par leur centromère sur la plaque équatoriale. Figure 2 : télophase, car la cellule s'étrangle au milieu et deux noyaux se reforment. Figure 3 : prophase, car les chromosomes condensés à deux chromatides apparaissent et l'enveloppe nucléaire disparaît. Figure 4 : anaphase, car les chromatides sœurs se séparent et migrent vers les pôles opposés (6 de chaque côté)."},
         "clavier": {"aides": ["car", "prophase", "métaphase", "anaphase", "télophase", "plaque équatoriale", "pôles opposés"], "pieges": ["interphase"]},
         "correction": {"lignes": [
             {"texte": "1 : figure 1 : métaphase (plaque équatoriale) ; figure 2 : télophase (étranglement, deux noyaux)", "mot": "figure un: la métaphase"},
             {"texte": "figure 3 : prophase (condensation, enveloppe qui disparaît) ; figure 4 : anaphase (migration vers les pôles opposés)", "mot": "figure trois: la prophase"}],
           "parole": "السؤال un. figure un: la métaphase، car les chromosomes متصفين على la plaque équatoriale. figure deux: la télophase، car la cellule كتضيق، et deux noyaux se forment. figure trois: la prophase، car les chromosomes كيتجمعو، وl'enveloppe nucléaire كتختفي. figure quatre: l'anaphase، car les chromatides كيمشيو نحو les pôles opposés."}},
        {"id": "2", "texte": "Classer les figures 1 à 4 dans l'ordre chronologique de la mitose.",
         "reponse": {"type": "phrase", "attendu": "3 (prophase) → 1 (métaphase) → 4 (anaphase) → 2 (télophase)."},
         "clavier": {"aides": ["→", "prophase", "métaphase", "anaphase", "télophase"], "pieges": ["1 → 2 → 3 → 4"]},
         "correction": {"lignes": [{"texte": "2 : 3 (prophase) → 1 (métaphase) → 4 (anaphase) → 2 (télophase)", "mot": "figure trois، من بعد figure un"}],
           "parole": "السؤال deux. figure trois، من بعد figure un، من بعد figure quatre، وفاللخر figure deux."}},
        {"id": "3", "texte": "Calculer le nombre de chromatides contenues dans la cellule de la figure 1.",
         "reponse": {"type": "valeur", "grandeur": "chromatides", "valeur": 12, "unite": "chromatides", "tolerance": 0.02,
                     "attendu": "2n = 6 chromosomes à deux chromatides : 6 × 2 = 12 chromatides"},
         "clavier": {"aides": ["2n = 6", "× 2", "chromatides"], "pieges": ["6 chromatides", "24"]},
         "correction": {"lignes": [{"texte": "3 : figure 1 (métaphase) : 6 chromosomes à deux chromatides", "mot": "six chromosomes à deux chromatides"},
                                   {"texte": "6 × 2 = 12 chromatides", "mot": "six fois deux، égale douze chromatides"}],
           "parole": "السؤال trois. فla figure un، la métaphase، il y a six chromosomes à deux chromatides. six fois deux، égale douze chromatides."}},
        {"id": "4", "texte": "Indiquer le nombre de chromatides qui arrivent à chaque pôle dans la figure 4, puis le nombre et l'état des chromosomes de chaque cellule fille. Conclure sur le rôle de la mitose.",
         "reponse": {"type": "phrase", "attendu": "Dans la figure 4 (anaphase), 6 chromatides arrivent à chaque pôle : une chromatide de chaque chromosome. Chaque cellule fille reçoit donc 6 chromosomes à une chromatide (2n = 6), comme la cellule mère. La mitose donne deux cellules filles génétiquement identiques : c'est une reproduction conforme."},
         "clavier": {"aides": ["6 chromatides", "à chaque pôle", "chromosomes à une chromatide", "2n = 6", "génétiquement identiques"], "pieges": ["12 chromatides à chaque pôle", "n = 3"]},
         "correction": {"lignes": [{"texte": "4 : anaphase : 6 chromatides à chaque pôle", "mot": "six chromatides"},
                                   {"texte": "chaque cellule fille : 6 chromosomes à une chromatide (2n = 6) ; deux cellules filles génétiquement identiques", "mot": "six chromosomes à une chromatide"}],
           "parole": "السؤال quatre. فla figure quatre، فكل pôle، six chromatides. كل cellule fille: six chromosomes à une chromatide، deux n égale six، بحال la cellule mère. إذن la mitose donne deux cellules filles génétiquement identiques."}}
      ]}}
}
ecrire(EX, sys.argv[1])
