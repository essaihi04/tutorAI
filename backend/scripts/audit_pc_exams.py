"""
Audit complet des examens Physique-Chimie pour toutes les annees.

Detecte :
  1. Documents (figures) referencees mais absentes de assets/
  2. Documents presents dans assets/ mais non referencees
  3. Questions qui mentionnent "figure N" sans avoir de doc attache
  4. Variables/grandeurs utilisees dans la correction mais absentes du contexte
  5. Total des points incoherent (somme questions vs declare)
  6. Corrections vides ou manquantes
  7. Contexte d'exercice trop court (< 80 caracteres) -> probable contexte manquant
  8. Questions mentionnant des variables nommees (V_A, C_B, etc.) sans
     definition trouvable dans le contexte

Usage : python backend/scripts/audit_pc_exams.py [--exam <id>]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
PHYSIQUE_DIR = ROOT / "data" / "exams" / "physique"

# Regex pour detecter des references explicites a une figure/document
FIG_REF = re.compile(r"\b(?:figure|sch[ée]ma|tableau|courbe|graphe|graphique|document|annexe)s?\s*(?:n[°\.\s]*)?(\d+|ci[-\s]?contre|ci[-\s]?dessous|ci[-\s]?dessus)", re.IGNORECASE)

# Variables typiques de physique-chimie : nom + indice
# V_A, V_BE, C_B, m(NaHSO3), pK_A, t_{1/2}, x_f, ...
VAR_REF = re.compile(r"\$([A-Za-z]_\{?[A-Za-z0-9,]+\}?(?:\([^)]+\))?)\$|\$([A-Za-z][A-Za-z]?)\$")

# Numerical values in question/correction that look like donnees
# ex : V_A = 20,0 mL, C_B = 0,10 mol/L
NUMERIC_DEF = re.compile(r"([A-Za-z][A-Za-z_0-9]*)\s*[=]\s*[-+]?\d")

# Detecte des affectations de valeur dans la correction (V_A = 20,0 mL)
# Format LaTeX : $V_A = 20,0\,\mathrm{mL}$ ou $V_{BE} = 9,6\,\mathrm{mL}$
VAR_VALUE_LATEX = re.compile(
    r"([A-Za-z](?:_(?:[A-Za-z0-9]|\{[^}]+\}))?)"   # nom + indice optionnel
    r"\s*=\s*"
    r"[-+]?\d+(?:[.,]\d+)?"                           # valeur numerique
    r"(?:\s*\\?(?:cdot|times|\*)?\s*10\^\{?-?\d+\}?)?"  # exposant optionnel
)


def gather_text(*chunks: str) -> str:
    return "\n".join(c or "" for c in chunks)


def extract_var_names(text: str) -> set[str]:
    """Recupere les noms de variables LaTeX-style ($V_A$, $C_B$, etc.)."""
    found = set()
    for m in VAR_REF.finditer(text or ""):
        v = (m.group(1) or m.group(2) or "").strip()
        if v and len(v) <= 20:
            # Normaliser : enlever {} et indices
            base = re.sub(r"[{}]", "", v)
            found.add(base)
    return found


def audit_exam(exam_path: Path, verbose: bool = False) -> dict:
    """Audit un seul examen. Retourne un dict de problemes detectes."""
    issues: list[str] = []
    warnings: list[str] = []

    try:
        with open(exam_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        return {"path": str(exam_path), "fatal": f"Impossible de lire JSON : {e}", "issues": [], "warnings": []}

    exam_dir = exam_path.parent
    assets_dir = exam_dir / "assets"
    asset_files = {p.name for p in assets_dir.glob("*")} if assets_dir.exists() else set()
    used_assets: set[str] = set()

    parts = data.get("parts", [])
    declared_total = data.get("total_points") or 20
    sum_points = 0.0

    for part in parts:
        for ex_idx, ex in enumerate(part.get("exercises", [])):
            ex_label = ex.get("name", f"Exercice {ex_idx+1}")[:60]
            ex_pts = ex.get("points", 0)
            ex_context = ex.get("context", "") or ""
            sum_points += ex_pts

            # ── (1) Contexte trop court ──
            if len(ex_context.strip()) < 80:
                warnings.append(
                    f"[{ex_label}] contexte tres court ({len(ex_context.strip())} car.) — donnees probablement manquantes"
                )

            # Map des doc ids declares dans cet exercice
            ex_docs = ex.get("documents", []) or []
            doc_ids = {d.get("id") for d in ex_docs if d.get("id")}

            # ── (2) Verifier que les fichiers des documents existent ──
            for d in ex_docs:
                src = d.get("src", "")
                if src.startswith("assets/"):
                    fname = src.split("/", 1)[1]
                    used_assets.add(fname)
                    if fname not in asset_files:
                        issues.append(f"[{ex_label}] doc {d.get('id')} pointe vers {src} qui N'EXISTE PAS")

            # ── Variables definies dans le contexte de l'exercice ──
            ctx_vars = extract_var_names(ex_context)
            ctx_text_lower = ex_context.lower()

            # Texte aggregant contexte + tous les enonces de question (pour validation amont)
            all_question_content = "\n".join(
                (q.get("content") or "") for q in ex.get("questions", [])
            )
            ex_full_text = ex_context + "\n" + all_question_content

            qpts = 0.0
            for q in ex.get("questions", []):
                qnum = q.get("number", "?")
                qcontent = q.get("content", "") or ""
                qcorr = (q.get("correction") or {}).get("content", "") or ""
                qpts += q.get("points", 0)

                if not qcontent.strip():
                    issues.append(f"[{ex_label}] Q{qnum} : contenu VIDE")
                if not qcorr.strip():
                    warnings.append(f"[{ex_label}] Q{qnum} : correction VIDE")

                # ── (3) Question mentionne "figure N" sans doc attache ──
                qrefs = q.get("documents", []) or []
                fig_mentions = FIG_REF.findall(qcontent)
                if fig_mentions and not qrefs:
                    issues.append(
                        f"[{ex_label}] Q{qnum} mentionne {fig_mentions} mais N'A AUCUN doc attache"
                    )

                # Verifier que les refs de doc existent dans l'exercice
                for ref in qrefs:
                    if ref not in doc_ids:
                        issues.append(f"[{ex_label}] Q{qnum} reference doc {ref} introuvable dans l'exercice")

                # ── (4) Variables utilisees dans correction mais pas dans contexte ──
                corr_vars = extract_var_names(qcorr)
                # Les variables suivantes sont autorisees sans definition (universelles)
                IMPLICIT = {"t", "x", "i", "u", "v", "K", "T", "f", "L", "C", "R", "m", "n",
                           "Q", "g", "h", "p", "E", "F", "G", "M", "N", "P", "U", "V",
                           "I", "k", "B", "A", "S", "H", "z", "y", "r", "d", "s",
                           "alpha", "beta", "gamma", "lambda", "omega", "phi", "theta",
                           "Delta", "ln", "log", "exp", "sin", "cos", "tan",
                           "infty", "epsilon", "circ", "dfrac", "frac", "sqrt", "left",
                           "right", "longrightarrow", "rightarrow", "approx", "times",
                           "cdot", "mathrm", "boxed", "stackrel", "AN", "iff", "Longleftrightarrow",
                           "begin", "end", "aligned", "cases", "longleftrightarrow", "rightleftharpoons"}
                missing_vars = []
                for v in corr_vars:
                    base = v.split("_")[0]
                    if (v in IMPLICIT or base in IMPLICIT or len(v) > 15
                            or v.startswith("\\") or v in ctx_vars):
                        continue
                    # Cherche le nom dans le contexte ou les questions precedentes
                    if v.lower() in ctx_text_lower or v in ex_context:
                        continue
                    # Tolerer si la lettre apparait quelque part dans le contexte
                    if re.search(r"\b" + re.escape(v) + r"\b", ex_context):
                        continue
                    missing_vars.append(v)
                if missing_vars and verbose:
                    warnings.append(
                        f"[{ex_label}] Q{qnum} correction utilise variables non definies dans le contexte : {missing_vars[:5]}"
                    )

                # ── (5) Question mentionne explicitement Partie 1/2 sans contexte de partie ──
                if re.search(r"partie\s*[12]", qcontent, re.IGNORECASE):
                    if not re.search(r"partie\s*[12]", ex_context, re.IGNORECASE):
                        warnings.append(
                            f"[{ex_label}] Q{qnum} mentionne 'Partie' mais pas de section Partie dans le contexte"
                        )

                # ── (6) Variables numeriques utilisees dans correction sans definition dans contexte ──
                # On collecte les "X = valeur" presentes dans la correction
                # Critere : variable AVEC indice (V_A, C_B, V_{BE}, t_{1/2}...) absente du contexte
                undefined_data = []
                for m in VAR_VALUE_LATEX.finditer(qcorr):
                    var = m.group(1)
                    # Skip si la variable n'a PAS d'indice (juste "V", "C", "T") -> ambigu
                    if "_" not in var:
                        continue
                    # Normaliser : V_{BE} -> V_BE, t_{1/2} -> t_1
                    var_norm = var.replace("{", "").replace("}", "")
                    # Verifier si la variable apparait dans le contexte de l'exercice
                    # On cherche "V_A", "V_{BE}", ou "VBE" (sans accolades)
                    patterns = [
                        re.escape(var) + r"\s*=",
                        re.escape(var_norm) + r"\s*=",
                    ]
                    # Chercher dans contexte + tous les enonces (pas dans les corrections
                    # des autres questions car on veut s'assurer que l'eleve VOIT la donnee)
                    found = False
                    for pat in patterns:
                        if re.search(pat, ex_full_text):
                            found = True
                            break
                    if found:
                        continue
                    # Tolerer si la valeur exacte est mentionnee
                    if m.group(0) in ex_full_text:
                        continue
                    undefined_data.append(var)
                if undefined_data:
                    # Dedupliquer
                    undefined_data = list(dict.fromkeys(undefined_data))
                    if len(undefined_data) >= 2:
                        # 2+ variables non definies = forte presomption de contexte manquant
                        issues.append(
                            f"[{ex_label}] Q{qnum} correction utilise {len(undefined_data)} valeurs numeriques "
                            f"non definies dans le contexte : {undefined_data[:6]} — DONNEES MANQUANTES ?"
                        )
                    elif verbose:
                        warnings.append(
                            f"[{ex_label}] Q{qnum} correction utilise valeur non definie : {undefined_data}"
                        )

            # ── (6) Total points exercice ──
            if abs(qpts - ex_pts) > 0.01:
                issues.append(
                    f"[{ex_label}] points incoherents : declare {ex_pts}, somme questions {qpts}"
                )

    # ── (7) Total examen ──
    if abs(sum_points - declared_total) > 0.01:
        issues.append(f"Total declare {declared_total} != somme exercices {sum_points}")

    # ── (8) Assets orphelins ──
    orphans = asset_files - used_assets
    # Filtrer les fichiers metadata
    orphans = {f for f in orphans if not f.startswith(".") and f.lower().endswith((".png", ".jpg", ".jpeg", ".svg"))}
    if orphans:
        warnings.append(f"Images presentes mais non referencees : {sorted(orphans)}")

    return {
        "path": str(exam_path.relative_to(ROOT)),
        "id": exam_dir.parent.name + "_" + exam_dir.name,
        "issues": issues,
        "warnings": warnings,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--exam", help="Auditer un seul examen (ex: 2025-normale)", default=None)
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--issues-only", action="store_true", help="N'afficher que les vrais problemes (pas les warnings)")
    args = ap.parse_args()

    if args.exam:
        targets = [PHYSIQUE_DIR / args.exam / "exam.json"]
    else:
        targets = sorted(PHYSIQUE_DIR.glob("*/exam.json"))

    total_issues = 0
    total_warnings = 0
    total_clean = 0

    print(f"Audit de {len(targets)} examen(s) Physique-Chimie\n" + "=" * 70)

    for path in targets:
        if not path.exists():
            print(f"\n  [SKIP] {path} introuvable")
            continue
        report = audit_exam(path, verbose=args.verbose)
        name = path.parent.name
        n_iss = len(report.get("issues", []))
        n_warn = len(report.get("warnings", []))
        total_issues += n_iss
        total_warnings += n_warn
        if "fatal" in report:
            print(f"\n[FATAL] {name} : {report['fatal']}")
            continue
        if n_iss == 0 and (args.issues_only or n_warn == 0):
            total_clean += 1
            if not args.issues_only:
                continue
        flag = "[!!]" if n_iss else "[ok]" if n_warn == 0 else "[~~]"
        print(f"\n{flag} {name}  ({n_iss} issues, {n_warn} warnings)")
        for s in report["issues"]:
            print(f"   ISSUE: {s}")
        if not args.issues_only:
            for s in report["warnings"]:
                print(f"   warn:  {s}")

    print("\n" + "=" * 70)
    print(f"Total : {total_issues} issues, {total_warnings} warnings sur {len(targets)} examens")
    print(f"Examens sans probleme : {total_clean}")
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
