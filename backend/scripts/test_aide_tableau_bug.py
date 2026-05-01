"""
Reproduction test — « Aide au tableau » répond sur la mauvaise leçon.

Scénario observé par l'utilisateur (cf. captures écran) :
  • Le chat a discuté de « Consommation matière organique / Respiration cellulaire ».
  • L'élève ouvre un examen SVT 2024 Rattrapage Exercice 2 (question sur le
    gène PRG / progranuline — GÉNÉTIQUE).
  • L'élève clique sur « Aide au tableau ».
  • L'assistant répond avec un tableau sur la RESPIRATION CELLULAIRE
    (matière organique, mitochondrie, ATP) au lieu de la génétique.

Ce script reproduit la situation EXACTE que le WebSocket handler met en place :
  1) build_libre_prompt(user_query=texte_envoyé_par_le_bouton) — comme prod.
  2) exam_view_block annexé contenant l'énoncé réel de la génétique — comme prod.
  3) historique chat précédent sur la respiration — comme prod.
  4) Appel LLM streaming et vérification :
       - réponse parle de génétique (PRG, gène, progranuline, neurone…) ✅
       - réponse NE parle PAS principalement de respiration cellulaire ❌

Sortie : pass/fail + extrait de la réponse + diagnostic du prompt.

Usage :
    python backend/scripts/test_aide_tableau_bug.py
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
import types as _types
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Stub heavy ML deps so we can import LLMService without loading FAISS.
_stub = _types.ModuleType("app.services.rag_service")
class _NoopRag:
    def build_grounded_context(self, *a, **kw): return ""
    def search(self, *a, **kw): return []
def _get_rag_service(): return _NoopRag()
_stub.get_rag_service = _get_rag_service  # type: ignore
sys.modules["app.services.rag_service"] = _stub

from app.config import get_settings  # noqa: E402
from app.services.llm_service import LLMService, llm_service  # noqa: E402

LLMService._ensure_rag_initialized = lambda self: None  # type: ignore


# ──────────────────────────────────────────────────────────────────────
#  Données du scénario réel (capture écran utilisateur)
# ──────────────────────────────────────────────────────────────────────
EXAM_VIEW = {
    "exam_id": "svt_2024_rattrapage",
    "subject": "SVT",
    "year": 2024,
    "session": "Rattrapage",
    "exam_title": "SVT 2024 Rattrapage",
    "exercise_index": 1,
    "exercise_total": 3,
    "exercise_name": "Exercice 2",
    "topic": "Génétique humaine",
    "question_number": 1,
    "question_total": 3,
    "question_points": 0.75,
    "question_type": "open",
    "question_content": (
        "En se basant sur les données du document 1, décrire le mode "
        "d'action de la progranuline sur les cellules nerveuses puis "
        "montrer la relation entre le taux plasmatique de la progranuline "
        "et l'état de santé de la personne."
    ),
    "question_correction": (
        "Le document 1 montre que la progranuline (codée par le gène PRG) "
        "agit sur les cellules nerveuses en assurant leur survie. Plus le "
        "taux plasmatique de progranuline est faible, plus le risque de "
        "dégénérescence neuronale et de maladies neurodégénératives est élevé."
    ),
}

# Historique chat AVANT le clic « Aide au tableau » — l'élève parlait de respiration.
PRIOR_HISTORY = [
    {"role": "user", "content": "Bonjour, je veux réviser la consommation matière organique."},
    {"role": "assistant", "content": "Très bien ! On va revoir la respiration cellulaire et le bilan énergétique."},
    {"role": "user", "content": "Donne-moi le bilan de la respiration cellulaire."},
    {"role": "assistant", "content": "C6H12O6 + 6O2 → 6CO2 + 6H2O + énergie (ATP). La respiration a lieu dans la mitochondrie."},
    {"role": "user", "content": "Et la fermentation lactique alors ?"},
    {"role": "assistant", "content": "La fermentation lactique se fait dans le hyaloplasme, sans dioxygène. Le bilan : glucose → 2 lactate + 2 ATP."},
]

# Le message exact que handleExplain() du frontend envoie au backend.
USER_CLICK_MESSAGE = (
    "Explique-moi comment résoudre la question 1 au tableau, donne-moi la méthode."
)


# ──────────────────────────────────────────────────────────────────────
#  Reproduction du build de prompt côté serveur (libre + exam_view_block)
# ──────────────────────────────────────────────────────────────────────
def build_exam_view_block(view: dict) -> str:
    """Reproduit fidèlement session_handler:1614-1640."""
    subject = str(view.get("subject", "") or "").strip()
    year = str(view.get("year", "") or "").strip()
    session = str(view.get("session", "") or "").strip()
    exam_title = str(view.get("exam_title", "") or "").strip()
    exercise_name = str(view.get("exercise_name", "") or "").strip()
    ex_idx = view.get("exercise_index")
    ex_total = view.get("exercise_total")
    q_num = view.get("question_number")
    q_total = view.get("question_total")
    q_content = str(view.get("question_content", "") or "").strip()
    q_correction = str(view.get("question_correction", "") or "").strip()
    q_points = view.get("question_points")

    session_label = session.capitalize() if session else ""
    header_bits = [b for b in [subject, session_label, str(year)] if b]
    header = " — ".join(header_bits) if header_bits else (exam_title or "Examen")

    ex_ref = exercise_name or (f"Exercice {ex_idx + 1}" if isinstance(ex_idx, int) else "")
    if isinstance(ex_idx, int) and isinstance(ex_total, int) and ex_total > 1:
        ex_ref = f"{ex_ref} ({ex_idx + 1}/{ex_total})"

    q_ref = ""
    if q_num is not None:
        q_ref = f"Question {q_num}" + (f"/{q_total}" if q_total else "")
        if q_points is not None:
            q_ref += f" ({q_points} pt)"

    block = f"""
[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ À L'ÉTUDIANT]
⚠️ L'étudiant a CE PANNEAU D'EXAMEN ouvert en ce moment. Tu DOIS te baser EXCLUSIVEMENT sur ces informations.

📚 Examen : {header}
📖 {ex_ref}
❓ {q_ref}

ÉNONCÉ EXACT DE LA QUESTION AFFICHÉE :
{q_content if q_content else '(non disponible)'}
"""
    if q_correction:
        block += f"\nCORRECTION OFFICIELLE DE CETTE QUESTION :\n{q_correction}\n"
    return block


# Topic / leak detection
GENETIQUE_KW = [
    r"\bPRG\b", r"progranulin", r"g[èe]ne", r"all[èe]le", r"chromosome",
    r"neurodeg", r"d[ée]g[ée]n[ée]rescence neuronal", r"prot[ée]ine prg",
]
RESPIRATION_KW = [
    r"respiration cellulaire", r"mitochondrie", r"\bATP\b",
    r"\bC6H12O6\b", r"glucose\s*\+\s*O2", r"krebs", r"glycolyse",
    r"fermentation\s+lactique", r"chaîne respiratoire",
]


def count_hits(text: str, patterns: list[str]) -> int:
    return sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))


def build_enriched_query(student_text: str, view: dict) -> str:
    """Reproduit l'enrichissement appliqué par session_handler après le fix
    (cf. session_handler.py §1559-1591)."""
    blob = " ".join(filter(None, [
        str(view.get("subject", "") or ""),
        str(view.get("topic", "") or ""),
        str(view.get("exercise_name", "") or ""),
        str(view.get("question_content", "") or "")[:600],
        str(view.get("question_correction", "") or "")[:600],
    ])).strip()
    return (student_text + " " + blob).strip() if blob else student_text


# ──────────────────────────────────────────────────────────────────────
def diagnose_prompt(label: str, user_query: str) -> dict:
    """Construit le libre_prompt comme prod et compte les signaux topicaux."""
    libre = llm_service.build_libre_prompt(
        language="français",
        student_name="Élève",
        proficiency="intermédiaire",
        user_query=user_query,
    )
    exam_block = build_exam_view_block(EXAM_VIEW)
    full = libre + "\n\n" + exam_block

    g_libre = count_hits(libre, GENETIQUE_KW)
    r_libre = count_hits(libre, RESPIRATION_KW)
    has_genetics_protocol = "GENETICS_BOARD_PROTOCOL" in libre or "ÉCHIQUIER" in libre.upper() or "PROTOCOLE GÉNÉTIQUE" in libre.upper()

    print(f"\n┌── {label}")
    print(f"│   user_query envoyé à build_libre_prompt = {user_query[:140]!r}{'…' if len(user_query) > 140 else ''}")
    print(f"│   taille libre_prompt              : {len(libre):>6d} chars")
    print(f"│   mots-clés génétique dans libre   : {g_libre}")
    print(f"│   mots-clés respiration dans libre : {r_libre}")
    print(f"│   protocole génétique injecté ?    : {'OUI ✅' if has_genetics_protocol else 'NON ❌'}")
    print(f"└──")
    return {
        "label": label,
        "libre": libre,
        "full": full,
        "g_libre": g_libre,
        "r_libre": r_libre,
        "has_genetics_protocol": has_genetics_protocol,
    }


async def llm_check(label: str, system_prompt: str) -> tuple[int, int, str]:
    settings = get_settings()
    api_key = (getattr(settings, "deepseek_api_key", None)
               or getattr(settings, "DEEPSEEK_API_KEY", None))
    base_url = (getattr(settings, "deepseek_base_url", None)
                or "https://api.deepseek.com/v1")
    if not api_key:
        return -1, -1, ""
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            *PRIOR_HISTORY,
            {"role": "user", "content": USER_CLICK_MESSAGE},
        ],
        "temperature": 0.3,
        "max_tokens": 1200,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=90.0) as client:
        resp = await client.post(
            f"{base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json=payload,
        )
        resp.raise_for_status()
        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""
    g = count_hits(content, GENETIQUE_KW)
    r = count_hits(content, RESPIRATION_KW)
    print(f"  → [{label}] LLM réponse — mots-clés génétique={g}  respiration={r}")
    return g, r, content


# ──────────────────────────────────────────────────────────────────────
async def main():
    print("=" * 78)
    print("DIAGNOSTIC — Reproduction du bug 'Aide au tableau'")
    print("=" * 78)
    print(f"Examen ouvert (frontend) : {EXAM_VIEW['subject']} {EXAM_VIEW['year']} "
          f"{EXAM_VIEW['session']} — {EXAM_VIEW['exercise_name']}")
    print(f"Topic interface          : {EXAM_VIEW['topic']}")
    print(f"Historique chat          : {len(PRIOR_HISTORY)} messages — sujet: respiration cellulaire")
    print(f"Click utilisateur        : {USER_CLICK_MESSAGE!r}")

    # ── Cas A : AVANT le fix — user_query = texte brut du bouton (générique)
    case_a = diagnose_prompt(
        label="A. AVANT FIX (user_query = texte générique du bouton)",
        user_query=USER_CLICK_MESSAGE,
    )

    # ── Cas B : APRÈS le fix — user_query enrichi avec contenu de la question
    enriched = build_enriched_query(USER_CLICK_MESSAGE, EXAM_VIEW)
    case_b = diagnose_prompt(
        label="B. APRÈS FIX (user_query enrichi avec question_content)",
        user_query=enriched,
    )

    # ── Verdict prompt-level (déterministe, sans LLM) ──
    print("\n" + "=" * 78)
    print("VERDICT — niveau prompt (déterministe)")
    print("=" * 78)
    delta_g = case_b["g_libre"] - case_a["g_libre"]
    print(f"  • Δ mots-clés génétique dans libre_prompt : +{delta_g}")
    print(f"  • Protocole génétique avant fix : "
          f"{'OUI' if case_a['has_genetics_protocol'] else 'NON'}")
    print(f"  • Protocole génétique après fix : "
          f"{'OUI' if case_b['has_genetics_protocol'] else 'NON'}")

    prompt_ok = (delta_g > 0) and case_b["has_genetics_protocol"] and not case_a["has_genetics_protocol"]
    if prompt_ok:
        print("\n  ✅ FIX VALIDÉ au niveau prompt — l'enrichissement fait passer "
              "le protocole génétique de OFF à ON et augmente la densité de "
              "mots-clés du sujet réel dans le libre_prompt.")
    elif case_b["has_genetics_protocol"] and case_a["has_genetics_protocol"]:
        print("\n  ⚠️  Le protocole génétique était déjà ON sans fix — le bug "
              "est ailleurs (bias de l'historique chat, RAG live).")
    else:
        print("\n  ❌ FIX NON VALIDÉ — le libre_prompt ne s'améliore pas.")

    # ── Vérif LLM (live, non-déterministe) si DEEPSEEK_API_KEY dispo ──
    print("\n" + "=" * 78)
    print("VÉRIFICATION LLM (live)")
    print("=" * 78)
    g_a, r_a, _ = await llm_check("AVANT FIX", case_a["full"])
    g_b, r_b, _ = await llm_check("APRÈS FIX", case_b["full"])

    if g_a < 0:
        print("  (DEEPSEEK_API_KEY absent — étape live ignorée.)")
        sys.exit(0 if prompt_ok else 1)

    print("\n  Synthèse :")
    print(f"    AVANT fix : génétique={g_a}, respiration={r_a}")
    print(f"    APRÈS fix : génétique={g_b}, respiration={r_b}")

    after_ok = (g_b >= 1 and r_b == 0)
    if prompt_ok and after_ok:
        print("\n  ✅ PASS — fix validé end-to-end (prompt + LLM).")
        sys.exit(0)
    if after_ok:
        print("\n  ✅ PASS — réponse LLM correcte après fix (prompt-level pas "
              "strictement requis).")
        sys.exit(0)
    print("\n  ❌ FAIL — la réponse LLM n'est pas centrée sur la génétique.")
    sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
