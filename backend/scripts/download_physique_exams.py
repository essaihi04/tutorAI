"""
Télécharge les examens nationaux Physique-Chimie (SPC — 2ème BAC Sciences
Physiques BIOF) depuis alloschool.com, de 2016 à 2025, sessions Normale et
Rattrapage.

Structure créée :
    backend/data/exams/physique/YYYY-session/pdfs/
        examen-national-physique-chimie-YYYY-session-sujet.pdf
        examen-national-physique-chimie-YYYY-session-corrige.pdf

Usage :
    python -m backend.scripts.download_physique_exams
        ou, depuis la racine du projet :
    python backend/scripts/download_physique_exams.py [--force]

Options :
    --force   re-télécharge même si le fichier existe déjà
    --year YYYY   ne télécharge que cette année
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
# Source : https://www.alloschool.com/course/physique-et-chimie-2eme-bac-sciences-physiques-biof
# ---------------------------------------------------------------------------
EXAMS: dict[tuple[int, str], dict[str, int]] = {
    (2016, "normale"):    {"sujet": 57700,  "corrige": 57703},
    (2016, "rattrapage"): {"sujet": 57706,  "corrige": 57709},
    (2017, "normale"):    {"sujet": 57712,  "corrige": 57715},
    (2017, "rattrapage"): {"sujet": 57718,  "corrige": 57721},
    (2018, "normale"):    {"sujet": 57727,  "corrige": 57730},
    (2018, "rattrapage"): {"sujet": 57733,  "corrige": 57736},
    (2019, "normale"):    {"sujet": 68301,  "corrige": 68304},
    (2019, "rattrapage"): {"sujet": 94420,  "corrige": 94423},
    (2020, "normale"):    {"sujet": 109738, "corrige": 109743},
    (2020, "rattrapage"): {"sujet": 109749, "corrige": 109755},
    (2021, "normale"):    {"sujet": 127285, "corrige": 136824},
    (2021, "rattrapage"): {"sujet": 127288, "corrige": 136827},
    (2022, "normale"):    {"sujet": 136622, "corrige": 136830},
    (2022, "rattrapage"): {"sujet": 136625, "corrige": 136833},
    (2023, "normale"):    {"sujet": 142477, "corrige": 142482},
    (2023, "rattrapage"): {"sujet": 142485, "corrige": 142488},
    (2024, "normale"):    {"sujet": 145764, "corrige": 145767},
    (2024, "rattrapage"): {"sujet": 145770, "corrige": 145773},
    (2025, "normale"):    {"sujet": 145797},  # pas encore de corrigé officiel
    (2025, "rattrapage"): {"sujet": 145800},  # pas encore de corrigé officiel
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
# Fallback : any .pdf link pointing to /assets/documents/course-
FALLBACK_RE = re.compile(r'href="([^"]+course-\d+/[^"]+\.pdf)"', re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def project_root() -> Path:
    """Répertoire backend/ (où se trouve data/)."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "data" / "exams").is_dir():
            return parent
    raise RuntimeError("Impossible de localiser backend/data/exams/")


def target_dir(year: int, session: str) -> Path:
    return project_root() / "data" / "exams" / "physique" / f"{year}-{session}" / "pdfs"


def fetch_pdf_url(element_id: int, session: requests.Session) -> Optional[str]:
    """
    Fait GET sur la page /element/<id> et retourne l'URL absolue du PDF.
    """
    url = f"{BASE}/element/{element_id}"
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"    ✗ HTTP error fetching {url}: {e}")
        return None

    html = r.text
    # 1) Chercher spécifiquement le lien "Téléchargez le document"
    m = PDF_LINK_RE.search(html)
    if not m:
        # 2) Fallback : premier lien PDF vers /assets/documents/course-NNN/
        m = FALLBACK_RE.search(html)
    if not m:
        print(f"    ✗ Aucun lien PDF trouvé sur {url}")
        return None

    pdf_url = m.group(1)
    # Décoder l'URL (ex: %70 -> p)
    pdf_url = unquote(pdf_url)
    # Rendre absolu si nécessaire
    if pdf_url.startswith("/"):
        pdf_url = urljoin(BASE, pdf_url)
    return pdf_url


def download_pdf(
    pdf_url: str, dest: Path, session: requests.Session, force: bool = False
) -> bool:
    """Télécharge le PDF vers dest. Retourne True si succès."""
    if dest.exists() and not force:
        print(f"    ✓ Déjà présent : {dest.name} ({dest.stat().st_size // 1024} KB)")
        return True

    try:
        r = session.get(pdf_url, headers=HEADERS, timeout=60, stream=True)
        r.raise_for_status()
    except Exception as e:
        print(f"    ✗ HTTP error downloading {pdf_url}: {e}")
        return False

    # Vérifier que c'est bien un PDF
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="re-télécharge même si présent")
    parser.add_argument("--year", type=int, help="ne traite que cette année")
    args = parser.parse_args()

    s = requests.Session()
    ok = 0
    fail = 0
    skipped = 0

    items = sorted(EXAMS.items())
    if args.year:
        items = [it for it in items if it[0][0] == args.year]
        if not items:
            print(f"Aucune entrée pour année {args.year}")
            return 1

    for (year, session), mapping in items:
        label = f"{year}-{session}"
        print(f"\n━━━ Physique {label} ━━━")
        out_dir = target_dir(year, session)
        out_dir.mkdir(parents=True, exist_ok=True)

        for kind, element_id in mapping.items():
            filename = f"examen-national-physique-chimie-{year}-{session}-{kind}.pdf"
            dest = out_dir / filename

            if dest.exists() and not args.force:
                size_kb = dest.stat().st_size // 1024
                if size_kb > 10:  # PDF valide si > 10 KB
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

            # Politesse : pause entre les requêtes
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
