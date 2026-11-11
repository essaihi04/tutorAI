SIM = "/media/simulations/physics/energie-nucleaire-tableau/"
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
