"""Règle du texte parlé (skill voix-du-cours) : chaque mot d'un texte darija est cherché dans le corpus
d'entraînement de la voix v4.

Usage : python verifier_texte_corpus.py COURS.json [selection_train.jsonl]
  COURS.json : un cours (backend/data/courses/…), on lit speech_text.mixed de chaque diapositive.
  selection_train.jsonl : téléchargé une fois avec
      kaggle datasets download zouhairessaihi/academy-v4-selection -f selection_train.jsonl -p <dossier>

Signale : un mot français vu moins de 20 fois qui n'est pas dans la liste des termes du programme ou des mots
d'examen ; un mot darija vu moins de 3 fois (en enlevant و ف ب ل ال collés devant).
"""
import collections
import importlib.util
import json
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).parent
COURS = pathlib.Path(sys.argv[1])
SEL = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ICI / "selection_train.jsonl"

W = collections.Counter()
for ligne in open(SEL, encoding="utf-8"):
    W.update(re.findall(r"[ء-ي]+|[a-zà-ÿ']+", json.loads(ligne)["texte"].lower().replace("’", "'")))

# Termes du programme et mots d'examen : restent en français même s'ils sont rares dans le corpus.
GARDES = set("""onde l'onde ondes perturbation propagation célérité retard milieu front signal élongation l'élongation aspect
l'aspect source transversale longitudinale mécanique progressive progressives périodiques homogène élastique matériel
l'énergie énergie matière sensibilité horizontale division divisions oscilloscope l'oscilloscope micros micro ultrasons sonar
réflexion l'écho écho hertz kilohertz ressort corde courbe courbes dimension durée longueur distance vitesse température
nature valeurs relation l'application numérique tp qcm définition phénomène grec parcourue reproduit transport d'énergie
d'une flèches droite l'axe fonction calculer déduire justifier déterminer exprimer représenter l'expression
milliseconde millisecondes""".split())

spec = importlib.util.spec_from_file_location("tp", ICI / "texte_parle.py")
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)


def connu(w):
    if W[w] >= 3:
        return True
    for pre in ("وال", "فال", "بال", "لل", "و", "ف", "ب", "ل"):
        r = w[len(pre):]
        if w.startswith(pre) and len(r) > 2 and (W[r] >= 3 or W["ال" + r] >= 3):
            return True
    return False


m = json.loads(COURS.read_text(encoding="utf-8"))
total = 0
for a in m["activities"]:
    for s in a["slides"]:
        p = tp.parle((s.get("speech_text") or {}).get("mixed") or "")
        fr = sorted({f"{w}({W[w]})" for w in re.findall(r"[a-zà-ÿ']+", p.lower()) if W[w] < 20 and w not in GARDES})
        ar = sorted({f"{w}({W[w]})" for w in re.findall(r"[ء-ي]+", p) if not connu(w)})
        total += len(fr) + len(ar)
        if fr or ar:
            print(f"{s['id']:24s} français rares : {fr}   darija rares : {ar}")
print("mots à revoir :", total)
