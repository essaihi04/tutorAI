"""
Audit du NIVEAU 2BAC — vérifie que les réponses du LLM aux questions
LÉGITIMES (au programme) restent au niveau lycée 2BAC PC BIOF.

Contrairement à audit_curriculum_compliance.py (qui teste le SCOPE
programme/hors-programme), ce script teste le NIVEAU PÉDAGOGIQUE :
- aucune formule supérieure (espaces vectoriels, lagrangien, ΔG, RMN...)
- aucun vocabulaire universitaire (endomorphisme, opérateur, tenseur...)
- aucune notation universitaire (∇·, ∂, polynôme caractéristique...)
- aucune méthode hors-programme (preuves ε-δ, séries entières...)

Sortie : scripts/audit_level_2bac_report.md
Aucune latence runtime — script offline pur, à lancer en CI.

Usage :
    python scripts/audit_level_2bac.py [--limit N] [--subject Maths]
"""
from __future__ import annotations

import argparse
import asyncio
import re
import sys
import time

# Fix Windows console encoding
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

# Stub heavy ML deps before importing LLMService
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

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ──────────────────────────────────────────────────────────────────────
#  Mots-clés / patterns interdits par matière (jargon universitaire)
# ──────────────────────────────────────────────────────────────────────
OFF_LEVEL_PATTERNS_BY_SUBJECT: dict[str, list[str]] = {
    "Mathematiques": [
        # Algèbre linéaire / sup
        r"(?i)\bespace[s]?\s+vectoriel",
        r"(?i)\bendomorphisme",
        r"(?i)\bbase\s+canonique",
        r"(?i)\bpolyn[ôo]me\s+caract[ée]ristique",
        r"(?i)\bdiagonalis(?:ation|er|able)",
        r"(?i)\bvaleur[s]?\s+propre",
        r"(?i)\bvecteur[s]?\s+propre",
        r"(?i)\bd[ée]terminant\s+(?:d['e ]une\s+matrice|de\s+la\s+matrice)",
        r"(?i)\bapplication\s+lin[ée]aire",
        # Topologie / analyse sup
        r"(?i)\bespace\s+m[ée]trique",
        r"(?i)\bcompl[ée]tude\b",
        r"(?i)\bconvergence\s+uniforme",
        r"(?i)\bcrit[èe]re\s+de\s+(?:Cauchy|d['Aa]lembert|Leibniz)",
        r"(?i)\bs[ée]rie[s]?\s+enti[èe]re",
        r"(?i)\bint[ée]grale\s+impropre",
        r"(?i)\b[ée]?quivalent\s+asymptotique",
        # Notations / opérateurs sup
        r"(?i)\bjacobien\b",
        r"(?i)\bdiff[ée]omorphisme",
        r"\b∇·\b", r"\b∇×\b",
        r"(?i)\bd[ée]riv[ée]e[s]?\s+partielle",
        # Probabilités / stats sup
        r"(?i)\bmesure\s+de\s+probabilit[ée]",
        r"(?i)\btribu\s+bor[ée]lienne",
        r"(?i)\bloi\s+normale\b",
        r"(?i)\bloi\s+de\s+Poisson",
    ],
    "Physique": [
        # Mécanique avancée
        r"(?i)\bformalisme\s+lagrangien",
        r"(?i)\bhamiltonien",
        r"(?i)\b[ée]quation[s]?\s+d['e ]Euler-Lagrange",
        r"(?i)\bprincipe\s+de\s+moindre\s+action",
        # Quantique / relativité
        r"(?i)\b[ée]quation\s+de\s+Schr[ôö]dinger",
        r"(?i)\brelativit[ée]\s+restreinte",
        r"(?i)\bdilatation\s+du\s+temps",
        r"(?i)\btransformation\s+de\s+Lorentz",
        # EM avancé
        r"(?i)\b[ée]quations?\s+de\s+Maxwell",
        r"(?i)\bth[ée]or[èe]me\s+d['e ]Amp[èe]re",
        r"(?i)\btransform[ée]e\s+de\s+Fourier",
        # Thermo / fluides hors PC
        r"(?i)\b1er\s+principe\s+de\s+la\s+thermodynamique",
        r"(?i)\bsecond\s+principe\b",
        r"(?i)\bentropie\s+de\s+Boltzmann",
        r"(?i)\b[ée]quation\s+de\s+Bernoulli",
        r"(?i)\bcycle\s+de\s+Carnot",
        # Optique géométrique
        r"(?i)\bformule\s+de\s+conjugaison",
        r"(?i)\brelation\s+de\s+Descartes",
        r"(?i)\blentille\s+(?:convergente|divergente)",
        # Notations sup
        r"(?i)\bnabla\b",
        r"\b∇·\b", r"\b∇×\b",
    ],
    "Chimie": [
        r"(?i)\b[ée]quation\s+de\s+Nernst",
        r"(?i)\bHenderson[- ]?Hasselbalch",
        r"(?i)\bloi\s+de\s+Hess",
        r"(?i)\benthalpie\s+(?:standard|libre)",
        r"(?i)\b[ée]nergie\s+libre\s+de\s+Gibbs",
        r"(?i)\b[ΔΔ]G\s*=\s*[ΔΔ]H",
        r"(?i)\bm[ée]canisme\s+SN[12]",
        r"(?i)\bm[ée]canisme\s+E[12]",
        r"(?i)\bspectre\s+RMN",
        r"(?i)\bnomenclature\s+IUPAC",
        r"(?i)\borbital[e]?[s]?\s+hybrid",
        r"(?i)\bth[ée]orie\s+VSEPR",
        r"(?i)\bdiagramme\s+E[- ]?pH",
        r"(?i)\bmaille\s+cubique",
        r"(?i)\bcristallographie",
    ],
    "SVT": [
        r"(?i)\bcycle\s+de\s+Calvin",
        r"(?i)\bphotosynth[èe]se",  # SVT track but not PC
        r"(?i)\blymphocyte[s]?\s+B\s+et\s+T",
        r"(?i)\bsynapse\b",
        r"(?i)\binsuline\b.*\bglucagon",
        r"(?i)\bs[ée]lection\s+naturelle",
        r"(?i)\bcha[îi]nes?\s+alimentaires?",
        r"(?i)\b(?:PCR|CRISPR|s[ée]quen[çc]age)\b",
        r"(?i)\bHardy[- ]?Weinberg",
        r"(?i)\bcycle\s+menstruel",
    ],
}


@dataclass
class LevelTestCase:
    subject: str
    query: str
    notes: str = ""
    # Optional positive patterns: at least ONE must appear (proves the LLM
    # actually answered the question rather than refusing). Only useful for
    # questions whose topic is genuinely at-program.
    must_contain_any: list[str] = field(default_factory=list)


# 32 questions LÉGITIMES au programme 2BAC PC BIOF — la réponse doit
# enseigner correctement, sans dériver vers le supérieur.
CASES: list[LevelTestCase] = [
    # ── MATHÉMATIQUES (au programme) ──────────────────────────────────
    LevelTestCase("Mathematiques", "Comment dériver la fonction f(x) = x³·ln(x) ?",
                  notes="Dérivation produit + ln, programme PC.",
                  must_contain_any=[r"(?i)d[ée]riv|f'\s*\("]),
    LevelTestCase("Mathematiques", "Calcule la limite de (sin(x)/x) quand x tend vers 0",
                  notes="Limite classique au programme.",
                  must_contain_any=[r"(?i)limit|=\s*1"]),
    LevelTestCase("Mathematiques", "Comment résoudre l'équation différentielle y' + 2y = 0 ?",
                  notes="EDO du 1er ordre — programme PC.",
                  must_contain_any=[r"(?i)e\^\{?-2", r"(?i)solution"]),
    LevelTestCase("Mathematiques", "Donne-moi la primitive de cos(2x)",
                  notes="Primitive standard.",
                  must_contain_any=[r"(?i)sin|primitive"]),
    LevelTestCase("Mathematiques", "Comment résoudre l'équation z² + z + 1 = 0 dans C ?",
                  notes="Nombres complexes au programme.",
                  must_contain_any=[r"(?i)complexe|discriminant|j\b|i\s*√"]),
    LevelTestCase("Mathematiques", "Étudie la suite u_(n+1) = 2*u_n + 3 avec u_0 = 1",
                  notes="Suite récurrente au programme.",
                  must_contain_any=[r"(?i)suite|r[ée]currente|g[ée]om[ée]trique"]),
    LevelTestCase("Mathematiques", "Calcule l'intégrale de e^(-x) entre 0 et 1",
                  notes="Intégrale propre au programme.",
                  must_contain_any=[r"(?i)int[ée]grale|=\s*1\s*-\s*"]),
    LevelTestCase("Mathematiques", "Comment trouver les racines d'un polynôme x³ - 3x² + 2 ?",
                  notes="Factorisation au programme.",
                  must_contain_any=[r"(?i)racine|factoris"]),

    # ── PHYSIQUE (au programme) ────────────────────────────────────────
    LevelTestCase("Physique", "Donne-moi le cours sur le mouvement d'un projectile",
                  notes="Mouvement dans un champ uniforme — programme PC.",
                  must_contain_any=[r"(?i)g\b|gravit|parabolique|trajectoire"]),
    LevelTestCase("Physique", "Comment fonctionne un dipôle RC en charge ?",
                  notes="Circuit RC au programme.",
                  must_contain_any=[r"(?i)RC|tau|τ|condensateur|charge"]),
    LevelTestCase("Physique", "Explique-moi la radioactivité alpha et bêta",
                  notes="Noyau / désintégration au programme.",
                  must_contain_any=[r"(?i)alpha|bêta|n[oô]yau|d[ée]sint[ée]gration"]),
    LevelTestCase("Physique", "Donne le cours sur les ondes mécaniques progressives",
                  notes="Ondes au programme.",
                  must_contain_any=[r"(?i)onde|c[ée]l[ée]rit[ée]|propag"]),
    LevelTestCase("Physique", "Comment calculer la période d'un pendule simple ?",
                  notes="Oscillateur mécanique au programme.",
                  must_contain_any=[r"(?i)p[ée]riode|2π|T\s*=|pendule"]),
    LevelTestCase("Physique", "Explique la diffraction d'une onde lumineuse",
                  notes="Diffraction — programme PC.",
                  must_contain_any=[r"(?i)diffract|fente|λ|longueur\s+d'?onde"]),
    LevelTestCase("Physique", "Comment fonctionne un dipôle RL en régime libre ?",
                  notes="Circuit RL au programme.",
                  must_contain_any=[r"(?i)RL|τ|tau|bobine|inductance"]),
    LevelTestCase("Physique", "Donne le cours sur la chute libre verticale d'un corps",
                  notes="Mécanique de base.",
                  must_contain_any=[r"(?i)g\b|9[,\.]\s*8|chute|gravit"]),

    # ── CHIMIE (au programme) ──────────────────────────────────────────
    LevelTestCase("Chimie", "Comment calcule-t-on un avancement de réaction chimique ?",
                  notes="Avancement / tableau d'avancement — programme PC.",
                  must_contain_any=[r"(?i)avancement|tableau|x\b|mol"]),
    LevelTestCase("Chimie", "Explique le titrage acide-base avec la phénolphtaléine",
                  notes="Titrage au programme.",
                  must_contain_any=[r"(?i)titrage|[ée]quivalence|pH|n[Aa]\s*v"]),
    LevelTestCase("Chimie", "Donne le cours sur l'estérification et l'hydrolyse",
                  notes="Esters au programme PC.",
                  must_contain_any=[r"(?i)estérification|hydrolyse|[ée]quilibre|carboxyl"]),
    LevelTestCase("Chimie", "Comment calculer le pH d'une solution d'acide fort ?",
                  notes="pH au programme.",
                  must_contain_any=[r"(?i)pH\s*=|log|H[+₃]O\+|concentration"]),
    LevelTestCase("Chimie", "Explique la cinétique chimique et le temps de demi-réaction",
                  notes="Cinétique au programme.",
                  must_contain_any=[r"(?i)cin[ée]tique|t1/2|demi-r[ée]action|vitesse"]),
    LevelTestCase("Chimie", "Comment fonctionne une pile électrochimique ?",
                  notes="Pile au programme PC.",
                  must_contain_any=[r"(?i)pile|[ée]lectrode|anode|cathode|[ée]lectron"]),
    LevelTestCase("Chimie", "Donne le cours sur les acides faibles et le pKa",
                  notes="pKa au programme.",
                  must_contain_any=[r"(?i)pKa|acide\s+faible|[ée]quilibre|Ka\b"]),
    LevelTestCase("Chimie", "Comment équilibrer une équation de réaction ?",
                  notes="Équilibrage de base.",
                  must_contain_any=[r"(?i)[ée]quilibr|conservation|coefficient"]),

    # ── SVT (au programme PC, niveau lycée) ────────────────────────────
    # NB : la SVT en PC se limite à des thèmes très restreints (déchets,
    # géologie de base). Pas photosynthèse, immunologie, neurone, etc.
    LevelTestCase("SVT", "Explique-moi la subduction et la formation des chaînes de montagnes",
                  notes="Géologie au programme PC.",
                  must_contain_any=[r"(?i)subduction|plaque|cha[îi]ne|tectonique"]),
    LevelTestCase("SVT", "Donne-moi le cours sur la valorisation des déchets organiques",
                  notes="Environnement / déchets — au programme PC.",
                  must_contain_any=[r"(?i)d[ée]chet|valoris|compost|m[ée]thanis"]),
    LevelTestCase("SVT", "Comment se forme un magma dans une zone de subduction ?",
                  notes="Géologie au programme PC.",
                  must_contain_any=[r"(?i)magma|fusion|p[ée]ridotite|hydrat"]),
    LevelTestCase("SVT", "Explique le métamorphisme et les faciès métamorphiques",
                  notes="Géologie — programme PC.",
                  must_contain_any=[r"(?i)m[ée]tamorphisme|faci[èe]s|pression|temp[ée]rature"]),

    # ── PIÈGES MIXTES — niveau adapté ──────────────────────────────────
    LevelTestCase("Mathematiques", "Que signifie 'continu' pour une fonction ?",
                  notes="Continuité — programme PC, mais sans définition ε-δ.",
                  must_contain_any=[r"(?i)continu|limit|graphe|tracer"]),
    LevelTestCase("Physique", "Pourquoi un satellite reste-t-il en orbite ?",
                  notes="Mouvement circulaire au programme.",
                  must_contain_any=[r"(?i)orbite|gravit|circulaire|attraction|Newton"]),
    LevelTestCase("Chimie", "Pourquoi un acide réagit-il avec un métal ?",
                  notes="Réaction acide-métal — programme.",
                  must_contain_any=[r"(?i)acide|m[ée]tal|H[+₂]|hydrog[èe]ne|[ée]lectron"]),
    LevelTestCase("Mathematiques", "Comment démontrer qu'une suite est croissante ?",
                  notes="Méthode étude de signe / récurrence.",
                  must_contain_any=[r"(?i)croissant|signe|u_n|r[ée]currence|d[ée]riv"]),
]


@dataclass
class CaseResult:
    case: LevelTestCase
    response: str
    elapsed_s: float
    passed: bool
    off_level_hits: list[str] = field(default_factory=list)
    missing_required: list[str] = field(default_factory=list)


def evaluate(case: LevelTestCase, response: str) -> CaseResult:
    text = response or ""

    # 1. Off-level patterns must NOT appear
    patterns = [re.compile(p) for p in OFF_LEVEL_PATTERNS_BY_SUBJECT.get(case.subject, [])]
    off_hits = []
    for pat in patterns:
        m = pat.search(text)
        if m:
            off_hits.append(m.group(0))

    # 2. Must contain at least ONE positive pattern (to ensure the LLM
    # didn't just refuse). A single match is enough.
    missing = []
    if case.must_contain_any:
        if not any(re.search(p, text) for p in case.must_contain_any):
            missing.append(" | ".join(case.must_contain_any))

    passed = (len(off_hits) == 0) and (len(missing) == 0)
    return CaseResult(
        case=case, response=text, elapsed_s=0.0,
        passed=passed, off_level_hits=off_hits, missing_required=missing,
    )


async def run_case(client, api_key, base_url, system_prompt, case: LevelTestCase):
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case.query},
        ],
        "temperature": 0.3,
        "max_tokens": 700,
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
    elapsed = time.time() - t0
    r = evaluate(case, content)
    r.elapsed_s = elapsed
    return r


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

    print(f"[AUDIT-NIVEAU] Running {len(cases)} cases against DeepSeek …")
    llm = LLMService()

    results: list[CaseResult] = []
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
            note = ""
            if r.off_level_hits:
                note = f" off-level=[{','.join(r.off_level_hits[:3])}]"
            if r.missing_required:
                note += " no-positive-match"
            print(f"[{i:02d}/{len(cases)}] {status:4s} ({r.elapsed_s:5.1f}s) {case.subject:14s} {case.query[:60]}{note}")

    passed_n = sum(1 for r in results if r.passed)
    failed_n = len(results) - passed_n

    out: list[str] = []
    out.append("# Audit niveau pédagogique 2BAC PC BIOF — Rapport\n")
    out.append(f"_Généré le {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")
    out.append("\n## Résumé\n")
    out.append(f"- **Total cas** : {len(results)}")
    out.append(f"- **Réussis** : {passed_n} ({100*passed_n/max(len(results),1):.0f}%)")
    out.append(f"- **Échecs** : {failed_n}")
    out.append("\n_Chaque cas pose une question LÉGITIME au programme. Le test échoue si :_")
    out.append("- _la réponse contient un terme/formule HORS-NIVEAU 2BAC (jargon supérieur), OU_")
    out.append("- _la réponse ne contient aucun élément attendu (refus à tort)._\n")

    fails = [r for r in results if not r.passed]
    if fails:
        out.append(f"\n## Échecs ({len(fails)})\n")
        for r in fails:
            out.append(f"### [{r.case.subject}] — {r.case.query}")
            if r.case.notes:
                out.append(f"_Note_ : {r.case.notes}")
            if r.off_level_hits:
                out.append(f"**🚨 Termes hors-niveau détectés** : `{', '.join(set(r.off_level_hits))}`")
            if r.missing_required:
                out.append(f"**❌ Aucun élément attendu** ({r.missing_required[0]})")
            out.append("**Réponse LLM (extrait) :**\n")
            snippet = r.response[:1500].strip()
            if len(r.response) > 1500:
                snippet += "\n…[tronqué]"
            out.append("```\n" + snippet + "\n```\n")

    out.append("\n## Détail complet\n")
    for r in results:
        flag = "PASS" if r.passed else "FAIL"
        out.append(f"- [{flag}] `{r.case.subject}` — {r.case.query}")

    report_path = Path(__file__).parent / "audit_level_2bac_report.md"
    report_path.write_text("\n".join(out), encoding="utf-8")
    print(f"\n[AUDIT-NIVEAU] Rapport : {report_path}")
    print(f"[AUDIT-NIVEAU] Score : {passed_n}/{len(results)} réussis ({100*passed_n/max(len(results),1):.0f}%)")
    sys.exit(0 if failed_n == 0 else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--subject", type=str, default=None)
    args = parser.parse_args()
    asyncio.run(main(limit=args.limit, subject_filter=args.subject))
