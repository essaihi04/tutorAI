"""Réactions PRÉPARÉES du tuteur pour chaque réponse possible des questions d'un cours (skill `cours-concentration`).

  python preparer_reponses.py items  <cours.json> <items.json>
      liste ce qu'il faut écrire : pour chaque question à clé (slide.question.correct, exercices QCM, chaque
      affirmation de vrai/faux) et chaque option : `juste` (bonne option) ou essai 1 (indice) et 2 (réponse).
  (sur le VPS) gen_reponses_vps.py <items.json> <sortie.json>   → DeepSeek écrit chaque réaction
  python preparer_reponses.py poser  <cours.json> <sortie.json> <pistes.json>
      écrit `concentration.reponses[cle][option][juste|1|2] = {parole, ecrit}` et la liste des pistes à dire.
  python gen_kaggle_cours_exemple.py reponses=<pistes.json>   → la voix de chaque réaction (Kaggle, depuis le VPS)
  python preparer_reponses.py audio  <cours.json> <dossier sortie Kaggle> <version>
      copie chaque <id>.wav dans /media/audio/courses/<deck>/reponses/ et pose son url (`audio`), si le texte
      dit est toujours le même (hash) ; rien n'est posé pour une piste qui murmure (detecter_murmures.py).
  python preparer_reponses.py verifier <cours.json>
      le cours est-il prêt pour le mode concentration ? mots des repères présents dans le texte dit, piste de
      chaque diapositive, clé de chaque question, réaction et voix pour chaque réponse possible.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

PUBLIC = Path(r"frontend/public")


def charger(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def ecrire(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diapos(cours):
    for a in cours["activities"]:
        yield from a["slides"]


def rid(slide_id, cle, o, quoi):
    return f"{slide_id}__{cle}_{o}_{quoi}"


def items(cours_p, sortie_p):
    m, out = charger(cours_p), []

    def ajoute(s, cle, genre, enonce, choix, bonne):
        for o, c in enumerate(choix):
            for t in ([1] if o == bonne else [1, 2]):
                out.append({"slide": s["id"], "qk": cle, "o": o, "t": t, "verdict": o == bonne,
                            "diapo": {"title": s["title"], "speech": (s.get("speech_text") or {}).get("mixed", "")},
                            "question": {"type": genre, "enonce": enonce, "choix": choix, "bonne": bonne}, "reponse": c})

    sans_cle = []
    for s in diapos(m):
        q = s.get("question")
        if q and len(q.get("options") or []) >= 2:
            if "correct" in q:
                ajoute(s, "q", "qcm", q["prompt"], q["options"], q["correct"])
            else:
                sans_cle.append(s["id"])
        for i, e in enumerate(s.get("exercises") or []):
            if e["type"] == "qcm":
                ajoute(s, f"e{i}", "qcm", e["prompt"], e["choices"], e.get("correct", 0))
            if e["type"] == "vrai_faux":
                for j, st in enumerate(e.get("statements") or []):
                    ajoute(s, f"e{i}s{j}", "vrai_faux", "Vrai ou faux ? " + st["text"], ["Vrai", "Faux"], 0 if st["correct"] else 1)
    ecrire(sortie_p, out)
    print(len(out), "réactions à écrire")
    if sans_cle:
        print("QUESTIONS SANS CLÉ (poser question.correct d'abord) :", sans_cle)


def poser(cours_p, llm_p, pistes_p):
    m, faits = charger(cours_p), charger(llm_p)
    par = {s["id"]: s for s in diapos(m)}
    pistes, manque = [], 0
    for i in faits:
        if "reaction" not in i:
            manque += 1
            continue
        quoi = "juste" if i["verdict"] else str(i["t"])
        r = {"parole": i["reaction"]["parole"], "ecrit": i["reaction"]["ecrit"]}
        par[i["slide"]].setdefault("concentration", {}).setdefault("reponses", {}).setdefault(i["qk"], {}) \
            .setdefault(str(i["o"]), {})[quoi] = r
        pistes.append({"id": rid(i["slide"], i["qk"], i["o"], quoi), "parole": r["parole"]})
    ecrire(cours_p, m)
    ecrire(pistes_p, pistes)
    print(len(pistes), "réactions posées ;", manque, "manquantes")


def audio(cours_p, sortie_dir, version):
    m = charger(cours_p)
    produits = {r["id"]: r for r in json.loads(next(Path(sortie_dir).rglob("cours.json")).read_text(encoding="utf-8"))}
    deck = m["stable_id"]
    dest = PUBLIC / "media/audio/courses" / deck / "reponses"
    dest.mkdir(parents=True, exist_ok=True)
    poses, manquants = 0, []
    for s in diapos(m):
        for cle, options in ((s.get("concentration") or {}).get("reponses") or {}).items():
            for o, quoi_r in options.items():
                for quoi, r in quoi_r.items():
                    ident = rid(s["id"], cle, o, quoi)
                    h = hashlib.sha256(r["parole"].strip().encode("utf-8")).hexdigest()
                    wav = next(Path(sortie_dir).rglob(f"{ident}.wav"), None)
                    if not wav or produits.get(ident, {}).get("hash") != h:
                        manquants.append(ident)
                        continue
                    cible = dest / f"{ident}_v{version}.wav"
                    shutil.copyfile(wav, cible)
                    r["audio"] = f"/media/audio/courses/{deck}/reponses/{cible.name}"
                    poses += 1
    ecrire(cours_p, m)
    print(poses, "pistes posées ; manquantes :", manquants)


def verifier(cours_p):
    m, pb = charger(cours_p), []
    for s in diapos(m):
        sid, dit = s["id"], (s.get("speech_text") or {}).get("mixed", "")
        c = s.get("concentration") or {}
        piste = ((s.get("audio") or {}).get("mixed") or {}).get("url")
        if not piste or not (PUBLIC / piste.lstrip("/")).exists():
            pb.append(f"{sid} : pas de piste audio")
        if not c:
            pb.append(f"{sid} : pas de données concentration")
        for x in (c.get("pointage") or []) + (c.get("centre") or []):
            if x["mot"] not in dit:
                pb.append(f"{sid} : mot absent du texte dit « {x['mot']} »")
        q = s.get("question")
        if q and len(q.get("options") or []) >= 2 and "correct" not in q:
            pb.append(f"{sid} : question sans clé (question.correct)")
        attendues = []
        if q and "correct" in q:
            attendues.append(("q", len(q["options"]), q["correct"]))
        for i, e in enumerate(s.get("exercises") or []):
            if e["type"] == "qcm":
                attendues.append((f"e{i}", len(e["choices"]), e.get("correct", 0)))
            for j, st in enumerate(e.get("statements") or []) if e["type"] == "vrai_faux" else []:
                attendues.append((f"e{i}s{j}", 2, 0 if st["correct"] else 1))
        for cle, n, bonne in attendues:
            for o in range(n):
                for quoi in (["juste"] if o == bonne else ["1", "2"]):
                    r = (((c.get("reponses") or {}).get(cle) or {}).get(str(o)) or {}).get(quoi)
                    if not r:
                        pb.append(f"{sid} : réaction manquante {cle}/{o}/{quoi}")
                    elif not r.get("audio") or not (PUBLIC / r["audio"].lstrip("/")).exists():
                        pb.append(f"{sid} : voix manquante {cle}/{o}/{quoi}")
    print("\n".join(pb) if pb else "cours prêt pour le mode concentration")
    sys.exit(1 if pb else 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"items": items, "poser": poser, "audio": audio, "verifier": verifier}[sys.argv[1]](*sys.argv[2:])
