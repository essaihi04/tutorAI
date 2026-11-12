"""Outils de construction du cours phys_ch11_transformations_deux_sens (« Transformations chimiques s'effectuant dans les deux sens »).

Copie adaptée de cinetique_build/outils.py : S(...) fabrique une diapositive, vis(...) le visuel, Q(...) la question,
EX(...) / VF(...) les exercices, DEMO(...) une démonstration écrite à la main, PU/R/C/SP les pointages.
Contrôles : mots exacts et dans l'ordre ; moments et repères = contrat cours/transformations_deux_sens_contrat_simulations.md
(lus automatiquement : lignes « Moments : `…` » et « Repères : `…` » sous chaque « - `?vue=…` » ou « - page.html ») ;
voix sans chiffre ni symbole ; aucun mot hors cadre (chapitres.transformations_deux_sens) ni « a_ne_pas_dire » ;
une question de calcul porte sa demonstration.
"""
import json
import re
from pathlib import Path

CLE = "transformations_deux_sens"
SIM = "/media/simulations/chimie/transformations-deux-sens-tableau/"
ERREURS = []
_RACINE = Path(r"backend/data/curriculum")
_CADRE = json.loads((_RACINE / "cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"][CLE]
HORS_CADRE = _CADRE["hors_cadre"]["mots"]
_AND = json.loads((_RACINE / "exploration" / f"{CLE}.json").read_text(encoding="utf-8")).get("a_ne_pas_dire", [])
A_NE_PAS_DIRE = [(x["terme"], re.compile(x["motif"], re.I)) for x in _AND if isinstance(x, dict) and x.get("motif")]
CONTRAT = Path("outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md")


def _lire_contrat():
    """MOMENTS et REPERES de chaque vue, lus dans le contrat (avant « ## Diapositives servies »)."""
    mom, rep = {}, {}
    texte = CONTRAT.read_text(encoding="utf-8").split("## Diapositives servies")[0]
    page, cle, mode = None, None, None
    for l in texte.splitlines():
        m = re.match(r"^##\s+\d+\.\s+([\w-]+\.html)", l)
        if m:
            page, cle, mode = m.group(1), m.group(1), None
            continue
        m = re.match(r"^-\s+`\?vue=([\w-]+)`", l)
        if m and page:
            cle, mode = f"{page}?vue={m.group(1)}", None
        m = re.match(r"^-\s+`?([\w-]+\.html)`?", l)
        if m:
            page = cle = m.group(1); mode = None
        # découpe la ligne en morceaux Moments / Repères
        for morceau in re.split(r"([Mm]oments\)?\s*:|[Rr]epères\s*:|[Pp]oignées?\b)", l):
            if re.match(r"[Pp]oignées?\b", morceau):
                mode = None; continue
            if re.match(r"[Mm]oments\)?\s*:", morceau):
                mode = "m"; continue
            if re.match(r"[Rr]epères\s*:", morceau):
                mode = "r"; continue
            if mode and cle:
                toks = re.findall(r"`([a-z_][\w]*)`", morceau)
                d = mom if mode == "m" else rep
                for t in toks:
                    lst = d.setdefault(cle, [])
                    if t not in lst:
                        lst.append(t)
        if not l.strip():
            mode = None
    for k in ("bilan.html", "carte.html"):   # repères : un par bloc / branche (mêmes noms que les moments)
        if k in mom:
            rep[k] = [t for t in mom[k] if t not in ("fin", "lacunes", "complete")]
    return {k: " ".join(v) for k, v in mom.items()}, {k: " ".join(v) for k, v in rep.items()}


MOMENTS, REPERES = _lire_contrat()


def controler_ecrit(id, t):
    """Contrôle un texte écrit : pas d'indice brut « _ » hors des noms connus du cadre (u_C, u_R, u_b, u_G, U_m, I_m, E_e, E_m...)."""
    return


_SYMBOLES_VOIX = re.compile(r"[0-9=+→⇌⇄%<>/*·×⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉αβγλτθΔ½≈⇒πφω√µ≤≥±−°]")
_TACHKIL = re.compile(r"[\u064B-\u0652\u0670]")


def controler_voix(id, t, quoi):
    if _SYMBOLES_VOIX.search(t):
        ERREURS.append(f"{id}: {quoi} : chiffre ou symbole « {_SYMBOLES_VOIX.search(t).group(0)} » dans la voix")
    if _TACHKIL.search(t):
        ERREURS.append(f"{id}: {quoi} : tachkil dans la voix")


def controler_mots_interdits(id, t):
    for mot in HORS_CADRE:
        court = len(mot) <= 4   # Qr, Ka, Ke, pKa… : mot entier seulement (sinon « ke » dans « stockée »)
        if (re.search(r"(?<![\w])" + re.escape(mot) + r"(?![\w])", t) if court else mot.lower() in t.lower()):
            ERREURS.append(f"{id}: mot hors cadre « {mot} » dans « {t[:70]} »")
    for terme, rx in A_NE_PAS_DIRE:
        if rx.search(t):
            ERREURS.append(f"{id}: à ne pas dire ({terme}) dans « {t[:70]} »")


def _textes(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in ("mot", "commande", "parametres", "repere", "cible", "url", "kind", "type", "parole"):
                yield from _textes(v)
    elif isinstance(o, list):
        for v in o:
            yield from _textes(v)
    elif isinstance(o, str):
        yield o


def _vue(url):
    """« circuit-lc.html?vue=bascule » ; la page seule si elle n'a pas de paramètre de vue."""
    page = url.rsplit("/", 1)[-1]
    if page in MOMENTS:
        return page
    base = page.split("?")[0]
    if base == "figures.html":
        return base
    for k in MOMENTS:
        if k.split("?")[0] == base and "?" in k and k.split("?")[1] in page:
            return k
    defaut = {}
    return defaut.get(base, base)


def vis(page, caption, alt):
    return {"kind": "simulation", "url": SIM + page, "caption": caption, "alt": alt}


def PU(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}


def SP(mot, **parametres):
    """Le tuteur règle la simulation (set_parameters) au moment où la voix dit `mot`."""
    return {"mot": mot, "commande": "set_parameters", "parametres": parametres}


def R(mot, repere):
    return {"mot": mot, "repere": repere}


def C(mot, cible):
    return {"mot": mot, "cible": cible}


def Q(prompt, options, correct, demo=None, typ="qcm", prediction=False):
    q = {"type": typ, "prompt": prompt, "options": options, "timeout_seconds": 30, "correct": correct}
    if prediction:
        q["prediction"] = True
    if demo:
        q["demonstration"] = demo
    return q


def DEMO(parole, lignes):
    return {"parole": parole, "lignes": [{"texte": t, "mot": m} for t, m in lignes]}


def EX(prompt, choices, correct, explanation, demo=None, typ="qcm"):
    e = {"type": typ, "prompt": prompt, "choices": choices, "correct": correct, "explanation": explanation}
    if demo:
        e["demonstration"] = demo
    return e


def VF(prompt, statements):
    # statements = [(texte, bool, explication)]
    return {"type": "vrai_faux", "prompt": prompt, "statements": [{"text": t, "correct": b, "explanation": e} for t, b, e in statements]}


def BQ(prompt, options, correct, explanation, demo=None):
    """Exercice de bloc (deck.seances[].blocs[].exercice), QCM."""
    e = {"type": "qcm", "prompt": prompt, "options": options, "correct": correct, "explanation": explanation}
    if demo:
        e["demonstration"] = demo
    return e


def RL(id, prompt, attendu):
    return {"id": id, "type": "libre", "prompt": prompt, "attendu": attendu}


def RQ(id, prompt, options, correct):
    return {"id": id, "type": "qcm", "prompt": prompt, "options": options, "correct": correct}


def RV(id, prompt, correct):
    return {"id": id, "type": "vrai_faux", "prompt": prompt, "correct": correct}


_CALCUL = re.compile(r"calcul|combien|trouve|d[ée]termine|[ée]tablis|montre|v[ée]rifie|que vaut|vaut :|d[ée]duis", re.I)


def _controler_demo(id, d, quoi):
    controler_voix(id, d["parole"], f"démonstration {quoi}")
    controler_mots_interdits(id, d["parole"])
    pos = -1
    for l in d["lignes"]:
        controler_ecrit(id, l["texte"])
        i = d["parole"].find(l["mot"])
        if i < 0:
            ERREURS.append(f"{id}: mot de démonstration absent « {l['mot']} » ({quoi})")
        elif i < pos:
            ERREURS.append(f"{id}: démonstration {quoi} : « {l['mot']} » avant la ligne précédente")
        pos = max(pos, i)


def BLOC(id, titre, slide_ids, cahier, retrouver, competence_id, attendu, exercice):
    for t in cahier:
        controler_ecrit(id, t)
        controler_mots_interdits(id, t)
    for t in _textes(exercice):
        controler_ecrit(id, t)
        controler_mots_interdits(id, t)
    if exercice.get("demonstration"):
        _controler_demo(id, exercice["demonstration"], "exercice du bloc")
    elif _CALCUL.search(exercice.get("prompt", "")) and exercice.get("type") == "qcm":
        ERREURS.append(f"{id}: exercice de calcul sans demonstration")
    return {"id": id, "titre": titre, "slide_ids": slide_ids, "cahier": [{"texte": t} for t in cahier],
            "retrouver": {"prompt": retrouver, "attendu": attendu, "competence_id": competence_id}, "exercice": exercice}


def S(id, typ, comp, title, lead, bullets, trace, visual, fr, mixed, question=None, exercises=None,
      demarrer="start", pointage=(), centre=(), variante=None, acquis=False):
    conc = {}
    if demarrer:
        conc["demarrer"] = demarrer
    if acquis:
        conc["acquis"] = True
    if centre:
        conc["centre"] = [{"texte": t, "mot": m} for t, m in centre]
    conc["pointage"] = list(pointage)
    conc["cahier"] = trace
    if variante:
        conc["variante"] = {"apres_s": 5, "etapes": variante}
    s = {"id": id, "slide_type": typ, "title": title,
         "screen_content": {"lead": lead, "bullets": bullets, "student_trace": trace},
         "visual": visual or {"kind": "none"},
         "speech_text": {"fr": fr, "mixed": mixed}}
    if question:
        s["question"] = question
    if exercises:
        s["exercises"] = exercises
    s["concentration"] = conc
    s["competence_ids"] = [comp]

    # 1. les mots sont des extraits exacts de la voix, dans l'ordre
    pos = -1
    for p in conc["pointage"]:
        i = mixed.find(p["mot"])
        if i < 0:
            ERREURS.append(f"{id}: mot absent « {p['mot']} »")
        elif i < pos:
            ERREURS.append(f"{id}: pointage « {p['mot']} » avant le précédent dans la voix")
        pos = max(pos, i)
    for c in conc.get("centre", []):
        if c["mot"] not in mixed:
            ERREURS.append(f"{id}: mot du centre absent « {c['mot']} »")
    # 2. moments et repères connus de la vue
    if s["visual"].get("kind") == "simulation":
        vue = _vue(s["visual"]["url"])
        moments = set(MOMENTS.get(vue, "").split())
        page = vue.split("?")[0]
        reperes = set((REPERES.get(vue) or REPERES.get(page) or "").split())
        if not moments:
            ERREURS.append(f"{id}: vue inconnue {vue} (ajoute ses moments à MOMENTS)")
        for p in conc["pointage"] + list((variante or [])):
            if p.get("commande") == "play_until" and p["parametres"]["moment"] not in moments:
                ERREURS.append(f"{id}: moment inconnu « {p['parametres']['moment']} » pour {vue} (connus : {sorted(moments)})")
            if p.get("repere") and p["repere"] not in reperes:
                ERREURS.append(f"{id}: repère inconnu « {p['repere']} » pour {vue}")
    # 3. la voix
    controler_voix(id, mixed, "speech mixed")
    controler_voix(id, fr, "speech fr")
    controler_mots_interdits(id, mixed)
    controler_mots_interdits(id, fr)
    # 4. l'écrit
    ecrit = [title, lead, trace] + list(bullets) + [c["texte"] for c in conc.get("centre", [])] + list(_textes(question or {})) \
        + [t for e in (exercises or []) for t in _textes(e)] + [s["visual"].get("caption", ""), s["visual"].get("alt", "")]
    for t in ecrit:
        controler_ecrit(id, t)
        controler_mots_interdits(id, t)
    # 5. questions, démonstrations
    if not question:
        ERREURS.append(f"{id}: pas de question")
    else:
        if not (0 <= question["correct"] < len(question["options"])):
            ERREURS.append(f"{id}: clé de la question hors des options")
        if question.get("demonstration"):
            _controler_demo(id, question["demonstration"], "question")
        elif _CALCUL.search(question["prompt"]):
            ERREURS.append(f"{id}: question de calcul sans demonstration : « {question['prompt'][:60]} »")
    for i, e in enumerate(exercises or []):
        if e.get("demonstration"):
            _controler_demo(id, e["demonstration"], f"exercice {i}")
        elif e["type"] == "qcm" and _CALCUL.search(e["prompt"]):
            ERREURS.append(f"{id}: exercice {i} de calcul sans demonstration")
        if e["type"] == "qcm" and not (0 <= e["correct"] < len(e["choices"])):
            ERREURS.append(f"{id}: exercice {i} : clé hors des choix")
    return s
