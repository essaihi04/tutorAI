"""Écritures sûres des mots rares (skill prononciation, § 6 ; demande de l'utilisateur, 19 novembre 2026).

« Nous avons déjà quelques mots avec leur erreur et leur correction ; les prochains mots avec le même problème, ou dont
on n'est pas certain qu'ils soient bien prononcés, il vaut mieux les écrire de la manière la plus sûre, comme micros et
fœtus. » Ce script cherche, dans les textes parlés de TOUS les cours, chaque mot français que la voix a vu moins de
3 fois à l'entraînement, et lui donne d'office l'écriture la plus sûre quand un des cas déjà corrigés s'applique :

  1. « s » final muet (pluriel, verbe) alors que le mot sans « s » est connu : on retire le « s »
     (micros -> micro, ohms -> ohm, écris -> écri, demis -> demi) ;
  2. mot latin en « -us » dont le « s » se dit : « -uss » (fœtus -> fétusse, locus -> locuss, stimulus -> stimuluss) ;
  3. « ch » qui se dit « k » (mots grecs : ch devant l ou r, écho, psych, tech) : « k »
     (chlorure -> klorure, chronomètre -> kronomètre, échographie -> ékographie).

Les mots corrigés à l'écoute par l'utilisateur (`PRONONCIATION`) passent avant et ne sont pas touchés. Le résultat est
écrit dans `backend/kaggle_tts/texte_parle.py`, entre les repères `# >>> ÉCRITURES SÛRES` et `# <<< ÉCRITURES SÛRES`
(le kernel n'embarque que ce fichier). Relancer après chaque nouveau cours, puis régénérer les pistes qui changent.

Usage (dans le dépôt) :  python -X utf8 scripts/voix/ecritures_sures.py [--ecrire]
Sans --ecrire : affiche les écritures proposées, avec le nombre de pistes de chaque mot.
"""
import collections, glob, importlib.util, json, re, sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]
sys.path.insert(0, str(ICI))
from pistes_cours import pistes

TP = RACINE / "backend/kaggle_tts/texte_parle.py"
DEBUT, FIN = "# >>> ÉCRITURES SÛRES", "# <<< ÉCRITURES SÛRES"
F = json.load(open(RACINE / "backend/data/voix/frequences_corpus_v4.json", encoding="utf-8"))
F = F.get("mots", F)
RARE = 3
# des mots en -us dont le s ne se dit pas, ou déjà connus autrement
US_MUET = {"plus", "dessus", "dessous", "au-dessus", "au-dessous", "par-dessus", "jus", "abus", "refus", "obus", "talus",
           "confus", "inclus", "exclus", "reclus", "conclus", "contenus", "tous", "vous", "nous", "sous", "tus", "vus"}


def charger_tp():
    sp = importlib.util.spec_from_file_location("texte_parle", TP)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


def proposer(w):
    lw = w.lower()
    if lw.endswith("s") and F.get(lw[:-1], 0) >= RARE:
        return lw[:-1]
    if re.search(r"[^aeiouéèê]us$", lw) and lw not in US_MUET and F.get(lw[:-1], 0) < RARE:
        return lw + "s"
    k = re.sub(r"ch(?=[lr])", "k", lw)
    k = re.sub(r"^écho", "éko", k)
    k = re.sub(r"psych", "psik", k)
    k = re.sub(r"^tech", "tek", k)
    if k != lw:
        return k
    return None


def main():
    tp = charger_tp()
    tp.ECRITURES_SURES = {}          # les mots déjà remplacés doivent rester visibles pour être recomptés
    deja = {m.pattern for m, _ in tp.PRONONCIATION}
    compte = collections.Counter()
    for f in sorted(glob.glob(str(RACINE / "backend/data/courses/*.json"))):
        try:
            m = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(m, dict) or "activities" not in m:
            continue
        for _, _, t, _ in pistes(m):
            p = tp.parle(t)
            for w in re.findall(r"[A-Za-zÀ-ÿœ][A-Za-zÀ-ÿœ-]+", p):
                lw = w.lower()
                if len(lw) > 3 and F.get(lw, 0) < RARE:
                    compte[lw] += 1
    sures = {}
    for w, n in compte.most_common():
        e = proposer(w)
        if e and e != w and not any(re.search(pat, w, re.I) for pat in deja):
            sures[w] = e
    for w, e in sures.items():
        print(f"{compte[w]:5d}  {w} -> {e}")
    print(len(sures), "écritures sûres")
    if "--ecrire" in sys.argv:
        s = TP.read_text(encoding="utf-8")
        a, b = s.index(DEBUT), s.index(FIN)
        corps = "ECRITURES_SURES = " + json.dumps(dict(sorted(sures.items())), ensure_ascii=False, indent=1) + "\n"
        s = s[:a] + DEBUT + " (générées par scripts/voix/ecritures_sures.py, ne pas modifier à la main)\n" + corps + s[b:]
        TP.write_text(s, encoding="utf-8", newline="\n")
        print("écrit dans", TP)


if __name__ == "__main__":
    main()
