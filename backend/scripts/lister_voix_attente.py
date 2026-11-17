"""Liste les pistes de voix à enregistrer dans les cours en attente (backend/data/courses/en_attente/).

Pour chaque cours : chaque texte parlé qui n'a pas encore de piste — voix d'une diapo (speech_text.mixed sans
audio.mixed), parole d'une démonstration, d'une réaction préparée, d'une observation — avec un id stable et le texte
exact à dire. Sortie JSON : {deck: [{id, type, texte}]} (à donner au lot Bodi sur le VPS, skill voix-du-cours §3).

    python -I backend/scripts/lister_voix_attente.py [deck…] > voix_attente.json
"""
import json
import sys
from pathlib import Path

ATTENTE = Path(__file__).resolve().parents[1] / "data" / "courses" / "en_attente"


def pistes(deck: dict) -> list[dict]:
    out = []

    def ajouter(id_, type_, texte):
        if isinstance(texte, str) and texte.strip():
            out.append({"id": id_, "type": type_, "texte": texte.strip()})

    def walk(o, chemin):
        if isinstance(o, dict):
            dm = o.get("demonstration")
            if isinstance(dm, dict) and not dm.get("audio"):
                ajouter(chemin + "__demo", "demonstration", dm.get("parole"))
            for k, v in o.items():
                if k == "demonstration":
                    continue
                if isinstance(v, dict) and "parole" in v and not v.get("audio") and k in ("juste", "1", "2", "solution"):
                    ajouter(f"{chemin}__{k}", "reaction", v["parole"])
                walk(v, f"{chemin}/{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{chemin}[{i}]")

    for a in deck.get("activities", []):
        for s in a.get("slides", []):
            if not ((s.get("audio") or {}).get("mixed")):
                ajouter(s["id"], "diapo", (s.get("speech_text") or {}).get("mixed"))
            walk(s, s["id"])
    walk({"seances": deck.get("seances", []), "competences": deck.get("competences", [])}, "deck")
    return out


def main() -> None:
    noms = sys.argv[1:] or sorted(p.stem for p in ATTENTE.glob("*.json"))
    res = {n: pistes(json.loads((ATTENTE / f"{n}.json").read_text(encoding="utf-8"))) for n in noms}
    json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
    for n, l in res.items():
        print(f"{n}: {len(l)} pistes, {sum(len(x['texte']) for x in l)} caractères", file=sys.stderr)


if __name__ == "__main__":
    main()
