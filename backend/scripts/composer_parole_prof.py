"""Compose la parole enregistrée des cours avec les gestes de prof (skill professeur) :
situation-problème en ouverture, rappel au début de chaque activité, « Je relis » de la phrase-clé.

Les ajouts viennent de data/courses/parole_prof.json. La parole d'origine est conservée dans
`speech_base` (la composition repart toujours d'elle : relancer le script ne double rien).
Usage : python -m scripts.composer_parole_prof [--apercu]
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parents[1] / "data" / "courses"
PROF = json.loads((ICI / "parole_prof.json").read_text(encoding="utf-8"))
ANNONCE = {
    "relire": {"fr": "Je relis : {k}", "mixed": "نعاود نقرا: {k}"},
    "rappel": {"fr": "Avant de continuer, un rappel : {k}", "mixed": "قبل ما نكملو، نتفكرو: {k}"},
}
OUVERTURES = ("Bienvenue", "مرحبا")


def point(t: str) -> str:
    t = t.strip()
    return t if t.endswith((".", "!", "?", "؟", "…")) else t + "."


def apres_salut(base: str, ajout: str) -> str:
    """La situation-problème vient juste après la phrase d'accueil, sinon en tête."""
    if base.startswith(OUVERTURES):
        for fin in (". ", ": ", "! "):
            i = base.find(fin)
            if i > 0:
                return base[: i + 1] + " " + ajout + " " + base[i + 2:]
    return ajout + " " + base


def composer(manifest: dict) -> int:
    deck = manifest.get("stable_id")
    question = (PROF["situations"].get(deck) or {}).get("question")
    # avant toute phrase-clé relue, le rappel reprend la question du chapitre
    derniere_cle = {"fr": f"notre question, {question}", "mixed": f"السؤال ديالنا، {question}"} if question else None
    n = 0
    for ai, activite in enumerate(manifest.get("activities") or []):
        for si, diapo in enumerate(activite.get("slides") or []):
            sid = diapo.get("stable_id") or diapo["id"]
            base = diapo.setdefault("speech_base", dict(diapo.get("speech_text") or {}))
            nouveau = {}
            for piste, texte in base.items():
                t = (texte or "").strip()
                if not t or piste not in ("fr", "mixed"):
                    nouveau[piste] = texte
                    continue
                if ai == 0 and si == 0 and deck in PROF["situations"]:
                    t = apres_salut(t, PROF["situations"][deck][piste])
                if ai > 0 and si == 0 and derniere_cle:
                    cle = derniere_cle[piste] if isinstance(derniere_cle, dict) else derniere_cle
                    t = ANNONCE["rappel"][piste].format(k=point(cle)) + " " + t
                if sid in PROF["relire"]:
                    t = point(t) + " " + ANNONCE["relire"][piste].format(k=point(PROF["relire"][sid]))
                nouveau[piste] = t
            if nouveau != diapo.get("speech_text"):
                n += 1
            diapo["speech_text"] = nouveau
            if sid in PROF["relire"]:
                derniere_cle = PROF["relire"][sid]
    return n


def main() -> None:
    apercu = "--apercu" in sys.argv
    for f in sorted(ICI.glob("*_course_v1.json")):
        m = json.loads(f.read_text(encoding="utf-8"))
        n = composer(m)
        if not apercu:
            f.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{f.name}: {n} diapositives composées" + (" (aperçu, rien écrit)" if apercu else ""))


if __name__ == "__main__":
    main()
