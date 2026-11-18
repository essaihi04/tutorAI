"""(skill logique-de-cours) Outils communs pour refaire la logique d'un cours (en attente)."""
import copy, json


def charger(p):
    return json.load(open(p, encoding="utf-8"))


def diapos(m):
    return {s["id"]: s for a in m["activities"] for s in a["slides"]}


def verifier_mots(s):
    t = s["speech_text"]["mixed"]
    c = s.get("concentration") or {}
    for p in c.get("pointage") or []:
        assert p["mot"] in t, (s["id"], "pointage", p["mot"])
    for p in c.get("centre") or []:
        assert p["mot"] in t, (s["id"], "centre", p["mot"])
    o = c.get("observation")
    if o:
        assert t.count(o["apres_mot"]) == 1, (s["id"], "apres_mot", o["apres_mot"], t.count(o["apres_mot"]))
    d = (s.get("question") or {}).get("demonstration")
    if d:
        for l in d.get("lignes") or []:
            assert l["mot"] in d["parole"], (s["id"], "demo", l["mot"])


def observation(apres_mot, enonce, enonce_dit, indices, choix, bonne, retours, solution, gestes=None, silence_s=10,
                sim_avant=None, sim_apres=None):
    o = {"apres_mot": apres_mot}
    if sim_avant:
        o["sim_avant"] = sim_avant
    if sim_apres:
        o["sim_apres"] = sim_apres
    o["gestes"] = gestes or []
    o.update({"enonce": enonce, "enonce_dit": enonce_dit, "silence_s": silence_s,
              "indices": [dict(texte=t, dit=d, **({"repere": r} if r else {})) for t, d, r in indices],
              "choix": choix, "bonne": bonne,
              "retours": [{"parole": p, "ecrit": e} for e, p in retours],
              "solution": {"parole": solution[1], "ecrit": solution[0]}})
    assert len(o["retours"]) == len(choix)
    return o


def reactions(correct, n, rep):
    """rep = {i: ((ecrit1, parole1), (ecrit2, parole2))} pour les fausses ; rep[correct] = (ecrit, parole)."""
    out = {}
    for i in range(n):
        if i == correct:
            e, p = rep[i]
            out[str(i)] = {"juste": {"parole": p, "ecrit": e}}
        else:
            (e1, p1), (e2, p2) = rep[i]
            out[str(i)] = {"1": {"parole": p1, "ecrit": e1}, "2": {"parole": p2, "ecrit": e2}}
    return out


def reecrire(s, fr=None, mixed=None, pointage=None, **champs):
    """Texte changé : la voix est perdue (audio retiré), le reste est gardé."""
    if fr is not None:
        s["speech_text"]["fr"] = fr
    if mixed is not None:
        s["speech_text"]["mixed"] = mixed
        s.pop("audio", None)
    if pointage is not None:
        s["concentration"]["pointage"] = pointage
    for k, v in champs.items():
        s[k] = v
    return s


def nouvelle(base, id_, title, **champs):
    s = copy.deepcopy(base)
    s["id"] = id_
    s["title"] = title
    s.pop("audio", None)
    s.pop("question", None)
    s.pop("exercises", None)
    s.pop("exercices_fin_de_cours", None)
    s.pop("reponses_fin_de_cours", None)
    c = s["concentration"]
    for k in ("observation", "variante", "reponses", "centre", "cahier_figures", "legende"):
        c.pop(k, None)
    c["reponses"] = {}
    for k, v in champs.items():
        s[k] = v
    return s


def recouper(m, plan_parties, plan_seances, D=None):
    """plan_parties = [(id_activite, titre|None, duree|None, [ids])] ; plan_seances = [(id, titre, [(id_bloc, titre, [ids])])]."""
    D = D or diapos(m)
    acts = {a["id"]: a for a in m["activities"]}
    vus = []
    nouvelles = []
    for aid, titre, duree, ids in plan_parties:
        a = acts[aid]
        if titre:
            a["title"] = titre
        if duree:
            a["duration_minutes"] = duree
        a["slides"] = [D[i] for i in ids]
        vus += ids
        nouvelles.append(a)
    assert len(vus) == len(set(vus)) == len(D), (len(vus), len(set(vus)), len(D), set(D) - set(vus))
    m["activities"] = nouvelles
    m["estimated_minutes"] = sum(a["duration_minutes"] for a in nouvelles)
    # blocs : on reprend « retrouver » et « exercice » du bloc ancien qui partage le plus de diapositives
    anciens = [b for se in m["seances"] for b in se["blocs"]]
    seances = []
    ordre = []
    for sid, stitre, blocs in plan_seances:
        bl = []
        for bid, btitre, ids in blocs:
            ordre += ids
            src = max(anciens, key=lambda b: len(set(b["slide_ids"]) & set(ids)))
            b = {"id": bid, "titre": btitre, "slide_ids": ids}
            cahier, figs = [], []
            for i in ids:
                c = D[i].get("concentration") or {}
                if c.get("cahier") and {"texte": c["cahier"]} not in cahier:
                    cahier.append({"texte": c["cahier"]})
                figs += c.get("cahier_figures") or []
            b["cahier"] = cahier
            if figs:
                b["cahier_figures"] = figs[:2]
            for k in ("retrouver", "exercice"):
                if src.get(k):
                    b[k] = copy.deepcopy(src[k])
            bl.append(b)
        seances.append({"id": sid, "titre": stitre, "blocs": bl})
    assert ordre == vus, "les blocs doivent suivre l'ordre du cours"
    m["seances"] = seances
    # compétences : slide_ids recalculés à partir des competence_ids des diapositives, dans l'ordre du cours
    for c in m["competences"]:
        c["slide_ids"] = [i for i in vus if c["id"] in (D[i].get("competence_ids") or [])]
    for i in vus:
        verifier_mots(D[i])
