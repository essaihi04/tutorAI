"""Méthode des blocs (règle du 11 novembre 2026, skill cours-concentration « Memory and rhythm » → « Data »).

Outil pour adapter un cours DÉJÀ construit sans toucher à ce qui est dit :

  python blocs.py base      <cours.json>
      photo des textes protégés (speech_text, paroles des réactions et démonstrations, questions et exercices
      existants) dans base/<deck>.json — à faire UNE fois, avant toute modification.
  python blocs.py apercu    <cours.json>
      plan du cours : diapositives, durée de voix, questions, exercices, cahier, compétences.
  python blocs.py appliquer <cours.json> <ajouts.json>
      ajoute au cours (relu juste avant d'écrire, rien d'autre ne change) :
        ajouts = {"seances": [...],                       → cours.seances
                  "rappels": {"C1": [...], ...},          → competences[].rappels
                  "predictions": ["slide_id", ...],       → question.prediction = true (retiré des autres)
                  "enonces": {"slide_id": "énoncé"}}      → question.prompt réécrit (jamais le texte dit)
  python blocs.py verifier  <cours.json> <chapitre>
      structure des séances/blocs, rappels, prédictions, paroles nouvelles (règles voix-du-cours), textes protégés
      inchangés depuis la photo, puis controler_cadre.py (« cadre : OK »).
  python blocs.py items     <cours.json> <items.json> [<demos.json>]
      réactions à écrire, même format que preparer_reponses.py items, pour les rappels QCM / vrai-faux et les
      exercices de blocs écrits pour l'occasion (un exercice repris d'une diapositive a déjà ses réactions) ;
      en option, la liste {id, parole} des nouvelles démonstrations à dire.
      Clés : slide = « rappel_<compétence> », qk = <id du rappel> ; slide = « bloc_<id du bloc> », qk = « ex » (QCM)
      ou « exs<j> » (affirmation j d'un vrai/faux). Le champ `cible` dit où poser la réaction.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
CONTROLE = r"outils/cours/voxtts/controler_cadre.py"


def charger(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def ecrire(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diapos(cours):
    for a in cours["activities"]:
        yield from a["slides"]


def h(o):
    return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def paroles(o, chemin=""):
    """Toutes les `parole` (réactions, démonstrations) sous o, avec leur chemin."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "parole" and isinstance(v, str):
                yield chemin, v
            else:
                yield from paroles(v, f"{chemin}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from paroles(v, f"{chemin}/{i}")


def protege(s):
    q = dict(s.get("question") or {})
    q.pop("prediction", None)
    q.pop("prompt", None)        # l'énoncé peut être réécrit pour une prédiction (jamais le texte dit)
    q.pop("reponses", None)
    q.pop("demonstration", None)
    q.pop("enonce_dit", None)    # énoncé lu, ajouté plus tard par la session principale (12 nov.)
    return {
        "speech_text": h(s.get("speech_text")),
        "paroles": {c: h(p) for c, p in paroles(s)},
        "question": h(q),
        "exercises": h([{k: v for k, v in e.items() if k not in ("demonstration", "enonce_dit")} for e in s.get("exercises") or []]),
    }


def base(cours_p):
    m = charger(cours_p)
    out = {"deck": m["stable_id"], "diapos": {s["id"]: protege(s) for s in diapos(m)},
           "enonces": {s["id"]: (s.get("question") or {}).get("prompt") for s in diapos(m)}}
    p = ICI / "base" / f"{m['stable_id']}.json"
    if p.exists():
        print("photo déjà prise :", p, "(on la garde)")
        return
    p.parent.mkdir(exist_ok=True)
    ecrire(p, out)
    print("photo :", p, len(out["diapos"]), "diapositives")


def apercu(cours_p):
    m = charger(cours_p)
    tot = 0
    for a in m["activities"]:
        print(f"## {a['id']} | {a['title']}")
        for s in a["slides"]:
            sec = duree(s)
            tot += sec
            q = s.get("question") or {}
            print(f"- {s['id']} [{','.join(s.get('competence_ids') or [])}] {sec:.0f}s | {s['title']} | {s.get('slide_type')}")
            if q:
                print(f"    Q({q.get('type')}{',PRED' if q.get('prediction') else ''}) {q.get('prompt', '')} | {q.get('options')} c={q.get('correct')}")
            for i, e in enumerate(s.get("exercises") or []):
                print(f"    E{i}({e.get('type')}) {json.dumps({k: v for k, v in e.items() if k not in ('type', 'demonstration')}, ensure_ascii=False)}")
            c = (s.get("concentration") or {}).get("cahier")
            if c:
                print(f"    CAHIER: {c}")
    print("VOIX TOTALE (min)", round(tot / 60, 1))
    for c in m.get("competences", []):
        print(" ", c["id"], c.get("cadre_ids"), c["label"], "|", c.get("slide_ids"), "| rappels:", len(c.get("rappels") or []))


def duree(s):
    au = ((s.get("audio") or {}).get("mixed") or {}).get("duration_ms")
    if au:
        return au / 1000
    return len((s.get("speech_text") or {}).get("mixed", "")) / 450 * 30


def appliquer(cours_p, ajouts_p):
    aj = charger(ajouts_p)
    m = charger(cours_p)          # relu juste avant d'écrire : d'autres sessions posent des pistes dans ce fichier
    ids = {s["id"] for s in diapos(m)}
    if "seances" in aj:
        m["seances"] = aj["seances"]
    for c in m.get("competences") or []:
        if c["id"] in aj.get("rappels", {}):
            c["rappels"] = aj["rappels"][c["id"]]
    inconnues = set(aj.get("rappels", {})) - {c["id"] for c in m.get("competences") or []}
    if inconnues:
        sys.exit(f"compétences inconnues : {inconnues}")
    if "predictions" in aj:
        pred = set(aj["predictions"])
        if pred - ids:
            sys.exit(f"diapositives inconnues : {pred - ids}")
        for s in diapos(m):
            q = s.get("question")
            if s["id"] in pred:
                if not q:
                    sys.exit(f"{s['id']} : pas de question pour une prédiction")
                q["prediction"] = True
            elif q and "prediction" in q:
                del q["prediction"]
    for sid, enonce in (aj.get("enonces") or {}).items():
        s = next(x for x in diapos(m) if x["id"] == sid)
        s["question"]["prompt"] = enonce
    ecrire(cours_p, m)
    print("appliqué :", len(m.get("seances") or []), "séances,",
          sum(len(c.get("rappels") or []) for c in m.get("competences") or []), "rappels,",
          sum(1 for s in diapos(m) if (s.get("question") or {}).get("prediction")), "prédictions")


ARABE = re.compile(r"[\u0600-\u06FF]")
TACHKIL = re.compile(r"[\u064B-\u0652\u0670]")
PERMIS = re.compile(r"[\w\s\u0600-\u06FF.,،:;?؟!'’«»\-]")


def controle_parole(t):
    pb = []
    if re.search(r"[0-9٠-٩]", t):
        pb.append("chiffre")
    if TACHKIL.search(t):
        pb.append("tachkil")
    autres = {c for c in t if not PERMIS.match(c)}
    if autres:
        pb.append("symbole " + "".join(sorted(autres)))
    for morceau in re.split(r"[.,،:;?؟!]", t):
        mots = morceau.split()
        if len(mots) > 10 and not ARABE.search(morceau):
            pb.append(f"phrase française de {len(mots)} mots sans virgule : « {morceau.strip()[:60]} »")
    return pb


def verifier(cours_p, chapitre):
    m = charger(cours_p)
    fautes, avis = [], []
    sl = list(diapos(m))
    ordre = [s["id"] for s in sl]
    par = {s["id"]: s for s in sl}
    comps = {c["id"]: c for c in m.get("competences") or []}

    # séances et blocs
    seances = m.get("seances") or []
    if not seances:
        fautes.append("pas de séances")
    vus, bids = [], set()
    for k, se in enumerate(seances):
        for champ in ("id", "titre", "blocs"):
            if not se.get(champ):
                fautes.append(f"séance {k} : {champ} manquant")
        nb = len(se.get("blocs") or [])
        if nb != 3:
            (avis if k == len(seances) - 1 and nb in (1, 2) else fautes).append(f"séance {se.get('id')} : {nb} bloc(s)")
        voix = 0
        for b in se.get("blocs") or []:
            bid = b.get("id")
            if bid in bids:
                fautes.append(f"bloc {bid} en double")
            bids.add(bid)
            ids = b.get("slide_ids") or []
            vus += ids
            if not 3 <= len(ids) <= 4:
                avis.append(f"bloc {bid} : {len(ids)} diapositive(s)")
            for x in ids:
                if x not in par:
                    fautes.append(f"bloc {bid} : diapositive inconnue {x}")
            voix += sum(duree(par[x]) for x in ids if x in par)
            if not b.get("titre"):
                fautes.append(f"bloc {bid} : titre manquant")
            cah = b.get("cahier") or []
            if not cah or not all(isinstance(c, dict) and c.get("texte", "").strip() for c in cah):
                fautes.append(f"bloc {bid} : cahier vide ou mal formé ([{{texte}}])")
            r = b.get("retrouver") or {}
            if not (r.get("prompt") and r.get("attendu") and r.get("competence_id")):
                fautes.append(f"bloc {bid} : retrouver incomplet")
            elif r["competence_id"] not in comps:
                fautes.append(f"bloc {bid} : retrouver.competence_id inconnu {r['competence_id']}")
            elif not any(r["competence_id"] in (par[x].get("competence_ids") or []) for x in ids if x in par):
                avis.append(f"bloc {bid} : la compétence du retrouver ({r['competence_id']}) n'est sur aucune diapositive du bloc")
            e = b.get("exercice") or {}
            fautes += [f"bloc {bid} : exercice — {x}" for x in controle_question(e, exercice=True)]
            if e.get("reprend"):
                sid, _, n = e["reprend"].partition("/e")
                src = (par.get(sid, {}).get("exercises") or [None] * 99)
                if sid not in ids or not n.isdigit() or int(n) >= len(src) or src[int(n)] is None:
                    fautes.append(f"bloc {bid} : exercice repris introuvable dans le bloc ({e['reprend']})")
            d = e.get("demonstration")
            if d and not e.get("reprend"):
                for x in controle_parole(d.get("parole", "")):
                    fautes.append(f"bloc {bid} : démonstration — {x}")
                for l in d.get("lignes") or []:
                    if l.get("mot") not in d.get("parole", ""):
                        fautes.append(f"bloc {bid} : démonstration — mot absent de la parole « {l.get('mot')} »")
            if e.get("type") == "libre" and "=" in str(e.get("attendu", "")) and not d:
                avis.append(f"bloc {bid} : exercice de calcul sans demonstration")
        print(f"  {se.get('id')} : {nb} blocs, voix {voix / 60:.1f} min — " +
              ", ".join(f"{b.get('id')}({len(b.get('slide_ids') or [])})" for b in se.get("blocs") or []))
    if vus != ordre:
        manquent = [x for x in ordre if x not in vus]
        doubles = sorted({x for x in vus if vus.count(x) > 1})
        fautes.append(f"blocs ≠ ordre du cours (manquent {manquent}, doubles {doubles})")
    if seances:
        der = {x for b in seances[-1].get("blocs") or [] for x in b.get("slide_ids") or []}
        for s in sl:
            fin = (s.get("concentration") or {}).get("acquis")  # seuls le bilan et la carte de fin (acquis: true) ; une carte d'aperçu reste à sa place
            if fin and s["id"] not in der:
                fautes.append(f"{s['id']} (bilan/carte) n'est pas dans la dernière séance")

    # rappels
    for c in comps.values():
        rs = c.get("rappels") or []
        if not 3 <= len(rs) <= 4:
            fautes.append(f"{c['id']} : {len(rs)} rappel(s)")
        if len({r.get("type") for r in rs}) < 2:
            fautes.append(f"{c['id']} : rappels d'une seule forme")
        for r in rs:
            if not r.get("id"):
                fautes.append(f"{c['id']} : rappel sans id")
            fautes += [f"{c['id']}/{r.get('id')} : {x}" for x in controle_question(r)]
    rids = [r.get("id") for c in comps.values() for r in c.get("rappels") or []]
    if len(rids) != len(set(rids)):
        fautes.append("ids de rappels en double")
    bonnes = [r["correct"] for c in comps.values() for r in c.get("rappels") or [] if r.get("type") == "qcm"]
    if bonnes and len(set(bonnes)) == 1:
        avis.append(f"tous les rappels QCM ont la bonne réponse en position {bonnes[0]}")

    # prédictions
    npred = sum(1 for s in sl if (s.get("question") or {}).get("prediction"))
    if npred * 3 < len(sl):
        fautes.append(f"prédictions : {npred} pour {len(sl)} diapositives (il en faut au moins {-(-len(sl) // 3)})")
    for a in m["activities"]:
        if not any((s.get("question") or {}).get("prediction") for s in a["slides"]) and \
                not any((s.get("concentration") or {}).get("acquis") or s.get("slide_type") == "synthesis" for s in a["slides"]):
            avis.append(f"partie {a['id']} : aucune prédiction")

    # textes protégés
    bp = ICI / "base" / f"{m['stable_id']}.json"
    if not bp.exists():
        fautes.append("pas de photo des textes protégés (blocs.py base)")
    else:
        b = charger(bp)
        for s in sl:
            avant, apres = b["diapos"].get(s["id"]), protege(s)
            if avant is None:
                fautes.append(f"{s['id']} : diapositive nouvelle")
                continue
            for k in ("speech_text", "question", "exercises"):
                if avant[k] != apres[k]:
                    fautes.append(f"{s['id']} : {k} modifié")
            for chemin, hp in avant["paroles"].items():
                if apres["paroles"].get(chemin) != hp:
                    fautes.append(f"{s['id']} : parole modifiée ou retirée {chemin}")
            if b["enonces"].get(s["id"]) != (s.get("question") or {}).get("prompt"):
                avis.append(f"{s['id']} : énoncé réécrit « {(s.get('question') or {}).get('prompt')} »")
        for x in set(b["diapos"]) - set(ordre):
            fautes.append(f"{x} : diapositive supprimée")

    print(f"  {len(seances)} séances, {len(bids)} blocs, {len(rids)} rappels, {npred} prédictions / {len(sl)} diapositives")
    for x in avis:
        print("AVIS  :", x)
    for x in fautes:
        print("FAUTE :", x)
    r = subprocess.run([sys.executable, CONTROLE, cours_p, chapitre], capture_output=True, text=True, encoding="utf-8")
    dern = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr
    for l in r.stdout.splitlines():
        if l.startswith("FAUTE"):
            print("CADRE", l)
    print(dern)
    ok = not fautes and r.returncode == 0
    print("blocs : OK" if ok else "blocs : à corriger")
    sys.exit(0 if ok else 1)


def controle_question(q, exercice=False):
    pb = []
    t = q.get("type")
    if t not in ("libre", "qcm", "vrai_faux"):
        return [f"type inconnu {t!r}"]
    if not (q.get("prompt") or "").strip():
        pb.append("prompt vide")
    if t == "libre" and not q.get("attendu"):
        pb.append("attendu manquant")
    if t == "qcm":
        o = q.get("options") or []
        if len(o) < 2:
            pb.append("moins de deux options")
        if not isinstance(q.get("correct"), int) or isinstance(q.get("correct"), bool) or not 0 <= q["correct"] < len(o):
            pb.append("correct invalide")
    if t == "vrai_faux":
        if exercice and "statements" in q:
            for st in q["statements"]:
                if not isinstance(st.get("correct"), bool) or not st.get("text"):
                    pb.append("affirmation mal formée")
        elif not isinstance(q.get("correct"), bool):
            pb.append("correct (true/false) manquant")
    return pb


def bloc_parle(m, b):
    par = {s["id"]: s for s in diapos(m)}
    return " ".join((par[x].get("speech_text") or {}).get("mixed", "") for x in b["slide_ids"] if x in par)[:2500]


def items(cours_p, sortie_p, demos_p=None):
    m, out, demos = charger(cours_p), [], []

    def ajoute(slide, titre, parle, cle, genre, enonce, choix, bonne, cible):
        for o, c in enumerate(choix):
            for t in ([1] if o == bonne else [1, 2]):
                out.append({"slide": slide, "qk": cle, "o": o, "t": t, "verdict": o == bonne,
                            "diapo": {"title": titre, "speech": parle},
                            "question": {"type": genre, "enonce": enonce, "choix": choix, "bonne": bonne},
                            "reponse": c, "cible": cible})

    par = {s["id"]: s for s in diapos(m)}
    for c in m.get("competences") or []:
        contexte = " ".join(str((par[x].get("concentration") or {}).get("cahier") or "") for x in c.get("slide_ids") or [] if x in par)
        for r in c.get("rappels") or []:
            cible = {"type": "rappel", "competence": c["id"], "rappel": r["id"]}
            if r["type"] == "qcm":
                ajoute(f"rappel_{c['id']}", c["label"], contexte, r["id"], "qcm", r["prompt"], r["options"], r["correct"], cible)
            elif r["type"] == "vrai_faux":
                ajoute(f"rappel_{c['id']}", c["label"], contexte, r["id"], "vrai_faux", "Vrai ou faux ? " + r["prompt"],
                       ["Vrai", "Faux"], 0 if r["correct"] else 1, cible)
    for se in m.get("seances") or []:
        for b in se["blocs"]:
            e = b.get("exercice") or {}
            if e.get("reprend"):
                continue
            cible = {"type": "bloc", "seance": se["id"], "bloc": b["id"]}
            if e.get("type") == "qcm":
                ajoute(f"bloc_{b['id']}", b["titre"], bloc_parle(m, b), "ex", "qcm", e["prompt"], e["options"], e["correct"], cible)
            elif e.get("type") == "vrai_faux":
                for j, st in enumerate(e.get("statements") or [{"text": e["prompt"], "correct": e["correct"]}]):
                    ajoute(f"bloc_{b['id']}", b["titre"], bloc_parle(m, b), f"exs{j}", "vrai_faux", "Vrai ou faux ? " + st["text"],
                           ["Vrai", "Faux"], 0 if st["correct"] else 1, cible)
            if e.get("demonstration"):
                demos.append({"id": f"bloc_{b['id']}__demo_ex", "parole": e["demonstration"]["parole"], "cible": cible})
    ecrire(sortie_p, out)
    print(len(out), "réactions à écrire (rappels QCM/vrai-faux et exercices de blocs)")
    if demos_p:
        ecrire(demos_p, demos)
        print(len(demos), "démonstrations nouvelles à dire")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"base": base, "apercu": apercu, "appliquer": appliquer, "verifier": verifier, "items": items}[sys.argv[1]](*sys.argv[2:])
