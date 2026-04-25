"""
Télécharge les examens nationaux Mathématiques ("Maths Sciences et Technologies")
— 2ème BAC Sciences Physiques BIOF — depuis alloschool.com, de 2016 à 2025,
sessions Normale et Rattrapage.

Structure créée :
    backend/data/exams/mathematiques/YYYY-session/pdfs/
        examen-national-mathematiques-YYYY-session-sujet.pdf
        examen-national-mathematiques-YYYY-session-corrige.pdf

Usage :
    python backend/scripts/download_math_exams.py [--force] [--year YYYY]
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urljoin

import requests

# ---------------------------------------------------------------------------
# Mapping (year, session) -> {'sujet': element_id, 'corrige': element_id}
# Source : https://www.alloschool.com/course/mathematiques-2eme-bac-sciences-physiques-biof
# ---------------------------------------------------------------------------
EXAMS: dict[tuple[int, str], dict[str, int]] = {
    (2016, "normale"):    {"sujet": 94485,  "corrige": 94490},
    (2016, "rattrapage"): {"sujet": 94502,  "corrige": 94520},
    (2017, "normale"):    {"sujet": 94525,  "corrige": 94530},
    (2017, "rattrapage"): {"sujet": 94535,  "corrige": 94540},
    (2018, "normale"):    {"sujet": 94699,  "corrige": 94704},
    (2018, "rattrapage"): {"sujet": 94709,  "corrige": 94714},
    (2019, "normale"):    {"sujet": 68527,  "corrige": 100965},
    (2019, "rattrapage"): {"sujet": 106247, "corrige": 106252},
    (2020, "normale"):    {"sujet": 109797, "corrige": 109803},
    (2020, "rattrapage"): {"sujet": 109808, "corrige": 109814},
    (2021, "normale"):    {"sujet": 127180, "corrige": 136793},
    (2021, "rattrapage"): {"sujet": 127185, "corrige": 136798},
    (2022, "normale"):    {"sujet": 136586, "corrige": 136803},
    (2022, "rattrapage"): {"sujet": 136591, "corrige": 136808},
    (2023, "normale"):    {"sujet": 137482, "corrige": 137472},
    (2023, "rattrapage"): {"sujet": 142250, "corrige": 142255},
    (2024, "normale"):    {"sujet": 144505, "corrige": 144510},
    (2024, "rattrapage"): {"sujet": 145811, "corrige": 145816},
    (2025, "normale"):    {"sujet": 145826},  # pas encore de corrigé officiel
    (2025, "rattrapage"): {"sujet": 145831},  # pas encore de corrigé officiel
}

BASE = "https://www.alloschool.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9",
}

PDF_LINK_RE = re.compile(
    r'href="([^"]+\.pdf)"[^>]*>[^<]*Téléchargez', re.IGNORECASE
)
FALLBACK_RE = re.compile(r'href="([^"]+course-\d+/[^"]+\.pdf)"', re.IGNORECASE)


def project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "data" / "exams").is_dir():
            return parent
    raise RuntimeError("Impossible de localiser backend/data/exams/")


def target_dir(year: int, session: str) -> Path:
    return project_root() / "data" / "exams" / "mathematiques" / f"{year}-{session}" / "pdfs"


def fetch_pdf_url(element_id: int, session: requests.Session) -> Optional[str]:
    url = f"{BASE}/element/{element_id}"
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"    ✗ HTTP error fetching {url}: {e}")
        return None

    html = r.text
    m = PDF_LINK_RE.search(html) or FALLBACK_RE.search(html)
    if not m:
        print(f"    ✗ Aucun lien PDF trouvé sur {url}")
        return None

    pdf_url = unquote(m.group(1))
    if pdf_url.startswith("/"):
        pdf_url = urljoin(BASE, pdf_url)
    return pdf_url


def download_pdf(
    pdf_url: str, dest: Path, session: requests.Session, force: bool = False
) -> bool:
    if dest.exists() and not force:
        print(f"    ✓ Déjà présent : {dest.name} ({dest.stat().st_size // 1024} KB)")
        return True

    try:
        r = session.get(pdf_url, headers=HEADERS, timeout=60, stream=True)
        r.raise_for_status()
    except Exception as e:
        print(f"    ✗ HTTP error downloading {pdf_url}: {e}")
        return False

    ct = r.headers.get("Content-Type", "")
    if "pdf" not in ct.lower() and not pdf_url.lower().endswith(".pdf"):
        print(f"    ✗ Content-Type inattendu : {ct}")
        return False

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part")
    total = 0
    with tmp.open("wb") as f:
        for chunk in r.iter_content(chunk_size=64 * 1024):
            if chunk:
                f.write(chunk)
                total += len(chunk)
    tmp.replace(dest)
    print(f"    ✓ Téléchargé : {dest.name} ({total // 1024} KB)")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--year", type=int)
    args = parser.parse_args()

    s = requests.Session()
    ok = fail = skipped = 0

    items = sorted(EXAMS.items())
    if args.year:
        items = [it for it in items if it[0][0] == args.year]
        if not items:
            print(f"Aucune entrée pour année {args.year}")
            return 1

    for (year, session), mapping in items:
        label = f"{year}-{session}"
        print(f"\n━━━ Mathématiques {label} ━━━")
        out_dir = target_dir(year, session)
        out_dir.mkdir(parents=True, exist_ok=True)

        for kind, element_id in mapping.items():
            filename = f"examen-national-mathematiques-{year}-{session}-{kind}.pdf"
            dest = out_dir / filename

            if dest.exists() and not args.force:
                size_kb = dest.stat().st_size // 1024
                if size_kb > 10:
                    print(f"  · {kind:8s} → déjà présent ({size_kb} KB)")
                    skipped += 1
                    continue

            print(f"  · {kind:8s} → element/{element_id}")
            pdf_url = fetch_pdf_url(element_id, s)
            if not pdf_url:
                fail += 1
                continue

            if download_pdf(pdf_url, dest, s, force=args.force):
                ok += 1
            else:
                fail += 1

            time.sleep(0.6)

    print(
        f"\n━━━ RÉSULTAT ━━━\n"
        f"  ✓ OK       : {ok}\n"
        f"  · Skipped  : {skipped}\n"
        f"  ✗ Échec    : {fail}"
    )
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
