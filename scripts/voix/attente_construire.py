"""Voix manquantes des cours en attente (14 novembre 2026).
Pour chaque backend/data/courses/en_attente/<deck>.json : les pistes sans voix (diapos sans audio.mixed, énoncés sans
enonce_audio, réactions et démonstrations sans audio, champs des questions d'observation sans audio), en excluant
celles que le dossier du cours en ligne sur le VPS produit déjà (même id, même texte).
Sortie : attente/att_<deck>/{cours.json, pistes.json, demonstrations.json} + carte.json (où poser chaque piste)."""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pistes_cours import pistes

AT = Path(__file__).resolve().parents[2]
S = Path(__import__("tempfile").gettempdir()) / "moalim-voix-attente"   # sorties hors du dépôt
S.mkdir(exist_ok=True)
H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
live_hash = json.load(open(S / "live_hash.json", encoding="utf-8"))   # {deck: {d/id: hash}} des dossiers du VPS


def obs_pistes(m):
    for a in m.get("activities") or []:
        for s in a["slides"]:
            o = (s.get("concentration") or {}).get("observation")
            if not o:
                continue
            base = f"enonce_obs_{s['id']}"
            if (o.get("enonce_dit") or o.get("enonce")) and not o.get("enonce_audio"):
                yield ("reponses", f"{base}_q", (o.get("enonce_dit") or o["enonce"]).strip(), (s["id"], "enonce"))
            for i, x in enumerate(o.get("indices") or []):
                t = (x.get("dit") or x.get("texte") or "").strip()
                if t and not x.get("audio"):
                    yield ("reponses", f"{base}_i{i}", t, (s["id"], f"indices.{i}"))
            for i, x in enumerate(o.get("retours") or []):
                t = (x.get("parole") or "").strip()
                if t and not x.get("audio"):
                    yield ("reponses", f"{base}_r{i}", t, (s["id"], f"retours.{i}"))
            so = o.get("solution") or {}
            if (so.get("parole") or "").strip() and not so.get("audio"):
                yield ("reponses", f"{base}_s", so["parole"].strip(), (s["id"], "solution"))


def manque(d, poser_obj_check):
    return poser_obj_check


total = 0
carte = {}
for p in sorted((AT / "backend/data/courses/en_attente").glob("*.json")):
    deck = p.stem
    m = json.loads(p.read_text(encoding="utf-8"))
    vus = {**live_hash.get("_observations", {}), **live_hash.get(deck, {})}
    diapos = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    travaux = []
    # diapos, réactions, démonstrations, énoncés : on pose sur une copie pour savoir si le champ est déjà rempli
    for d, i, t, poser in pistes(m):
        # déjà une voix ? on regarde le champ visé en le posant sur un objet témoin
        temoin = {}
        if d == "mixed":
            a = (diapos[i].get("audio") or {}).get("mixed") or {}
            deja = bool(a.get("url")) and a.get("speech_hash") == H(t)
        else:
            # le poseur écrit obj["audio"] ou obj["enonce_audio"] : on retrouve l'objet par la fermeture
            cellules = poser.__closure__ or ()
            obj = next((c.cell_contents for c in cellules if isinstance(c.cell_contents, dict)), {})
            deja = bool(obj.get("enonce_audio" if i.startswith("enonce_") else "audio"))
        if deja:
            continue
        if vus.get(f"{d}/{i}") == H(t):
            continue          # le dossier du cours en ligne la produit déjà, avec le même texte
        travaux.append((d, i, t))
    for d, i, t, ou in obs_pistes(m):
        if vus.get(f"{d}/{i}") == H(t):
            continue
        travaux.append((d, i, t))
        carte.setdefault(deck, []).append({"id": i, "diapo": ou[0], "champ": ou[1]})
    if not travaux:
        print(deck, ": rien à dire")
        continue
    D = S / f"att_{deck}"
    D.mkdir(exist_ok=True)
    ids_mixed = {i for d, i, _ in travaux if d == "mixed"}
    seul = dict(m)
    seul["activities"] = [dict(a, slides=[s for s in a["slides"] if s["id"] in ids_mixed]) for a in m["activities"]]
    seul["activities"] = [a for a in seul["activities"] if a["slides"]]
    (D / "cours.json").write_text(json.dumps(seul, ensure_ascii=False), encoding="utf-8")
    (D / "pistes.json").write_text(json.dumps([{"id": i, "parole": t} for d, i, t in travaux if d == "reponses"], ensure_ascii=False), encoding="utf-8")
    (D / "demonstrations.json").write_text(json.dumps([{"id": i, "parole": t} for d, i, t in travaux if d == "demos"], ensure_ascii=False), encoding="utf-8")
    n = len(travaux); total += n
    print(f"{deck} : {len(ids_mixed)} diapos, {sum(1 for d,*_ in travaux if d=='reponses')} énoncés/réactions/observations, "
          f"{sum(1 for d,*_ in travaux if d=='demos')} démos, {sum(len(t) for *_, t in travaux)} caractères")
json.dump(carte, open(S / "carte_observations.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TOTAL", total, "pistes")
