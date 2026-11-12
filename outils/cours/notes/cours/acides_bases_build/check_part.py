"""Contrôle une partie seule : python3 outils/cours/notes/cours/acides_bases_build/check_part.py p2  (depuis la racine du dépôt)."""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
m = importlib.import_module(sys.argv[1])
n = 0
for k in dir(m):
    if k.startswith("PARTIE") or k == "BILAN":
        v = getattr(m, k); n += len(v)
        print(k, [s["id"] for s in v])
print(n, "diapositives")
print("\n".join(outils.ERREURS) if outils.ERREURS else "AUCUNE ERREUR")
