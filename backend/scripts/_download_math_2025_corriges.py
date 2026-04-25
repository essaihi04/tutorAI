"""
Télécharge les corrigés manquants des examens Maths 2025 (Normale + Rattrapage)
depuis monstremath.com, car alloschool.com ne les a pas encore publiés.

URLs :
  https://monstremath.com/Examen-Nationaux/Examen-National-Maths-Sciences-pc-et-svt/C/
    Corrige Examen National Maths Sciences et Technologies 2025 Normale.pdf
    Corrige Examen National Maths Sciences et Technologies 2025 Rattrapage.pdf
"""
from __future__ import annotations
import sys
from pathlib import Path
from urllib.parse import quote
import requests

HERE = Path(__file__).resolve()
BACKEND = next(p for p in HERE.parents if (p / "data" / "exams").is_dir())
MATH_DIR = BACKEND / "data" / "exams" / "mathematiques"

BASE_URL = (
    "https://monstremath.com/Examen-Nationaux/"
    "Examen-National-Maths-Sciences-pc-et-svt/C/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Referer": "https://monstremath.com/Examen-Nationaux/Examen-National-Maths-Sciences-pc-et-svt/",
}

TARGETS = {
    "normale":    "Corrige Examen National Maths Sciences et Technologies 2025 Normale.pdf",
    "rattrapage": "Corrige Examen National Maths Sciences et Technologies 2025 Rattrapage.pdf",
}


def main() -> int:
    ok = fail = 0
    for session, filename in TARGETS.items():
        url = BASE_URL + quote(filename)
        dest_dir = MATH_DIR / f"2025-{session}" / "pdfs"
        dest = dest_dir / f"examen-national-mathematiques-2025-{session}-corrige.pdf"

        print(f"\n━━━ Math 2025-{session} ━━━")
        print(f"  URL  : {url}")
        print(f"  Dest : {dest.relative_to(BACKEND)}")

        if dest.exists() and dest.stat().st_size > 20_000:
            print(f"  · déjà présent ({dest.stat().st_size // 1024} KB) — skip")
            continue

        try:
            r = requests.get(url, headers=HEADERS, timeout=60, stream=True)
            r.raise_for_status()
        except Exception as e:
            print(f"  ✗ HTTP error: {e}")
            fail += 1
            continue

        ct = r.headers.get("Content-Type", "").lower()
        if "pdf" not in ct:
            print(f"  ✗ Content-Type inattendu : {ct}")
            fail += 1
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(".part")
        total = 0
        with tmp.open("wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)
                    total += len(chunk)

        # Verify PDF signature
        with tmp.open("rb") as f:
            sig = f.read(5)
        if sig != b"%PDF-":
            print(f"  ✗ Signature invalide : {sig!r}")
            tmp.unlink(missing_ok=True)
            fail += 1
            continue

        tmp.replace(dest)
        print(f"  ✓ Téléchargé ({total // 1024} KB, signature %PDF- OK)")
        ok += 1

    print(f"\n━━━ RÉSULTAT ━━━\n  ✓ OK: {ok}\n  ✗ Échec: {fail}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
