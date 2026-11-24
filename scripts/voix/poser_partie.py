"""Pose dans les exercices seulement les pistes d'une partie (lot Colab ou Kaggle), après écoute de l'utilisateur.

Usage (depuis la racine du dépôt ou un worktree partiel) :
  python -X utf8 scripts/voix/poser_partie.py VERSION LISTE.json [RACINE]
LISTE.json : la liste du lot ([{cle: "<exercice>/<dossier>/<piste>", texte, cours}]). Les WAV sont lus sur le VPS
(att_<exercice>/<dossier>/<piste>.wav, hash du texte vérifié) par pistes_exercice._poser ; les autres pistes de
l'exercice ne sont pas touchées. Skill voix-du-cours, § 3 ter.
"""
import json, sys
from pathlib import Path

W = Path(sys.argv[3]) if len(sys.argv) > 3 else Path(__file__).resolve().parents[2]
cles = {x["cle"] for x in json.load(open(sys.argv[2], encoding="utf-8"))}
sys.path.insert(0, str(W / "scripts/voix"))
import pistes_exercice as P  # noqa: E402

orig = P.pistes


def filtre(e):
    for d, i, t, poser in orig(e):
        if f"{e['id']}/{d}/{i}" in cles:
            yield d, i, t, poser


P.pistes = filtre
ex = sorted({c.split("/")[0] for c in cles})
P._poser(int(sys.argv[1]), [str(W / f"frontend/public/media/exercices/{x}.json") for x in ex])
