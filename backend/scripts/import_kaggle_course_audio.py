"""Enregistre dans le registre hors base (ledger.json) des audios de cours générés ailleurs (GPU Kaggle).

Même convention que ``generate_course_audio.py generate --offline`` : fichier
``frontend/public/media/audio/courses/<deck>/<langue>/<slide>_vN.wav`` (N = version suivante, jamais
d'écrasement), entrée ajoutée à l'historique de la diapositive avec l'empreinte du texte, les anciennes
versions passent à ``stale``. Rien n'est publié : ``import-ledger`` puis ``verify`` restent nécessaires.

Entrée : un dossier contenant ``cours.json`` (liste de {id, piste, hash, duree_s}) et
``cours/<piste>/<id>.wav`` — c'est ce que produit ``voxtts/kaggle_cours.py``.

    python -m scripts.import_kaggle_course_audio --deck phys_ch1_waves --source C:/chemin/vers/cours_kaggle
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import sys
from datetime import datetime, timezone
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from scripts.generate_course_audio import (  # noqa: E402
    PROJECT_ROOT, load_ledger, load_manifest, manifest_slides, save_ledger, ledger_path,
)


def importer(deck_stable_id: str, source: Path, provider: str) -> None:
    _, manifest = load_manifest(deck_stable_id)
    produits = {(r["id"], r["piste"]): r for r in json.loads((source / "cours.json").read_text(encoding="utf-8"))}
    bilan: dict[str, list[str]] = {"importés": [], "texte différent": [], "absents": []}
    for langue in sorted({p for _, p in produits}):
        ledger = load_ledger(manifest, langue)
        for slide in manifest_slides(manifest):
            sid = slide.get("stable_id") or slide["id"]
            speech = (slide.get("speech_text") or {}).get(langue)
            prod = produits.get((sid, langue))
            if not speech or not prod:
                bilan["absents"].append(f"{langue}/{sid}")
                continue
            speech_hash = hashlib.sha256(speech.strip().encode("utf-8")).hexdigest()
            if prod["hash"] != speech_hash:  # le manifeste a changé depuis la génération : on ne mélange pas
                bilan["texte différent"].append(f"{langue}/{sid}")
                continue
            wav = source / "cours" / langue / f"{sid}.wav"
            if not wav.exists():
                bilan["absents"].append(f"{langue}/{sid}")
                continue
            audio = wav.read_bytes()
            history = ledger["slides"].get(sid) or []
            latest = history[-1] if history else None
            if latest and latest.get("speech_hash") == speech_hash and latest.get("checksum") == hashlib.sha256(audio).hexdigest():
                continue  # déjà importé tel quel
            version = int(latest.get("version") or 0) + 1 if latest else 1
            while True:
                rel = Path("media") / "audio" / "courses" / manifest["stable_id"] / langue / f"{sid}_v{version}.wav"
                out = PROJECT_ROOT / "frontend" / "public" / rel
                if not out.exists():
                    break
                version += 1
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(audio)
            for row in history:
                if row.get("status") != "rejected":
                    row["status"] = "stale"
            history.append({
                "language": langue, "version": version, "speech_hash": speech_hash,
                "file_path": "/" + rel.as_posix(),
                "mime_type": mimetypes.guess_type(out.name)[0] or "audio/wav",
                "provider": provider, "checksum": hashlib.sha256(audio).hexdigest(),
                "size_bytes": len(audio), "status": "generated",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            })
            ledger["slides"][sid] = history
            bilan["importés"].append(f"{langue}/{sid} v{version} ({prod.get('duree_s', '?')} s)")
        save_ledger(manifest, langue, ledger)
        print(f"registre : {ledger_path(manifest, langue)}")
    for k, v in bilan.items():
        print(f"{k} : {len(v)}")
        for x in v:
            print("  ", x)
    print("Rien n'est publié : import-ledger puis verify sur le serveur.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--provider", default="academy")
    a = ap.parse_args()
    importer(a.deck, a.source, a.provider)


if __name__ == "__main__":
    main()
