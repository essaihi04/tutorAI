"""Branche les voix de l'évaluation du Tronc Commun : écrit dans `voixExamen.ts` la liste des pistes qui existent
(`frontend/public/media/audio/courses/tc_svt_examen/<type>/<id>.mp3`). Usage : python -I scripts/brancher_voix_examen.py"""
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "frontend/public/media/audio/courses/tc_svt_examen"
CIBLE = RACINE / "frontend/src/publication/tronc-commun/voixExamen.ts"

cles = sorted(p.relative_to(DOSSIER).with_suffix("").as_posix() for p in DOSSIER.rglob("*.mp3")) if DOSSIER.is_dir() else []
texte = CIBLE.read_text(encoding="utf-8")
debut = texte.index("export const VOIX_EXAMEN")
CIBLE.write_text(texte[:debut] + "export const VOIX_EXAMEN: string[] = [\n" + "".join(f"  '{c}',\n" for c in cles) + "];\n", encoding="utf-8")
print(len(cles), "pistes branchées")
