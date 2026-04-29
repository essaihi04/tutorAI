"""
Audit de conformité du LLM au programme officiel 2BAC PC BIOF (Maroc).

Lance ~50 questions piégeuses (sujets HORS-PROGRAMME, pourcentages, demandes
ambiguës) contre le système de prompt en MODE LIBRE et détecte si le modèle :
  - enseigne du contenu hors-programme au lieu de refuser,
  - invente des pourcentages / chapitres absents du cadre officiel,
  - mélange programme PC avec SVT track / SM / français.

Génère un rapport Markdown : backend/scripts/audit_curriculum_report.md

Usage :
    cd backend
    python -m scripts.audit_curriculum_compliance
    # ou: python scripts/audit_curriculum_compliance.py [--limit 10] [--subject Maths]
"""
from __future__ import annotations

import argparse
import asyncio
import re
import sys
import time

# Fix Windows console encoding (cp1252 chokes on ∞, π, etc.)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ── Stub heavy ML deps BEFORE importing LLMService ───────────────────────
# rag_service.py top-level imports torch/torchcodec which fail on this box.
# We don't need RAG retrieval for the audit: the DETERMINISTIC official
# program block (OFFICIAL_WEIGHTS + _OFF_PROGRAM_TOPICS) we audit is built
# WITHOUT RAG. So we stub get_rag_service() to return a no-op object.
import types as _types
_stub_rag = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service():  # noqa
    return _NoopRag()
_stub_rag.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub_rag

from app.config import get_settings  # type: ignore  # noqa: E402
from app.services.llm_service import LLMService  # type: ignore  # noqa: E402

# Belt-and-suspenders: also no-op the lazy init in case it's called
LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


REFUSE_REQUIRED = [
    r"(?i)(pas\s+au\s+programme|hors[- ]programme|n'est\s+pas\s+au)",
]


@dataclass
class TestCase:
    subject: str
    query: str
    expect: str  # "refuse" or "answer"
    forbidden: list = field(default_factory=list)
    required: list = field(default_factory=list)
    note: str = ""


CASES: list = [
    # ── MATHS HORS PROGRAMME ─────────────────────────────────────────────
    TestCase("Mathematiques", "Explique-moi le théorème du rang et la dimension d'un espace vectoriel",
             expect="refuse",
             forbidden=[r"(?i)\bth[éeè]or[èe]me\s+du\s+rang\b", r"(?i)dim\s*\(?\s*ker"],
             required=REFUSE_REQUIRED, note="Algèbre linéaire = SM"),
    TestCase("Mathematiques", "Donne-moi un cours sur la diagonalisation des matrices",
             expect="refuse",
             forbidden=[r"(?i)diagonali[sz]", r"(?i)valeurs\s+propres"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Comment calculer un déterminant 3x3 par la règle de Sarrus ?",
             expect="refuse",
             forbidden=[r"(?i)sarrus", r"(?i)d[ée]terminant\s+3"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Apprends-moi l'arithmétique modulaire et les congruences",
             expect="refuse",
             forbidden=[r"(?i)congruen", r"(?i)classe\s+r[ée]siduelle"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Explique-moi la loi normale et l'écart-type pour le BAC PC",
             expect="refuse",
             forbidden=[r"(?i)loi\s+normale", r"(?i)gauss"],
             required=REFUSE_REQUIRED, note="Seule la loi binomiale est au programme"),
    TestCase("Mathematiques", "Comment résoudre une équation différentielle de Riccati ?",
             expect="refuse",
             forbidden=[r"(?i)riccati"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Étudie une courbe paramétrée x(t)=cos(t), y(t)=sin(2t)",
             expect="refuse",
             forbidden=[r"(?i)courbe\s+param[ée]tr"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Démontre la convergence de la série harmonique",
             expect="refuse",
             forbidden=[r"(?i)s[ée]rie\s+harmonique"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Calcule l'intégrale impropre de 1/x² sur [1, +∞[",
             expect="refuse",
             forbidden=[r"(?i)int[ée]grale\s+impropre", r"(?i)g[ée]n[ée]ralis[ée]e"],
             required=REFUSE_REQUIRED),
    TestCase("Mathematiques", "Définis un groupe et un anneau commutatif",
             expect="refuse",
             forbidden=[r"(?i)structure\s+alg"],
             required=REFUSE_REQUIRED),

    # ── MATHS AU PROGRAMME ───────────────────────────────────────────────
    TestCase("Mathematiques", "Comment résoudre l'équation différentielle y'' + 4y = 0 ?",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme", r"(?i)hors[- ]programme"],
             required=[r"(?i)cos|sin|exp|caract[ée]ristique"],
             note="y''+ay'+by=0 EST au programme (1.2.24)"),
    TestCase("Mathematiques", "Donne-moi le cours sur l'intégration par parties",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)int[ée]gration\s+par\s+parties|IPP"],
             note="IPP EST au programme (1.3.1)"),
    TestCase("Mathematiques", "Explique la loi binomiale B(n,p)",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)binomial|B\(n"],
             note="Loi binomiale EST au programme (2.5.6)"),
    TestCase("Mathematiques", "Comment calculer l'argument et le module d'un nombre complexe ?",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)module|arg(ument)?"]),

    # ── PHYSIQUE HORS PROGRAMME ──────────────────────────────────────────
    TestCase("Physique", "Explique-moi la dilatation du temps en relativité restreinte",
             expect="refuse",
             forbidden=[r"(?i)dilatation\s+du\s+temps", r"(?i)Lorentz"],
             required=REFUSE_REQUIRED),
    TestCase("Physique", "Donne le 1er principe de la thermodynamique avec ΔU = Q + W",
             expect="refuse",
             forbidden=[r"(?i)1er\s+principe", r"(?i)entropie"],
             required=REFUSE_REQUIRED),
    TestCase("Physique", "Démontre les équations de Maxwell de l'électromagnétisme",
             expect="refuse",
             forbidden=[r"(?i)maxwell"],
             required=REFUSE_REQUIRED),
    TestCase("Physique", "Comment former une image avec une lentille convergente ?",
             expect="refuse",
             forbidden=[r"(?i)lentille\s+convergente", r"(?i)foyer"],
             required=REFUSE_REQUIRED, note="Optique géométrique = 1ère"),
    TestCase("Physique", "Explique l'équation de Schrödinger Hψ = Eψ",
             expect="refuse",
             forbidden=[r"(?i)schr[öo]dinger", r"(?i)fonction\s+d'?onde"],
             required=REFUSE_REQUIRED),
    TestCase("Physique", "Énonce le théorème d'Ampère pour le calcul du champ magnétique",
             expect="refuse",
             forbidden=[r"(?i)th[ée]or[èe]me\s+d'?amp[èe]re"],
             required=REFUSE_REQUIRED),
    TestCase("Physique", "Comment l'équation de Bernoulli s'applique-t-elle à un fluide ?",
             expect="refuse",
             forbidden=[r"(?i)bernoulli"],
             required=REFUSE_REQUIRED),

    # ── PHYSIQUE AU PROGRAMME ────────────────────────────────────────────
    TestCase("Physique", "Quelle est l'équation différentielle d'un circuit RC en régime libre ?",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)RC|τ", r"(?i)charge|d[ée]charge|condensateur"]),
    TestCase("Physique", "Décris la décroissance radioactive et la constante λ",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)d[ée]croissance|N\s*=\s*N", r"(?i)λ|demi-vie|t1/2"]),
    TestCase("Physique", "Quelles sont les ondes mécaniques progressives ?",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)onde",
                       r"(?i)c[ée]l[ée]rit[ée]|longueur\s+d'?onde|λ|propag|p[ée]riode|fr[ée]quence|transvers|longitudin"]),

    # ── CHIMIE HORS PROGRAMME ────────────────────────────────────────────
    TestCase("Chimie", "Explique le mécanisme SN2 d'une substitution nucléophile",
             expect="refuse",
             forbidden=[r"(?i)\bSN2\b", r"(?i)nucl[ée]ophile"],
             required=REFUSE_REQUIRED),
    TestCase("Chimie", "Donne le cours sur les alcanes et leur nomenclature IUPAC",
             expect="refuse",
             forbidden=[r"(?i)CnH2n\+2", r"(?i)IUPAC"],
             required=REFUSE_REQUIRED),
    TestCase("Chimie", "Comment lire un spectre RMN du proton ?",
             expect="refuse",
             forbidden=[r"(?i)\bRMN\b", r"(?i)d[ée]placement\s+chimique"],
             required=REFUSE_REQUIRED),
    TestCase("Chimie", "Calcule l'enthalpie standard de réaction avec la loi de Hess",
             expect="refuse",
             forbidden=[r"(?i)enthalpie", r"(?i)loi\s+de\s+hess"],
             required=REFUSE_REQUIRED),
    TestCase("Chimie", "Décris la maille cubique faces centrées",
             expect="refuse",
             forbidden=[r"(?i)cubique\s+faces?\s+centr", r"(?i)compacit[ée]"],
             required=REFUSE_REQUIRED),
    TestCase("Chimie", "Explique l'équation de Nernst pour calculer un potentiel d'électrode",
             expect="refuse",
             forbidden=[r"(?i)nernst", r"(?i)0[,.]059"],
             required=REFUSE_REQUIRED, note="Nernst détaillée = SM"),
    TestCase("Chimie", "Donne la formule de Henderson-Hasselbalch pour un tampon",
             expect="refuse",
             forbidden=[r"(?i)henderson|hasselbalch"],
             required=REFUSE_REQUIRED),

    # ── CHIMIE AU PROGRAMME ──────────────────────────────────────────────
    TestCase("Chimie", "Explique l'estérification et son équilibre",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)est[ée]rification", r"(?i)acide|alcool|rendement|[ée]quilibre"]),
    TestCase("Chimie", "Définis le quotient de réaction Qr et la constante d'équilibre K",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)quotient", r"(?i)constante\s+d'?[ée]quilibre|K"]),
    TestCase("Chimie", "Comment fonctionne une pile Daniell ?",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)pile|[ée]lectrode", r"(?i)anode|cathode|Zn|Cu"]),

    # ── SVT HORS PROGRAMME (track SVT, pas PC) ───────────────────────────
    TestCase("SVT", "Explique-moi la photosynthèse et le cycle de Calvin",
             expect="refuse",
             forbidden=[r"(?i)photosynth[èe]se", r"(?i)cycle\s+de\s+calvin"],
             required=REFUSE_REQUIRED, note="Photosynthèse = SVT track"),
    TestCase("SVT", "Décris la réponse immunitaire spécifique et les lymphocytes B et T",
             expect="refuse",
             forbidden=[r"(?i)lymphocytes?\s+[BT]", r"(?i)anticorps"],
             required=REFUSE_REQUIRED),
    TestCase("SVT", "Comment fonctionne un neurone et la transmission synaptique ?",
             expect="refuse",
             forbidden=[r"(?i)neurone", r"(?i)synap"],
             required=REFUSE_REQUIRED),
    TestCase("SVT", "Explique la régulation de la glycémie par l'insuline et le glucagon",
             expect="refuse",
             forbidden=[r"(?i)insuline", r"(?i)glucagon"],
             required=REFUSE_REQUIRED),
    TestCase("SVT", "Donne le cours sur la reproduction humaine et le cycle menstruel",
             expect="refuse",
             forbidden=[r"(?i)cycle\s+menstruel", r"(?i)ovulation"],
             required=REFUSE_REQUIRED),
    TestCase("SVT", "Décris la sélection naturelle et la théorie de l'évolution",
             expect="refuse",
             forbidden=[r"(?i)s[ée]lection\s+naturelle", r"(?i)darwin"],
             required=REFUSE_REQUIRED),
    TestCase("SVT", "Explique les chaînes alimentaires dans un écosystème",
             expect="refuse",
             forbidden=[r"(?i)cha[îi]ne\s+alimentaire", r"(?i)producteur|consommateur"],
             required=REFUSE_REQUIRED),

    # ── SVT AU PROGRAMME ─────────────────────────────────────────────────
    TestCase("SVT", "Décris la respiration cellulaire et la production d'ATP",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)respiration|mitoch", r"(?i)ATP|krebs|glycolyse"]),
    TestCase("SVT", "Comment se déroule la méiose et le brassage génétique ?",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)m[ée]iose", r"(?i)brassage|chromosome|gam[èe]te"]),
    TestCase("SVT", "Explique la subduction et la formation des chaînes de montagnes",
             expect="answer",
             forbidden=[r"(?i)pas\s+au\s+programme"],
             required=[r"(?i)subduction", r"(?i)cha[îi]nes?|tectonique"]),

    # ── PIÈGES MIXTES — pourcentages inventés ────────────────────────────
    TestCase("SVT", "Quel pourcentage représente la photosynthèse dans l'examen SVT 2BAC PC ?",
             expect="refuse",
             forbidden=[r"(?i)photosynth[èe]se.{0,30}\d+\s*%",
                        r"(?i)\d+\s*%.{0,30}photosynth[èe]se"],
             required=[r"(?i)pas\s+au\s+programme|hors[- ]programme|n'est\s+pas\s+au"]),
    TestCase("Mathematiques", "Donne-moi la répartition exacte des points de l'examen de maths PC en %",
             expect="answer",
             # Forbid mentions of off-program topics WITHIN A WEIGHT/% context
             # (we don't penalize a parenthetical "pas d'algèbre linéaire").
             forbidden=[r"(?i)alg[èe]bre\s+lin[ée]aire\s*[:\-]?\s*\d+\s*%",
                        r"(?i)\d+\s*%[^\n]{0,40}alg[èe]bre\s+lin[ée]aire",
                        r"(?i)matrices?\s*[:\-]?\s*\d+\s*%"],
             required=[r"(?i)analyse|suites?|complexes?|probabilit"],
             note="Doit citer Analyse 55%, Algèbre-Géométrie 15%+30%"),
]


@dataclass
class CaseResult:
    case: TestCase
    response: str
    elapsed_s: float
    passed: bool
    failures: list = field(default_factory=list)


def evaluate(case: TestCase, response: str):
    """Evaluate a case.

    For expect=refuse cases : the LLM may legitimately MENTION the off-program
    topic name inside its refusal (e.g. "Ce sujet (Diagonalisation) n'est pas
    au programme"). So if a clear refusal pattern is present, FORBIDDEN
    matches are tolerated — what matters is that the refusal itself is there.

    For expect=answer cases : forbidden patterns must NOT appear (the LLM
    must not refuse a topic that IS at the program), and required patterns
    must appear (real teaching content).
    """
    failures = []
    text = response or ""

    # Required patterns must always be present
    required_missing = [pat for pat in case.required if not re.search(pat, text)]
    for pat in required_missing:
        failures.append(f"REQUIRED missing: /{pat}/")

    # Forbidden patterns: tolerated if a clear refusal exists in expect=refuse
    has_refusal = bool(re.search(REFUSE_REQUIRED[0], text))
    if case.expect == "refuse" and has_refusal:
        # Genuine refusal — don't penalize topic name mentions inside refusal
        pass
    else:
        for pat in case.forbidden:
            if re.search(pat, text):
                failures.append(f"FORBIDDEN match: /{pat}/")

    return (len(failures) == 0), failures


async def run_case(client, api_key, base_url, system_prompt, case):
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case.query},
        ],
        "temperature": 0.3,
        "max_tokens": 600,
        "stream": False,
    }
    t0 = time.time()
    try:
        resp = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=60.0,
        )
        resp.raise_for_status()
        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""
    except Exception as e:
        content = f"[ERROR: {e}]"
    dt = time.time() - t0
    passed, failures = evaluate(case, content)
    return CaseResult(case=case, response=content, elapsed_s=dt, passed=passed, failures=failures)


async def main(limit: Optional[int] = None, subject_filter: Optional[str] = None):
    settings = get_settings()
    api_key = getattr(settings, "deepseek_api_key", None) or getattr(settings, "DEEPSEEK_API_KEY", None)
    base_url = getattr(settings, "deepseek_base_url", None) or "https://api.deepseek.com/v1"
    if not api_key:
        print("[FATAL] DEEPSEEK_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    cases = CASES
    if subject_filter:
        cases = [c for c in cases if subject_filter.lower() in c.subject.lower()]
    if limit:
        cases = cases[:limit]

    print(f"[AUDIT] Running {len(cases)} cases against DeepSeek …")
    llm = LLMService()

    results = []
    async with httpx.AsyncClient() as client:
        for i, case in enumerate(cases, 1):
            system_prompt = llm.build_libre_prompt(
                language="français",
                student_name="Audit",
                proficiency="intermédiaire",
                user_query=case.query,
            )
            r = await run_case(client, api_key, base_url, system_prompt, case)
            results.append(r)
            status = "PASS" if r.passed else "FAIL"
            print(f"[{i:02d}/{len(cases)}] {status:4s} ({r.elapsed_s:5.1f}s) {case.subject:14s} {case.query[:70]}")
            for f in r.failures:
                print(f"        -> {f}")

    passed_n = sum(1 for r in results if r.passed)
    failed_n = len(results) - passed_n
    refuse_cases = [r for r in results if r.case.expect == "refuse"]
    answer_cases = [r for r in results if r.case.expect == "answer"]
    refuse_pass = sum(1 for r in refuse_cases if r.passed)
    answer_pass = sum(1 for r in answer_cases if r.passed)

    out = []
    out.append("# Audit conformité programme BAC 2BAC PC BIOF — Rapport\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append("\n## Résumé\n")
    out.append(f"- **Total cas** : {len(results)}")
    out.append(f"- **Réussis** : {passed_n} ({100*passed_n/max(len(results),1):.0f}%)")
    out.append(f"- **Échecs** : {failed_n}")
    out.append(f"- Refus attendus (HORS-PROGRAMME) : {refuse_pass}/{len(refuse_cases)}")
    out.append(f"- Réponses attendues (au programme) : {answer_pass}/{len(answer_cases)}\n")

    fails = [r for r in results if not r.passed]
    if fails:
        out.append(f"\n## Échecs ({len(fails)})\n")
        for r in fails:
            out.append(f"### [{r.case.subject}] expect={r.case.expect} — {r.case.query}")
            if r.case.note:
                out.append(f"_Note_ : {r.case.note}")
            out.append("**Échecs détectés :**")
            for f in r.failures:
                out.append(f"- {f}")
            out.append("**Réponse LLM :**\n")
            snippet = r.response[:1500].strip()
            if len(r.response) > 1500:
                snippet += "\n…[tronqué]"
            out.append("```\n" + snippet + "\n```\n")

    out.append("\n## Détail complet\n")
    for r in results:
        flag = "PASS" if r.passed else "FAIL"
        out.append(f"- [{flag}] `{r.case.subject}` (expect={r.case.expect}) — {r.case.query}")

    report_path = Path(__file__).parent / "audit_curriculum_report.md"
    report_path.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[AUDIT] Rapport : {report_path}")
    print(f"[AUDIT] Score : {passed_n}/{len(results)} réussis ({100*passed_n/max(len(results),1):.0f}%)")
    sys.exit(0 if failed_n == 0 else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--subject", type=str, default=None)
    args = parser.parse_args()
    asyncio.run(main(limit=args.limit, subject_filter=args.subject))

