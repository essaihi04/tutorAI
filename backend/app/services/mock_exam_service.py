"""
Mock Exam Service — AI-powered exam blanc generator.

Reads the curriculum (cadre de référence) and blueprint, samples real exam
questions as few-shot examples, and uses DeepSeek to generate a new exam
that is structurally and thematically faithful to the national BAC format.

Generated exams include text prompts for images (not images themselves);
the admin drops actual images into the assets/ folder before publishing.
"""
import json
import logging
import random
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
CURRICULUM_DIR = DATA_DIR / "curriculum"
EXAMS_DIR = DATA_DIR / "exams"
MOCK_EXAMS_DIR = DATA_DIR / "mock_exams"
MOCK_EXAMS_DIR.mkdir(parents=True, exist_ok=True)


# ─── Helpers ───────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def _call_deepseek(system: str, prompt: str, label: str, max_tokens: int = 8192) -> dict:
    """Call DeepSeek API and return parsed JSON."""
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.deepseek_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
    }
    logger.info(f"[MockExam:{label}] prompt ~{len(prompt)//4} tokens")
    async with httpx.AsyncClient(timeout=180.0) as client:
        resp = await client.post(settings.deepseek_api_url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
    content = data["choices"][0]["message"]["content"]
    finish = data["choices"][0].get("finish_reason", "")
    logger.info(f"[MockExam:{label}] response {len(content)} chars, finish={finish}")
    # Parse JSON (handle markdown fences)
    content = re.sub(r"^```(?:json)?\s*", "", content.strip())
    content = re.sub(r"\s*```$", "", content.strip())
    return json.loads(content)


# ─── Sample real exam questions for few-shot examples ──────────────────

def _sample_exercises(subject: str, domain: str, count: int = 3) -> list[dict]:
    """Pick `count` random real exercises from the exam bank for a domain."""
    subject_dir = EXAMS_DIR / subject.lower()
    if not subject_dir.exists():
        return []
    
    candidates = []
    for exam_dir in subject_dir.iterdir():
        exam_path = exam_dir / "exam.json"
        if not exam_path.exists():
            continue
        try:
            exam = _load_json(exam_path)
        except Exception:
            continue
        parts = exam.get("parts", [])
        if not parts:
            continue
        # Scan all parts — SVT uses parts[1], Math has exercises in any part
        for part in parts:
            for ex in part.get("exercises", []):
                # Simple domain matching via keywords
                if _exercise_matches_domain(ex, domain):
                    candidates.append({
                        "exam": f"{exam.get('year', '?')} {exam.get('session', '?')}",
                        "exercise": ex,
                    })
    random.shuffle(candidates)
    return candidates[:count]


def _exercise_matches_domain(ex: dict, domain: str) -> bool:
    """Check if exercise text matches a domain."""
    text = json.dumps(ex, ensure_ascii=False).lower()
    domain_keywords = {
        # SVT domains
        "consommation_matiere_organique": ["respiration", "fermentation", "glycolyse", "krebs", "atp", "mitochondri", "muscle", "contraction", "effort", "endurance"],
        "genetique_expression": ["gene", "allele", "mutation", "proteine", "transcri", "traduction", "codon", "arnm", "maladie"],
        "genetique_transmission": ["croisement", "f1", "f2", "dominant", "recessif", "echiquier", "dihybrid"],
        "geologie": ["subduction", "collision", "metamorphi", "magma", "plaque", "faille", "chaine"],
        "environnement_sante": ["pollution", "nitrate", "pesticide", "dechet", "step", "ozone", "co2", "rechauffement"],
        # Math domains
        "geometrie_espace": ["sphère", "sphere", "plan", "espace", "produit vectoriel", "cartésien", "paramétrique", "orthogon", "distance"],
        "nombres_complexes": ["complexe", "affixe", "module", "argument", "rotation", "similitude", "trigonométrique"],
        "probabilites": ["probabilit", "urne", "boule", "variable aléatoire", "espérance", "indépendan"],
        "suites_numeriques": ["suite", "récurrence", "convergent", "arithmétique", "géométrique"],
        "analyse_probleme": ["fonction", "dérivée", "intégr", "limite", "asymptote", "variation", "primitive"],
        # Physique-Chimie domains
        "chimie": ["dosage", "électrolyse", "pile", "acide", "base", "estérification", "hydrolyse", "pka", "ph"],
        "ondes": ["onde", "diffraction", "célérité", "longueur d'onde", "ultrason", "sonore"],
        "nucleaire": ["désintégration", "radioactiv", "demi-vie", "nucléaire", "noyau", "activité"],
        "electricite": ["condensateur", "dipôle", "rlc", "bobine", "modulation", "démodulation", "échelon"],
        "mecanique": ["chute", "mouvement", "pendule", "oscillateur", "satellite", "vitesse limite", "projectile"],
    }
    kws = domain_keywords.get(domain, [])
    return sum(1 for k in kws if k in text) >= 2


def _sample_part1_questions(subject: str, count: int = 5) -> list[dict]:
    """Pick Part1 questions as examples."""
    subject_dir = EXAMS_DIR / subject.lower()
    if not subject_dir.exists():
        return []
    
    candidates = []
    for exam_dir in subject_dir.iterdir():
        exam_path = exam_dir / "exam.json"
        if not exam_path.exists():
            continue
        try:
            exam = _load_json(exam_path)
        except Exception:
            continue
        parts = exam.get("parts", [])
        if not parts:
            continue
        for q in parts[0].get("questions", []):
            candidates.append({
                "exam": f"{exam.get('year', '?')} {exam.get('session', '?')}",
                "question": q,
            })
    random.shuffle(candidates)
    return candidates[:count]


# ─── Generation ────────────────────────────────────────────────────────

class MockExamService:

    def __init__(self):
        self._curriculum: dict = {}
        self._blueprint: dict = {}
    
    @staticmethod
    def _normalize_subject(subject: str) -> str:
        """Normalize subject name for filesystem paths."""
        s = subject.lower().strip()
        if s in ("math", "mathematiques", "mathématiques"):
            return "mathematiques"
        if s in ("physique", "physique-chimie", "physique chimie", "pc"):
            return "physique"
        return s

    def _ensure_loaded(self, subject: str):
        subj = subject.lower()
        if subj not in self._curriculum:
            path = CURRICULUM_DIR / f"{subj}.json"
            self._curriculum[subj] = _load_json(path) if path.exists() else {}
        if subj not in self._blueprint:
            path = CURRICULUM_DIR / f"{subj}_blueprint.json"
            self._blueprint[subj] = _load_json(path) if path.exists() else {}

    async def generate_mock_exam(
        self,
        subject: str = "SVT",
        target_domains: Optional[list[str]] = None,
    ) -> dict:
        """Generate a mock exam at the EXACT level of the national BAC exam.
        
        Supports both SVT and Mathématiques subjects.
        Domain logic is based on deep analysis of 2016-2025 exams.
        
        Returns the exam JSON with image prompts (PROMPT_IMAGE fields)
        instead of actual image files.
        """
        # Route to subject-specific generators
        if subject.lower() in ("math", "mathematiques", "mathématiques"):
            return await self.generate_math_mock_exam(target_domains)
        if subject.lower() in ("physique", "physique-chimie", "physique chimie", "pc"):
            return await self.generate_physique_mock_exam(target_domains)

        self._ensure_loaded(subject)
        curriculum = self._curriculum.get(subject.lower(), {})
        blueprint = self._blueprint.get(subject.lower(), {})
        
        if not curriculum or not blueprint:
            raise ValueError(f"No curriculum/blueprint found for {subject}")

        exam_id = f"mock_{subject.lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # ── Choose domain distribution (deep rotation logic) ──
        domains = self._pick_domains_2026(curriculum, target_domains)
        logger.info(f"[MockExam] Generating {exam_id} | P1={domains['part1']} | P2={domains['part2']}")

        # ── Generate Part 1 ──
        part1 = await self._generate_part1(subject, curriculum, blueprint, domains)

        # ── Generate Part 2 exercises ──
        structure = blueprint.get("structure", {})
        part2_info = structure.get("part2", {})
        patterns = part2_info.get("exercise_patterns", [])
        pattern = random.choices(
            patterns,
            weights=[int(p.get("frequency", "50").rstrip("%")) for p in patterns],
            k=1,
        )[0]
        
        exercises = []
        points_list = pattern["points"]
        for i, pts in enumerate(points_list):
            domain = domains["part2"][i] if i < len(domains["part2"]) else domains["part2"][-1]
            ex = await self._generate_exercise(
                subject, curriculum, blueprint, domain, pts, i + 1, domains
            )
            exercises.append(ex)

        part2 = {
            "name": "Deuxième partie : Raisonnement scientifique et communication écrite et graphique",
            "points": 15,
            "exercises": exercises,
        }

        # ── Assemble final exam ──
        exam = {
            "id": exam_id,
            "title": f"Examen Blanc SVT — Session Normale {datetime.utcnow().year}",
            "subject": subject,
            "year": datetime.utcnow().year,
            "session": "Blanc (Normale)",
            "duration_minutes": 180,
            "coefficient": 5,
            "total_points": 20,
            "domains_covered": domains,
            "generated_at": datetime.utcnow().isoformat(),
            "status": "draft",
            "parts": [part1, part2],
        }

        # Save to disk
        exam_dir = MOCK_EXAMS_DIR / subject.lower() / exam_id
        _save_json(exam_dir / "exam.json", exam)
        (exam_dir / "assets").mkdir(exist_ok=True)

        # Extract image prompts for the admin
        image_prompts = self._extract_image_prompts(exam)
        _save_json(exam_dir / "image_prompts.json", image_prompts)

        logger.info(f"[MockExam] Generated {exam_id}: {len(exercises)} exercises, {len(image_prompts)} image prompts")
        return exam

    # ── All plausible 2026 Normale exam profiles ──
    # Each profile is a unique combination of domain layout + sub-topic variants.
    # Respects ALL 9 rules from analysis of 20 real exams (2016-2025 N+R).
    # GEO NEVER in Ex1. CMO in Ex1 when not in Part1. GEN always in Part2.
    EXAM_PROFILES = [
        # ── P1=CMO (85% likely) ──  Order: GEN → ENV → GEO
        {
            "id": "A1", "weight": 18,
            "label": "CMO/P1 — Gènes indépendants — Déchets+eau — Subduction+magmatisme",
            "part1": "consommation_matiere_organique",
            "part2": ["genetique_expression+transmission", "environnement_sante", "geologie"],
            "gen_variant": "genes_independants",
            "geo_variant": "subduction_magmatisme",
            "env_variant": "dechets_pollution_eau",
            "cmo_p1_focus": "glycolyse_krebs_chaine_resp",
        },
        {
            "id": "A2", "weight": 14,
            "label": "CMO/P1 — Gènes indépendants — Déchets+air — Collision+métamorphisme",
            "part1": "consommation_matiere_organique",
            "part2": ["genetique_expression+transmission", "environnement_sante", "geologie"],
            "gen_variant": "genes_independants",
            "geo_variant": "collision_metamorphisme",
            "env_variant": "dechets_pollution_air",
            "cmo_p1_focus": "muscle_effort_fermentation",
        },
        {
            "id": "A3", "weight": 12,
            "label": "CMO/P1 — Codominance — Déchets+sol — Obduction+ophiolite",
            "part1": "consommation_matiere_organique",
            "part2": ["genetique_expression+transmission", "environnement_sante", "geologie"],
            "gen_variant": "codominance_dihybridisme",
            "geo_variant": "obduction_ophiolite",
            "env_variant": "dechets_pollution_sol",
            "cmo_p1_focus": "glycolyse_krebs_chaine_resp",
        },
        {
            "id": "A4", "weight": 10,
            "label": "CMO/P1 — Gènes liés — Déchets+biogaz — Collision+magmatisme",
            "part1": "consommation_matiere_organique",
            "part2": ["genetique_expression+transmission", "environnement_sante", "geologie"],
            "gen_variant": "genes_lies_crossing_over",
            "geo_variant": "collision_magmatisme_granite",
            "env_variant": "dechets_biogaz_compostage",
            "cmo_p1_focus": "muscle_effort_fermentation",
        },
        {
            "id": "A5", "weight": 8,
            "label": "CMO/P1 — Lié au sexe — Déchets+énergie — Subduction+collision",
            "part1": "consommation_matiere_organique",
            "part2": ["genetique_expression+transmission", "environnement_sante", "geologie"],
            "gen_variant": "sex_linked_transmission",
            "geo_variant": "subduction_collision",
            "env_variant": "dechets_energies_renouvelables",
            "cmo_p1_focus": "levure_aerobie_anaerobie",
        },
        {
            "id": "A6", "weight": 8,
            "label": "CMO/P1 — Dominance incomplète — Déchets+lixiviat — Métamorphisme contact",
            "part1": "consommation_matiere_organique",
            "part2": ["genetique_expression+transmission", "environnement_sante", "geologie"],
            "gen_variant": "dominance_incomplete",
            "geo_variant": "metamorphisme_contact_aureole",
            "env_variant": "dechets_lixiviat_decharge",
            "cmo_p1_focus": "glycolyse_krebs_chaine_resp",
        },
        # ── P1=GEO (15% likely) ──  Order: CMO → GEN → ENV
        {
            "id": "B1", "weight": 8,
            "label": "GEO/P1 — CMO levure — Gènes indépendants — Déchets+eau",
            "part1": "geologie",
            "part2": ["consommation_matiere_organique", "genetique_expression+transmission", "environnement_sante"],
            "gen_variant": "genes_independants",
            "geo_variant": None,
            "env_variant": "dechets_pollution_eau",
            "cmo_p2_focus": "levure_aerobie_anaerobie",
        },
        {
            "id": "B2", "weight": 7,
            "label": "GEO/P1 — CMO muscle — Gènes liés — Déchets+air",
            "part1": "geologie",
            "part2": ["consommation_matiere_organique", "genetique_expression+transmission", "environnement_sante"],
            "gen_variant": "genes_lies_crossing_over",
            "geo_variant": None,
            "env_variant": "dechets_pollution_air",
            "cmo_p2_focus": "muscle_effort_respiration",
        },
        {
            "id": "B3", "weight": 5,
            "label": "GEO/P1 — CMO mitochondrie — Codominance — Déchets+biogaz",
            "part1": "geologie",
            "part2": ["consommation_matiere_organique", "genetique_expression+transmission", "environnement_sante"],
            "gen_variant": "codominance_dihybridisme",
            "geo_variant": None,
            "env_variant": "dechets_biogaz_compostage",
            "cmo_p2_focus": "mitochondrie_bilan_energetique",
        },
        {
            "id": "B4", "weight": 5,
            "label": "GEO/P1 — CMO fermentation — Lié au sexe — Déchets+lixiviat",
            "part1": "geologie",
            "part2": ["consommation_matiere_organique", "genetique_expression+transmission", "environnement_sante"],
            "gen_variant": "sex_linked_transmission",
            "geo_variant": None,
            "env_variant": "dechets_lixiviat_decharge",
            "cmo_p2_focus": "fermentation_comparaison",
        },
    ]

    def _get_used_profile_ids(self, subject: str) -> set[str]:
        """Return profile IDs already used in generated mock exams."""
        used = set()
        subj_dir = MOCK_EXAMS_DIR / subject.lower()
        if not subj_dir.exists():
            return used
        for exam_dir in subj_dir.iterdir():
            ep = exam_dir / "exam.json"
            if ep.exists():
                try:
                    e = _load_json(ep)
                    pid = e.get("domains_covered", {}).get("profile_id")
                    if pid:
                        used.add(pid)
                except Exception:
                    pass
        return used

    def _pick_domains_2026(self, curriculum: dict, target: Optional[list[str]]) -> dict:
        """Select domains using probability profiles.
        
        Each generation picks a DIFFERENT profile from already-generated exams,
        maximizing coverage of all plausible 2026 Normale scenarios.
        All 9 rules from deep analysis (20 exams) are respected.
        """
        if target and len(target) >= 4:
            part1_domain = target[0]
            part2_domains = [d for d in target[1:] if d != part1_domain][:3]
            return {
                "part1": part1_domain,
                "part2": part2_domains,
                "profile_id": "custom",
                "exclusivity_rule": f"Part1({part1_domain}) EXCLUDED from Part2",
            }

        # Get already-used profiles
        used = self._get_used_profile_ids("svt")
        available = [p for p in self.EXAM_PROFILES if p["id"] not in used]
        
        # If all used, reset (allow reuse but shuffle)
        if not available:
            logger.info("[MockExam] All profiles used — resetting pool")
            available = list(self.EXAM_PROFILES)
        
        # Weighted random pick from available profiles
        weights = [p["weight"] for p in available]
        profile = random.choices(available, weights=weights, k=1)[0]
        
        logger.info(f"[MockExam] Picked profile {profile['id']}: {profile['label']}")
        
        return {
            "part1": profile["part1"],
            "part2": profile["part2"],
            "profile_id": profile["id"],
            "profile_label": profile["label"],
            "gen_variant": profile.get("gen_variant"),
            "geo_variant": profile.get("geo_variant"),
            "env_variant": profile.get("env_variant"),
            "cmo_focus": profile.get("cmo_p1_focus") or profile.get("cmo_p2_focus"),
            "exclusivity_rule": f"Part1({profile['part1']}) EXCLUDED from Part2",
        }

    async def _generate_part1(self, subject: str, curriculum: dict, blueprint: dict, domains: dict) -> dict:
        """Generate Part 1 (Restitution des connaissances) at national exam level."""
        # Get domain details from curriculum
        domain_info = {}
        for d in curriculum.get("domains", []):
            if d["id"] == domains["part1"]:
                domain_info = d
                break
        
        # Sample real Part1 questions as few-shot examples
        examples = _sample_part1_questions(subject, 5)
        examples_text = ""
        for ex in examples:
            q = ex["question"]
            examples_text += f"\n--- Exemple ({ex['exam']}) ---\n"
            examples_text += f"Type: {q.get('type', 'open')}\n"
            examples_text += f"Points: {q.get('points', 0)}\n"
            examples_text += f"Contenu: {q.get('content', '')[:300]}\n"
            if q.get("sub_questions"):
                for sq in q["sub_questions"][:2]:
                    examples_text += f"  - {sq.get('content', '')[:150]}\n"

        # Get blueprint slot structure
        slots = blueprint.get("structure", {}).get("part1", {}).get("question_slots", [])
        slots_text = json.dumps(slots, ensure_ascii=False, indent=2)

        # Curriculum topics for this domain
        topics_text = json.dumps(domain_info.get("chapters", []), ensure_ascii=False, indent=2)

        system = """Tu es un expert en création d'examens nationaux SVT du Baccalauréat marocain.
Tu génères UNIQUEMENT la Première partie (Restitution des connaissances, 5pts).
RÈGLE ABSOLUE: toutes les questions doivent porter sur le programme officiel SVT 2ème Bac (cadre de référence).
NIVEAU: IDENTIQUE à l'examen national réel du Baccalauréat. Ni plus facile, ni plus difficile.

ANALYSE DES EXAMENS 2020-2025 — STRUCTURE Part1 STABLE depuis 2023:
- Position 1: Question ouverte (définition ou citation) — TOUJOURS présent (90%+ des examens)
- Position 2: QCM 4 items — TOUJOURS présent (apparaît dans 100% des examens récents)
- Position 3: Vrai/Faux 4 affirmations — présent dans 2023N, 2024N, 2024R, 2025N, 2025R
- Position 4: Association ensemble A ↔ ensemble B — présent dans 2022N+, quasi systématique
Le SET standard 2023-2025 est: {open, qcm, vrai_faux, association}. RESPECTE CE PATTERN.

Réponds en JSON valide uniquement."""

        prompt = f"""Génère la Première partie d'un examen blanc SVT — Session Normale 2026.

DOMAINE PRINCIPAL: {domain_info.get('name', domains['part1'])}

CHAPITRES AUTORISÉS (ne sors JAMAIS de ce cadre):
{topics_text}

STRUCTURE ATTENDUE (4-5 questions, total 5pts):
{slots_text}

EXEMPLES DE VRAIES QUESTIONS NATIONALES:
{examples_text}

INSTRUCTIONS (basées sur l'analyse de 20 examens réels):
1. Question I: Ouverte courte — Définir 1-2 notions OU citer 2 éléments. 0.5 à 1pt.
   Exemple: "Définir les notions suivantes: Incinération – Lixiviat" (2025R)
   Exemple: "Citer deux caractéristiques géophysiques des zones de subduction" (2025N)
2. Question II: QCM avec 4 items (0.5pt chacun, total 2pts). 4 choix a/b/c/d. UNE seule bonne réponse.
   Formulation EXACTE: "Pour chacune des propositions numérotées de 1 à 4, il y a une seule suggestion correcte."
3. Question III: Vrai/Faux avec 4 affirmations (0.25pt chacune, total 1pt).
   Formulation EXACTE: "Recopier les lettres a, b, c, et d puis écrire devant chaque lettre « Vrai » ou « Faux »."
4. Question IV: Association de 4 éléments ensemble A avec ensemble B (5 éléments dans B, 1 distracteur). 1pt.
   Formulation EXACTE: "Recopier les couples (1,...), (2,...), (3,...) et (4,...) et adresser à chaque numéro la lettre correspondante."
5. Chaque question DOIT avoir une correction complète et détaillée.
6. Style FORMEL identique aux examens nationaux marocains — PAS de simplification.

Réponds avec ce JSON:
{{"name":"Première partie : Restitution des connaissances","points":5,"questions":[
  {{"id":"p1q1","type":"qcm","points":2,"content":"Pour chacune des propositions...","sub_questions":[
    {{"content":"1. ...","points":0.5,"choices":[{{"letter":"a","text":"..."}},{{"letter":"b","text":"..."}},{{"letter":"c","text":"..."}},{{"letter":"d","text":"..."}}],"correction":{{"correct_answer":"c"}}}}
  ]}},
  {{"id":"p1q2","type":"open","points":0.5,"content":"...","correction":{{"content":"..."}}}},
  {{"id":"p1q3","type":"vrai_faux","points":1,"content":"Recopier les lettres a, b, c, et d...","sub_questions":[
    {{"content":"a. ...","points":0.25,"correction":{{"correct_answer":"vrai"}}}}
  ]}},
  {{"id":"p1q4","type":"association","points":1,"content":"Recopier les couples...","items_left":[...],"items_right":[...],"correct_pairs":[{{"left":"1","right":"b"}}]}}
]}}"""

        return await _call_deepseek(system, prompt, "Part1", max_tokens=4096)

    # ── Sub-topic rotation data from analysis of 20 real exams ──
    SUBTOPIC_GUIDANCE = {
        "consommation_matiere_organique": {
            "description": """ANALYSE 20 EXAMENS — SOUS-TOPICS CMO:
Les exercices CMO combinent TOUJOURS plusieurs de ces sous-topics:
- muscle_effort (15x): contraction musculaire, fibre musculaire, effort physique
- bilan_energetique (13x): ATP, rendement, bilan chiffré
- glycolyse (12x): glucose→pyruvate, cytoplasme
- krebs (12x): cycle de Krebs, matrice mitochondriale
- chaine_respiratoire (11x): NADH, FADH2, ATP synthase, phosphorylation oxydative
- mitochondrie (10x): ultrastructure, rôle des compartiments
- fermentation (8x): anaérobie, éthanol, lactique — alterne avec respiration
- levure (7x): modèle expérimental fréquent
- consommation_O2 (6x): respiromètre, mesure du dioxygène

PATTERN TYPIQUE: Expérience sur levures/muscles → mesure O2/CO2 → comparer aérobie/anaérobie → schéma bilan""",
            "scenario_types": [
                "Expérience avec des levures dans différentes conditions (aérobie/anaérobie)",
                "Mesure de la consommation d'O2 par des cellules musculaires à l'effort",
                "Comparaison fermentation vs respiration avec données numériques",
                "Étude de l'ultrastructure mitochondriale et ses fonctions",
            ],
        },
        "genetique_expression+transmission": {
            "description": """ANALYSE 20 EXAMENS — SOUS-TOPICS GÉNÉTIQUE:

EXPRESSION (toujours dans 1ère partie de l'exercice):
- relation_gene_proteine (13x): séquence nucléotides→acides aminés
- mutation (12x): substitution, délétion, impact sur protéine
- electrophorese (9x): comparer protéines normale/mutée
- maladie_genetique (8x): drépanocytose(3x), myopathie, mucoviscidose, phénylcétonurie
- transcription (7x): ADN→ARNm
- traduction (7x): ARNm→protéine, code génétique
- code_genetique (7x): tableau des codons

TRANSMISSION (toujours dans 2ème partie de l'exercice):
- dihybridisme (10x): DOMINANT — deux gènes, deux caractères
- dominance_complete (10x): rapport 3:1 ou 9:3:3:1
- genes_lies (8x): même chromosome, crossing-over, parentaux/recombinés
- echiquier (6x): croisement test, prédiction
- genes_independants (5x): chromosomes différents, brassage inter
- sex_linked (3x): lié au chromosome X
- codominance (2x): rare
- dominance_incomplete (2x): phénotype intermédiaire

ROTATION GÈNES LIÉS vs INDÉPENDANTS:
2016N: liés+indép | 2018N: liés | 2019N: indép | 2020N: liés+indép
2020R: codominance | 2021R: liés | 2023N: indép+codominance | 2025R: liés
→ ALTERNANCE: liés et indépendants alternent quasi régulièrement.
→ 2025R avait gènes liés → 2026N devrait avoir gènes INDÉPENDANTS ou codominance.""",
            "scenario_types": [
                "Cas clinique: maladie génétique → électrophorèse → séquence → croisements familiaux",
                "Étude d'une anomalie héréditaire → relation gène-protéine → arbre généalogique",
                "Mutation et impact phénotypique → code génétique → transmission dihybride",
            ],
        },
        "geologie": {
            "description": """ANALYSE 20 EXAMENS — SOUS-TOPICS GÉOLOGIE:
- subduction (9x): fosse, plan de Benioff, volcanisme explosif
- faille (9x): faille inverse, compression
- carte_coupe (8x): carte géologique, coupe, affleurement
- metamorphisme_subduction (8x): schiste bleu, éclogite, HP-BT, glaucophane
- collision (8x): Himalaya, Alpes, chevauchement, nappe de charriage
- tectonique_plaques (7x): convergence, divergence
- magmatisme (6x): granite, anatexie, fusion partielle, pluton
- metamorphisme_contact (5x): auréole, cornéenne, thermique
- obduction (4x): ophiolite, Oman, Beni Bousera
- metamorphisme_collision (4x): foliation, schistosité, régional
- ouverture_oceanique (3x): rift, dorsale, accrétion

ROTATION DES THÈMES PRINCIPAUX:
2016R: subduction+collision | 2017N: collision+magmatisme | 2018N: collision+obduction
2018R: obduction | 2019R: collision+métam | 2020R: subduction+magmatisme
2022N: subduction+magmatisme | 2023N: magmatisme+collision | 2023R: subduction+collision
2025R: métam_contact+magmatisme+collision

LIEUX GÉOGRAPHIQUES UTILISÉS (jamais le même!):
Himalaya, Andes, Vosges, Oman, Alpes, Rif, Atlas, Anti-Atlas, Hoggar
→ 2026N: utiliser un NOUVEAU lieu (ex: Appalaches, Oural, chaîne alpine italienne...)""",
            "scenario_types": [
                "Carte géologique d'une région → roches métamorphiques → diagramme P-T → reconstituer l'histoire",
                "Données sismiques zone de subduction → magmatisme associé → conditions fusion",
                "Indices tectoniques d'une chaîne de collision → nappes de charriage → chronologie",
                "Étude d'un complexe ophiolitique → obduction → reconstitution paléogéographique",
            ],
        },
        "environnement_sante": {
            "description": """ANALYSE 20 EXAMENS — SOUS-TOPICS ENVIRONNEMENT:
- dechets (8x): TOUJOURS PRÉSENT — ordures ménagères, gestion, tri
- impact_sante (5x): toxicité, maladies, risques
- lixiviat (4x): décharge, percolation, contamination
- biogaz_compostage (3x): méthanisation, matière organique
- pollution_eau (2x): nappe phréatique, nitrates, eutrophisation
- pollution_sol (2x): engrais, érosion
- pollution_air (1x): CO2, ozone, gaz à effet de serre
- energies_renouvelables (1x): rare

PATTERN TYPIQUE: Problème de pollution → données → solutions → argumenter
→ Les déchets ménagers dominent largement (8/8 examens)
→ 2026N: combiner déchets + pollution eau OU pollution air (sous-représenté)""",
            "scenario_types": [
                "Étude de l'impact d'une décharge sur la nappe phréatique → analyses → solutions",
                "Comparaison techniques de gestion des déchets → incinération vs compostage vs enfouissement",
                "Pollution de l'air par les gaz à effet de serre → données → solutions durables",
            ],
        },
    }

    async def _generate_exercise(
        self, subject: str, curriculum: dict, blueprint: dict,
        domain: str, points: float, exercise_num: int,
        domains: Optional[dict] = None
    ) -> dict:
        """Generate a single Part 2 exercise with context, documents, and questions."""
        # Find domain info
        domain_info = {}
        for d in curriculum.get("domains", []):
            if d["id"] == domain or domain.startswith(d["id"]):
                domain_info = d
                break

        # Get sub-topic guidance for this domain
        guidance = self.SUBTOPIC_GUIDANCE.get(domain, {})
        subtopic_analysis = guidance.get("description", "")
        scenario_types = guidance.get("scenario_types", [])
        scenario_hint = random.choice(scenario_types) if scenario_types else ""

        # ── Variant-specific instructions from profile ──
        variant_hint = ""
        if domains:
            if "genetique" in domain:
                gv = domains.get("gen_variant", "")
                variant_map = {
                    "genes_independants": "OBLIGATOIRE: Utilise des GÈNES INDÉPENDANTS (sur chromosomes différents). Dihybridisme avec brassage interchromosomique. Rapport 9:3:3:1 en F2.",
                    "genes_lies_crossing_over": "OBLIGATOIRE: Utilise des GÈNES LIÉS (sur le même chromosome). Montre le crossing-over avec des recombinés. Rapport différent de 9:3:3:1.",
                    "codominance_dihybridisme": "OBLIGATOIRE: Utilise la CODOMINANCE (les deux allèles s'expriment simultanément). Phénotype intermédiaire ou co-expression.",
                    "dominance_incomplete": "OBLIGATOIRE: Utilise la DOMINANCE INCOMPLÈTE. L'hétérozygote a un phénotype intermédiaire entre les deux homozygotes.",
                    "sex_linked_transmission": "OBLIGATOIRE: Utilise un caractère LIÉ AU SEXE (chromosome X). Transmission différente chez mâles et femelles.",
                }
                variant_hint = variant_map.get(gv, "")
            elif "geologie" in domain:
                gv = domains.get("geo_variant", "")
                variant_map = {
                    "subduction_magmatisme": "FOCUS: Zone de SUBDUCTION et magmatisme associé. Fosse, plan de Benioff, volcanisme explosif, fusion partielle.",
                    "collision_metamorphisme": "FOCUS: Chaîne de COLLISION et métamorphisme régional. Nappe de charriage, foliation, HP-BT.",
                    "obduction_ophiolite": "FOCUS: OBDUCTION et complexe ophiolitique. Séquence ophiolitique, Beni Bousera/Oman.",
                    "collision_magmatisme_granite": "FOCUS: COLLISION et magmatisme granitique. Anatexie, fusion partielle de la croûte, granite d'anatexie.",
                    "subduction_collision": "FOCUS: Comparaison SUBDUCTION vs COLLISION. Différences de magmatisme, métamorphisme, structures.",
                    "metamorphisme_contact_aureole": "FOCUS: MÉTAMORPHISME DE CONTACT. Auréole métamorphique, cornéennes, intrusion granitique.",
                }
                variant_hint = variant_map.get(gv, "") if gv else ""
            elif "environnement" in domain:
                ev = domains.get("env_variant", "")
                variant_map = {
                    "dechets_pollution_eau": "FOCUS: Gestion des DÉCHETS + pollution de l'EAU. Nappe phréatique, nitrates, eutrophisation, STEP.",
                    "dechets_pollution_air": "FOCUS: Gestion des DÉCHETS + pollution de l'AIR. CO₂, gaz à effet de serre, ozone, réchauffement.",
                    "dechets_pollution_sol": "FOCUS: Gestion des DÉCHETS + pollution du SOL. Engrais, pesticides, érosion, fertilité.",
                    "dechets_biogaz_compostage": "FOCUS: Gestion des DÉCHETS + BIOGAZ/COMPOSTAGE. Méthanisation, valorisation matière organique.",
                    "dechets_energies_renouvelables": "FOCUS: Gestion des DÉCHETS + ÉNERGIES RENOUVELABLES. Solaire, éolien, biomasse comme alternatives.",
                    "dechets_lixiviat_decharge": "FOCUS: Gestion des DÉCHETS + LIXIVIAT. Décharge, percolation, contamination des eaux souterraines.",
                }
                variant_hint = variant_map.get(ev, "")
            elif "consommation" in domain:
                cf = domains.get("cmo_focus", "")
                variant_map = {
                    "glycolyse_krebs_chaine_resp": "FOCUS: Glycolyse → Krebs → Chaîne respiratoire. Bilan énergétique complet, rôle de chaque étape.",
                    "muscle_effort_fermentation": "FOCUS: Muscle à l'EFFORT. Comparaison respiration vs fermentation lactique, dette d'O₂.",
                    "levure_aerobie_anaerobie": "FOCUS: Expérience avec LEVURES. Comparer milieu aérobie vs anaérobie, mesure O₂/CO₂/éthanol.",
                    "muscle_effort_respiration": "FOCUS: Cellule musculaire à l'effort. Consommation O₂, production CO₂, rôle mitochondrie.",
                    "mitochondrie_bilan_energetique": "FOCUS: MITOCHONDRIE ultrastructure et bilan. Crêtes, matrice, ATP synthase, bilan 36/38 ATP.",
                    "fermentation_comparaison": "FOCUS: FERMENTATION alcoolique vs lactique. Levures vs muscle, bilan comparé, rendement.",
                }
                variant_hint = variant_map.get(cf, "")

        # Sample 2-3 real exercises from this domain as few-shot
        examples = _sample_exercises(subject, domain, 3)
        examples_text = ""
        for ex in examples:
            e = ex["exercise"]
            examples_text += f"\n--- Exemple ({ex['exam']}) ---\n"
            examples_text += f"Nom: {e.get('name', '')}\n"
            examples_text += f"Points: {e.get('points', 0)}\n"
            examples_text += f"Contexte: {(e.get('context') or '')[:400]}\n"
            docs = e.get("documents", [])
            for doc in docs[:3]:
                examples_text += f"  Document: type={doc.get('type','?')}, desc={doc.get('description','')[:150]}\n"
            qs = e.get("questions", [])
            for q in qs[:3]:
                examples_text += f"  Q{q.get('number','?')} ({q.get('type','open')}): {q.get('content','')[:200]}\n"

        topics_text = json.dumps(domain_info.get("chapters", []), ensure_ascii=False, indent=2)
        typical_docs = json.dumps(domain_info.get("typical_documents", []), ensure_ascii=False)
        
        n_questions = random.randint(3, 5)
        n_docs = random.randint(2, 4)

        system = f"""Tu es un expert en création d'examens nationaux SVT du Baccalauréat marocain.
Tu génères UN exercice de la Deuxième partie (Raisonnement scientifique).
RÈGLE ABSOLUE: l'exercice doit porter UNIQUEMENT sur le programme officiel SVT 2ème Bac.
NIVEAU: IDENTIQUE à l'examen national réel du Baccalauréat. Mêmes types de raisonnement, même profondeur.

{subtopic_analysis}

Réponds en JSON valide uniquement."""

        prompt = f"""Génère l'Exercice {exercise_num} ({points}pts) d'un examen blanc SVT — Session Normale 2026.

DOMAINE: {domain_info.get('name', domain)}

CHAPITRES AUTORISÉS (ne sors JAMAIS de ce cadre):
{topics_text}

TYPES DE DOCUMENTS TYPIQUES POUR CE DOMAINE:
{typical_docs}

SCÉNARIO SUGGÉRÉ (adapte librement, invente un contexte ORIGINAL):
{scenario_hint}

{('VARIANTE SPÉCIFIQUE POUR CET EXAMEN:' + chr(10) + variant_hint) if variant_hint else ''}

EXEMPLES DE VRAIS EXERCICES NATIONAUX:
{examples_text}

INSTRUCTIONS:
1. Écris un CONTEXTE scientifique ORIGINAL (200-500 caractères) — NE COPIE PAS les exemples.
   Invente un nouveau scénario, un nouvel organisme/lieu/cas clinique.
2. Crée {n_docs} documents. Pour CHAQUE document, donne:
   - id: "doc_e{exercise_num}_N"
   - type: "figure", "schema", "tableau", "graphique"
   - title: "Document N"
   - description: description TRÈS détaillée du contenu visuel (axes, valeurs, légendes, couleurs)
   - PROMPT_IMAGE: prompt détaillé pour générer l'image (style BAC marocain: sobre, scientifique)
3. Crée {n_questions} questions progressives (du simple au complexe), total = {points}pts.
4. Chaque question référence ses documents via "documents": ["doc_e{exercise_num}_N"].
5. Chaque question a une correction COMPLÈTE et STRUCTURÉE.
6. Questions progressives: décrire → comparer → expliquer → déduire → proposer une hypothèse
7. Style IDENTIQUE aux examens nationaux marocains (formulations formelles en français).

Réponds avec ce JSON:
{{"name":"Exercice {exercise_num}","points":{points},"context":"...","documents":[
  {{"id":"doc_e{exercise_num}_1","type":"figure","title":"Document 1","description":"...","PROMPT_IMAGE":"...","src":"assets/doc{exercise_num}_1.png"}}
],"questions":[
  {{"number":"1","type":"open","points":1.5,"content":"En se basant sur le document 1, ...","documents":["doc_e{exercise_num}_1"],"correction":{{"content":"..."}}}}
]}}"""

        result = await _call_deepseek(system, prompt, f"Ex{exercise_num}", max_tokens=6144)
        return result

    # ═══════════════════════════════════════════════════════════════════
    # MATH EXAM GENERATION — Based on 20 exams analysis (2016-2025 N+R)
    # ═══════════════════════════════════════════════════════════════════

    # 12 probability profiles covering all plausible 2026N Math combos.
    # Rules from analysis:
    # - COMPLEXES always present (100%), GEO 80%, PROB 80%, SUITES 55%
    # - Problème always last, always analysis (étude de fonction)
    # - LN/EXP alternate N↔R: 2025N=LN → 2026N likely LN or LN+EXP
    # - Rotation in CPX: 2025N=HOM, 2025R=ROT → 2026N likely ROT or SIM
    # - GEO always has sphere (100%)
    # - PROB context always urne/boules (100%)
    # - 3ex+PB(11pts) = 45%, 4ex+PB(8pts) = 40%, 3ex+multiPB = 15%
    MATH_EXAM_PROFILES = [
        # ── Structure A: 3 exercices (9pts) + Problème 11pts ── (45%)
        {
            "id": "M_A1", "weight": 14,
            "label": "3ex(GEO+CPX+PROB) — PB:LN+suite+intégrale — CPX:rotation",
            "structure": "3ex_11pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 11,
            "probleme_type": "single",
            "func_type": "LN",
            "has_suite": True, "has_integrale": True, "has_reciproque": False,
            "cpx_transfo": "rotation", "cpx_subtopics": ["equation_z2", "forme_trigo", "triangle", "ensemble_pts"],
            "geo_subtopics": ["sphere", "prod_vectoriel", "eq_cartesienne", "distance"],
            "prob_subtopics": ["calculer_proba", "var_aleatoire", "loi_proba"],
        },
        {
            "id": "M_A2", "weight": 12,
            "label": "3ex(GEO+CPX+PROB) — PB:LN+réciproque+aire — CPX:similitude",
            "structure": "3ex_11pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 11,
            "probleme_type": "single",
            "func_type": "LN",
            "has_suite": False, "has_integrale": True, "has_reciproque": True,
            "cpx_transfo": "similitude", "cpx_subtopics": ["forme_exp", "cercle", "alignement"],
            "geo_subtopics": ["sphere", "eq_parametrique", "orthogonalite", "plan_tangent"],
            "prob_subtopics": ["calculer_proba", "independance", "conditionnelle"],
        },
        {
            "id": "M_A3", "weight": 10,
            "label": "3ex(GEO+CPX+PROB) — PB:EXP+suite+réciproque — CPX:rotation",
            "structure": "3ex_11pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 11,
            "probleme_type": "single",
            "func_type": "EXP",
            "has_suite": True, "has_integrale": True, "has_reciproque": True,
            "cpx_transfo": "rotation", "cpx_subtopics": ["equation_z2", "module_argument", "image_transfo", "alignement"],
            "geo_subtopics": ["sphere", "prod_vectoriel", "intersection", "parallelisme"],
            "prob_subtopics": ["calculer_proba", "var_aleatoire", "esperance"],
        },
        # ── Structure B: 4 exercices (12pts) + Problème 8pts ── (40%)
        {
            "id": "M_B1", "weight": 12,
            "label": "4ex(SUITE+GEO+CPX+PROB) — PB:LN+intégrale — CPX:rotation",
            "structure": "4ex_8pb",
            "exercises": [
                {"domain": "suites_numeriques", "points": 3},
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 8,
            "probleme_type": "single",
            "func_type": "LN",
            "has_suite": False, "has_integrale": True, "has_reciproque": True,
            "cpx_transfo": "rotation", "cpx_subtopics": ["equation_z2", "forme_trigo", "triangle", "nature_figure"],
            "geo_subtopics": ["sphere", "eq_cartesienne", "distance", "orthogonalite"],
            "prob_subtopics": ["calculer_proba", "var_aleatoire", "loi_proba"],
            "suite_subtopics": ["geometrique", "recurrence", "convergence", "monotonie"],
        },
        {
            "id": "M_B2", "weight": 10,
            "label": "4ex(SUITE+GEO+CPX+PROB) — PB:EXP+aire — CPX:homothetie",
            "structure": "4ex_8pb",
            "exercises": [
                {"domain": "suites_numeriques", "points": 3},
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3.5},
                {"domain": "probabilites", "points": 2.5},
            ],
            "probleme_points": 8,
            "probleme_type": "single",
            "func_type": "EXP",
            "has_suite": False, "has_integrale": True, "has_reciproque": False,
            "cpx_transfo": "homothetie", "cpx_subtopics": ["module_argument", "cercle", "image_transfo"],
            "geo_subtopics": ["sphere", "prod_vectoriel", "eq_cartesienne", "section_cercle"],
            "prob_subtopics": ["calculer_proba", "independance"],
            "suite_subtopics": ["recurrence", "convergence", "monotonie"],
        },
        {
            "id": "M_B3", "weight": 8,
            "label": "4ex(SUITE+GEO+CPX+PROB) — PB:LN+POLY+aire — CPX:translation",
            "structure": "4ex_8pb",
            "exercises": [
                {"domain": "suites_numeriques", "points": 3},
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 8,
            "probleme_type": "single",
            "func_type": "LN+POLY",
            "has_suite": False, "has_integrale": True, "has_reciproque": False,
            "cpx_transfo": "translation", "cpx_subtopics": ["equation_z2", "triangle", "ensemble_pts", "lieu"],
            "geo_subtopics": ["sphere", "eq_parametrique", "orthogonalite", "plan_tangent"],
            "prob_subtopics": ["calculer_proba", "conditionnelle", "var_aleatoire"],
            "suite_subtopics": ["arithmetique", "geometrique", "convergence"],
        },
        # ── Structure C: 3 exercices + Problème multi-parties (11pts) ── (15%)
        {
            "id": "M_C1", "weight": 8,
            "label": "3ex(GEO+CPX+PROB) — PB multi: PI(prélim)+PII(LN)+PIII(suite)",
            "structure": "3ex_multi_pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3.5},
                {"domain": "probabilites", "points": 2.5},
            ],
            "probleme_points": 11,
            "probleme_type": "multi",
            "probleme_parts": [
                {"name": "Partie I — Préliminaires", "points": 2.75, "content": "courbe_donnee+inegalite+aire"},
                {"name": "Partie II — Étude de fonction", "points": 6.5, "content": "etude_complete+reciproque"},
                {"name": "Partie III — Suite numérique", "points": 1.75, "content": "u_n+1=f(u_n)+recurrence+convergence"},
            ],
            "func_type": "LN",
            "has_suite": True, "has_integrale": True, "has_reciproque": True,
            "cpx_transfo": "rotation", "cpx_subtopics": ["equation_z2", "forme_trigo", "alignement", "perpendiculaire"],
            "geo_subtopics": ["sphere", "prod_scalaire", "prod_vectoriel", "intersection"],
            "prob_subtopics": ["calculer_proba", "independance", "esperance", "var_aleatoire"],
        },
        {
            "id": "M_C2", "weight": 6,
            "label": "3ex(GEO+CPX+PROB) — PB multi: PI(prélim)+PII(EXP+LN) — no suite",
            "structure": "3ex_multi_pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 4},
                {"domain": "probabilites", "points": 2},
            ],
            "probleme_points": 11,
            "probleme_type": "multi",
            "probleme_parts": [
                {"name": "Partie I — Préliminaires", "points": 3, "content": "tracer_courbes+justifier_graphiquement+aire"},
                {"name": "Partie II — Étude de fonction", "points": 8, "content": "etude_complete+integrale+reciproque"},
            ],
            "func_type": "EXP+LN",
            "has_suite": False, "has_integrale": True, "has_reciproque": True,
            "cpx_transfo": "homothetie", "cpx_subtopics": ["forme_exp", "cercle", "triangle", "lieu"],
            "geo_subtopics": ["sphere", "eq_cartesienne", "distance", "orthogonalite"],
            "prob_subtopics": ["calculer_proba", "loi_proba"],
        },
        # ── Variantes supplémentaires pour diversité ──
        {
            "id": "M_D1", "weight": 7,
            "label": "3ex(GEO+CPX+PROB) — PB:EXP+FRAC+intégrale — CPX:rotation+triangle",
            "structure": "3ex_11pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 11,
            "probleme_type": "single",
            "func_type": "EXP+FRAC",
            "has_suite": True, "has_integrale": False, "has_reciproque": False,
            "cpx_transfo": "rotation", "cpx_subtopics": ["equation_z2", "triangle", "isocele", "nature_figure"],
            "geo_subtopics": ["sphere", "prod_vectoriel", "eq_cartesienne", "volume"],
            "prob_subtopics": ["calculer_proba", "var_aleatoire", "esperance", "variance"],
        },
        {
            "id": "M_D2", "weight": 7,
            "label": "4ex(SUITE+GEO+CPX+PROB) — PB:LN+réciproque+tangente — CPX:rotation",
            "structure": "4ex_8pb",
            "exercises": [
                {"domain": "suites_numeriques", "points": 3},
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3.5},
                {"domain": "probabilites", "points": 2.5},
            ],
            "probleme_points": 8,
            "probleme_type": "single",
            "func_type": "LN",
            "has_suite": False, "has_integrale": True, "has_reciproque": True,
            "cpx_transfo": "rotation", "cpx_subtopics": ["module_argument", "forme_trigo", "alignement", "ensemble_pts"],
            "geo_subtopics": ["sphere", "eq_cartesienne", "plan_tangent", "section_cercle"],
            "prob_subtopics": ["calculer_proba", "conditionnelle"],
            "suite_subtopics": ["recurrence", "convergence", "monotonie", "nombre_premier"],
        },
        {
            "id": "M_D3", "weight": 6,
            "label": "4ex(SUITE+GEO+CPX+PROB) — PB:EXP+suite_dans_pb — CPX:similitude",
            "structure": "4ex_8pb",
            "exercises": [
                {"domain": "suites_numeriques", "points": 2.5},
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3.5},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 8,
            "probleme_type": "single",
            "func_type": "EXP",
            "has_suite": True, "has_integrale": True, "has_reciproque": False,
            "cpx_transfo": "similitude", "cpx_subtopics": ["forme_exp", "triangle", "image_transfo", "cercle"],
            "geo_subtopics": ["sphere", "prod_vectoriel", "parallelisme", "eq_parametrique"],
            "prob_subtopics": ["calculer_proba", "independance", "var_aleatoire"],
            "suite_subtopics": ["geometrique", "convergence", "adjacent"],
        },
        {
            "id": "M_D4", "weight": 5,
            "label": "3ex(GEO+CPX+PROB) — PB multi: PI(EXP prélim)+PII(EXP+LN)+PIII(suite)",
            "structure": "3ex_multi_pb",
            "exercises": [
                {"domain": "geometrie_espace", "points": 3},
                {"domain": "nombres_complexes", "points": 3},
                {"domain": "probabilites", "points": 3},
            ],
            "probleme_points": 11,
            "probleme_type": "multi",
            "probleme_parts": [
                {"name": "Partie I — Préliminaires", "points": 2.5, "content": "tracer_courbes+aire_entre_courbes"},
                {"name": "Partie II — Étude de fonction", "points": 6.75, "content": "etude_complete+integrale"},
                {"name": "Partie III — Suite numérique", "points": 1.75, "content": "u_n+1=f(u_n)+recurrence+convergence"},
            ],
            "func_type": "EXP+LN",
            "has_suite": True, "has_integrale": True, "has_reciproque": False,
            "cpx_transfo": "rotation", "cpx_subtopics": ["forme_trigo", "equation_z2", "nature_figure", "image_transfo"],
            "geo_subtopics": ["sphere", "prod_vectoriel", "distance", "section_cercle"],
            "prob_subtopics": ["calculer_proba", "var_aleatoire", "loi_proba", "esperance"],
        },
    ]

    # ── Math sub-topic guidance for AI prompts ──
    MATH_SUBTOPIC_GUIDANCE = {
        "geometrie_espace": {
            "description": """ANALYSE 16 EXERCICES DE GÉOMÉTRIE DANS L'ESPACE (2016-2025):
Éléments TOUJOURS présents:
- Sphère (100%): équation, centre, rayon, intersection plan-sphère
- Équation cartésienne (81%): montrer qu'un plan a une équation donnée
- Produit vectoriel (75%): AB∧AC, en déduire aire du triangle
- Rayon/centre (75%): identifier à partir de l'équation développée
- Orthogonalité (68%): droite ⊥ plan, plans ⊥
- Section/Cercle (68%): section de la sphère par un plan
- Plan tangent (50%): plan tangent à la sphère en un point
- Distance point-plan (43%): formule d(M,P) = |ax₀+by₀+cz₀+d|/√(a²+b²+c²)

STRUCTURE TYPIQUE D'UN EXERCICE:
1. Vérifier/montrer l'équation d'un plan ou d'une sphère
2. Montrer appartenance d'un point à la sphère
3. Produit vectoriel → aire du triangle ou vecteur normal
4. Distance point-plan OU intersection plan-sphère
5. Plan tangent OU orthogonalité/parallélisme""",
        },
        "nombres_complexes": {
            "description": """ANALYSE 20 EXERCICES DE NOMBRES COMPLEXES (2016-2025):
Questions TOUJOURS présentes:
- Rotation (80%): identifier la rotation, calculer l'image
- Affixe (80%): calculer l'affixe d'un point
- Image par transformation (75%): z' = e^{iθ}(z-a)+a
- Forme trigonométrique (60%): |z|, arg(z), z = |z|e^{iθ}
- Triangle/nature (60%): isocèle, rectangle, équilatéral
- Équation z² (50%): résoudre z²+bz+c=0

ROTATION DES TRANSFORMATIONS:
2016-2019: Rotation dominante
2021-2022: Homothétie apparaît
2023-2024: Rotation dominante
2025N: Homothétie, 2025R: Rotation
→ 2026N: ROTATION probable (ou Similitude directe)

STRUCTURE TYPIQUE:
1. Résoudre z²+bz+c=0 OU écrire z sous forme trigonométrique
2. Calculer z₂/z₁, en déduire la transformation
3. Image d'un point par la transformation
4. Nature d'un triangle OU alignement
5. Ensemble de points |z-a|=r OU lieu géométrique""",
        },
        "probabilites": {
            "description": """ANALYSE 16 EXERCICES DE PROBABILITÉS (2016-2025):
- Contexte TOUJOURS = urne + boules de couleurs (100%)
- Calculer p(A) (68%): probabilité simple
- Variable aléatoire (56%): loi de X, E(X)
- Loi de probabilité (50%): tableau de la loi
- Cardinal/dénombrement (50%): nombre de tirages possibles
- Indépendance (25%): vérifier si A et B sont indépendants
- Conditionnelle (25%): p(A|B) = p(A∩B)/p(B)
- Binomiale (6%): très rare

STRUCTURE TYPIQUE:
1. Calculer/montrer p(A) = ...
2. Montrer que p(B) = ... (arbre ou dénombrement)
3. Indépendance OU probabilité conditionnelle
4. Variable aléatoire X: loi, E(X), V(X)""",
        },
        "suites_numeriques": {
            "description": """ANALYSE 11 EXERCICES STANDALONE DE SUITES (2016-2025):
Types de suites:
- Géométrique + récurrence (dominant: 7/11)
- Récurrence u_{n+1} = f(u_n) (7/11)
- Convergence + monotonie (10/11)
- Arithmétique (3/11, surtout rattrapage)
- Nombres premiers (3/11, rattrapage)

STRUCTURE TYPIQUE:
1. Vérifier que u_{n+1} = expression en u_n
2. Montrer par récurrence que a ≤ u_n ≤ b
3. Montrer u_{n+1} - u_n = ... → monotonie
4. En déduire convergence
5. Calculer la limite""",
        },
    }

    def _pick_domains_math(self, curriculum: dict, target: Optional[list[str]]) -> dict:
        """Select Math domains using probability profiles.
        
        Each generation picks a DIFFERENT profile from already-generated Math exams,
        maximizing coverage of all plausible 2026 Normale scenarios.
        """
        if target:
            return {
                "exercises": [{"domain": d, "points": 3} for d in target],
                "probleme_points": 20 - 3 * len(target),
                "profile_id": "custom",
                "profile_label": "Custom domains",
            }

        # Get already-used profiles
        used = self._get_used_profile_ids("mathematiques")
        available = [p for p in self.MATH_EXAM_PROFILES if p["id"] not in used]
        
        if not available:
            logger.info("[MockExam:Math] All profiles used — resetting pool")
            available = list(self.MATH_EXAM_PROFILES)
        
        weights = [p["weight"] for p in available]
        profile = random.choices(available, weights=weights, k=1)[0]
        
        logger.info(f"[MockExam:Math] Picked profile {profile['id']}: {profile['label']}")
        
        return {
            "exercises": profile["exercises"],
            "probleme_points": profile["probleme_points"],
            "probleme_type": profile.get("probleme_type", "single"),
            "probleme_parts": profile.get("probleme_parts"),
            "func_type": profile.get("func_type", "LN"),
            "has_suite": profile.get("has_suite", False),
            "has_integrale": profile.get("has_integrale", True),
            "has_reciproque": profile.get("has_reciproque", False),
            "cpx_transfo": profile.get("cpx_transfo", "rotation"),
            "cpx_subtopics": profile.get("cpx_subtopics", []),
            "geo_subtopics": profile.get("geo_subtopics", []),
            "prob_subtopics": profile.get("prob_subtopics", []),
            "suite_subtopics": profile.get("suite_subtopics", []),
            "profile_id": profile["id"],
            "profile_label": profile["label"],
            "structure": profile.get("structure", "3ex_11pb"),
        }

    async def generate_math_mock_exam(
        self,
        target_domains: Optional[list[str]] = None,
    ) -> dict:
        """Generate a Math mock exam using deep analysis of 20 real exams."""
        subject = "Mathématiques"
        subj_key = "mathematiques"
        self._ensure_loaded(subj_key)
        curriculum = self._curriculum.get(subj_key, {})
        blueprint = self._blueprint.get(subj_key, {})
        
        if not curriculum:
            raise ValueError(f"No curriculum found for {subject}")

        exam_id = f"mock_math_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # Pick profile
        domains = self._pick_domains_math(curriculum, target_domains)
        logger.info(f"[MockExam:Math] Generating {exam_id} | profile={domains.get('profile_id')}")

        # Generate exercises
        exercises = []
        for i, ex_info in enumerate(domains["exercises"]):
            ex = await self._generate_math_exercise(
                curriculum, ex_info["domain"], ex_info["points"], i + 1, domains
            )
            exercises.append(ex)

        # Generate Problème
        probleme_parts = await self._generate_math_probleme(curriculum, domains)

        # Assemble
        all_parts = []
        if exercises:
            all_parts.append({
                "name": "Exercices",
                "exercises": exercises,
            })
        # Problème as separate part(s)
        if isinstance(probleme_parts, list):
            all_parts.append({
                "name": "Problème",
                "exercises": probleme_parts,
            })
        else:
            all_parts.append({
                "name": "Problème",
                "exercises": [probleme_parts],
            })

        total_ex_pts = sum(ex_info["points"] for ex_info in domains["exercises"])
        exam = {
            "id": exam_id,
            "title": f"Examen Blanc Mathématiques — Session Normale {datetime.utcnow().year}",
            "subject": subject,
            "year": datetime.utcnow().year,
            "session": "Blanc (Normale)",
            "duration_minutes": 180,
            "coefficient": 7,
            "total_points": 20,
            "domains_covered": domains,
            "generated_at": datetime.utcnow().isoformat(),
            "status": "draft",
            "general_note": "L'usage de la calculatrice non programmable est autorisé.",
            "parts": all_parts,
        }

        # Save
        exam_dir = MOCK_EXAMS_DIR / subj_key / exam_id
        _save_json(exam_dir / "exam.json", exam)
        (exam_dir / "assets").mkdir(exist_ok=True)

        image_prompts = self._extract_image_prompts(exam)
        _save_json(exam_dir / "image_prompts.json", image_prompts)

        logger.info(f"[MockExam:Math] Generated {exam_id}: {len(exercises)} exercises + problème")
        return exam

    async def _generate_math_exercise(
        self, curriculum: dict, domain: str, points: float,
        exercise_num: int, domains: dict
    ) -> dict:
        """Generate a single Math exercise (GEO, CPX, PROB, or SUITES)."""
        domain_info = {}
        for d in curriculum.get("domains", []):
            if d["id"] == domain:
                domain_info = d
                break

        guidance = self.MATH_SUBTOPIC_GUIDANCE.get(domain, {})
        subtopic_desc = guidance.get("description", "")

        # Build variant hints from profile
        variant_hint = ""
        if domain == "nombres_complexes":
            transfo = domains.get("cpx_transfo", "rotation")
            subs = domains.get("cpx_subtopics", [])
            variant_hint = f"""TRANSFORMATION PRINCIPALE: {transfo.upper()}
Sous-topics à inclure: {', '.join(subs)}
"""
            if transfo == "rotation":
                variant_hint += "Utilise une rotation de centre Ω et d'angle θ. Forme: z' = e^{iθ}(z - ω) + ω."
            elif transfo == "similitude":
                variant_hint += "Utilise une similitude directe. Forme: z' = az + b avec |a|≠1."
            elif transfo == "homothetie":
                variant_hint += "Utilise une homothétie de centre Ω et rapport k. Forme: z' = k(z - ω) + ω."
            elif transfo == "translation":
                variant_hint += "Utilise une translation de vecteur b. Forme: z' = z + b."
        elif domain == "geometrie_espace":
            subs = domains.get("geo_subtopics", [])
            variant_hint = f"Sous-topics à inclure: {', '.join(subs)}\nIMPORTANT: L'exercice DOIT contenir une sphère (100% des examens réels)."
        elif domain == "probabilites":
            subs = domains.get("prob_subtopics", [])
            variant_hint = f"Sous-topics à inclure: {', '.join(subs)}\nIMPORTANT: Le contexte DOIT être une urne avec des boules de couleurs (100% des examens réels)."
        elif domain == "suites_numeriques":
            subs = domains.get("suite_subtopics", [])
            variant_hint = f"Sous-topics à inclure: {', '.join(subs)}"

        # Sample real exercises
        examples = _sample_exercises("mathematiques", domain, 3)
        examples_text = ""
        for ex in examples:
            e = ex["exercise"]
            examples_text += f"\n--- Exemple ({ex['exam']}) ---\n"
            examples_text += f"Nom: {e.get('name', '')}\n"
            examples_text += f"Points: {e.get('points', 0)}\n"
            examples_text += f"Contexte: {(e.get('context') or '')[:300]}\n"
            for q in e.get("questions", [])[:4]:
                examples_text += f"  Q{q.get('number','?')} ({q.get('points',0)}pts): {q.get('content','')[:200]}\n"

        topics_text = json.dumps(domain_info.get("chapters", []), ensure_ascii=False, indent=2)
        patterns_text = json.dumps(domain_info.get("typical_question_patterns", []), ensure_ascii=False, indent=2)

        system = f"""Tu es un expert en création d'examens nationaux de Mathématiques du Baccalauréat marocain (2ème Bac Sciences).
Tu génères UN exercice conforme au format exact de l'examen national.
RÈGLE ABSOLUE: l'exercice doit porter UNIQUEMENT sur le programme officiel.
NIVEAU: IDENTIQUE à l'examen national réel — mêmes types de raisonnement, même profondeur.
NOTATION: Utilise la notation LaTeX pour TOUTES les formules: $f(x)$, $\\lim$, $\\int$, $\\frac{{}}{{}}$, $\\overrightarrow{{AB}}$, etc.

{subtopic_desc}

Réponds en JSON valide uniquement."""

        prompt = f"""Génère l'Exercice {exercise_num} ({points}pts) d'un examen blanc Mathématiques — Session Normale 2026.

DOMAINE: {domain_info.get('name', domain)}

PROGRAMME AUTORISÉ:
{topics_text}

TYPES DE QUESTIONS TYPIQUES:
{patterns_text}

{('VARIANTE SPÉCIFIQUE:' + chr(10) + variant_hint) if variant_hint else ''}

EXEMPLES DE VRAIS EXERCICES NATIONAUX:
{examples_text}

INSTRUCTIONS:
1. Génère un exercice avec 4-7 questions progressives, total = {points}pts.
2. Chaque question a un numéro (ex: "1.a", "2", "3.a"), des points, un contenu en LaTeX, et une correction COMPLÈTE.
3. Les premières questions sont simples (vérifier, calculer), les dernières plus avancées (montrer, déduire).
4. La correction doit inclure TOUTES les étapes de calcul.
5. Style IDENTIQUE aux examens nationaux marocains (formulations formelles en français, notation LaTeX).
6. NE PAS inclure de documents/images — les exercices de maths sont purement textuels.

Réponds avec ce JSON:
{{"name":"Exercice {exercise_num} — {domain_info.get('name', domain)}","points":{points},"context":"","questions":[
  {{"number":"1.a","type":"open","points":0.5,"content":"Montrer que ...","correction":{{"content":"..."}}}}
]}}"""

        return await _call_deepseek(system, prompt, f"Math_Ex{exercise_num}", max_tokens=6144)

    async def _generate_math_probleme(self, curriculum: dict, domains: dict) -> list | dict:
        """Generate the Math Problème (étude de fonction, intégrales, suites)."""
        domain_info = {}
        for d in curriculum.get("domains", []):
            if d["id"] == "analyse_probleme":
                domain_info = d
                break

        func_type = domains.get("func_type", "LN")
        has_suite = domains.get("has_suite", False)
        has_integrale = domains.get("has_integrale", True)
        has_reciproque = domains.get("has_reciproque", False)
        pb_points = domains.get("probleme_points", 11)
        pb_type = domains.get("probleme_type", "single")
        pb_parts_info = domains.get("probleme_parts")

        # Build function type instruction
        func_hint = ""
        if func_type == "LN":
            func_hint = "La fonction DOIT contenir ln (logarithme népérien). Exemples: f(x) = x - (ln x)²/x, f(x) = 2 - 2/x + (1-ln x)², f(x) = x·ln(x) - x."
        elif func_type == "EXP":
            func_hint = "La fonction DOIT contenir exp (exponentielle). Exemples: f(x) = x - 1 + 4/(e^x + 2), f(x) = 2 - x·e^{-x+1}, f(x) = (x²-x)e^{-x} + x."
        elif func_type == "EXP+LN":
            func_hint = "La fonction DOIT combiner exp ET ln. Exemples: f(x) = x+1-ln(e^x-x), f(x) = e^{-x}·ln(1+e^x)."
        elif func_type == "LN+POLY":
            func_hint = "La fonction combine ln ET polynôme. Exemples: f(x) = x⁴(ln x - 1)², f(x) = x + (1-2/x)·ln x."
        elif func_type == "EXP+FRAC":
            func_hint = "La fonction combine exp ET fraction. Exemples: f(x) = x - 1 + 4/(e^x + 2), f(x) = x(e^{x/2} - 1)²."

        # Content requirements
        content_parts = []
        content_parts.append("LIMITES aux bornes du domaine avec interprétation géométrique (OBLIGATOIRE)")
        content_parts.append("DÉRIVÉE f'(x) = ... et tableau de variations (OBLIGATOIRE)")
        if has_integrale:
            content_parts.append("INTÉGRALE: primitive, IPP (intégration par parties), et/ou calcul d'AIRE entre courbes")
        if has_reciproque:
            content_parts.append("FONCTION RÉCIPROQUE: restriction de f, montrer que f⁻¹ existe, calculer (f⁻¹)'")
        if has_suite:
            content_parts.append("SUITE u_{n+1}=f(u_n): montrer par récurrence a≤u_n≤b, monotonie, convergence, limite")

        flow_text = json.dumps(domain_info.get("typical_question_flow", []), ensure_ascii=False, indent=2)

        # Sample real problems
        examples = _sample_exercises("mathematiques", "analyse_probleme", 2)
        examples_text = ""
        for ex in examples:
            e = ex["exercise"]
            examples_text += f"\n--- Exemple ({ex['exam']}) ---\n"
            examples_text += f"Nom: {e.get('name', '')}\n"
            examples_text += f"Points: {e.get('points', 0)}\n"
            for q in e.get("questions", [])[:5]:
                examples_text += f"  Q{q.get('number','?')} ({q.get('points',0)}pts): {q.get('content','')[:200]}\n"

        system = f"""Tu es un expert en création d'examens nationaux de Mathématiques du Baccalauréat marocain.
Tu génères le PROBLÈME (étude de fonction numérique) — la partie la plus importante de l'examen.
NIVEAU: IDENTIQUE à l'examen national réel. Mêmes types de raisonnement et de calcul.
NOTATION: LaTeX OBLIGATOIRE pour toutes les formules.

FLOW STANDARD DU PROBLÈME (basé sur 20 examens réels):
{flow_text}

ANALYSE DES FONCTIONS UTILISÉES:
- LN pur (40%): f(x) implique ln(x), (ln x)², x·ln(x)
- EXP pur (35%): f(x) implique e^x, xe^{{-x}}, (ax+b)e^{{cx}}
- LN+EXP mixte (15%): f(x) combine les deux
- EXP+FRAC (10%): f(x) combine exp et fraction rationnelle

TRACER vs COURBE DONNÉE:
- 83% des problèmes demandent de TRACER la courbe
- 16% DONNENT la courbe et demandent de justifier graphiquement
- Tendance 2024-2025: Partie I donne la courbe, Partie II demande de tracer

Réponds en JSON valide uniquement."""

        if pb_type == "multi" and pb_parts_info:
            # Multi-part problem (2024-2025 style)
            parts_json = []
            for j, pinfo in enumerate(pb_parts_info):
                part_prompt = f"""Génère la {pinfo['name']} ({pinfo['points']}pts) du Problème d'un examen blanc Mathématiques 2026.

TYPE DE FONCTION: {func_hint}
CONTENU DE CETTE PARTIE: {pinfo['content']}

{"EXEMPLES:" + examples_text if j == 0 else ""}

INSTRUCTIONS:
1. Génère 3-6 questions progressives pour cette partie, total = {pinfo['points']}pts.
2. Chaque question en LaTeX avec correction COMPLÈTE.
3. Style identique aux examens nationaux marocains.

Réponds avec ce JSON:
{{"name":"{pinfo['name']}","points":{pinfo['points']},"context":"","questions":[
  {{"number":"{j+1}.1","type":"open","points":0.5,"content":"...","correction":{{"content":"..."}}}}
]}}"""
                part_result = await _call_deepseek(system, part_prompt, f"Math_PB_P{j+1}", max_tokens=6144)
                parts_json.append(part_result)
            return parts_json
        else:
            # Single-block problem
            prompt = f"""Génère le Problème ({pb_points}pts) d'un examen blanc Mathématiques — Session Normale 2026.

TYPE DE FONCTION: {func_hint}

CONTENU OBLIGATOIRE:
{chr(10).join('- ' + c for c in content_parts)}

EXEMPLES DE VRAIS PROBLÈMES NATIONAUX:
{examples_text}

INSTRUCTIONS:
1. Invente une fonction f ORIGINALE du type demandé. NE COPIE PAS les exemples.
2. Génère 12-18 questions progressives, total = {pb_points}pts.
3. Questions de 0.25 à 2pts chacune (la plupart 0.5pts).
4. Flow: limites → asymptote → dérivée → variation → [inflexion] → tracer → [réciproque] → [intégrale+aire] → [suite]
5. Chaque question a une correction COMPLÈTE avec toutes les étapes.
6. La dernière question de tracé: "Construire la courbe $(C_f)$ et la droite $(\\delta)$ dans le repère $(O,\\vec{{i}},\\vec{{j}})$."
7. Notation LaTeX OBLIGATOIRE.

Réponds avec ce JSON:
{{"name":"Problème — Étude d'une fonction numérique","points":{pb_points},"context":"Soit $f$ la fonction numérique définie sur ... par $f(x) = ...$. On désigne par $(C_f)$ sa courbe représentative dans un repère orthonormé $(O,\\vec{{i}},\\vec{{j}})$.","questions":[
  {{"number":"1.a","type":"open","points":0.5,"content":"Calculer $\\displaystyle\\lim_{{x\\to ...}} f(x)$...","correction":{{"content":"..."}}}}
]}}"""
            return await _call_deepseek(system, prompt, "Math_Probleme", max_tokens=8192)

    # ═══════════════════════════════════════════════════════════════════
    # PHYSIQUE-CHIMIE EXAM GENERATION — Based on 20 exams (2016-2025)
    # ═══════════════════════════════════════════════════════════════════

    # 12 probability profiles for Physique-Chimie.
    # Deep analysis of 20 exams (2016-2025 N+R):
    #
    # STRUCTURE: 4ex=70% (14/20), 5ex=30% (6/20). Trend: alternates 4/5 every 2yrs.
    # CHIMIE:  ALWAYS Ex1, ALWAYS 7pts (20/20). 2 parties. 10-15Q. 0-3 docs.
    # ELEC:    ALWAYS present (20/20). Combos: RC+RL+RLC(35%), RL+RLC(10%), RL+LC+modAM(10%).
    # MECA:    ALWAYS last exercise (20/20). 2.5-6pts. 0-3 docs.
    # ONDES+NUC: Combined in 4ex, separated in 5ex. 3/20 combined, 6/20 separated, rest partial.
    #
    # CHIMIE COMBOS:  DOSAGE+ELEC(20%), DOSAGE+PILE(20%), rest varied (14 unique combos)
    # ELEC COMBOS:    RC+RL+RLC(35%), RL+LC+modAM(10%), RL+RLC(10%), RL+modAM+demod(5%)...
    # MECA COMBOS:    oscillateur(45%), plan_incline(30%), chute_visqueuse(20%), projectile(15%)
    #
    # QUESTION TYPES: 98% open, 1.5% vrai_faux, 0.7% qcm
    # POINTS/Q:       0.5pts(62%), 0.75pts(20%), 0.25pts(14%), 1.0pts(4%)
    #
    # 2026N PREDICTIONS (rotation):
    #   CHIMIE:  PILE or ELECTROLYSE (2025N=CIN+DOS+EST, 2025R=DOS+EST → need PILE/ELEC)
    #   ELEC:    RC+RL+RLC or RL+RLC (2025N=RC+demod, 2025R=RL+LC+mod → need RLC)
    #   MECA:    chute_visqueuse or projectile (2025N=satellite, 2025R=skieur+torsion)
    #   STRUCT:  4ex likely (2025=4ex, but 2024=5ex → alternation pattern)
    PHYSIQUE_EXAM_PROFILES = [
        # ── 4 exercises format (high probability for 2026N) ──
        {
            "id": "PC_A1", "weight": 14,
            "label": "4ex: CHIM(pile+dosage) + ONDES+NUC(méca+désint) + ELEC(RC+RL+RLC) + MECA(chute_visq+oscill)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 3},
                {"domain": "electricite", "points": 4.5},
                {"domain": "mecanique", "points": 5.5},
            ],
            "chimie_variant": "pile_dosage",
            "ondes_sub": "ondes_mecaniques", "nuc_sub": "desintegration",
            "elec_variant": "RC_RL_RLC",
            "meca_variant": "chute_visqueuse_oscillateur",
        },
        {
            "id": "PC_A2", "weight": 12,
            "label": "4ex: CHIM(electrolyse+ester) + ONDES+NUC(diffr+désint) + ELEC(RL+modAM) + MECA(proj+pendule_torsion)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 3.5},
                {"domain": "electricite", "points": 5},
                {"domain": "mecanique", "points": 4.5},
            ],
            "chimie_variant": "electrolyse_esterification",
            "ondes_sub": "diffraction", "nuc_sub": "desintegration",
            "elec_variant": "RL_modulation",
            "meca_variant": "projectile_pendule_torsion",
        },
        {
            "id": "PC_A3", "weight": 10,
            "label": "4ex: CHIM(pile+ester) + ONDES+NUC(ultrasons+désint) + ELEC(RC+RL+RLC) + MECA(satellite+oscill)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 2.5},
                {"domain": "electricite", "points": 5},
                {"domain": "mecanique", "points": 5.5},
            ],
            "chimie_variant": "pile_esterification",
            "ondes_sub": "ultrasons", "nuc_sub": "desintegration",
            "elec_variant": "RC_RL_RLC",
            "meca_variant": "satellite_oscillateur",
        },
        {
            "id": "PC_A4", "weight": 10,
            "label": "4ex: CHIM(electrolyse+dosage) + NUC(désint+fusion) + ELEC(RL+RLC) + MECA(plan_incl+oscill)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 2.5},
                {"domain": "electricite", "points": 5},
                {"domain": "mecanique", "points": 5.5},
            ],
            "chimie_variant": "electrolyse_dosage",
            "ondes_sub": None, "nuc_sub": "desintegration",
            "elec_variant": "RL_RLC",
            "meca_variant": "plan_incline_oscillateur",
        },
        {
            "id": "PC_A5", "weight": 8,
            "label": "4ex: CHIM(cinetique+dosage) + ONDES+NUC(sonore+désint) + ELEC(RC+LC+modAM) + MECA(chute_libre+oscill)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 3.5},
                {"domain": "electricite", "points": 4.5},
                {"domain": "mecanique", "points": 5},
            ],
            "chimie_variant": "cinetique_dosage",
            "ondes_sub": "ondes_sonores", "nuc_sub": "desintegration",
            "elec_variant": "RC_LC_modulation",
            "meca_variant": "chute_libre_oscillateur",
        },
        {
            "id": "PC_A6", "weight": 7,
            "label": "4ex: CHIM(pile+dosage) + ONDES+NUC(lumineuse+fusion) + ELEC(RL+LC+modAM) + MECA(champ_mag+pendule_simple)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 3},
                {"domain": "electricite", "points": 4.5},
                {"domain": "mecanique", "points": 5.5},
            ],
            "chimie_variant": "pile_dosage",
            "ondes_sub": "ondes_lumineuses", "nuc_sub": "fusion_fission",
            "elec_variant": "RL_LC_modulation",
            "meca_variant": "champ_magnetique_pendule",
        },
        # ── 5 exercises format (30%) ──
        {
            "id": "PC_B1", "weight": 9,
            "label": "5ex: CHIM(pile+dosage) + ONDES(méca) + NUC(désint) + ELEC(RC+RL+RLC) + MECA(chute_visq)",
            "structure": "5ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes", "points": 3},
                {"domain": "nucleaire", "points": 2.5},
                {"domain": "electricite", "points": 5},
                {"domain": "mecanique", "points": 2.5},
            ],
            "chimie_variant": "pile_dosage",
            "ondes_sub": "ondes_mecaniques", "nuc_sub": "desintegration",
            "elec_variant": "RC_RL_RLC",
            "meca_variant": "chute_visqueuse",
        },
        {
            "id": "PC_B2", "weight": 8,
            "label": "5ex: CHIM(electrolyse+dosage) + ONDES(diffr) + NUC(désint) + ELEC(RL+RLC) + MECA(proj+pendule)",
            "structure": "5ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes", "points": 2.5},
                {"domain": "nucleaire", "points": 2},
                {"domain": "electricite", "points": 3.5},
                {"domain": "mecanique", "points": 5},
            ],
            "chimie_variant": "electrolyse_dosage",
            "ondes_sub": "diffraction", "nuc_sub": "desintegration",
            "elec_variant": "RL_RLC",
            "meca_variant": "projectile_pendule_torsion",
        },
        {
            "id": "PC_B3", "weight": 7,
            "label": "5ex: CHIM(cinetique+ester) + ONDES(lumineuse) + NUC(désint) + ELEC(RC+RL+RLC) + MECA(plan_incl)",
            "structure": "5ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes", "points": 2.5},
                {"domain": "nucleaire", "points": 2},
                {"domain": "electricite", "points": 4.75},
                {"domain": "mecanique", "points": 3.75},
            ],
            "chimie_variant": "cinetique_esterification",
            "ondes_sub": "ondes_lumineuses", "nuc_sub": "desintegration",
            "elec_variant": "RC_RL_RLC",
            "meca_variant": "plan_incline_oscillateur",
        },
        # ── Variantes supplémentaires ──
        {
            "id": "PC_C1", "weight": 7,
            "label": "4ex: CHIM(cinetique+ester) + ONDES+NUC(méca+datation) + ELEC(RC+RL+RLC) + MECA(chute_visq+satellite)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 3.5},
                {"domain": "electricite", "points": 4.5},
                {"domain": "mecanique", "points": 5},
            ],
            "chimie_variant": "cinetique_esterification",
            "ondes_sub": "ondes_mecaniques", "nuc_sub": "datation",
            "elec_variant": "RC_RL_RLC",
            "meca_variant": "chute_visqueuse_satellite",
        },
        {
            "id": "PC_C2", "weight": 6,
            "label": "5ex: CHIM(pile+ester) + ONDES(sonore) + NUC(désint) + ELEC(RC+LC+modAM) + MECA(parachutiste)",
            "structure": "5ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes", "points": 2.75},
                {"domain": "nucleaire", "points": 2.5},
                {"domain": "electricite", "points": 5.25},
                {"domain": "mecanique", "points": 2.5},
            ],
            "chimie_variant": "pile_esterification",
            "ondes_sub": "ondes_sonores", "nuc_sub": "desintegration",
            "elec_variant": "RC_LC_modulation",
            "meca_variant": "chute_libre_parachutiste",
        },
        {
            "id": "PC_C3", "weight": 6,
            "label": "4ex: CHIM(electrolyse+dosage+cinetique) + ONDES+NUC(diffr) + ELEC(RC+modAM+demod) + MECA(chute+pendule_simple)",
            "structure": "4ex",
            "exercises": [
                {"domain": "chimie", "points": 7},
                {"domain": "ondes_nucleaire", "points": 3},
                {"domain": "electricite", "points": 5},
                {"domain": "mecanique", "points": 5},
            ],
            "chimie_variant": "electrolyse_dosage_cinetique",
            "ondes_sub": "diffraction", "nuc_sub": None,
            "elec_variant": "RC_modulation_demodulation",
            "meca_variant": "chute_libre_pendule_simple",
        },
    ]

    # ── Physique-Chimie sub-topic guidance for AI prompts ──
    PHYSIQUE_SUBTOPIC_GUIDANCE = {
        "chimie": {
            "description": """ANALYSE APPROFONDIE 20 EXERCICES DE CHIMIE (2016-2025):
L'exercice de Chimie est TOUJOURS en position 1, TOUJOURS 7pts, TOUJOURS 2 parties indépendantes.

14 COMBINAISONS UNIQUES OBSERVÉES:
- DOSAGE+ELECTROLYSE: 4x (20%) — ex: 2016N, 2022N, 2022R, 2023R
- DOSAGE+PILE: 4x (20%) — ex: 2019R, 2020N, 2021R, 2024R
- CINETIQUE+DOSAGE: 1x — 2024N (tendance récente)
- CINETIQUE+DOSAGE+ESTERIFICATION: 1x — 2025N
- PILE: 1x — 2020R (pile seule!)
- CINETIQUE: 1x — 2023N
→ TENDANCE 2024-2025: cinétique apparaît 3x dans les 4 derniers examens!
→ 2026N PRÉDICTION: PILE ou ELECTROLYSE + DOSAGE (retour classique après tendance cinétique)

DISTRIBUTION POINTS/QUESTION CHIMIE:
0.5pts: 155x (63%), 0.75pts: 64x (26%), 0.25pts: 17x (7%), 1.0pts: 9x (4%)
→ La plupart des questions = 0.5pts. Questions à 1pt = début de partie ou calcul complexe.

TYPES DE QUESTIONS CHIMIE (par fréquence d'action):
- "Déterminer..." (50x) — la plus fréquente
- "Écrire l'équation..." (44x) — équations de réaction
- "Calculer..." (39x) — applications numériques
- "Montrer que..." / "Vérifier que..." (17x) — démonstrations guidées
- "Donner..." / "Préciser..." (10x) — réponses courtes
- "Dresser le tableau d'avancement..." (4x)
- "Définir..." (2x)

STRUCTURE TYPE: 10-15 questions (moy. 12.3Q), 0-3 docs (moy. 1.3 docs)
DOCUMENTS CHIMIE: 0docs=10%, 1doc=50%, 2docs=30%, 3docs=10%
DONNÉES OBLIGATOIRES: M, pKa, Ke=10⁻¹⁴, concentrations, volumes, constante de Faraday.

──── MOLÉCULES & RÉACTIFS — ROTATION (analyse ultra-profonde) ────
ACIDES CARBOXYLIQUES UTILISÉS (ne PAS répéter les récents):
  - acide éthanoïque CH₃COOH: 6x (dont 2025R) → ÉVITER 2026N
  - acide méthanoïque HCOOH: 4x (dont 2023N) → possible
  - acide propanoïque C₂H₅COOH: 2x (2022N) → possible
  - acide butanoïque C₃H₇COOH: 1x (2017N) → BON CANDIDAT 2026N
  - acide lactique: 1x (2018N) → BON CANDIDAT
  - acide benzoïque C₆H₅COOH: 1x (2019N) → possible
  - acide ascorbique (vit C): 1x (2024N) → contexte original
  → 2026N PRÉDICTION: acide butanoïque, lactique ou benzoïque

BASES UTILISÉES:
  - soude NaOH: 7x (par défaut pour dosages)
  - ammoniac NH₃: 6x (base faible classique)
  - méthylamine CH₃NH₂: 2x (2022R, 2023R)
  - éthylamine C₂H₅NH₂: 2x (2022R, 2023R)
  → TENDANCE: amines fréquentes en rattrapage 2022+

MÉTAUX (pile/électrolyse): Fe(6x), Zn(5x), Cu(4x), Ag(3x), Pb(2x), Ni(2x), Al(2x)
ALCOOLS (estérification): éthanol(7x dominant), méthanol(3x)

──── VALEURS NUMÉRIQUES TYPIQUES ────
- pH: 2.4 à 11.6 (moy 4.58, acides faibles dominent)
- Concentrations: 10⁻² à 10⁻¹ mol/L pour S_A, S_B
- Volumes: V_A = 10-20 mL, V_B = 5-25 mL
- Courant électrolyse: I = 0.5-5 A
- Temps de demi-réaction: t₁/₂ entre 5 et 60 min

──── VERBES D'ATTAQUE Q1 (chimie) ────
TOP: "Écrire l'équation..." (6x), "Calculer..." (2x), "Parmi... choisir..." (2x)
→ Q1.1 commence souvent par "Écrire l'équation de la réaction de dosage."

──── PROFONDEUR NUMÉROTATION ────
Chimie utilise majoritairement 2 niveaux (1.1, 1.2, 2.1, 2.2): 152/246 questions
Niveau 1 (1, 2, 3): 81/246 — pour ex simples
Niveau 3 (1.1.1): 13/246 — pour sous-questions complexes
→ STRUCTURER: Partie 1 (Q1.1, Q1.2, ...) + Partie 2 (Q2.1, Q2.2, ...)

──── PHRASES D'INTRODUCTION ────
"Cet exercice porte sur..." (13x) ou "On se propose de..." (13x) sont les TOP

──── BARÈME CHIMIE (analyse niveau 3) ────
ÉQUILIBRE PARFAIT entre parties: Partie 1 ≈ Partie 2 (ratio 1.01)
- 2 parties: viser ~3.5pts chacune
- 3 parties: 2.5+2.5+2pts (cas fréquent quand combo triple)
- Partie 3 présente dans 17/20 examens

POSITION QUESTIONS HAUTE VALEUR (≥0.75pts):
- 39% en fin (Q75-100%) — questions de synthèse
- 25% en milieu-fin (Q50-75%)
- 19% en milieu-début (Q25-50%)
- 17% en début (Q1-25%)
→ Mettre les questions difficiles surtout en FIN de partie

QUESTIONS HAUTE VALEUR — VERBES TYPIQUES:
"Déterminer..." (38x), "Trouver..." (16x), "Calculer..." (14x), "Montrer..." (9x)
→ JAMAIS de définition à 0.75+pts. Toujours calcul ou démonstration.

QUESTIONS COURTES (≤0.25pts) — RÉPARTITION UNIFORME
Définitions, choix QCM, écriture simple → réparties partout

──── RÈGLES ROTATION SPÉCIFIQUES PC (différentes de SVT!) ────
- Chevauchement N vs R même année: 80% chimie, 70% élec, 40% méca
  → MÉCA est le domaine qui change le PLUS entre N et R
  → Chimie/Élec se RÉPÈTENT partiellement (DOSAGE, OSCIL, combos RC/RL/RLC)
- R(y) → N(y+1): RÉPÉTITIONS FRÉQUENTES (DOSAGE 4x, OSCIL souvent)
  → La règle SVT 'R≠N+1' NE S'APPLIQUE PAS en PC
- Pour différencier 2026N: VARIER LA MÉCA en priorité, plus que la chimie""",
        },
        "ondes": {
            "description": """ANALYSE 16 EXERCICES D'ONDES (2016-2025):
- Ondes mécaniques (50%): propagation surface eau, célérité v=d/Δt, retard τ, longueur d'onde λ
- Diffraction (35%): fente, sin(θ)=λ/a, largeur tache centrale L=2λD/a
- Ondes sonores (30%): célérité son, niveau sonore L=10log(I/I₀)
- Ondes lumineuses (30%): diffraction lumière, indice de réfraction n=c/v
- Ultrasons (10%): échographie, mesure distances d=vt/2

POINTS/QUESTION: 0.5pts dominant, puis 0.75pts
DOCUMENTS: 0docs=20%, 1doc=40%, 2docs=40%
STRUCTURE TYPE: 2-8 questions, 2-3.5pts, souvent 1-2 schémas (dispositif expérimental, figure diffraction).""",
        },
        "nucleaire": {
            "description": """ANALYSE 15 EXERCICES NUCLÉAIRES (2016-2025):
- Désintégration (90%): α, β⁻, β⁺, lois de conservation A et Z
- Activité (75%): A(t) = λN(t) = A₀e^{-λt}
- Demi-vie (80%): t₁/₂ = ln2/λ, détermination graphique
- Fusion/fission (10%): rare (2016N, 2023N)
- Datation (5%): carbone-14 (2022R uniquement)

ÉLÉMENTS DÉJÀ UTILISÉS (NE PAS RÉUTILISER):
Na-24(2016R), Pu-241(2018R), Co-60(2017R), Po-210(2020N), U-234(2020R),
Pu-238(2021N), P-32(2021R), I-131(2022N), Ir-192(2024N), Cd-107(2025N)
→ 2026N: NOUVEL élément obligatoire: Ra-226, Cs-137, Sr-90, Am-241, Bi-214, Th-232

DOCS: 60% sans document, 40% avec 1 doc (diagramme, courbe N(t) ou A(t))
POINTS/QUESTION: 0.5pts (moy.), parfois 1.0pts pour calcul d'énergie
STRUCTURE TYPE: 2-7 questions, 2-2.5pts.""",
        },
        "electricite": {
            "description": """ANALYSE APPROFONDIE 20 EXERCICES D'ÉLECTRICITÉ (2016-2025):

COMBINAISONS EXACTES (classées par fréquence):
1. RC+RL+RLC: 7x (35%) — LA PLUS FRÉQUENTE! Ex: 2016N, 2017R, 2019N, 2020N, 2020R, 2022N, 2024R
2. RL+RLC: 2x (10%) — 2018N, 2021R
3. RL+LC+modAM: 2x (10%) — 2023N, 2025R
4. RL+modAM+demod: 1x — 2016R
5. RL+modAM: 1x — 2017N
6. RL+LC+modAM+demod: 1x — 2018R
7. RL+RLC+modAM: 1x — 2019R
8. RC+LC+modAM: 1x — 2021N
9. RL+RLC+LC: 1x — 2022R
10. RC+RL+RLC+modAM: 1x — 2023R
11. RC+RL: 1x — 2024N
12. RC+modAM+demod: 1x — 2025N

→ 2026N PRÉDICTION: RC+RL+RLC (retour au combo #1) ou RL+RLC (2025N avait RC, rotation vers RL)

DOCUMENTS ELECTRICITÉ: 2-6 docs (schémas circuits, courbes u_C(t), i(t), oscillogrammes)
POINTS: 3.5-5.5pts, moy. 4.7pts
QUESTIONS: 7-12, moy. 10.1 questions par exercice.""",
        },
        "mecanique": {
            "description": """ANALYSE APPROFONDIE 20 EXERCICES DE MÉCANIQUE (2016-2025):

SOUS-TOPICS ISOLÉS (fréquence comme exercice principal):
- oscillateur seul: 9x (45%) — pendule simple/torsion/élastique, T₀
- plan_incline seul: 6x (30%) — avec/sans frottements, 2ème loi Newton
- chute_visqueuse: 4x (20%) — vitesse limite, f=kv
- projectile: 3x (15%) — mouvement parabolique, portée

COMBINAISONS OBSERVÉES:
- plan_incline+oscillateur: 2x (2022R, 2025R)
- chute_visqueuse+chute_libre+oscillateur: 1x (2018N)
- chute_libre+projectile+pendule_torsion: 1x (2019R)
- pendule_simple+champ_magnetique: 1x (2016N)
- chute_visqueuse+satellite: 1x (2022N)
- oscillateur+satellite: 1x (2025N)
- chute_libre+projectile+pendule_simple: 1x (2023N)

ROTATION RÉCENTE:
2024N=chute_visqueuse+plan_incline | 2024R=chute_libre+plan_incline
2025N=satellite+oscillateur | 2025R=skieur+pendule_torsion
→ 2026N PRÉDICTION: chute_visqueuse+oscillateur ou projectile+pendule (retour aux classiques)

DOCUMENTS MÉCANIQUE: 0docs=15%, 1doc=15%, 2docs=50%, 3docs=15%
STRUCTURE TYPE: 5-10 questions, 2.5-6pts, TOUJOURS dernier exercice.""",
        },
    }

    def _pick_domains_physique(self, curriculum: dict, target: Optional[list[str]]) -> dict:
        """Select Physique-Chimie domains using probability profiles."""
        if target:
            return {
                "exercises": [{"domain": d, "points": 5} for d in target],
                "profile_id": "custom",
                "profile_label": "Custom domains",
            }

        used = self._get_used_profile_ids("physique")
        available = [p for p in self.PHYSIQUE_EXAM_PROFILES if p["id"] not in used]
        
        if not available:
            logger.info("[MockExam:PC] All profiles used — resetting pool")
            available = list(self.PHYSIQUE_EXAM_PROFILES)
        
        weights = [p["weight"] for p in available]
        profile = random.choices(available, weights=weights, k=1)[0]
        
        logger.info(f"[MockExam:PC] Picked profile {profile['id']}: {profile['label']}")
        
        return {
            "exercises": profile["exercises"],
            "chimie_variant": profile.get("chimie_variant", "pile_dosage"),
            "ondes_sub": profile.get("ondes_sub"),
            "nuc_sub": profile.get("nuc_sub", "desintegration"),
            "elec_variant": profile.get("elec_variant", "RC_RLC"),
            "meca_variant": profile.get("meca_variant", "chute_visqueuse_oscillateur"),
            "structure": profile.get("structure", "4ex"),
            "profile_id": profile["id"],
            "profile_label": profile["label"],
        }

    async def generate_physique_mock_exam(
        self,
        target_domains: Optional[list[str]] = None,
    ) -> dict:
        """Generate a Physique-Chimie mock exam."""
        subject = "Physique-Chimie"
        subj_key = "physique"
        self._ensure_loaded(subj_key)
        curriculum = self._curriculum.get(subj_key, {})
        
        if not curriculum:
            raise ValueError(f"No curriculum found for {subject}")

        exam_id = f"mock_pc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        domains = self._pick_domains_physique(curriculum, target_domains)
        logger.info(f"[MockExam:PC] Generating {exam_id} | profile={domains.get('profile_id')}")

        exercises = []
        for i, ex_info in enumerate(domains["exercises"]):
            ex = await self._generate_physique_exercise(
                curriculum, ex_info["domain"], ex_info["points"], i + 1, domains
            )
            exercises.append(ex)

        exam = {
            "id": exam_id,
            "title": f"Examen Blanc Physique-Chimie — Session Normale {datetime.utcnow().year}",
            "subject": subject,
            "year": datetime.utcnow().year,
            "session": "Blanc (Normale)",
            "duration_minutes": 180,
            "coefficient": 7,
            "total_points": 20,
            "domains_covered": domains,
            "generated_at": datetime.utcnow().isoformat(),
            "status": "draft",
            "general_note": "L'usage de la calculatrice scientifique non programmable est autorisé. Les expressions littérales doivent être établies avant les applications numériques.",
            "parts": [{
                "name": "Examen",
                "exercises": exercises,
            }],
        }

        exam_dir = MOCK_EXAMS_DIR / subj_key / exam_id
        _save_json(exam_dir / "exam.json", exam)
        (exam_dir / "assets").mkdir(exist_ok=True)

        image_prompts = self._extract_image_prompts(exam)
        _save_json(exam_dir / "image_prompts.json", image_prompts)

        logger.info(f"[MockExam:PC] Generated {exam_id}: {len(exercises)} exercises")
        return exam

    async def _generate_physique_exercise(
        self, curriculum: dict, domain: str, points: float,
        exercise_num: int, domains: dict
    ) -> dict:
        """Generate a single Physique-Chimie exercise."""
        # Handle combined ondes_nucleaire domain
        actual_domain = domain
        if domain == "ondes_nucleaire":
            actual_domain = "ondes"  # Will combine in variant hint

        domain_info = {}
        for d in curriculum.get("domains", []):
            if d["id"] == actual_domain or d["id"] == domain:
                domain_info = d
                break

        guidance = self.PHYSIQUE_SUBTOPIC_GUIDANCE.get(actual_domain, {})
        subtopic_desc = guidance.get("description", "")

        # Build variant hints
        variant_hint = ""
        if domain == "chimie":
            cv = domains.get("chimie_variant", "pile_dosage")
            variant_map = {
                "pile_dosage": "STRUCTURE: Partie I — Étude d'une PILE électrochimique (f.é.m., équation-bilan, Q=nF). Partie II — DOSAGE acido-basique (courbe pH, V_éq, C_A).",
                "electrolyse_dosage": "STRUCTURE: Partie I — ÉLECTROLYSE (lois de Faraday, masse déposée). Partie II — DOSAGE acido-basique (pH-métrie, conductimétrie).",
                "pile_esterification": "STRUCTURE: Partie I — Étude d'une PILE. Partie II — ESTÉRIFICATION (réaction lente+limitée, constante K, rendement).",
                "electrolyse_esterification": "STRUCTURE: Partie I — ÉLECTROLYSE. Partie II — ESTÉRIFICATION et/ou HYDROLYSE basique.",
                "cinetique_dosage": "STRUCTURE: Partie I — CINÉTIQUE chimique (suivi temporel, v(t), t₁/₂). Partie II — DOSAGE acido-basique.",
                "cinetique_esterification": "STRUCTURE: Partie I — CINÉTIQUE (vitesse, facteurs cinétiques). Partie II — ESTÉRIFICATION (K, rendement).",
                "electrolyse_dosage_cinetique": "STRUCTURE: Partie I — ÉLECTROLYSE. Partie II — DOSAGE + suivi CINÉTIQUE.",
            }
            variant_hint = variant_map.get(cv, "")
            variant_hint += "\nIMPORTANT: L'exercice fait TOUJOURS 7pts avec 10-15 questions. Fournir TOUTES les données numériques (M, pKa, Ke, C, V)."
        elif domain == "ondes_nucleaire":
            ondes_sub = domains.get("ondes_sub")
            nuc_sub = domains.get("nuc_sub")
            parts = []
            if ondes_sub:
                sub_map = {
                    "ondes_mecaniques": "ONDES MÉCANIQUES: propagation surface eau, célérité v=d/Δt, longueur d'onde λ=vT",
                    "diffraction": "DIFFRACTION de la lumière: fente, sin(θ)=λ/a, largeur tache L=2λD/a",
                    "ultrasons": "ULTRASONS: échographie, mesure distance d=vt/2, célérité",
                    "ondes_sonores": "ONDES SONORES: célérité son, niveau sonore L=10log(I/I₀)",
                    "ondes_lumineuses": "ONDES LUMINEUSES: diffraction, indice réfraction n=c/v, Snell-Descartes",
                }
                parts.append(sub_map.get(ondes_sub, "Ondes"))
            if nuc_sub:
                nuc_map = {
                    "desintegration": "DÉSINTÉGRATION radioactive: écrire l'équation, λ, t₁/₂, A(t). Utiliser un NOUVEL élément (Ra-226, Cs-137, Sr-90, Am-241).",
                    "fusion_fission": "ÉNERGIE NUCLÉAIRE: fusion ou fission, défaut de masse, E=Δm×c², courbe d'Aston",
                    "datation": "DATATION radioactive: carbone-14 ou autre, t=-ln(N/N₀)/λ",
                }
                parts.append(nuc_map.get(nuc_sub, "Nucléaire"))
            variant_hint = "CONTENU COMBINÉ:\n" + "\n".join(f"- {p}" for p in parts)
        elif domain == "ondes":
            ondes_sub = domains.get("ondes_sub", "ondes_mecaniques")
            sub_map = {
                "ondes_mecaniques": "FOCUS: Ondes mécaniques progressives. Célérité, retard, longueur d'onde, diffraction.",
                "diffraction": "FOCUS: Diffraction de la lumière. Fente, sin(θ)=λ/a, tache centrale.",
                "ultrasons": "FOCUS: Ultrasons. Échographie, mesure de distances.",
                "ondes_sonores": "FOCUS: Ondes sonores. Célérité, niveau d'intensité sonore.",
                "ondes_lumineuses": "FOCUS: Ondes lumineuses. Diffraction, indice de réfraction.",
            }
            variant_hint = sub_map.get(ondes_sub, "")
        elif domain == "nucleaire":
            nuc_sub = domains.get("nuc_sub", "desintegration")
            nuc_map = {
                "desintegration": "FOCUS: Désintégration radioactive. Écrire l'équation, calculer λ, t₁/₂, A(t). Utiliser un NOUVEL élément.",
                "fusion_fission": "FOCUS: Énergie nucléaire. Fusion ou fission, défaut de masse, E=Δm×c².",
                "datation": "FOCUS: Datation radioactive. Utiliser carbone-14 ou autre isotope.",
            }
            variant_hint = nuc_map.get(nuc_sub, "")
        elif domain == "electricite":
            ev = domains.get("elec_variant", "RC_RL_RLC")
            elec_map = {
                "RC_RL_RLC": "STRUCTURE (combo #1, 35%): Partie I — Dipôle RC (charge/décharge, τ=RC, énergie E=½Cu²). Partie II — Dipôle RL (échelon, τ=L/R). Partie III — Circuit RLC série (oscillations amorties, pseudo-période, équation diff).",
                "RL_modulation": "STRUCTURE (combo #3): Partie I — Dipôle RL (échelon de tension, τ=L/R, i(t)). Partie II — Modulation d'amplitude (signal modulé u(t), taux m≤1, spectre).",
                "RC_demodulation": "STRUCTURE: Partie I — Dipôle RC (charge/décharge). Partie II — Démodulation AM (détection d'enveloppe, filtre passe-bas RC).",
                "RL_RLC": "STRUCTURE (combo #2, 10%): Partie I — Dipôle RL (échelon, τ=L/R). Partie II — Circuit RLC série (oscillations libres amorties, pseudo-période).",
                "RC_LC_modulation": "STRUCTURE: Partie I — Dipôle RC (charge, τ=RC). Partie II — Circuit LC (oscillations libres, T₀=2π√LC). Partie III — Modulation d'amplitude.",
                "RL_LC_modulation": "STRUCTURE (combo #3, 10%): Partie I — Dipôle RL (échelon, τ=L/R). Partie II — Circuit LC (T₀=2π√LC). Partie III — Modulation d'amplitude (taux m).",
                "RC_modulation_demodulation": "STRUCTURE: Partie I — Dipôle RC (charge/décharge). Partie II — Modulation AM. Partie III — Démodulation (détection enveloppe + filtre passe-bas).",
            }
            variant_hint = elec_map.get(ev, "")
        elif domain == "mecanique":
            mv = domains.get("meca_variant", "chute_visqueuse_oscillateur")
            meca_map = {
                "chute_visqueuse_oscillateur": "STRUCTURE: Partie I — Chute dans un liquide VISQUEUX (v_lim, régime permanent). Partie II — Oscillateur mécanique (T₀, énergie).",
                "projectile_pendule_torsion": "STRUCTURE: Partie I — Mouvement PARABOLIQUE (projectile, portée, flèche). Partie II — Pendule de TORSION (T₀=2π√(J/C)).",
                "satellite_oscillateur": "STRUCTURE: Partie I — Mouvement d'un SATELLITE (v orbitale, T, Kepler). Partie II — Oscillateur mécanique.",
                "plan_incline_oscillateur": "STRUCTURE: Partie I — Mouvement sur PLAN INCLINÉ (avec frottements). Partie II — Oscillateur mécanique (pendule élastique).",
                "chute_libre_oscillateur": "STRUCTURE: Partie I — Chute LIBRE (a=g, v=gt). Partie II — Oscillateur mécanique.",
                "champ_magnetique_pendule": "STRUCTURE: Partie I — Mouvement dans un champ MAGNÉTIQUE (force de Lorentz, r=mv/qB). Partie II — Pendule simple.",
                "chute_visqueuse": "Chute dans un liquide visqueux — vitesse limite, équation différentielle, régime transitoire/permanent.",
                "chute_visqueuse_satellite": "STRUCTURE: Partie I — Chute VISQUEUSE. Partie II — Mouvement d'un SATELLITE.",
                "chute_libre_pendule_simple": "STRUCTURE: Partie I — Chute LIBRE. Partie II — Pendule SIMPLE (T₀=2π√(l/g)).",
                "chute_libre_parachutiste": "STRUCTURE: Partie I — Chute LIBRE puis avec frottements (parachutiste: v_lim, régimes). Exercice court (2.5pts, 5-7Q).",
            }
            variant_hint = meca_map.get(mv, "")

        # Get domain info for combined ondes_nucleaire
        if domain == "ondes_nucleaire":
            # Merge ondes + nucleaire chapters
            nuc_info = {}
            for d in curriculum.get("domains", []):
                if d["id"] == "nucleaire":
                    nuc_info = d
                    break
            chapters = domain_info.get("chapters", []) + nuc_info.get("chapters", [])
            patterns = domain_info.get("typical_question_patterns", []) + nuc_info.get("typical_question_patterns", [])
            nuc_guidance = self.PHYSIQUE_SUBTOPIC_GUIDANCE.get("nucleaire", {}).get("description", "")
            subtopic_desc = subtopic_desc + "\n\n" + nuc_guidance
        else:
            chapters = domain_info.get("chapters", [])
            patterns = domain_info.get("typical_question_patterns", [])

        # Sample real exercises
        sample_domain = "ondes" if domain == "ondes_nucleaire" else domain
        examples = _sample_exercises("physique", sample_domain, 3)
        if domain == "ondes_nucleaire":
            examples += _sample_exercises("physique", "nucleaire", 2)
        examples_text = ""
        for ex in examples:
            e = ex["exercise"]
            examples_text += f"\n--- Exemple ({ex['exam']}) ---\n"
            examples_text += f"Nom: {e.get('name', '')}\n"
            examples_text += f"Points: {e.get('points', 0)}\n"
            examples_text += f"Contexte: {(e.get('context') or '')[:300]}\n"
            for q in e.get("questions", [])[:4]:
                examples_text += f"  Q{q.get('number','?')} ({q.get('points',0)}pts): {q.get('content','')[:200]}\n"

        topics_text = json.dumps(chapters, ensure_ascii=False, indent=2)
        patterns_text = json.dumps(patterns, ensure_ascii=False, indent=2)

        n_docs = random.randint(1, 4) if domain != "chimie" else random.randint(1, 2)
        n_questions = random.randint(8, 13) if domain == "chimie" else random.randint(4, 10)

        system = f"""Tu es un expert en création d'examens nationaux de Physique-Chimie du Baccalauréat marocain (2ème Bac Sciences Physiques).
Tu génères UN exercice conforme au format exact de l'examen national.
RÈGLE ABSOLUE: l'exercice doit porter UNIQUEMENT sur le programme officiel.
NIVEAU: IDENTIQUE à l'examen national réel — mêmes types de raisonnement, même profondeur.
NOTATION: LaTeX pour TOUTES les formules: $v = \\frac{{d}}{{\\Delta t}}$, $\\tau = RC$, etc.
UNITÉS: TOUJOURS inclure les unités (SI) dans les données ET les réponses.
EXPRESSIONS LITTÉRALES: Établir AVANT les applications numériques.

{subtopic_desc}

Réponds en JSON valide uniquement."""

        domain_label = domain_info.get('name', domain)
        if domain == "ondes_nucleaire":
            domain_label = "Ondes et Transformations nucléaires"

        prompt = f"""Génère l'Exercice {exercise_num} ({points}pts) d'un examen blanc Physique-Chimie — Session Normale 2026.

DOMAINE: {domain_label}

PROGRAMME AUTORISÉ:
{topics_text}

TYPES DE QUESTIONS TYPIQUES:
{patterns_text}

{('VARIANTE SPÉCIFIQUE:' + chr(10) + variant_hint) if variant_hint else ''}

EXEMPLES DE VRAIS EXERCICES NATIONAUX:
{examples_text}

INSTRUCTIONS:
1. Génère un exercice COMPLET avec {n_questions} questions progressives, total = {points}pts.
2. Fournir un CONTEXTE scientifique (données numériques, constantes, conditions expérimentales).
3. Inclure {n_docs} documents (schéma circuit, courbe, figure expérimentale) si pertinent.
4. Chaque question: numéro, points (0.25 à 1.5pts), contenu en LaTeX, correction COMPLÈTE.
5. Les corrections incluent TOUJOURS l'expression littérale PUIS l'application numérique.
6. Style IDENTIQUE aux examens nationaux marocains.
7. Pour les documents, fournir un PROMPT_IMAGE décrivant le contenu visuel.

Réponds avec ce JSON:
{{"name":"Exercice {exercise_num} — {domain_label}","points":{points},"context":"Les deux parties sont indépendantes...\\n\\n**Données :**\\n- ...","documents":[
  {{"id":"doc_e{exercise_num}_1","type":"schema","title":"Document 1","description":"...","PROMPT_IMAGE":"...","src":"assets/doc{exercise_num}_1.png"}}
],"questions":[
  {{"number":"1.1","type":"open","points":0.5,"content":"Écrire l'équation...","documents":["doc_e{exercise_num}_1"],"correction":{{"content":"..."}}}}
]}}"""

        return await _call_deepseek(system, prompt, f"PC_Ex{exercise_num}", max_tokens=6144)

    def _extract_image_prompts(self, exam: dict) -> list[dict]:
        """Extract all PROMPT_IMAGE fields from the exam for the admin."""
        prompts = []
        for part in exam.get("parts", []):
            for ex in part.get("exercises", []):
                for doc in ex.get("documents", []):
                    if doc.get("PROMPT_IMAGE"):
                        prompts.append({
                            "doc_id": doc.get("id", ""),
                            "exercise": ex.get("name", ""),
                            "title": doc.get("title", ""),
                            "type": doc.get("type", ""),
                            "description": doc.get("description", ""),
                            "prompt": doc["PROMPT_IMAGE"],
                            "target_file": doc.get("src", ""),
                        })
        return prompts

    # ─── List & manage mock exams ──────────────────────────────────────

    def list_mock_exams(self, subject: Optional[str] = None) -> list[dict]:
        """List all generated mock exams."""
        exams = []
        search_dir = MOCK_EXAMS_DIR / self._normalize_subject(subject) if subject else MOCK_EXAMS_DIR
        if not search_dir.exists():
            return []
        for subj_dir in (search_dir.iterdir() if not subject else [search_dir]):
            if not subj_dir.is_dir():
                continue
            for exam_dir in subj_dir.iterdir():
                exam_path = exam_dir / "exam.json"
                if not exam_path.exists():
                    continue
                try:
                    exam = _load_json(exam_path)
                    exams.append({
                        "id": exam.get("id", exam_dir.name),
                        "title": exam.get("title", ""),
                        "subject": exam.get("subject", ""),
                        "status": exam.get("status", "draft"),
                        "generated_at": exam.get("generated_at", ""),
                        "domains_covered": exam.get("domains_covered", {}),
                    })
                except Exception as e:
                    logger.warning(f"Could not load mock exam {exam_dir}: {e}")
        return sorted(exams, key=lambda x: x.get("generated_at", ""), reverse=True)

    def get_mock_exam(self, subject: str, exam_id: str) -> Optional[dict]:
        """Load a specific mock exam.

        Auto-detects uploaded images: if a doc has empty ``src`` but a file
        matching ``{doc_id}.*`` exists in ``assets/``, the ``src`` is filled
        in on-the-fly so the frontend / printable HTML can render it.
        """
        exam_dir = MOCK_EXAMS_DIR / self._normalize_subject(subject) / exam_id
        path = exam_dir / "exam.json"
        if not path.exists():
            return None
        exam = _load_json(path)
        # Lazy import to avoid a circular dependency (exam_service imports
        # mock_exam_service indirectly via the API layer).
        from app.services.exam_service import _autofill_doc_src_from_assets
        _autofill_doc_src_from_assets(exam, exam_dir / "assets")
        return exam

    def get_image_prompts(self, subject: str, exam_id: str) -> list[dict]:
        """Load image prompts for a mock exam."""
        path = MOCK_EXAMS_DIR / self._normalize_subject(subject) / exam_id / "image_prompts.json"
        if path.exists():
            return _load_json(path)
        return []

    def update_mock_exam_status(self, subject: str, exam_id: str, status: str) -> bool:
        """Update the status of a mock exam (draft → published)."""
        path = MOCK_EXAMS_DIR / self._normalize_subject(subject) / exam_id / "exam.json"
        if not path.exists():
            return False
        exam = _load_json(path)
        exam["status"] = status
        _save_json(path, exam)
        return True

    def publish_mock_exam(self, subject: str, exam_id: str) -> bool:
        """Publish a mock exam: copy to the main exams directory."""
        return self.update_mock_exam_status(subject, exam_id, "published")


mock_exam_service = MockExamService()
