"""
Mock exam printable HTML generator.

Renders a mock exam (sujet or corrige) as a self-contained HTML page styled
like an official Moroccan BAC paper. The page is intended to be opened in
the browser and saved as PDF via Ctrl+P (the embedded ``@media print`` CSS
already produces a clean A4 layout with proper page-breaks).
"""
from __future__ import annotations

import html
import re
from typing import Any


# --------------------------------------------------------------------------- #
#  Inline content helpers
# --------------------------------------------------------------------------- #

def _md_inline(text: str) -> str:
    """Very light markdown: ``**bold**`` and ``*italic*``.

    Runs *after* HTML escaping so we re-introduce only the tags we need.
    LaTeX (``$...$`` / ``$$...$$``) is left untouched so KaTeX auto-render
    can pick it up client-side.
    """
    if not text:
        return ""
    s = html.escape(text)
    # **bold**
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    # *italic*  (avoid matching list bullets at line start by requiring a
    # non-space char on both sides)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)
    # Newlines → <br>
    s = s.replace("\n", "<br>")
    return s


def _doc_url(subject_norm: str, exam_id: str, src: str) -> str:
    """Resolve an image ``src`` (``assets/foo.png``) to a public URL."""
    if not src:
        return ""
    if src.startswith(("http://", "https://", "/")):
        return src
    return f"/static/mock-exams/{subject_norm}/{exam_id}/{src}"


# --------------------------------------------------------------------------- #
#  Block renderers
# --------------------------------------------------------------------------- #

def _render_documents(docs: list[dict], subject_norm: str, exam_id: str) -> str:
    if not docs:
        return ""
    out = ['<div class="documents">']
    for d in docs:
        title = d.get("title") or "Document"
        desc = d.get("description") or ""
        src = _doc_url(subject_norm, exam_id, d.get("src") or "")
        out.append('<figure class="doc">')
        out.append(f'<figcaption class="doc-title">{html.escape(title)}</figcaption>')
        if src:
            out.append(f'<img src="{html.escape(src)}" alt="{html.escape(title)}" class="doc-img"/>')
        if desc:
            out.append(f'<div class="doc-desc">{_md_inline(desc)}</div>')
        out.append("</figure>")
    out.append("</div>")
    return "\n".join(out)


def _render_choices(choices: list[dict]) -> str:
    if not choices:
        return ""
    out = ['<ol class="choices" type="a">']
    for c in choices:
        letter = c.get("letter") or ""
        text = c.get("text") or ""
        out.append(f'<li><span class="choice-letter">{html.escape(letter)})</span> {_md_inline(text)}</li>')
    out.append("</ol>")
    return "\n".join(out)


def _render_correction_block(corr: Any) -> str:
    """Render a correction block (sujet hides this; corrigé shows it)."""
    if not corr:
        return ""
    if isinstance(corr, dict):
        text = corr.get("content") or corr.get("correct_answer") or ""
    else:
        text = str(corr)
    if not text:
        return ""
    return (
        '<div class="correction">'
        '<div class="correction-label">Correction</div>'
        f'<div class="correction-body">{_md_inline(text)}</div>'
        "</div>"
    )


def _render_question(q: dict, subject_norm: str, exam_id: str, *, with_correction: bool, depth: int = 0) -> str:
    """Render a single question dict.

    Supports both flat questions (PC/Math style with ``number``, ``content``)
    and SVT-style group questions with ``sub_questions``/``choices``.
    """
    out = []
    number = q.get("number") or ""
    content = q.get("content") or ""
    pts = q.get("points")
    qtype = q.get("type") or ""

    cls = "q" if depth == 0 else "subq"
    out.append(f'<div class="{cls}">')
    head_bits = []
    if number:
        head_bits.append(f'<span class="q-num">{html.escape(str(number))}.</span>')
    head_bits.append(f'<span class="q-text">{_md_inline(content)}</span>')
    if pts is not None and pts != "":
        head_bits.append(f'<span class="q-points">({_format_points(pts)} pt)</span>')
    out.append('<div class="q-line">' + " ".join(head_bits) + "</div>")

    # QCM / Vrai-Faux choices at this level
    if q.get("choices"):
        out.append(_render_choices(q["choices"]))

    # Inline documents on the question
    inline_docs = q.get("documents")
    if inline_docs and inline_docs and isinstance(inline_docs[0], dict):
        out.append(_render_documents(inline_docs, subject_norm, exam_id))

    # Sub-questions
    for sq in q.get("sub_questions") or []:
        out.append(_render_question(sq, subject_norm, exam_id, with_correction=with_correction, depth=depth + 1))

    if with_correction:
        out.append(_render_correction_block(q.get("correction")))

    out.append("</div>")
    return "\n".join(out)


def _format_points(pts: Any) -> str:
    try:
        f = float(pts)
        if f == int(f):
            return str(int(f))
        return f"{f:g}".replace(".", ",")
    except Exception:
        return str(pts)


def _render_exercise(ex: dict, subject_norm: str, exam_id: str, *, with_correction: bool) -> str:
    out = ['<section class="exercise">']
    name = ex.get("name") or "Exercice"
    pts = ex.get("points")
    pts_str = f' <span class="ex-points">({_format_points(pts)} points)</span>' if pts is not None else ""
    out.append(f'<h2 class="ex-title">{_md_inline(name)}{pts_str}</h2>')

    # Theme/context
    if ex.get("theme"):
        out.append(f'<div class="ex-theme"><em>{_md_inline(ex["theme"])}</em></div>')
    if ex.get("context"):
        out.append(f'<div class="ex-context">{_md_inline(ex["context"])}</div>')

    # Top-level documents
    docs = ex.get("documents") or []
    if docs:
        out.append(_render_documents(docs, subject_norm, exam_id))

    # Questions
    for q in ex.get("questions") or []:
        out.append(_render_question(q, subject_norm, exam_id, with_correction=with_correction))

    out.append("</section>")
    return "\n".join(out)


def _render_part(part: dict, idx: int, subject_norm: str, exam_id: str, *, with_correction: bool) -> str:
    out = ['<section class="part">']
    name = part.get("name") or f"Partie {idx + 1}"
    pts = part.get("points")
    pts_str = f' <span class="part-points">({_format_points(pts)} points)</span>' if pts is not None else ""
    out.append(f'<h1 class="part-title">{_md_inline(name)}{pts_str}</h1>')

    if part.get("theme"):
        out.append(f'<div class="part-theme"><em>{_md_inline(part["theme"])}</em></div>')

    # Part-level documents (SVT Part 1)
    if part.get("documents"):
        out.append(_render_documents(part["documents"], subject_norm, exam_id))

    # Either nested exercises (PC/Math) or direct questions (SVT Part 1)
    if part.get("exercises"):
        for ex in part["exercises"]:
            out.append(_render_exercise(ex, subject_norm, exam_id, with_correction=with_correction))
    elif part.get("questions"):
        for q in part["questions"]:
            out.append(_render_question(q, subject_norm, exam_id, with_correction=with_correction))

    out.append("</section>")
    return "\n".join(out)


# --------------------------------------------------------------------------- #
#  Top-level template
# --------------------------------------------------------------------------- #

_FILIERE_BY_SUBJECT = {
    "svt": "Filière : Sciences Expérimentales — Option : Sciences de la Vie et de la Terre",
    "physique": "Filière : Sciences Expérimentales — Option : Sciences Physiques (PC) / SVT",
    "mathematiques": "Filière : Sciences Expérimentales / Sciences Mathématiques",
}

_SUBJECT_LABEL = {
    "svt": "Sciences de la Vie et de la Terre",
    "physique": "Physique-Chimie",
    "mathematiques": "Mathématiques",
}


def render_printable_html(
    exam: dict,
    subject_norm: str,
    *,
    variant: str = "sujet",
) -> str:
    """Build the standalone HTML for a mock exam (sujet or corrige)."""
    with_correction = variant == "corrige"
    exam_id = exam.get("id") or ""
    title = exam.get("title") or "Examen Blanc"
    subject_full = exam.get("subject_full") or _SUBJECT_LABEL.get(subject_norm, "")
    year = exam.get("year") or ""
    session_label = exam.get("session") or "Blanc"
    duration = exam.get("duration_minutes") or 180
    coefficient = exam.get("coefficient") or 5
    total_points = exam.get("total_points") or 20
    note = exam.get("note") or ""

    filiere = _FILIERE_BY_SUBJECT.get(subject_norm, "")
    matiere = _SUBJECT_LABEL.get(subject_norm, "")

    parts_html = "\n".join(
        _render_part(p, i, subject_norm, exam_id, with_correction=with_correction)
        for i, p in enumerate(exam.get("parts") or [])
    )

    # Standard BAC instructions block (used when exam.note is empty)
    default_note = (
        "L'usage de la calculatrice scientifique non programmable est autorisé. "
        "Le candidat peut traiter les exercices dans l'ordre de son choix. "
        "Les expressions littérales doivent être établies avant toute application numérique."
    )
    consigne = note or default_note

    variant_label = "CORRIGÉ" if with_correction else "SUJET"

    return f"""<!doctype html>
<html lang=\"fr\">
<head>
<meta charset=\"utf-8\"/>
<title>{html.escape(title)} — {variant_label}</title>
<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css\"/>
<script defer src=\"https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js\"></script>
<script defer src=\"https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js\"
  onload=\"renderMathInElement(document.body,{{delimiters:[
    {{left:'$$',right:'$$',display:true}},
    {{left:'$',right:'$',display:false}},
    {{left:'\\\\(',right:'\\\\)',display:false}},
    {{left:'\\\\[',right:'\\\\]',display:true}}
  ],throwOnError:false}});\"></script>
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ background: #f4f4f7; }}
  body {{
    font-family: 'Cambria','Times New Roman',Georgia,serif;
    color: #111;
    margin: 0;
    padding: 24px 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .page {{
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto 16px;
    padding: 18mm 18mm 22mm;
    background: #fff;
    box-shadow: 0 4px 20px rgba(0,0,0,.08);
    position: relative;
  }}
  /* Watermark for mock exams */
  .page::before {{
    content: "{'CORRIGÉ — EXAMEN BLANC' if with_correction else 'EXAMEN BLANC'}";
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: rotate(-30deg);
    font-size: 80px;
    font-weight: 800;
    color: rgba(180, 30, 30, 0.06);
    letter-spacing: 8px;
    pointer-events: none;
    z-index: 0;
  }}
  .page > * {{ position: relative; z-index: 1; }}

  /* ── Header ─────────────────────────────────────── */
  .official-header {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    text-align: center;
    border-bottom: 2px solid #111;
    padding-bottom: 8px;
    margin-bottom: 14px;
    font-size: 12.5px;
    line-height: 1.45;
  }}
  .official-header .ar {{ direction: rtl; font-family: 'Amiri','Times New Roman',serif; }}
  .official-header .ar p {{ margin: 0; }}
  .official-header .fr p {{ margin: 0; }}
  .official-header .crest {{
    width: 64px; height: 64px;
    border: 1.5px solid #111;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; font-weight: 800;
    background: #fff;
  }}
  .exam-banner {{
    text-align: center;
    margin: 10px 0 6px;
    padding: 6px 0;
    border-top: 1px solid #111;
    border-bottom: 1px solid #111;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}
  .exam-banner small {{ display:block; font-weight:600; font-size: 11px; letter-spacing: 4px; color:#a32424; margin-top:2px; }}
  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px 12px;
    border: 1px solid #111;
    padding: 6px 8px;
    margin: 8px 0 14px;
    font-size: 12.5px;
  }}
  .meta-grid b {{ font-weight: 700; }}
  .filiere {{ text-align:center; font-weight:700; font-size: 13px; margin: 6px 0 8px; }}
  .consigne {{
    border-left: 4px solid #a32424;
    background: #fcf6f6;
    padding: 8px 12px;
    margin: 8px 0 16px;
    font-size: 12.5px;
    line-height: 1.55;
  }}

  /* ── Body ─────────────────────────────────────── */
  .part-title {{
    font-size: 15px;
    margin: 16px 0 6px;
    padding: 6px 10px;
    background: #efeae0;
    border-left: 4px solid #a32424;
  }}
  .part-points, .ex-points, .q-points {{ font-weight: 600; color:#a32424; }}
  .part-theme {{ margin: -4px 0 8px 4px; font-size: 12.5px; color:#444; }}
  .ex-title {{
    font-size: 14px;
    margin: 14px 0 4px;
    padding-bottom: 2px;
    border-bottom: 1.5px solid #111;
  }}
  .ex-context {{ margin: 6px 0 10px; font-size: 13px; line-height: 1.55; text-align: justify; }}
  .ex-theme {{ font-size: 12.5px; color: #444; margin: 2px 0 6px; }}

  .exercise {{ break-inside: avoid; page-break-inside: avoid; }}

  .q, .subq {{ margin: 6px 0; font-size: 13px; line-height: 1.55; }}
  .subq {{ margin-left: 18px; }}
  .q-num {{ font-weight: 700; margin-right: 4px; }}
  .q-points {{ margin-left: 4px; font-size: 11.5px; }}

  .choices {{ margin: 4px 0 6px 22px; padding: 0; }}
  .choices li {{ margin: 2px 0; }}
  .choice-letter {{ font-weight: 700; margin-right: 4px; }}

  .documents {{ display:grid; grid-template-columns: 1fr; gap: 8px; margin: 8px 0 12px; }}
  .doc {{ border: 1px solid #ccc; border-radius: 6px; padding: 6px 8px; margin: 0; break-inside: avoid; page-break-inside: avoid; background:#fafafa; }}
  .doc-title {{ font-weight: 700; font-size: 12.5px; margin-bottom: 4px; }}
  .doc-img {{ max-width: 100%; max-height: 360px; display:block; margin: 4px auto; }}
  .doc-desc {{ font-size: 11.5px; color: #333; line-height: 1.5; font-style: italic; }}

  .correction {{
    margin: 6px 0 10px;
    background: #f1f7ee;
    border-left: 3px solid #2e7d32;
    padding: 8px 12px;
    font-size: 12.5px;
    line-height: 1.55;
  }}
  .correction-label {{
    font-weight: 700; color: #2e7d32; font-size: 11px;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;
  }}

  .footer {{
    margin-top: 20px;
    padding-top: 6px;
    border-top: 1px solid #999;
    font-size: 11px;
    text-align: center;
    color: #666;
  }}

  /* ── Toolbar (no print) ─────────────────────────── */
  .toolbar {{
    position: fixed; top: 12px; right: 12px; z-index: 999;
    display: flex; gap: 6px;
  }}
  .toolbar button {{
    background:#111; color:#fff; border:0; padding:8px 14px; font-size:13px;
    border-radius:8px; cursor:pointer; box-shadow: 0 4px 12px rgba(0,0,0,.2);
  }}
  .toolbar button:hover {{ background:#333; }}

  @media print {{
    html, body {{ background: #fff !important; padding: 0; margin:0; }}
    .toolbar {{ display:none !important; }}
    .page {{
      box-shadow: none !important;
      margin: 0 !important;
      padding: 14mm 14mm 14mm !important;
      width: auto;
      min-height: 0;
    }}
    @page {{ size: A4; margin: 12mm; }}
  }}
</style>
</head>
<body>
<div class=\"toolbar\">
  <button onclick=\"window.print()\">Imprimer / Sauvegarder PDF</button>
</div>
<div class=\"page\">
  <header class=\"official-header\">
    <div class=\"ar\">
      <p>المملكة المغربية</p>
      <p>وزارة التربية الوطنية والتعليم الأولي والرياضة</p>
      <p>المركز الوطني للتقويم والامتحانات والتوجيه</p>
    </div>
    <div class=\"crest\">★</div>
    <div class=\"fr\">
      <p>Royaume du Maroc</p>
      <p>Ministère de l'Éducation Nationale,<br/>du Préscolaire et des Sports</p>
      <p>Centre National d'Évaluation,<br/>des Examens et de l'Orientation</p>
    </div>
  </header>

  <div class=\"exam-banner\">
    Examen National du Baccalauréat — Session {html.escape(str(session_label))} {html.escape(str(year))}
    <small>Épreuve blanche — {variant_label}</small>
  </div>

  <div class=\"filiere\">{html.escape(filiere)}</div>

  <div class=\"meta-grid\">
    <div><b>Matière :</b> {html.escape(matiere)}</div>
    <div><b>Durée :</b> {html.escape(str(duration))} min</div>
    <div><b>Coefficient :</b> {html.escape(str(coefficient))}</div>
    <div><b>Total :</b> {_format_points(total_points)} points</div>
  </div>

  <div class=\"consigne\">{_md_inline(consigne)}</div>

  {parts_html}

  <div class=\"footer\">
    Examen blanc généré — {html.escape(exam_id)} · Tutorat BAC
  </div>
</div>
</body>
</html>"""
