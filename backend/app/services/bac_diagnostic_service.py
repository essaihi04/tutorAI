"""
BAC Diagnostic Service
Serves 20 real QCM questions from the BAC exam bank,
scores them, predicts a BAC note, and generates a personalized 28-day plan.
"""
import json
import random
from pathlib import Path
from typing import Optional


_BANK_PATH = Path(__file__).resolve().parents[2] / "data/diagnostic_qcm_bank.json"

# Domain → chapter / resource description for the plan
_DOMAIN_INFO: dict[str, dict] = {
    "Géologie": {
        "emoji": "🌋",
        "tasks": [
            "Réviser la tectonique des plaques (subduction, collision, obduction)",
            "Étudier les roches et le métamorphisme",
            "S'entraîner avec les schémas BAC de géologie",
        ],
    },
    "Génétique": {
        "emoji": "🧬",
        "tasks": [
            "Revoir les lois de Mendel et les croisements",
            "Pratiquer les exercices de génétique de transmission",
            "Étudier les mutations et maladies génétiques",
        ],
    },
    "Métabolisme énergétique": {
        "emoji": "⚡",
        "tasks": [
            "Maîtriser la glycolyse, le cycle de Krebs et la chaîne respiratoire",
            "Réviser la fermentation (alcoolique et lactique)",
            "S'entraîner avec les bilans énergétiques et les calculs ATP",
        ],
    },
    "Environnement": {
        "emoji": "♻️",
        "tasks": [
            "Étudier la gestion des déchets (compostage, biogaz, lixiviat)",
            "Réviser l'impact environnemental et l'effet de serre",
            "Mémoriser les définitions et les cycles",
        ],
    },
    "Neurophysiologie": {
        "emoji": "🧠",
        "tasks": [
            "Réviser l'influx nerveux et la synapse",
            "Étudier l'arc réflexe et l'intégration nerveuse",
            "S'entraîner avec les schémas de neurophysiologie",
        ],
    },
    "Chimie": {
        "emoji": "⚗️",
        "tasks": [
            "Réviser les acides/bases, l'électrolyse et les dosages",
            "Retravailler les équations chimiques et les calculs",
            "S'entraîner avec les exercices d'oxydoréduction",
        ],
    },
    "Mécanique": {
        "emoji": "⚙️",
        "tasks": [
            "Réviser les lois de Newton et la cinématique",
            "Étudier les oscillations (pendule, ressort)",
            "Pratiquer les problèmes de dynamique",
        ],
    },
    "Électricité": {
        "emoji": "🔌",
        "tasks": [
            "Réviser les circuits RC, RL et LC",
            "Étudier les régimes transitoires et permanent",
            "S'entraîner avec les calculs d'énergie électrique",
        ],
    },
    "Ondes": {
        "emoji": "〰️",
        "tasks": [
            "Réviser la propagation et la célérité des ondes",
            "Étudier la diffraction et les interférences",
            "Mémoriser les formules essentielles",
        ],
    },
    "SVT": {
        "emoji": "🔬",
        "tasks": [
            "Réviser les notions fondamentales de SVT",
            "S'entraîner avec les questions BAC de restitution",
            "Mémoriser les définitions clés",
        ],
    },
}


class BacDiagnosticService:
    def __init__(self):
        self._bank: Optional[dict] = None

    def _load_bank(self) -> dict:
        if self._bank is None:
            self._bank = json.loads(_BANK_PATH.read_text(encoding="utf-8"))
        return self._bank

    def get_questions(self, n_svt: int = 12, n_pc: int = 8) -> list[dict]:
        """
        Return n_svt SVT + n_pc PC questions randomly selected from the bank.
        Correct answers are stripped — sent separately at scoring time.
        """
        bank = self._load_bank()
        all_q = bank["questions"]

        svt_pool = [q for q in all_q if q["subject"] == "SVT"]
        pc_pool = [q for q in all_q if q["subject"] == "Physique-Chimie"]

        selected = (
            random.sample(svt_pool, min(n_svt, len(svt_pool)))
            + random.sample(pc_pool, min(n_pc, len(pc_pool)))
        )
        random.shuffle(selected)

        result = []
        for pos, q in enumerate(selected, 1):
            # Shuffle choice order so 'a' is not always correct
            choices = q["choices"][:]
            correct_text = next(
                (c["text"] for c in choices if c["letter"] == q["correct_answer"]), ""
            )
            random.shuffle(choices)
            # Re-letter after shuffle
            letters = "abcd"
            new_correct = "a"
            for i, c in enumerate(choices):
                c = dict(c)
                c["letter"] = letters[i]
                if c["text"] == correct_text:
                    new_correct = letters[i]
                choices[i] = c

            result.append({
                "id": q["id"],
                "position": pos,
                "subject": q["subject"],
                "domain": q.get("domain", ""),
                "year": q.get("year"),
                "session": q.get("session"),
                "content": q["content"],
                "choices": choices,
                "type": q.get("type", "qcm"),
                # correct_answer stored server-side only; sent back after submission
                "_correct": new_correct,
            })

        return result

    def score(self, session_questions: list[dict], answers: dict) -> dict:
        """
        Score the diagnostic given:
          session_questions: the list returned by get_questions() (with _correct field)
          answers: {str(position): letter_chosen, …}

        Returns full analysis + 28-day plan.
        """
        total = len(session_questions)
        n_correct = 0
        by_subject: dict[str, dict] = {}
        by_domain: dict[str, dict] = {}
        detailed: list[dict] = []

        for q in session_questions:
            pos = str(q["position"])
            user_ans = (answers.get(pos) or "").lower().strip()
            correct_ans = q.get("_correct", "").lower().strip()
            is_ok = user_ans == correct_ans and bool(user_ans)

            if is_ok:
                n_correct += 1

            subj = q["subject"]
            dom = q.get("domain") or subj

            by_subject.setdefault(subj, {"correct": 0, "total": 0})
            by_subject[subj]["total"] += 1
            if is_ok:
                by_subject[subj]["correct"] += 1

            by_domain.setdefault(dom, {"correct": 0, "total": 0, "subject": subj})
            by_domain[dom]["total"] += 1
            if is_ok:
                by_domain[dom]["correct"] += 1

            detailed.append({
                "position": q["position"],
                "subject": subj,
                "domain": dom,
                "content": q["content"],
                "choices": q.get("choices", []),
                "user_answer": user_ans,
                "correct_answer": correct_ans,
                "is_correct": is_ok,
            })

        bac_note = self._predict_bac_note(n_correct, total)
        gain_if_subscribed = self._compute_gain(n_correct, total)
        plan = self._build_28day_plan(by_domain)

        # Weak domains (worst first)
        weak = sorted(
            [
                {
                    "domain": d,
                    "subject": s["subject"],
                    "correct": s["correct"],
                    "total": s["total"],
                    "pct": round(s["correct"] / s["total"] * 100) if s["total"] else 0,
                }
                for d, s in by_domain.items()
            ],
            key=lambda x: x["pct"],
        )

        return {
            "score": n_correct,
            "total": total,
            "bac_note_predicted": bac_note,
            "gain_if_subscribed": gain_if_subscribed,
            "by_subject": {
                s: {
                    **v,
                    "pct": round(v["correct"] / v["total"] * 100) if v["total"] else 0,
                }
                for s, v in by_subject.items()
            },
            "by_domain": by_domain,
            "weak_domains": weak,
            "detailed": detailed,
            "plan": plan,
        }

    # ── private helpers ────────────────────────────────────────────────────

    def _predict_bac_note(self, score: int, total: int) -> float:
        if not total:
            return 10.0
        pct = score / total
        # Calibrated to Moroccan BAC: diagnostic is slightly harder than Part 1
        # but easier than the full exam. Mapping anchored to real BAC outcomes.
        if pct >= 0.90:
            return 17.0
        if pct >= 0.80:
            return 15.5
        if pct >= 0.70:
            return 13.5
        if pct >= 0.60:
            return 12.0
        if pct >= 0.50:
            return 10.5
        if pct >= 0.40:
            return 9.0
        if pct >= 0.30:
            return 7.5
        return 6.0

    def _compute_gain(self, score: int, total: int) -> float:
        """Estimated extra BAC points attainable with personalised coaching."""
        if not total:
            return 2.0
        pct = score / total
        # Students below 60% have the most to gain
        if pct < 0.40:
            return 3.5
        if pct < 0.60:
            return 2.5
        if pct < 0.75:
            return 1.5
        return 0.8

    def _build_28day_plan(self, by_domain: dict) -> list[dict]:
        """Generate a concrete 28-day study calendar from domain weakness map."""
        # Sort: weakest first
        sorted_domains = sorted(
            [(d, s) for d, s in by_domain.items() if s["total"] > 0],
            key=lambda x: x[1]["correct"] / x[1]["total"],
        )

        plan: list[dict] = []
        day = 1

        for domain, stats in sorted_domains:
            if day > 24:
                break
            pct = stats["correct"] / stats["total"] if stats["total"] else 0
            # Days allocated proportional to weakness
            if pct < 0.40:
                days = 4
            elif pct < 0.60:
                days = 3
            elif pct < 0.80:
                days = 2
            else:
                days = 1

            info = _DOMAIN_INFO.get(domain, _DOMAIN_INFO["SVT"])
            label = "🔴 Priorité haute" if pct < 0.40 else ("🟡 À renforcer" if pct < 0.70 else "🟢 À maintenir")

            plan.append({
                "day_start": day,
                "day_end": min(day + days - 1, 28),
                "subject": stats["subject"],
                "domain": domain,
                "emoji": info["emoji"],
                "score_pct": round(pct * 100),
                "label": label,
                "tasks": info["tasks"],
            })
            day += days

        # Sprint final — always add
        if day <= 28:
            plan.append({
                "day_start": day,
                "day_end": 28,
                "subject": "Tous",
                "domain": "Sprint final",
                "emoji": "🏁",
                "score_pct": None,
                "label": "🏁 Dernière ligne droite",
                "tasks": [
                    "Refaire les annales BAC des 3 dernières années (SVT + PC)",
                    "Réviser les formules et définitions essentielles",
                    "Passer un examen blanc complet en conditions réelles",
                ],
            })

        return plan


bac_diagnostic_service = BacDiagnosticService()
