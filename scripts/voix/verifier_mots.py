"""Vérifie les mots que la voix devra dire, SANS le corpus (sessions cloud comprises) : skills voix-du-cours et
prononciation (18 novembre 2026).

Lit toutes les pistes d'un cours (diapositives, réactions, démonstrations, énoncés : scripts/voix/pistes_cours.py),
et signale chaque mot rare dans le corpus d'entraînement de la voix (backend/data/voix/frequences_corpus_v4.json) :
  - mot français vu moins de 3 fois : risque d'être mal dit (« siemens », vu 1 fois, sortait « milliseconde ») ;
  - mot darija vu moins de 3 fois (après avoir enlevé و ف ب ل ال collés devant) : la voix le connaît mal.
Un mot déjà réécrit par une règle de PRONONCIATION (texte_parle.py) n'est pas signalé.
Remède : un mot plus courant (le chercher aussi), une tournure plus simple ; un terme du programme que l'élève doit
entendre se garde, mais il est signalé dans la liste des voix à écouter.

Usage : python -X utf8 scripts/voix/verifier_mots.py <deck> [id_piste ...]
  sans id : toutes les pistes ; avec des ids : seulement ces pistes (ex. les diapositives réécrites).
Code de sortie 0 ; la liste sert à relire, pas à bloquer."""
import json, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..", "..")
sys.path[:0] = [ICI, os.path.join(RACINE, "backend", "kaggle_tts")]
from pistes_cours import pistes
import texte_parle
from texte_parle import parle

F = json.load(open(os.path.join(RACINE, "backend/data/voix/frequences_corpus_v4.json"), encoding="utf-8"))["mots"]
MOT = re.compile(r"[ء-ي]+|[a-zà-ÿ'-]+")
PREFIXES = ("وال", "فال", "بال", "لل", "ال", "و", "ف", "ب", "ل")


def frequence(w):
    if re.match(r"[ء-ي]", w):
        vus = [F.get(w, 0)]
        for p in PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 2:
                vus.append(F.get(w[len(p):], 0))
        return max(vus), "darija"
    w = re.sub(r"^(l|d|qu|n|s|j|c)'", "", w).strip("'-")
    return F.get(w, 0), "français"


deck, ids = sys.argv[1], set(sys.argv[2:])
m = json.load(open(os.path.join(RACINE, "backend/data/courses", deck + ".json"), encoding="utf-8"))
total = 0
for d, i, t, _ in pistes(m):
    if ids and i not in ids:
        continue
    reecrit = parle(t).lower().replace("’", "'")               # ce que la voix reçoit (règles appliquées)
    rares = []
    for w in sorted(set(MOT.findall(reecrit))):
        if len(w) < 3:
            continue
        n, langue = frequence(w)
        if n < 3:
            rares.append(f"{w} ({langue}, {n})")
    if rares:
        total += len(rares)
        print(f"{d}/{i} : " + ", ".join(rares))
print(f"--- {total} mots rares dans {deck}" + (f" (pistes {', '.join(sorted(ids))})" if ids else ""))
