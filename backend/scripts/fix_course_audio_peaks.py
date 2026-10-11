"""Ramène sous -0,5 dBFS le pic des WAV d'un registre hors base (ledger.json) et met à jour
checksum et taille dans le registre. Gain appliqué au fichier entier (pas de compression) : au plus
quelques dixièmes de dB, inaudible, mais supprime les échantillons écrêtés.

    python -m scripts.fix_course_audio_peaks --deck phys_ch1_waves --language fr

À lancer AVANT import-ledger : la base doit recevoir les checksums définitifs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import wave
from pathlib import Path

import numpy as np

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PUBLIC = BACKEND_ROOT.parent / "frontend" / "public"
AUDIO_ROOT = PUBLIC / "media" / "audio" / "courses"
TARGET = 0.944  # -0,5 dBFS


def fix(deck: str, language: str) -> None:
    ledger_file = AUDIO_ROOT / deck / language / "ledger.json"
    ledger = json.loads(ledger_file.read_text(encoding="utf-8"))
    fixed = untouched = 0
    for stable_id, history in ledger["slides"].items():
        row = history[-1]
        path = PUBLIC / row["file_path"].lstrip("/")
        if path.suffix != ".wav" or not path.exists():
            continue
        with wave.open(str(path)) as w:
            params = w.getparams()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        peak = float(np.abs(x).max()) if len(x) else 0.0
        if peak <= TARGET:
            untouched += 1
            continue
        y = np.clip(x * (TARGET / peak), -1.0, 1.0)
        with wave.open(str(path), "wb") as w:
            w.setparams(params)
            w.writeframes((y * 32767).astype("<i2").tobytes())
        data = path.read_bytes()
        row["checksum"] = hashlib.sha256(data).hexdigest()
        row["size_bytes"] = len(data)
        row["peak_fixed_db"] = round(20 * np.log10(TARGET / peak), 2)
        fixed += 1
    ledger_file.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{deck}/{language} : {fixed} fichiers corrigés, {untouched} déjà sous -0,5 dBFS.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck", required=True)
    parser.add_argument("--language", required=True, choices=("fr", "ar", "mixed"))
    args = parser.parse_args()
    fix(args.deck, args.language)
