"""Écrit la partie « diapositive par diapositive » d'une architecture à partir du cours en attente et d'un fichier de
raisons ({id: raison}) : séance → bloc → diapositive (id, titre, À toi, voix gardée ou à refaire, raison).
Usage : python -X utf8 scripts/logique/ecrire_architecture.py <deck> <raisons.json> <entete.md> <pied.md>"""
import json, os, sys

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
deck, raisons, entete, pied = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3], sys.argv[4]
d = json.load(open(os.path.join(RACINE, "backend/data/courses/en_attente", deck + ".json"), encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}
partie = {s["id"]: a["title"] for a in d["activities"] for s in a["slides"]}
out = [open(entete, encoding="utf-8").read().rstrip(), "", "## L'architecture, diapositive par diapositive", "",
       f"{len(S)} diapositives, {len(d['seances'])} séances, "
       f"{sum(len(se['blocs']) for se in d['seances'])} blocs, durée prévue {d['estimated_minutes']} min. "
       "« ✏️ » : la diapositive porte le « À toi » du bloc ; « 🔊 » : sa voix est gardée ; « 🆕 voix » : à enregistrer.", ""]
manque = []
derniere_partie = None
for se in d["seances"]:
    out += [f"### {se['titre']}", ""]
    for b in se["blocs"]:
        out += [f"**{b['titre']}** (`{b['id']}`)", "", "| Diapositive | Titre | | Pourquoi ici |", "|---|---|---|---|"]
        for i in b["slide_ids"]:
            s = S[i]
            if partie[i] != derniere_partie:
                derniere_partie = partie[i]
            marque = ("✏️ " if s.get("question") or s.get("exercises") else "") + \
                     ("🔊" if (s.get("audio") or {}).get("mixed") else "🆕 voix")
            r = raisons.get(i)
            if not r:
                manque.append(i)
            out.append(f"| `{i}` | {s['title']} | {marque} | {r or '—'} |")
        out.append("")
out.append(open(pied, encoding="utf-8").read().rstrip())
p = os.path.join(RACINE, "backend/data/curriculum/architecture", deck + ".md")
open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(p, "raisons manquantes :", manque)
