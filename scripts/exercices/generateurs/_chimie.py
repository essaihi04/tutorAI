# Outils communs aux générateurs d'exercices de chimie (ch. 10 à 13) : mêmes formes que le pilote
# phys_ex_ch1_corde_1.py (rep, qcm_facile, diapositive de simulation), en fonctions pour qu'une donnée changée une fois
# change partout. Les courbes sont CALCULÉES par la chimie (cinétique d'ordre un, bilan des charges pour le pH).
import json, math, sys

SIMS = "/media/simulations/chimie/"


# ---------------------------------------------------------------- nombres écrits (virgule française)
def fr(x, n=2):
    """fr(0.0125, 4) -> '0,0125' ; n = nombre de décimales (zéros finaux gardés)."""
    s = f"{x:.{n}f}".replace(".", ",")
    return s.replace("-", "−")


def sci(x, n=1):
    """sci(0.00125, 2) -> '1,25 × 10⁻³' (n décimales sur la mantisse)."""
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, n) >= 10:
        m /= 10; e += 1
    sup = str(e).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"{fr(m, n)} × 10{sup}"


# ---------------------------------------------------------------- réponses et questions
def val(grandeur, valeur, unite, attendu, tol=0.03):
    d = {"type": "valeur", "grandeur": grandeur, "valeur": valeur, "tolerance": tol, "attendu": attendu}
    if unite:
        d["unite"] = unite
    return d


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


def Q(id, texte, texte_dit, reponse, clavier, aides, lignes, parole, explication=None, facile=None):
    """aides = [(texte, dit), …] ; lignes = [(texte, mot), …] (mot : passage de parole où la ligne s'écrit)."""
    q = {"id": id, "texte": texte}
    if texte_dit:
        q["texte_dit"] = texte_dit
    q["reponse"] = reponse
    q["clavier"] = {"aides": clavier[0], "pieges": clavier[1]}
    if aides:
        q["aides"] = [{"texte": t, "dit": d} for t, d in aides]
    q["correction"] = {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}
    if explication:
        q["explication"] = explication
    if facile:
        q["facile"] = facile
    return q


def QS(id, texte, reponse, clavier, lignes, parole):
    """question de l'exercice semblable : réponse, clavier et correction seulement."""
    return Q(id, texte, None, reponse, clavier, None, lignes, parole)


# ---------------------------------------------------------------- diapositive d'explication (simulation du cours)
def _pointage(p):
    mot, quoi = p
    if isinstance(quoi, dict):
        if "set" in quoi:
            return {"mot": mot, "commande": "set_parameters", "parametres": quoi["set"]}
        return {"mot": mot, "commande": "play_until", "parametres": {"moment": quoi["moment"]}}
    if quoi in ("start", "reset", "pause", "resume"):
        return {"mot": mot, "commande": quoi}
    if quoi.startswith("centre:"):
        return {"mot": mot, "cible": quoi}
    if quoi.startswith("repere:"):
        return {"mot": mot, "repere": quoi[7:]}
    if quoi.startswith("moment:"):
        return {"mot": mot, "commande": "play_until", "parametres": {"moment": quoi[7:]}}
    raise ValueError(quoi)


def sim(sid, titre, lead, url, caption, mixed, centre, pointage):
    """url relative à /media/simulations/chimie/ (ex. « cinetique-tableau/courbe.html?vue=lecture ») ;
    centre = [(texte écrit, mot)] ; pointage = [(mot, 'start' | 'moment:x' | {'set': {...}} | 'repere:r' | 'centre:0')].
    Les « centre » sont pointés d'office à leur mot."""
    pts = [_pointage(p) for p in pointage]
    for i, (_, m) in enumerate(centre):
        if not any(p.get("cible") == f"centre:{i}" for p in pts):
            pts.append({"mot": m, "cible": f"centre:{i}"})
    return {"id": sid, "slide_type": "simulation", "title": titre,
            "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": SIMS + url, "caption": caption},
            "speech_text": {"mixed": mixed},
            "concentration": {"demarrer": "reset",
                              "centre": [{"texte": t, "mot": m} for t, m in centre],
                              "pointage": pts}}


# ---------------------------------------------------------------- versions faciles
def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def qcm(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """reactions : {i: ('juste', parole, ecrit)} pour la bonne option, {i: ((parole1, ecrit1), (parole2, ecrit2))}
    pour chaque option fausse (1 = indice sans la réponse, 2 = la réponse et sa justification)."""
    r = {}
    for i, v in reactions.items():
        if v[0] == "juste":
            r[str(i)] = {"juste": rep(v[1], v[2])}
        else:
            r[str(i)] = {"1": rep(*v[0]), "2": rep(*v[1])}
    assert set(r) == {str(i) for i in range(len(options))}, (sid, "une réaction par option")
    assert "juste" in r[str(bonne)], (sid, "la bonne option doit être « juste »")
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": prompt},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": r}}}


def vf(sid, titre, lead, intro, affirmations):
    """affirmations = [(texte, vrai?, explication)]"""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": lead},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?",
                           "statements": [{"text": t, "correct": c, "explanation": e} for t, c, e in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def assoc(sid, titre, lead, intro, prompt, gauche, droite, couples, retours, bilan):
    """gauche/droite = [(id, texte)] ; couples = {g: d} ; retours = {"g-d": (juste?, texte, dit)} (une par paire
    possible, ou "g-*" par défaut) ; bilan = (texte, dit)."""
    for g, _ in gauche:
        for d, _ in droite:
            assert f"{g}-{d}" in retours or f"{g}-*" in retours, (sid, g, d)
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": lead},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": prompt, "association": {
                "gauche": [{"id": i, "texte": t} for i, t in gauche],
                "droite": [{"id": i, "texte": t} for i, t in droite],
                "couples": couples,
                "retours": {k: {"juste": j, "texte": t, "dit": d} for k, (j, t, d) in retours.items()},
                "bilan": {"texte": bilan[0], "dit": bilan[1]}}},
            "concentration": {"demarrer": "reset"}}


# ---------------------------------------------------------------- figures (FigureCahierData), calculées
def courbe_fig(titre, axes, elements, legende=None, ratio=None):
    """axes = ((xmin, xmax, nom, unite, grads), (ymin, ymax, nom, unite, grads))."""
    (x0, x1, nx, ux, gx), (y0, y1, ny, uy, gy) = axes
    ax = {"x": {"min": x0, "max": x1, "nom": nx, "graduations": gx}, "y": {"min": y0, "max": y1, "nom": ny, "graduations": gy}}
    if ux:
        ax["x"]["unite"] = ux
    if uy:
        ax["y"]["unite"] = uy
    f = {"type": "courbe", "titre": titre, "axes": ax, "elements": elements}
    if legende:
        f["legende"] = legende
    if ratio:
        f["ratio"] = ratio
    return f


def x_ordre1(xf, t12):
    """x(t) = x_f·(1 − e^(−t·ln2/t½)) : le modèle des courbes du cours (montée rapide puis palier)."""
    k = math.log(2) / t12
    return (lambda t: xf * (1 - math.exp(-k * t))), f"{xf}*(1-exp(-{k:.6f}*x))"


def pente_ordre1(xf, t12, t):
    """dx/dt à la date t pour x_ordre1 (pente de la tangente)."""
    k = math.log(2) / t12
    return xf * k * math.exp(-k * t)


def tangente(xf, t12, t, de, a):
    """élément « courbe » de la tangente en t (droite)."""
    x, _ = x_ordre1(xf, t12)
    p = pente_ordre1(xf, t12, t)
    b = x(t) - p * t
    return {"f": "courbe", "expr": f"{p:.6f}*x+{b:.6f}", "de": de, "a": a, "couleur": "orange", "trait": "pointille"}


def ph_dosage(Va, Ca, Cb, V, pKa=None, acide=True, pKe=14.0):
    """pH du mélange quand on verse V (mL) de titrant dans Va (mL) d'acide (acide=True ; titrant : base forte)
    ou de base (acide=False ; titrant : acide fort). pKa=None : espèce titrée forte. Bilan des charges, résolu par
    dichotomie sur log[H3O+]."""
    Ke = 10 ** -pKe
    Vt = (Va + V) / 1000
    na, nt = Ca * Va / 1000, Cb * V / 1000
    ca, ct = na / Vt, nt / Vt
    Ka = 10 ** -pKa if pKa is not None else None

    def f(lh):
        h = 10 ** lh; oh = Ke / h
        if acide:
            a_moins = ca if Ka is None else ca * Ka / (Ka + h)
            return h + ct - oh - a_moins           # [H3O+] + [Na+] = [HO-] + [A-]
        bh = ca if Ka is None else ca * h / (Ka + h)
        return h + bh - oh - ct                    # [H3O+] + [BH+] = [HO-] + [Cl-]
    lo, hi = -14.5, 0.5
    for _ in range(80):
        m = (lo + hi) / 2
        if f(m) > 0:
            hi = m
        else:
            lo = m
    return -(lo + hi) / 2


def courbe_ph(Va, Ca, Cb, Vmax, pKa=None, acide=True, n=120):
    """points [V, pH] de la courbe de dosage (plus serrés autour de l'équivalence)."""
    Ve = Ca * Va / Cb
    vs = sorted(set([round(Vmax * i / n, 3) for i in range(n + 1)] +
                    [round(Ve + d, 3) for d in (-1, -.6, -.4, -.25, -.15, -.08, -.04, -.02, 0, .02, .04, .08, .15, .25, .4, .6, 1) if 0 <= Ve + d <= Vmax]))
    return [[v, round(ph_dosage(Va, Ca, Cb, v, pKa, acide), 3)] for v in vs]


def tableau_texte(titre, entetes, lignes, cadre=(10, 0.7)):
    """un tableau écrit à la craie (schéma) : une ligne de texte par rangée, colonnes alignées."""
    l, hl = cadre
    nl = len(lignes) + 1
    h = hl * nl + 0.2
    ncol = len(entetes)
    els = []
    for j, row in enumerate([entetes] + lignes):
        y = h - 0.1 - hl * (j + 0.5)
        for i, c in enumerate(row):
            els.append({"f": "texte", "at": [l * (i + 0.5) / ncol, y], "t": c, "couleur": "jaune" if j == 0 else "blanc",
                        "ancre": "centre", "taille": "petit"})
        if j < nl - 1:
            yl = h - 0.1 - hl * (j + 1)
            els.append({"f": "ligne", "pts": [[0, yl], [l, yl]], "couleur": "faible"})
    for i in range(1, ncol):
        x = l * i / ncol
        els.append({"f": "ligne", "pts": [[x, 0.1], [x, h - 0.1]], "couleur": "faible"})
    return {"type": "schema", "titre": titre, "cadre": {"l": l, "h": h}, "elements": els}


# ---------------------------------------------------------------- assemblage et écriture
def exercice(id, cours, chapitre, titre, niveau, duree, competences, intro, intro_dit, figures, donnees, questions,
             explications, faciles, sim_titre, sim_intro, sim_intro_dit, sim_figures, sim_donnees, sim_questions):
    ids_ex = {s["id"] for s in explications}
    ids_fa = {s["id"] for s in faciles}
    for q in questions:
        assert q.get("explication") in ids_ex, (id, q["id"], "explication")
        assert q.get("facile") in ids_fa, (id, q["id"], "facile")
        assert len(q.get("aides", [])) >= 2, (id, q["id"], "aides")
    assert [q["id"] for q in questions] == [q["id"] for q in sim_questions], (id, "similaire : mêmes questions")
    return {
        "id": id, "type": "exercice", "version": 1, "status": "published",
        "matiere": "physique", "chapitre": chapitre, "cours": cours,
        "titre": titre, "niveau": niveau, "duree_min": duree,
        "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
        "competences": competences,
        "enonce": {"intro": intro, "intro_dit": intro_dit, "figures": figures, "donnees": donnees, "questions": questions},
        "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": explications}]},
        "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": faciles}]},
        "similaire": {"id": id + "_b", "titre": sim_titre,
                      "enonce": {"intro": sim_intro, "intro_dit": sim_intro_dit, "figures": sim_figures,
                                 "donnees": sim_donnees, "questions": sim_questions}},
    }


VOIX = {"intro_dit", "texte_dit", "dit", "parole", "mixed", "enonce_dit", "mot"}


def _voix(o, k=""):
    if isinstance(o, dict):
        return {kk: _voix(v, kk) for kk, v in o.items()}
    if isinstance(o, list):
        return [_voix(v, k) for v in o]
    if isinstance(o, str) and k in VOIX:
        return o.replace("thêta", "teta")
    return o


def ecrire(EX, chemin=None):
    chemin = chemin or sys.argv[1]
    EX = _voix(EX)
    json.dump(EX, open(chemin, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok", chemin)
