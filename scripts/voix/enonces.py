"""Énoncés des questions à faire lire par le tuteur (12 novembre 2026).
  python enonces.py extraire <sortie.json> <cours.json>...   → [{deck, chemin, id, texte}] (énoncés sans enonce_dit)
  python enonces.py poser <sortie_llm.json>                  → enonce_dit posé dans chaque cours
Chemins : ["q", slide] question de diapositive, ["e", slide, i] exercice, ["r", rappel], ["bx", bloc] exercice de
bloc, ["br", bloc] retrouver. id de piste : enonce_<…> (dossier reponses de la voix)."""
import json, sys
from pathlib import Path

AT = Path(__file__).resolve().parents[2] / "backend/data/courses"


def cibles(m):
    for a in m["activities"]:
        for s in a["slides"]:
            q = s.get("question") or {}
            if q.get("prompt"):
                yield ["q", s["id"]], f"enonce_{s['id']}_q", q
            for i, e in enumerate(s.get("exercises") or []):
                if e.get("prompt"):
                    yield ["e", s["id"], i], f"enonce_{s['id']}_e{i}", e
    for c in m.get("competences") or []:
        for r in c.get("rappels") or []:
            if r.get("prompt"):
                yield ["r", r["id"]], f"enonce_rappel_{r['id']}", r
    for se in m.get("seances") or []:
        for b in se.get("blocs") or []:
            for cle, quoi in (("bx", "exercice"), ("br", "retrouver")):
                o = b.get(quoi) or {}
                if o.get("prompt"):
                    yield [cle, b["id"]], f"enonce_bloc_{b['id']}_{quoi}", o


def texte(o):
    t = o["prompt"].strip()
    if o.get("statements"):
        t += "\n" + "\n".join(f"- {st.get('text', '')}" for st in o["statements"])
    return t


if __name__ != "__main__":
    pass
elif sys.argv[1] == "extraire":
    out = []
    for f in sys.argv[3:]:
        m = json.loads(Path(f).read_text(encoding="utf-8"))
        deck = Path(f).stem
        for chemin, ident, o in cibles(m):
            if not o.get("enonce_dit"):
                out.append({"deck": deck, "chemin": chemin, "id": ident, "texte": texte(o),
                            "titre": next((s["title"] for a in m["activities"] for s in a["slides"]
                                           if chemin[0] in "qe" and s["id"] == chemin[1]), "")})
    Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(len(out), "énoncés")
else:
    faits = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    par = {}
    for x in faits:
        if x.get("dit"):
            par.setdefault(x["deck"], {})[x["id"]] = x["dit"]
    for deck, dits in par.items():
        p = AT / f"{deck}.json"
        m = json.loads(p.read_text(encoding="utf-8"))
        n = 0
        for chemin, ident, o in cibles(m):
            if ident in dits:
                o["enonce_dit"] = dits[ident]
                n += 1
        p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(deck, ":", n, "énoncés posés")
