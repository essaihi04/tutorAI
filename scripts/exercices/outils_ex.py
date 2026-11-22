"""Outils communs des générateurs d'exercices (partie « Exercices », skill `.agents/skills/exercices/SKILL.md`).

Un générateur `scripts/exercices/generateurs/<id>.py` fait :
    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from outils_ex import *
    EX = {...}
    ecrire(EX)          # sys.argv[1] ou frontend/public/media/exercices/<id>.json

`ecrire` contrôle la structure (§ 7 du skill) AVANT d'écrire : chaque question a reponse, clavier, 2 aides,
correction ; chaque id d'explication / de version facile existe ; la simulation existe ; le nombre lu dans `attendu`
(même lecture que `juger.ts`) est la `valeur` ; le semblable a les mêmes questions ; aucune voix n'a de chiffre ni
de symbole. Puis lancer `finir.py` (règle des nombres darija → français, mots du pointage).
"""
import json, math, re, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
PUBLIC = RACINE / "frontend" / "public"

# ---------------------------------------------------------------- petits constructeurs

def rep(parole, ecrit):
    """Réaction préparée d'un QCM : ce qui est dit, ce qui est écrit."""
    return {"parole": parole, "ecrit": ecrit}


def aide(texte, dit):
    return {"texte": texte, "dit": dit}


def valeur(grandeur, v, unite, attendu, tol=0.03):
    return {"type": "valeur", "grandeur": grandeur, "valeur": v, "unite": unite, "tolerance": tol, "attendu": attendu}


def phrase(attendu):
    return {"type": "phrase", "attendu": attendu}


def corr(lignes, parole):
    """lignes : [(texte écrit, mot = passage exact de parole)]."""
    return {"lignes": [{"texte": t, "mot": m} for t, m in lignes], "parole": parole}


def question(qid, texte, texte_dit, reponse, clavier_aides, clavier_pieges, aides, correction, explication, facile):
    return {"id": qid, "texte": texte, "texte_dit": texte_dit, "reponse": reponse,
            "clavier": {"aides": clavier_aides, "pieges": clavier_pieges}, "aides": aides,
            "correction": correction, "explication": explication, "facile": facile}


def question_semblable(qid, texte, reponse, clavier_aides, clavier_pieges, correction):
    return {"id": qid, "texte": texte, "reponse": reponse,
            "clavier": {"aides": clavier_aides, "pieges": clavier_pieges}, "correction": correction}


def diapo_sim(sid, titre, lead, url, caption, mixed, centre=(), pointage=(), demarrer="reset"):
    """Diapositive d'explication animée : une simulation EXISTANTE du cours.
    centre : [(texte écrit au tableau, mot)] ; pointage : dicts du cours ({"mot", "commande", "parametres"} ou {"mot", "repere"})."""
    return {"id": sid, "slide_type": "simulation", "title": titre,
            "screen_content": {"lead": lead},
            "visual": {"kind": "simulation", "url": url, "caption": caption},
            "speech_text": {"mixed": mixed},
            "concentration": {"demarrer": demarrer,
                              "centre": [{"texte": t, "mot": m} for t, m in centre],
                              "pointage": list(pointage)}}


def qcm_facile(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """Version facile en QCM : reactions = {"<i>": {"juste": rep(..)} pour la bonne, {"1": rep, "2": rep} pour les autres}."""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": prompt},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}


def vrai_faux_facile(sid, titre, intro, lead, affirmations):
    """affirmations : [(texte, vrai?, explication)]."""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": lead}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?",
                           "statements": [{"text": t, "correct": c, "explanation": e} for t, c, e in affirmations]}],
            "concentration": {"demarrer": "reset"}}


def association_facile(sid, titre, intro, lead, consigne, gauche, droite, couples, retours, bilan_texte, bilan_dit):
    """gauche/droite : [(id, texte)] ; couples {"1": "a"} ; retours {"1-a": (juste?, texte, dit)} pour CHAQUE paire."""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": lead}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "association", "prompt": consigne,
                         "association": {"gauche": [{"id": i, "texte": t} for i, t in gauche],
                                         "droite": [{"id": i, "texte": t} for i, t in droite],
                                         "couples": couples,
                                         "retours": {k: {"juste": j, "texte": t, "dit": d} for k, (j, t, d) in retours.items()},
                                         "bilan": {"texte": bilan_texte, "dit": bilan_dit}}},
            "concentration": {"demarrer": "reset"}}


def deck(nom, titre, slides):
    return {"activities": [{"id": nom, "title": titre, "slides": slides}]}

# ---------------------------------------------------------------- figures : courbes

def pts(f, x0, x1, n=120, nd=4):
    """Points [x, f(x)] calculés par la physique (même formule que la simulation)."""
    return [[round(x0 + (x1 - x0) * i / n, nd), round(f(x0 + (x1 - x0) * i / n), nd)] for i in range(n + 1)]


def axe(nom, mn, mx, unite=None, graduations=None):
    a = {"min": mn, "max": mx, "nom": nom}
    if unite: a["unite"] = unite
    if graduations is not None: a["graduations"] = graduations
    return a


def figure_courbe(titre, ax, ay, elements, legende=None, ratio=None):
    f = {"type": "courbe", "titre": titre, "axes": {"x": ax, "y": ay}, "elements": elements}
    if legende: f["legende"] = legende
    if ratio: f["ratio"] = ratio
    return f

# ---------------------------------------------------------------- figures : schémas de circuits
# Un circuit = des segments horizontaux ou verticaux (p1 -> p2) ; chaque segment est un fil ou un dipôle dessiné
# au milieu du segment, avec ses fils d'arrivée. Coordonnées du cadre (0, 0) en bas à gauche, mêmes unités en x et y.

def _dir(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy)
    return dx / L, dy / L, L


def _pt(p, u, v, a, b=0.0):
    """p + a·(u, v) + b·(normale)."""
    return [round(p[0] + a * u - b * v, 3), round(p[1] + a * v + b * u, 3)]


def fil(*points, couleur=None):
    e = {"f": "ligne", "pts": [list(p) for p in points]}
    if couleur: e["couleur"] = couleur
    return [e]


def dipole(p1, p2, sorte, t=None, pos=None, couleur=None, taille=1.0):
    """sorte : 'R' (rectangle), 'C' (deux armatures), 'L' (bobine, 4 boucles), 'G' (générateur de tension idéal),
    'I' (générateur de courant), 'K' (interrupteur ouvert), 'Kf' (fermé), 'lampe', 'D' (diode, passante de p1 vers p2),
    'A' (ampèremètre), 'V' (voltmètre). t = étiquette (« R », « C », « (L, r) ») écrite à côté (pos : côté)."""
    u, v, L = _dir(p1, p2)
    m = L / 2
    els = []
    w = {"R": 1.0, "C": 0.24, "L": 1.2, "G": 0.8, "I": 0.8, "K": 0.9, "Kf": 0.9, "lampe": 0.7, "D": 0.5, "A": 0.7, "V": 0.7}[sorte] * taille
    a0, a1 = m - w / 2, m + w / 2
    els.append({"f": "ligne", "pts": [list(p1), _pt(p1, u, v, a0)]})
    els.append({"f": "ligne", "pts": [_pt(p1, u, v, a1), list(p2)]})
    c = couleur
    def add(e):
        if c and "couleur" not in e: e["couleur"] = c
        els.append(e)
    h = 0.22 * taille
    if sorte == "R":
        q = [_pt(p1, u, v, a0, -h), _pt(p1, u, v, a1, h)]
        add({"f": "rect", "de": [min(q[0][0], q[1][0]), min(q[0][1], q[1][1])], "a": [max(q[0][0], q[1][0]), max(q[0][1], q[1][1])]})
    elif sorte == "C":
        for a in (a0, a1):
            add({"f": "ligne", "pts": [_pt(p1, u, v, a, -0.4 * taille), _pt(p1, u, v, a, 0.4 * taille)], "epais": True})
    elif sorte == "L":
        r = w / 8
        ang = math.degrees(math.atan2(v, u))
        for k in range(4):
            cc = _pt(p1, u, v, a0 + r * (2 * k + 1))
            add({"f": "arc", "c": cc, "r": r, "de": round(ang, 1), "a": round(ang + 180, 1)})
    elif sorte in ("G", "I", "lampe", "A", "V"):
        cc = _pt(p1, u, v, m)
        add({"f": "cercle", "c": cc, "r": w / 2})
        if sorte == "G":
            add({"f": "ligne", "pts": [_pt(p1, u, v, a0), _pt(p1, u, v, a1)]})
        elif sorte == "I":
            add({"f": "ligne", "pts": [_pt(p1, u, v, m, -w / 2), _pt(p1, u, v, m, w / 2)]})
            add({"f": "fleche", "de": _pt(p1, u, v, m - w / 4), "a": _pt(p1, u, v, m + w / 4)})
        elif sorte == "lampe":
            d = w / 2 / math.sqrt(2)
            add({"f": "ligne", "pts": [_pt(p1, u, v, m - d, -d), _pt(p1, u, v, m + d, d)]})
            add({"f": "ligne", "pts": [_pt(p1, u, v, m - d, d), _pt(p1, u, v, m + d, -d)]})
        else:
            add({"f": "texte", "at": [cc[0], cc[1] - 0.12], "t": sorte, "ancre": "centre"})
    elif sorte in ("K", "Kf"):
        add({"f": "point", "at": _pt(p1, u, v, a0)})
        add({"f": "point", "at": _pt(p1, u, v, a1), "creux": True})
        fin = _pt(p1, u, v, a1, 0.38 * taille) if sorte == "K" else _pt(p1, u, v, a1)
        add({"f": "ligne", "pts": [_pt(p1, u, v, a0), fin], "epais": True})
    elif sorte == "D":
        add({"f": "ligne", "pts": [_pt(p1, u, v, a0, -h), _pt(p1, u, v, a1), _pt(p1, u, v, a0, h)], "ferme": True})
        add({"f": "ligne", "pts": [_pt(p1, u, v, a1, -h), _pt(p1, u, v, a1, h)], "epais": True})
    if t:
        off = 0.55 * taille
        if pos is None:
            pos = "n" if abs(u) > abs(v) else "e"
        dx, dy = {"n": (0, off), "s": (0, -off - 0.15), "e": (off, -0.08), "o": (-off, -0.08)}[pos]
        cc = _pt(p1, u, v, m)
        add({"f": "texte", "at": [round(cc[0] + dx, 3), round(cc[1] + dy, 3)], "t": t,
             "ancre": {"n": "centre", "s": "centre", "e": "gauche", "o": "droite"}[pos]})
    return els


def inverseur(pivot, c1, c2, vers=None, t="K", pos_t=None):
    """Interrupteur à deux positions : lame partant de `pivot` vers le contact c1 (« 1 ») ou c2 (« 2 ») ; vers=None : entre les deux."""
    els = [{"f": "point", "at": list(pivot)},
           {"f": "point", "at": list(c1), "t": "1", "pos": "n", "creux": True},
           {"f": "point", "at": list(c2), "t": "2", "pos": "n", "creux": True}]
    if vers == 1: bout = c1
    elif vers == 2: bout = c2
    else: bout = [(c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2 - 0.25]
    els.append({"f": "ligne", "pts": [list(pivot), list(bout)], "epais": True})
    if t:
        els.append({"f": "texte", "at": pos_t or [pivot[0], pivot[1] - 0.45], "t": t, "ancre": "centre"})
    return els


def tension(de, a, t, couleur="cyan", pos="n"):
    """Flèche de tension (de la borne B vers la borne A pour u_AB), à côté du dipôle."""
    return [{"f": "fleche", "de": list(de), "a": list(a), "texte": t, "couleur": couleur, "pos": pos}]


def courant(at, sens, t="i", couleur="jaune"):
    """Chevron du sens du courant sur un fil : sens 'd', 'g', 'h', 'b' (droite, gauche, haut, bas)."""
    x, y = at
    s = 0.18
    pts_ = {"d": [[x - s, y + s], [x, y], [x - s, y - s]], "g": [[x + s, y + s], [x, y], [x + s, y - s]],
            "h": [[x - s, y - s], [x, y], [x + s, y - s]], "b": [[x - s, y + s], [x, y], [x + s, y + s]]}[sens]
    tx = {"d": [x - 0.05, y + 0.32], "g": [x + 0.05, y + 0.32], "h": [x + 0.35, y - 0.1], "b": [x + 0.35, y]}[sens]
    return [{"f": "ligne", "pts": pts_, "couleur": couleur, "epais": True},
            {"f": "texte", "at": tx, "t": t, "couleur": couleur}]


def borne(at, t, pos="n", couleur=None):
    e = {"f": "point", "at": list(at), "t": t, "pos": pos}
    if couleur: e["couleur"] = couleur
    return [e]


def texte(at, t, couleur=None, ancre="centre", taille=None):
    e = {"f": "texte", "at": list(at), "t": t, "ancre": ancre}
    if couleur: e["couleur"] = couleur
    if taille: e["taille"] = taille
    return [e]


def schema(titre, l, h, *groupes, legende=None):
    els = []
    for g in groupes: els += g
    f = {"type": "schema", "titre": titre, "cadre": {"l": l, "h": h}, "elements": els}
    if legende: f["legende"] = legende
    return f

# ---------------------------------------------------------------- contrôles et écriture

EXPOSANTS = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-'}


def lire_nombre(texte):
    """Même lecture que frontend/src/components/exercice/juger.ts (lireNombre)."""
    s = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^" + "".join(EXPOSANTS[c] for c in m.group(0)), texte)
    coupe = max(s.rfind("="), s.rfind("≈"))
    if coupe >= 0: s = s[coupe + 1:]
    s = re.sub(r"\s+", "", s).replace(",", ".").replace("−", "-")
    s = re.sub(r"[×x·*]10\^?\(?(-?\d+)\)?", r"e\1", s)
    m = re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", s)
    return float(m.group(0)) if m else None


CHAMPS_VOIX = {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit"}
SYMBOLES = re.compile(r"[=×÷/^√≈%τθλΔ∞→⇒·₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁻µΩ°]")
AR = re.compile(r"[؀-ۿ]")
_NB = r"(?:un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|quarante|cinquante|soixante|cent|mille|zéro|moins)"
COLLE = re.compile(r"[\u0600-\u06FF]" + _NB + r"\b")
DARIJA_NOMBRE = re.compile(r"(?<![\u0600-\u06FF])(?:تقريبا\s+" + _NB + r"|جوج|زوج|واحد|ثلاثة|تلاتة|ربعة|خمسة|ستة|سبعة|تمنية|تسعة|عشرة|ميا|ألف)(?![\u0600-\u06FF])")


def _voix(o):
    """Lecture des lettres grecques comme dans le pilote (θ : « teta »)."""
    if isinstance(o, dict): return {k: _voix(v) for k, v in o.items()}
    if isinstance(o, list): return [_voix(v) for v in o]
    if isinstance(o, str): return o.replace("thêta", "teta").replace("Thêta", "Teta")
    return o


def controler(EX):
    pb = []
    def q_ok(q, ou, semblable=False):
        for k in ("id", "texte", "reponse", "clavier", "correction"):
            if k not in q: pb.append((ou, q.get("id"), "manque " + k))
        r = q.get("reponse", {})
        if r.get("type") == "valeur":
            lu = lire_nombre(r.get("attendu", ""))
            if lu is None or abs(lu - r["valeur"]) > 1e-6 * max(abs(r["valeur"]), 1e-12) * 1000:
                pb.append((ou, q["id"], f"attendu lu {lu} ≠ valeur {r.get('valeur')}"))
            if not r.get("unite"): pb.append((ou, q["id"], "valeur sans unité"))
        elif r.get("type") != "phrase":
            pb.append((ou, q["id"], "type de réponse inconnu"))
        cl = q.get("clavier", {})
        if not cl.get("aides") or not cl.get("pieges"): pb.append((ou, q["id"], "clavier incomplet"))
        att = r.get("attendu", "")
        for a in cl.get("aides", []):
            if a.strip() == att.strip(): pb.append((ou, q["id"], "le clavier donne la réponse"))
        c = q.get("correction", {})
        if not c.get("lignes") or not c.get("parole"): pb.append((ou, q["id"], "correction incomplète"))
        if not c.get("lignes", [{}])[0].get("texte", "").startswith(q["id"]):
            pb.append((ou, q["id"], "la correction doit commencer par le numéro de la question"))
        if not semblable:
            if len(q.get("aides", [])) < 2: pb.append((ou, q["id"], "moins de 2 aides"))
            for k in ("texte_dit", "explication", "facile"):
                if not q.get(k): pb.append((ou, q["id"], "manque " + k))
    ids_ex = {s["id"]: s for a in EX["explication"]["activities"] for s in a["slides"]}
    ids_fa = {s["id"]: s for a in EX["facile"]["activities"] for s in a["slides"]}
    qs = EX["enonce"]["questions"]
    for q in qs:
        q_ok(q, "énoncé")
        if q.get("explication") not in ids_ex: pb.append(("énoncé", q["id"], "explication absente"))
        if q.get("facile") not in ids_fa: pb.append(("énoncé", q["id"], "facile absente"))
    sq = EX["similaire"]["enonce"]["questions"]
    if [q["id"] for q in sq] != [q["id"] for q in qs]: pb.append(("semblable", "-", "pas les mêmes questions"))
    for q in sq:
        q_ok(q, "semblable", True)
        for k in ("aides", "explication", "facile"):
            if k in q: pb.append(("semblable", q["id"], k + " interdit"))
    for s in ids_ex.values():
        url = s["visual"].get("url", "")
        if s["visual"].get("kind") != "simulation" or not (PUBLIC / url.lstrip("/").split("?")[0]).exists():
            pb.append(("explication", s["id"], "simulation introuvable : " + url))
    for s in ids_fa.values():
        qq = s.get("question")
        if qq and qq.get("type") == "qcm":
            reac = s["concentration"]["reponses"]["q"]
            for i in range(len(qq["options"])):
                r = reac.get(str(i), {})
                if i == qq["correct"] and "juste" not in r: pb.append(("facile", s["id"], f"option {i} : réaction juste manquante"))
                if i != qq["correct"] and not ("1" in r and "2" in r): pb.append(("facile", s["id"], f"option {i} : réactions 1 et 2 manquantes"))
        if qq and qq.get("type") == "association":
            a = qq["association"]
            for g in a["gauche"]:
                for d in a["droite"]:
                    if f"{g['id']}-{d['id']}" not in a["retours"]: pb.append(("facile", s["id"], f"retour {g['id']}-{d['id']} manquant"))
    def voix(o, k=""):
        if isinstance(o, dict): [voix(v, kk) for kk, v in o.items()]
        elif isinstance(o, list): [voix(v, k) for v in o]
        elif isinstance(o, str) and k in CHAMPS_VOIX:
            if re.search(r"\d", o): pb.append(("voix", k, "chiffre : " + o[:60]))
            g = COLLE.search(o)
            if g: pb.append(("voix", k, f"mot darija collé à un nombre : « {g.group(0)} »"))
            g = DARIJA_NOMBRE.search(o)
            if g: pb.append(("voix", k, f"nombre darija : « {g.group(0)} » (dire le nombre en français)"))
            m = SYMBOLES.search(o)
            if m: pb.append(("voix", k, f"symbole « {m.group(0)} » : " + o[max(0, m.start() - 30):m.start() + 30]))
    voix(EX)
    for k in ("id", "type", "version", "status", "matiere", "chapitre", "cours", "titre", "niveau", "duree_min", "origine", "competences"):
        if k not in EX: pb.append(("tête", k, "manque"))
    return pb


def ecrire(EX, chemin=None):
    EX = _voix(EX)
    pb = controler(EX)
    for p in pb: print("  PROBLÈME", p)
    chemin = chemin or (sys.argv[1] if len(sys.argv) > 1 else str(PUBLIC / "media" / "exercices" / f"{EX['id']}.json"))
    json.dump(EX, open(chemin, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print("ok" if not pb else f"{len(pb)} problème(s)", chemin)
    return pb
