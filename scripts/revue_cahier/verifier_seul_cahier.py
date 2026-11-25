"""Vérifie qu'un cours n'a changé QUE dans ses champs de cahier par rapport à origin/main.
Usage : python -I verifier_seul_cahier.py <worktree> <chemin du cours relatif au worktree> [...]
Champs autorisés : cahier, cahier_figures (dans blocs[] et dans concentration). Tout autre écart → ÉCHEC."""
import json
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1])
CHAMPS = {"cahier", "cahier_figures"}


def nettoie(x):
    if isinstance(x, dict):
        return {k: nettoie(v) for k, v in x.items() if k not in CHAMPS}
    if isinstance(x, list):
        return [nettoie(v) for v in x]
    return x


ok = True
for rel in sys.argv[2:]:
    avant = subprocess.run(["git", "-C", str(WT), "show", f"origin/main:{rel}"], capture_output=True, check=True).stdout.decode("utf-8")
    apres = (WT / rel).read_text(encoding="utf-8")
    bon = nettoie(json.loads(avant)) == nettoie(json.loads(apres))
    fins = ("\r\n" in avant) == ("\r\n" in apres) and avant.endswith("\n") == apres.endswith("\n")
    print(("OK   " if bon and fins else "ÉCHEC"), rel, "" if fins else "(fins de ligne ou fin de fichier changées)")
    ok &= bon and fins
sys.exit(0 if ok else 1)
