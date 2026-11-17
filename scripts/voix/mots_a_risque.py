"""Mots que la voix risque de mal dire (skill prononciation, 16 novembre 2026).

Un mot français que le modèle n'a presque jamais entendu à l'entraînement peut sortir déformé (« siemens », vu une
fois en 38 852 phrases, sortait « milliseconde »). Ce script :
  1. liste les mots français des textes parlés de tous les cours (diapositives, réactions, démonstrations, énoncés)
     vus moins de 3 fois dans le corpus d'entraînement, avec le nombre de pistes qui les disent ;
  2. si on lui donne des transcriptions MoulSot (JSON {clé: {texte, stt}} ou liste de {deck, type, id, texte, stt}),
     calcule pour chaque mot rare la part des pistes où MoulSot l'entend : un mot rarement entendu est à écouter.

Usage (dans le dépôt) :
  python -X utf8 scripts/voix/mots_a_risque.py [TRANSCRIPTIONS.json ...]
Corpus : C:/Users/HP/Desktop/voxtts/corpus_v4/selection_train.jsonl (ou variable CORPUS_VOIX).
"""
import collections, difflib, glob, json, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [ICI, os.path.join(ICI, "..", "..", "backend", "kaggle_tts")]
from pistes_cours import pistes
import texte_parle
texte_parle.prononciation = lambda p: p   # on juge le mot écrit, pas sa réécriture
from texte_parle import parle

CORPUS = os.environ.get("CORPUS_VOIX", "C:/Users/HP/Desktop/voxtts/corpus_v4/selection_train.jsonl")
MOT = re.compile(r"[a-zà-ÿ'-]+")


def norm(w):
    return re.sub(r"^(l|d|qu|n|s|j|c)'", "", w.replace("’", "'"))


W = collections.Counter()
for ligne in open(CORPUS, encoding="utf-8"):
    W.update(norm(w) for w in MOT.findall(json.loads(ligne)["texte"].lower()))

rares = collections.defaultdict(set)
for f in sorted(glob.glob("backend/data/courses/*_ch*_*.json")):
    if "_course_v1" in f or "_script_" in f:
        continue
    deck = os.path.basename(f)[:-5]
    for d, i, t, _ in pistes(json.load(open(f, encoding="utf-8"))):
        for w in set(norm(x) for x in MOT.findall(parle(t).lower())):
            if len(w) >= 4 and "-" not in w and W[w] < 3:
                rares[w].add(f"{deck}/{d}/{i}")

transcrits = {}
for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    items = d.items() if isinstance(d, dict) else ((f"{x['deck']}/{x['type']}/{x['id']}", x) for x in d)
    for k, v in items:
        if v.get("stt"):
            transcrits[k] = (parle(v["texte"]).lower(), v["stt"].lower())

if not transcrits:
    print(len(rares), "mots français vus moins de 3 fois à l'entraînement (les plus dits d'abord) :")
    for w, s in sorted(rares.items(), key=lambda kv: -len(kv[1]))[:100]:
        print(f"{len(s):5d} pistes  {w}  (corpus : {W[w]})")
    sys.exit(0)

stat = collections.defaultdict(lambda: [0, 0])
for tx, st in transcrits.values():
    entendus = [norm(w) for w in MOT.findall(st)]
    for w in set(norm(x) for x in MOT.findall(tx)):
        if w in rares:
            stat[w][0] += 1
            if w in entendus or difflib.get_close_matches(w, entendus, 1, 0.8):
                stat[w][1] += 1
r = sorted(((w, n, ok) for w, (n, ok) in stat.items() if n >= 3), key=lambda x: (x[2] / x[1], -x[1]))
print(len(transcrits), "pistes transcrites ;", len(r), "mots rares présents dans au moins 3 d'entre elles")
print("entendu  pistes transcrites  mot  (pistes qui le disent, tous cours)")
for w, n, ok in r:
    if ok / n < 0.5:
        print(f"{100 * ok // n:5d} %  {n:6d}             {w}  ({len(rares[w])})")
