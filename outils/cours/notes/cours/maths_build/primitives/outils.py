SIM = "/media/simulations/maths/"   # vis("limites-continuite-tableau/traversee.html?vue=une", caption, alt)
ERREURS = []

def vis(page, caption, alt):
    return {"kind": "simulation", "url": SIM + page, "caption": caption, "alt": alt}

def PU(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}

def R(mot, repere):
    return {"mot": mot, "repere": repere}

def C(mot, cible):
    return {"mot": mot, "cible": cible}

def Q(prompt, options, correct, demo=None, typ="qcm"):
    q = {"type": typ, "prompt": prompt, "options": options, "timeout_seconds": 30, "correct": correct}
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
    # contrôle des mots
    mots = [p["mot"] for p in conc["pointage"]] + [c["mot"] for c in conc.get("centre", [])]
    for m in mots:
        if m not in mixed:
            ERREURS.append(f"{id}: mot absent « {m} »")
    for obj in [question] + list(exercises or []):
        if obj and obj.get("demonstration"):
            d = obj["demonstration"]
            for l in d["lignes"]:
                if l["mot"] not in d["parole"]:
                    ERREURS.append(f"{id}: mot de démonstration absent « {l['mot']} »")
    return s

# --- Cours Fonctions primitives : calculs écrits à la main (primitives-tableau/calculs.html?vue=<id>, données écrites par build.py dans calculs-vues.js) ---
DOSSIER = "primitives-tableau/"
CALCULS = {}

def L(t, c=None, m=None, **kw):
    """Une ligne de calculs.html : texte, couleur, moment ; kw : cadre (couleur), r=(repère, libellé), barre, x, dx, meme, taille, inter, p."""
    d = {"t": t}
    if c: d["c"] = c
    if m: d["m"] = m
    d.update(kw)
    return d

def CALC(vue, titre, lignes, caption, alt, **kw):
    """Déclare une vue de calculs.html et renvoie le visuel de la diapositive."""
    assert vue not in CALCULS, vue
    d = {"titre": titre, "lignes": lignes}; d.update(kw)
    CALCULS[vue] = d
    return vis(DOSSIER + "calculs.html?vue=" + vue, caption, alt)

def V(page, caption, alt):
    return vis(DOSSIER + page, caption, alt)

def D(*paires):
    """Démonstration : [(ligne écrite, phrase dite)] ; le mot = les premiers mots de la phrase (3 à 7, unique)."""
    parole = " ".join(p for _, p in paires)
    lignes, vus = [], set()
    for t, p in paires:
        mots = p.split()
        for k in range(3, 9):
            m = " ".join(mots[:k])
            if m not in vus and parole.count(m) == 1:
                break
        vus.add(m)
        lignes.append((t, m))
    return DEMO(parole, lignes)
