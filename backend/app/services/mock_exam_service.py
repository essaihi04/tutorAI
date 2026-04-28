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
        difficulty: str = "moyen",
        target_domains: Optional[list[str]] = None,
    ) -> dict:
        """Generate a full mock exam for a given subject.
        
        Returns the exam JSON with image prompts (PROMPT_IMAGE fields)
        instead of actual image files.
        """
        self._ensure_loaded(subject)
        curriculum = self._curriculum.get(subject.lower(), {})
        blueprint = self._blueprint.get(subject.lower(), {})
        
        if not curriculum or not blueprint:
            raise ValueError(f"No curriculum/blueprint found for {subject}")

        exam_id = f"mock_{subject.lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # ── Choose domain distribution ──
        domains = self._pick_domains(curriculum, blueprint, target_domains)
        logger.info(f"[MockExam] Generating {exam_id} | domains: {domains}")

        # ── Generate Part 1 ──
        part1 = await self._generate_part1(subject, curriculum, blueprint, domains, difficulty)

        # ── Generate Part 2 exercises ──
        # Choose exercise pattern
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
                subject, curriculum, blueprint, domain, pts, i + 1, difficulty
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
            "title": f"Examen Blanc SVT - Niveau {difficulty.capitalize()}",
            "subject": subject,
            "year": datetime.utcnow().year,
            "session": "Blanc",
            "duration_minutes": 180,
            "coefficient": 5,
            "total_points": 20,
            "difficulty": difficulty,
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

    def _pick_domains(self, curriculum: dict, blueprint: dict, target: Optional[list[str]]) -> dict:
        """Select domains for Part1 and Part2 based on rotation analysis."""
        all_domains = [d["id"] for d in curriculum.get("domains", [])]
        
        if target:
            # User-specified domains
            part2_domains = target[:4]
            while len(part2_domains) < 3:
                extra = random.choice([d for d in all_domains if d not in part2_domains])
                part2_domains.append(extra)
        else:
            # Use rotation analysis: pick mandatory + alternating
            rotation = blueprint.get("structure", {}).get("part2", {}).get("domain_rotation", {})
            mandatory = [m["domain"] for m in rotation.get("mandatory", [])]
            alternates = [a["domain"] for a in rotation.get("third_exercise_alternates", [])]
            third = random.choice(alternates) if alternates else "environnement_sante"
            part2_domains = mandatory + [third]

        # Part1 typically covers geologie or consommation
        part1_domain = random.choice(["geologie", "consommation_matiere_organique", part2_domains[0]])
        
        return {
            "part1": part1_domain,
            "part2": part2_domains,
        }

    async def _generate_part1(self, subject: str, curriculum: dict, blueprint: dict, domains: dict, difficulty: str) -> dict:
        """Generate Part 1 (Restitution des connaissances)."""
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

        system = f"""Tu es un expert en création d'examens nationaux SVT du Baccalauréat marocain.
Tu génères UNIQUEMENT la Première partie (Restitution des connaissances, 5pts).
RÈGLE ABSOLUE: toutes les questions doivent porter sur le programme officiel SVT 2ème Bac (cadre de référence).
Difficulté: {difficulty}
Réponds en JSON valide uniquement."""

        prompt = f"""Génère la Première partie d'un examen blanc SVT.

DOMAINE PRINCIPAL: {domain_info.get('name', domains['part1'])}

CHAPITRES AUTORISÉS (ne sors JAMAIS de ce cadre):
{topics_text}

STRUCTURE ATTENDUE (4 questions, total 5pts):
{slots_text}

EXEMPLES DE VRAIES QUESTIONS NATIONALES:
{examples_text}

INSTRUCTIONS:
1. Question I: QCM avec 4 items (0.5pt chacun, total 2pts). 4 choix a/b/c/d. UNE seule bonne réponse.
2. Question II: Question ouverte courte (définition, citation, explication). 0.5 ou 1pt.
3. Question III: Vrai/Faux avec 4 affirmations (0.25pt chacune, total 1pt). 
4. Question IV: Association de 4 éléments ensemble A avec ensemble B (5 éléments, 1 distracteur). 1pt.
5. Chaque question DOIT avoir une correction complète.
6. Le style doit être identique aux examens nationaux (formulations en français, style formel).

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

    async def _generate_exercise(
        self, subject: str, curriculum: dict, blueprint: dict,
        domain: str, points: float, exercise_num: int, difficulty: str
    ) -> dict:
        """Generate a single Part 2 exercise with context, documents, and questions."""
        # Find domain info
        domain_info = {}
        for d in curriculum.get("domains", []):
            if d["id"] == domain or domain.startswith(d["id"]):
                domain_info = d
                break

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
Difficulté: {difficulty}
Réponds en JSON valide uniquement."""

        prompt = f"""Génère l'Exercice {exercise_num} ({points}pts) d'un examen blanc SVT.

DOMAINE: {domain_info.get('name', domain)}

CHAPITRES AUTORISÉS (ne sors JAMAIS de ce cadre):
{topics_text}

TYPES DE DOCUMENTS TYPIQUES POUR CE DOMAINE:
{typical_docs}

EXEMPLES DE VRAIS EXERCICES NATIONAUX:
{examples_text}

INSTRUCTIONS:
1. Écris un CONTEXTE scientifique réaliste (200-500 caractères) introduisant un phénomène biologique/géologique.
2. Crée {n_docs} documents. Pour CHAQUE document, donne:
   - id: "doc_e{exercise_num}_N"
   - type: "figure", "schema", "tableau", "graphique"
   - title: "Document N"
   - description: description détaillée du contenu visuel
   - PROMPT_IMAGE: un prompt DÉTAILLÉ pour générer cette image (style scientifique BAC marocain: axes, légendes, valeurs numériques, couleurs sobres)
3. Crée {n_questions} questions progressives (du simple au complexe), total = {points}pts.
4. Chaque question référence ses documents via "documents": ["doc_e{exercise_num}_N"].
5. Chaque question a une correction complète et structurée.
6. Les questions utilisent les verbes: décrire, comparer, expliquer, déduire, montrer, proposer une hypothèse...
7. Style IDENTIQUE aux examens nationaux marocains.

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
                        "difficulty": exam.get("difficulty", ""),
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
