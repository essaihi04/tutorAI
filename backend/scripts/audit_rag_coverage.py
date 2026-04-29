"""
Audit de couverture RAG : compare les PDF du programme sur le disque avec
ceux effectivement indexés dans `data/rag_cache/`, et vérifie pour chaque
domaine du cadre de référence officiel qu'il existe au moins un chunk
correspondant dans la base RAG.

Sortie :
- scripts/audit_rag_coverage_report.md
- Code retour 1 si lacunes critiques détectées (PDF non indexés ou
  domaine du cadre de référence sans aucun chunk).

Aucun appel LLM, aucun chargement FAISS — script purement offline rapide.

Usage :
    python scripts/audit_rag_coverage.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
COURSES_DIR = ROOT / "cours 2bac pc"
CACHE_DIR = ROOT / "data" / "rag_cache"
CADRES_DIR = COURSES_DIR / "cadres de references 2BAC PC"

SUBJECT_DIRS = {
    "Math": COURSES_DIR / "Math",
    "PC": COURSES_DIR / "PC",
    "SVT": COURSES_DIR / "SVT",
}


def _normalize(s: str) -> str:
    """Lower-case, strip accents, drop punctuation — for keyword matching."""
    if not s:
        return ""
    repl = (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("â", "a"),
            ("î", "i"), ("ï", "i"), ("ô", "o"), ("ö", "o"), ("ù", "u"),
            ("û", "u"), ("ç", "c"), ("ë", "e"), ("'", " "), ("’", " "))
    s = s.lower()
    for a, b in repl:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _tokens(s: str, min_len: int = 4) -> set[str]:
    """Tokenize and drop stopwords / very short words."""
    STOP = {
        "dans", "pour", "avec", "cette", "celle", "leur", "leurs", "elle",
        "elles", "etre", "etre", "des", "les", "une", "ses", "qui", "que",
        "quoi", "donc", "selon", "vers", "sans", "sous", "sur", "ainsi",
        "entre", "alors", "plus", "mais", "tout", "tous", "toutes", "afin",
        "est", "sont", "ont", "fait", "faire", "etre", "leur", "soit",
        "pour", "non", "bien", "comme", "tres", "plus", "moins", "aux",
        "aux", "deux", "ainsi", "aussi", "etc", "the", "and", "for",
    }
    norm = _normalize(s)
    return {t for t in norm.split() if len(t) >= min_len and t not in STOP}


def load_caches() -> dict[str, dict]:
    """Load *_rag_cache.json files from data/rag_cache."""
    caches: dict[str, dict] = {}
    for p in CACHE_DIR.glob("*_rag_cache.json"):
        key = p.stem.replace("_rag_cache", "").lower()
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            caches[key] = data
        except Exception as e:
            print(f"[WARN] Failed to load {p.name}: {e}")
    return caches


def list_disk_pdfs() -> dict[str, list[Path]]:
    """List PDFs present on disk by subject."""
    out = {}
    for subject, d in SUBJECT_DIRS.items():
        if d.exists():
            out[subject] = sorted(d.glob("*.pdf"))
        else:
            out[subject] = []
    return out


# ─── Cadre de référence parsing ──────────────────────────────────────
def _walk_strings(node, out: list[str]):
    """Collect all string fields from a JSON cadre de référence."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and len(v) > 3:
                out.append(v)
            else:
                _walk_strings(v, out)
    elif isinstance(node, list):
        for v in node:
            _walk_strings(v, out)


def extract_cadre_domains() -> dict[str, list[dict]]:
    """
    Parse the 3 cadre de référence JSONs.
    Return per-subject list of {name, keywords} for each top-level domain.
    """
    out: dict[str, list[dict]] = {"Mathématiques": [], "Physique-Chimie": [], "SVT": []}
    if not CADRES_DIR.exists():
        return out

    for path in CADRES_DIR.glob("*.json"):
        name = path.name.lower()
        if "maths" in name:
            subject = "Mathématiques"
        elif "physique-chimie" in name:
            subject = "Physique-Chimie"
        elif "svt" in name:
            subject = "SVT"
        else:
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] Cannot parse {path.name}: {e}")
            continue

        # Cadres come in 3 incompatible shapes:
        #   - SVT  : top-level list of {nom, ...} domain dicts
        #   - PC   : list[1] -> {content_structure_physics, content_structure_chemistry}
        #            with nested sub_domains[].title
        #   - Math : list of pages with `section`/`content` fields
        # Strategy: walk the whole JSON; treat any dict that has a sub_domains
        # list as a domain. As a fallback, treat each top-level dict with a
        # `nom` / `title` / `section` field and substantive nested text as a
        # domain.
        domains = []

        def _harvest(node, ancestors_title: str = ""):
            if isinstance(node, dict):
                title = (node.get("nom") or node.get("name") or node.get("titre")
                         or node.get("title") or node.get("domaine")
                         or node.get("domaine_principal")
                         or node.get("section") or "").strip()
                # Trigger a domain when sub_domains/sous_sections is present.
                sub_list = (node.get("sub_domains")
                            or node.get("sous_sections")
                            or node.get("sous_domaines"))
                if isinstance(sub_list, list) and title:
                    parent_title = title
                    # Add the parent domain itself.
                    strings: list[str] = []
                    _walk_strings(node, strings)
                    kw = sorted(_tokens(" ".join(strings), min_len=5))[:30]
                    domains.append({"name": parent_title, "keywords": kw})
                    # Each sub_domain becomes its own (more granular) entry.
                    for sd in sub_list:
                        if not isinstance(sd, dict):
                            continue
                        sd_title = (sd.get("title") or sd.get("nom")
                                    or sd.get("titre") or "").strip()
                        if not sd_title:
                            continue
                        strs: list[str] = []
                        _walk_strings(sd, strs)
                        kws = sorted(_tokens(" ".join(strs), min_len=5))[:30]
                        domains.append({
                            "name": f"{parent_title} → {sd_title}",
                            "keywords": kws,
                        })
                    # Don't recurse further into this branch (already harvested).
                    return
                # Generic dict: continue descent.
                for k, v in node.items():
                    _harvest(v, ancestors_title=title or ancestors_title)
            elif isinstance(node, list):
                for v in node:
                    _harvest(v, ancestors_title=ancestors_title)

        _harvest(data)

        # Fallback for cadres without sub_domains: SVT-style list of domain dicts.
        if not domains and isinstance(data, list):
            for d in data:
                if not isinstance(d, dict):
                    continue
                nm = (d.get("nom") or d.get("name") or d.get("titre")
                      or d.get("title") or d.get("domaine") or "").strip()
                if not nm:
                    continue
                strs: list[str] = []
                _walk_strings(d, strs)
                kws = sorted(_tokens(" ".join(strs), min_len=5))[:30]
                domains.append({"name": nm, "keywords": kws})

        # Final fallback for Math cadre (page-based): treat each page section
        # as a domain. Skip purely cosmetic/admin sections.
        ADMIN_SECTIONS = {
            "introductory letter", "title page", "instructions and conclusion",
            "header", "footer", "memo", "table of contents", "preface",
            "introduction",
        }
        if not domains and isinstance(data, list):
            for d in data:
                if isinstance(d, dict) and d.get("section"):
                    section_name = str(d["section"]).strip()
                    if section_name.lower() in ADMIN_SECTIONS:
                        continue  # Skip cover / intro pages
                    strs: list[str] = []
                    _walk_strings(d, strs)
                    kws = sorted(_tokens(" ".join(strs), min_len=5))[:30]
                    if kws:
                        domains.append({
                            "name": section_name,
                            "keywords": kws,
                        })

        out[subject] = domains
    return out


def index_chunks_by_subject(caches: dict[str, dict]) -> dict[str, list[str]]:
    """Concatenate chunk texts per subject for fast keyword scanning."""
    by_subject: dict[str, list[str]] = defaultdict(list)
    name_map = {"math": "Mathématiques", "pc": "Physique-Chimie", "svt": "SVT"}
    for key, cache in caches.items():
        subject = name_map.get(key, key)
        for d in cache.get("documents", []):
            txt = d.get("text") or ""
            if txt.strip():
                by_subject[subject].append(_normalize(txt))
    return by_subject


def domain_coverage_score(keywords: list[str], chunk_texts: list[str]) -> tuple[int, int]:
    """Return (matched_keywords, total_keywords)."""
    if not keywords:
        return (0, 0)
    if not chunk_texts:
        return (0, len(keywords))
    matched = 0
    blob = " ".join(chunk_texts)
    for kw in keywords:
        if kw in blob:
            matched += 1
    return (matched, len(keywords))


# ─── Main ────────────────────────────────────────────────────────────
def main():
    print("[AUDIT-RAG] Loading caches & disk inventory …")
    caches = load_caches()
    disk = list_disk_pdfs()

    # ── A. PDFs on disk vs indexed ──────────────────────────────────
    pdf_audit: list[dict] = []
    for subject, pdfs in disk.items():
        cache = caches.get(subject.lower(), {})
        cached_hashes = cache.get("file_hashes", {}) or {}
        cached_files = set(cached_hashes.keys())
        chunks = cache.get("documents", []) or []
        chunk_count = len(chunks)
        # Group chunk count by source pdf
        per_pdf_chunks = defaultdict(int)
        for d in chunks:
            per_pdf_chunks[d.get("source", "?")] += 1

        for pdf in pdfs:
            indexed = pdf.name in cached_files
            stem = pdf.stem
            chunks_this = per_pdf_chunks.get(stem, 0)
            pdf_audit.append({
                "subject": subject, "pdf": pdf.name,
                "size_kb": pdf.stat().st_size // 1024,
                "indexed": indexed, "chunks": chunks_this,
            })

    # ── B. Cadres de référence coverage ─────────────────────────────
    print("[AUDIT-RAG] Parsing cadres de référence …")
    cadre_domains = extract_cadre_domains()
    chunks_by_subject = index_chunks_by_subject(caches)
    coverage_by_subject: dict[str, list[dict]] = {}
    for subject, domains in cadre_domains.items():
        # PC cadre maps to "Physique-Chimie" cache key but our
        # PC chunks live under "Physique-Chimie" subject. Same for SVT/Math.
        chunk_pool = chunks_by_subject.get(subject, [])
        if not chunk_pool and subject == "Mathématiques":
            chunk_pool = chunks_by_subject.get("Math", [])
        rows = []
        for d in domains:
            mk, tk = domain_coverage_score(d["keywords"], chunk_pool)
            rows.append({"name": d["name"], "matched": mk, "total": tk})
        coverage_by_subject[subject] = rows

    # ── Build report ────────────────────────────────────────────────
    out: list[str] = []
    out.append("# Audit de couverture RAG — Programme officiel 2BAC PC BIOF\n")

    out.append("## A. PDFs du programme — état d'indexation\n")
    out.append("| Matière | PDFs sur disque | Indexés | Non indexés | Chunks total |")
    out.append("|---|---:|---:|---:|---:|")
    for subject in ("Math", "PC", "SVT"):
        rows = [r for r in pdf_audit if r["subject"] == subject]
        n_total = len(rows)
        n_idx = sum(1 for r in rows if r["indexed"])
        n_miss = n_total - n_idx
        n_chunks = sum(r["chunks"] for r in rows)
        flag = "✅" if n_miss == 0 else "⚠️"
        out.append(f"| {flag} {subject} | {n_total} | {n_idx} | {n_miss} | {n_chunks} |")

    missing_pdfs = [r for r in pdf_audit if not r["indexed"]]
    if missing_pdfs:
        out.append("\n### PDFs non indexés (à traiter)\n")
        for r in missing_pdfs:
            out.append(f"- `{r['subject']}/{r['pdf']}` ({r['size_kb']} KB)")
    else:
        out.append("\n_Tous les PDFs disponibles sont indexés._\n")

    out.append("\n## B. Domaines du cadre de référence — couverture par chunks RAG\n")
    out.append("Score = nb mots-clés du domaine présents dans au moins un chunk indexé.\n")

    critical_gaps = []
    for subject, rows in coverage_by_subject.items():
        if not rows:
            out.append(f"### {subject}\n_(Cadre de référence non parsé — structure JSON inattendue.)_\n")
            continue
        out.append(f"\n### {subject} — {len(rows)} domaine(s)\n")
        out.append("| Domaine | Match | Total | Couverture |")
        out.append("|---|---:|---:|---:|")
        for r in rows:
            pct = (100 * r["matched"] / r["total"]) if r["total"] else 0
            flag = "✅" if pct >= 50 else ("⚠️" if pct >= 20 else "🚨")
            out.append(f"| {flag} {r['name']} | {r['matched']} | {r['total']} | {pct:.0f}% |")
            if pct < 20 and r["total"] > 0:
                critical_gaps.append(f"{subject} — {r['name']} ({pct:.0f}%)")

    out.append("\n## C. Résumé\n")
    out.append(f"- **PDFs non indexés** : {len(missing_pdfs)}")
    out.append(f"- **Domaines avec couverture < 20%** : {len(critical_gaps)}")
    if critical_gaps:
        out.append("\n### Domaines critiques\n")
        for g in critical_gaps:
            out.append(f"- 🚨 {g}")

    report = CACHE_DIR.parent.parent / "scripts" / "audit_rag_coverage_report.md"
    report.write_text("\n".join(out), encoding="utf-8")
    print(f"[AUDIT-RAG] Rapport : {report}")
    print(f"[AUDIT-RAG] PDFs non indexés : {len(missing_pdfs)}  |  Domaines critiques : {len(critical_gaps)}")
    sys.exit(0 if (not missing_pdfs and not critical_gaps) else 1)


if __name__ == "__main__":
    main()
