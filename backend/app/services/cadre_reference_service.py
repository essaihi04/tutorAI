"""
Cadre de Référence Service
===========================
Loads and provides exam requirements from official BAC reference documents.
Identifies what is required for exams vs supplementary content.
"""
import json
import logging
from pathlib import Path
from typing import Optional

_log = logging.getLogger(__name__)

CADRES_DIR = Path(__file__).parent.parent.parent / "cours 2bac pc" / "cadres de references 2BAC PC"

# Map subject names to their cadre de référence JSON files
CADRE_FILES = {
    "SVT": "cadre-de-reference-de-l-examen-national-svt-sciences-physiques (1).json",
    "Mathematiques": "cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json",
    "Physique": "cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json",
    "Chimie": "cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json",
}


class CadreReferenceService:
    """Service to access exam requirements from cadres de référence."""
    
    def __init__(self):
        self._cache: dict[str, dict] = {}
    
    def _load_cadre(self, subject: str) -> Optional[dict]:
        """Load cadre de référence JSON for a subject."""
        # Normalize subject name
        subject_key = self._normalize_subject(subject)
        
        if subject_key in self._cache:
            return self._cache[subject_key]
        
        filename = CADRE_FILES.get(subject_key)
        if not filename:
            _log.warning(f"No cadre de référence found for subject: {subject}")
            return None
        
        filepath = CADRES_DIR / filename
        if not filepath.exists():
            _log.warning(f"Cadre file not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Some JSON files are lists (e.g., physics/chemistry) instead of dicts
            # Normalize: if list, take first element; wrap non-dict in a dict
            if isinstance(data, list):
                data = data[0] if data and isinstance(data[0], dict) else {"raw": data}
            if not isinstance(data, dict):
                data = {"raw": data}
            self._cache[subject_key] = data
            return data
        except Exception as e:
            _log.error(f"Error loading cadre: {e}")
            return None
    
    def _normalize_subject(self, subject: str) -> str:
        """Normalize subject name to match CADRE_FILES keys."""
        s = subject.lower().strip()
        if "math" in s:
            return "Mathematiques"
        if "physi" in s:
            return "Physique"
        if "chimi" in s:
            return "Chimie"
        if "svt" in s or "vie" in s:
            return "SVT"
        return subject
    
    def get_exam_requirements(self, subject: str, topic: str = "") -> dict:
        """
        Get exam requirements for a subject/topic.
        Returns:
            - connaissances: List of knowledge items required for exam
            - objectifs: List of objectives/skills tested in exam
            - pourcentage: Weight in exam (e.g., "25%")
            - types_questions: Types of questions asked
            - priorite: Priority level (haute/moyenne/basse)
        """
        cadre = self._load_cadre(subject)
        if not cadre or not isinstance(cadre, dict):
            return {"error": "Cadre de référence non disponible"}
        
        result = {
            "subject": subject,
            "connaissances_examen": [],
            "objectifs_examen": [],
            "pourcentage_examen": "",
            "types_questions": [],
            "habiletes": [],
        }
        
        # Try SVT-style structure (has "sections" key)
        sections = cadre.get("sections", [])
        if isinstance(sections, list) and sections:
            self._extract_from_svt_structure(sections, topic, result)
            return result
        
        # Try Physics/Chemistry-style structure (has "content_structure_physics" etc.)
        self._extract_from_physics_structure(cadre, topic, result)
        return result

    def _extract_from_svt_structure(self, sections: list, topic: str, result: dict):
        """Extract requirements from SVT-style JSON with sections/sous_sections."""
        for section in sections:
            if not isinstance(section, dict):
                continue
            # Section II contains the detailed requirements
            if section.get("id") == "II":
                for sous_section in section.get("sous_sections", []):
                    if not isinstance(sous_section, dict):
                        continue
                    # Tableau des contenus
                    if sous_section.get("id") == "1":
                        tableau = sous_section.get("tableau", [])
                        if not isinstance(tableau, list):
                            continue
                        for domaine in tableau:
                            if not isinstance(domaine, dict):
                                continue
                            domaine_name = domaine.get("domaine", "")
                            pourcentage = domaine.get("pourcentage_recouvrement", "")
                            
                            # If topic specified, filter by domain
                            if topic and topic.lower() not in domaine_name.lower():
                                continue
                            
                            result["pourcentage_examen"] = pourcentage
                            
                            for sd in domaine.get("sous_domaines", []):
                                if not isinstance(sd, dict):
                                    continue
                                sd_name = sd.get("nom", "")
                                connaissances = sd.get("connaissances", [])
                                objectifs = sd.get("objectifs", [])
                                
                                for c in connaissances:
                                    if isinstance(c, str):
                                        result["connaissances_examen"].append({
                                            "domaine": domaine_name,
                                            "sous_domaine": sd_name,
                                            "contenu": c,
                                            "priorite": "haute"
                                        })
                                
                                for o in objectifs:
                                    if isinstance(o, str):
                                        result["objectifs_examen"].append({
                                            "domaine": domaine_name,
                                            "sous_domaine": sd_name,
                                            "objectif": o,
                                            "priorite": "haute"
                                        })
                    
                    # Tableau des habiletés
                    if sous_section.get("id") == "2":
                        tableau = sous_section.get("tableau", [])
                        if not isinstance(tableau, list):
                            continue
                        for hab in tableau:
                            if not isinstance(hab, dict):
                                continue
                            result["habiletes"].append({
                                "domaine": hab.get("domaine_habiletes", ""),
                                "importance": hab.get("importance", ""),
                                "description": hab.get("habiletes", [])
                            })
            
            # Section III contains exam structure
            if section.get("id") == "III":
                structure = section.get("structure")
                if isinstance(structure, dict):
                    partie1 = structure.get("partie_1")
                    if isinstance(partie1, dict):
                        result["types_questions"] = partie1.get("types_questions", [])

    def _extract_from_physics_structure(self, cadre: dict, topic: str, result: dict):
        """Extract requirements from Physics/Chemistry-style JSON with content_structure_* keys."""
        subject_key = self._normalize_subject(result.get("subject", ""))
        
        # Determine which content structure to use
        content_keys = []
        if subject_key in ("Physique",):
            content_keys = ["content_structure_physics"]
        elif subject_key in ("Chimie",):
            content_keys = ["content_structure_chemistry"]
        else:
            content_keys = ["content_structure_physics", "content_structure_chemistry"]
        
        for ck in content_keys:
            structure = cadre.get(ck)
            if not isinstance(structure, dict):
                continue
            sub_domains = structure.get("sub_domains", [])
            if not isinstance(sub_domains, list):
                continue
            for sd in sub_domains:
                if not isinstance(sd, dict):
                    continue
                sd_title = sd.get("title", "")
                topics_list = sd.get("topics", [])
                
                # If topic specified, filter
                if topic and topic.lower() not in sd_title.lower():
                    # Also check if topic matches any individual topic
                    has_match = any(topic.lower() in t.lower() for t in topics_list if isinstance(t, str))
                    if not has_match:
                        continue
                
                for t in topics_list:
                    if isinstance(t, str):
                        result["connaissances_examen"].append({
                            "domaine": structure.get("domaine_principal", ""),
                            "sous_domaine": sd_title,
                            "contenu": t,
                            "priorite": "haute"
                        })
        
        # Extract weights
        weight_tables = cadre.get("weight_tables")
        if isinstance(weight_tables, dict):
            domains_weights = weight_tables.get("domains_weights", {})
            if isinstance(domains_weights, dict):
                for domain_name, domain_data in domains_weights.items():
                    if isinstance(domain_data, dict):
                        result["pourcentage_examen"] = domain_data.get("total_weight", "")
                        details = domain_data.get("details", [])
                        if isinstance(details, list):
                            for d in details:
                                if isinstance(d, dict):
                                    result["habiletes"].append({
                                        "domaine": d.get("sub_domain", ""),
                                        "importance": d.get("weight", ""),
                                        "description": []
                                    })
    
    def get_priority_notes(self, subject: str, topic: str = "") -> str:
        """
        Generate a formatted string of priority items to note for exam.
        This is what the student should write in their notebook.
        """
        reqs = self.get_exam_requirements(subject, topic)
        
        if "error" in reqs:
            return ""
        
        lines = []
        lines.append(f"📚 **ÉLÉMENTS PRIORITAIRES À NOTER** ({subject})")
        lines.append(f"⚠️ Ces éléments sont demandés à l'examen national BAC")
        lines.append("")
        
        # Connaissances
        if reqs["connaissances_examen"]:
            lines.append("### 📝 CONNAISSANCES REQUISES:")
            seen_domains = set()
            for c in reqs["connaissances_examen"][:10]:  # Limit to 10
                domain = c.get("sous_domaine", "")
                if domain not in seen_domains:
                    lines.append(f"\n**{domain}**")
                    seen_domains.add(domain)
                lines.append(f"  • {c['contenu']}")
        
        # Objectifs
        if reqs["objectifs_examen"]:
            lines.append("\n### 🎯 OBJECTIFS À MAÎTRISER:")
            for o in reqs["objectifs_examen"][:8]:  # Limit to 8
                lines.append(f"  • {o['objectif']}")
        
        # Types de questions
        if reqs["types_questions"]:
            lines.append("\n### ❓ TYPES DE QUESTIONS À L'EXAMEN:")
            for t in reqs["types_questions"]:
                lines.append(f"  • {t}")
        
        # Pourcentage
        if reqs["pourcentage_examen"]:
            lines.append(f"\n📊 **Poids dans l'examen:** {reqs['pourcentage_examen']}")
        
        return "\n".join(lines)
    
    def get_topic_exam_info(self, subject: str, topic: str) -> dict:
        """
        Get specific exam info for a topic.
        Returns structured data for display in coaching mode.
        """
        reqs = self.get_exam_requirements(subject, topic)
        
        if "error" in reqs:
            return {"is_exam_topic": False, "priority": "basse"}
        
        # Check if topic is in exam requirements
        is_exam_topic = bool(reqs["connaissances_examen"] or reqs["objectifs_examen"])
        
        return {
            "is_exam_topic": is_exam_topic,
            "priority": "haute" if is_exam_topic else "basse",
            "pourcentage": reqs["pourcentage_examen"],
            "connaissances_count": len(reqs["connaissances_examen"]),
            "objectifs_count": len(reqs["objectifs_examen"]),
            "note_en_cahier": is_exam_topic,  # Should be noted in notebook
        }


# Singleton instance
cadre_service = CadreReferenceService()
