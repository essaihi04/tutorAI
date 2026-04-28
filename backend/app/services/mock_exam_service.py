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
        if len(parts) < 2:
            continue
        for ex in parts[1].get("exercises", []):
            ctx = (ex.get("context") or "").lower()
            name = (ex.get("name") or "").lower()
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
        "consommation_matiere_organique": ["respiration", "fermentation", "glycolyse", "krebs", "atp", "mitochondri", "muscle", "contraction", "effort", "endurance"],
        "genetique_expression": ["gene", "allele", "mutation", "proteine", "transcri", "traduction", "codon", "arnm", "maladie"],
        "genetique_transmission": ["croisement", "f1", "f2", "dominant", "recessif", "echiquier", "dihybrid"],
        "geologie": ["subduction", "collision", "metamorphi", "magma", "plaque", "faille", "chaine"],
        "environnement_sante": ["pollution", "nitrate", "pesticide", "dechet", "step", "ozone", "co2", "rechauffement"],
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
        
        Domain logic is based on deep analysis of 2016-2025 exams:
        - Part1 domain is ALWAYS different from Part2 domains (mutual exclusivity)
        - Part1 Normale != Part1 Rattrapage for the same year  
        - Part2 Ex1 = CMO (60%), Ex2 = GEN_EXP (60%), Ex3 = ENV/GEO/GEN_TRANS
        - After GEO in 2025N, 2026N likely has CMO or ENV in Part1
        
        Returns the exam JSON with image prompts (PROMPT_IMAGE fields)
        instead of actual image files.
        """
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
        search_dir = MOCK_EXAMS_DIR / subject.lower() if subject else MOCK_EXAMS_DIR
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
        """Load a specific mock exam."""
        path = MOCK_EXAMS_DIR / subject.lower() / exam_id / "exam.json"
        if path.exists():
            return _load_json(path)
        return None

    def get_image_prompts(self, subject: str, exam_id: str) -> list[dict]:
        """Load image prompts for a mock exam."""
        path = MOCK_EXAMS_DIR / subject.lower() / exam_id / "image_prompts.json"
        if path.exists():
            return _load_json(path)
        return []

    def update_mock_exam_status(self, subject: str, exam_id: str, status: str) -> bool:
        """Update the status of a mock exam (draft → published)."""
        path = MOCK_EXAMS_DIR / subject.lower() / exam_id / "exam.json"
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
