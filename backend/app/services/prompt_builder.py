"""
Prompt Builder Service
Builds dynamic prompts for the AI tutor based on lesson context and student profile.
Uses RAG from cadres de référence for coaching and diagnostic prompts.
"""
from typing import Optional
from app.services.rag_service import get_rag_service


class PromptBuilder:
    def build_lesson_prompt(
        self,
        subject: str,
        chapter_title: str,
        lesson_title: str,
        phase: str,
        objective: str,
        scenario: Optional[str] = None,
        student_name: str = "l'étudiant",
        proficiency: str = "intermédiaire",
        language: str = "français",
        teaching_mode: str = "Socratique",
        struggles: str = "aucune identifiée",
        mastered: str = "aucun",
    ) -> dict:
        """Build complete prompt context for a lesson phase."""
        return {
            "subject": subject,
            "language": language,
            "chapter_title": chapter_title,
            "lesson_title": lesson_title,
            "phase": phase,
            "objective": objective,
            "scenario_context": scenario or "",
            "student_name": student_name,
            "proficiency": proficiency,
            "struggles": struggles,
            "mastered": mastered,
            "teaching_mode": teaching_mode,
        }

    def build_exercise_correction_prompt(
        self,
        exercise_question: str,
        student_answer: str,
        correct_answer: str,
        is_correct: bool,
        explanation: str,
        language: str = "français"
    ) -> str:
        """Build a prompt for exercise correction feedback."""
        if is_correct:
            return (
                f"L'étudiant a correctement répondu à la question: '{exercise_question}'. "
                f"Sa réponse: '{student_answer}'. "
                f"Félicite-le brièvement et explique pourquoi c'est correct en 1-2 phrases. "
                f"Explication de référence: {explanation}"
            )
        else:
            return (
                f"L'étudiant s'est trompé à la question: '{exercise_question}'. "
                f"Sa réponse: '{student_answer}'. Réponse correcte: '{correct_answer}'. "
                f"Corrige-le avec douceur. Identifie la potentielle misconception. "
                f"Explique pourquoi la bonne réponse est correcte en 2-3 phrases. "
                f"Explication de référence: {explanation}"
            )

    def build_diagnostic_prompt(self, subject: str, language: str = "français") -> str:
        """Build prompt for diagnostic assessment phase with RAG context."""
        rag_section = ""
        try:
            rag = get_rag_service()
            rag_context = rag.get_subject_program_context(subject)
            if rag_context:
                rag_section = (
                    f"\n\nCADRE DE RÉFÉRENCE OFFICIEL DU BAC MAROCAIN POUR {subject.upper()}:\n"
                    f"{rag_context}\n\n"
                    f"RÈGLE: Tes questions doivent couvrir les domaines ci-dessus "
                    f"proportionnellement à leur poids à l'examen."
                )
        except Exception:
            pass
        
        return (
            f"Tu effectues une évaluation diagnostique en {subject} pour déterminer le niveau "
            f"de l'étudiant. Pose des questions progressives du niveau basique au niveau avancé. "
            f"Après chaque réponse, évalue si l'étudiant maîtrise le concept et ajuste la "
            f"difficulté. Langue: {language}. Sois bref et direct dans tes questions."
            f"{rag_section}"
        )

    def build_review_prompt(
        self,
        lesson_title: str,
        key_concepts: list[str],
        subject: str = "",
        language: str = "français"
    ) -> str:
        """Build prompt for spaced repetition review session with RAG context."""
        concepts = ", ".join(key_concepts)
        
        rag_section = ""
        if subject:
            try:
                rag = get_rag_service()
                rag_context = rag.get_subject_program_context(subject)
                if rag_context:
                    rag_section = (
                        f"\n\nINFORMATIONS OFFICIELLES DU PROGRAMME:\n{rag_context}\n"
                        f"Utilise ces informations pour contextualiser la révision "
                        f"et mentionner le poids de ce domaine à l'examen."
                    )
            except Exception:
                pass
        
        return (
            f"C'est une session de révision espacée sur '{lesson_title}'. "
            f"Concepts clés à revoir: {concepts}. "
            f"Pose 3-5 questions rapides pour vérifier que l'étudiant se souvient. "
            f"Si l'étudiant a oublié quelque chose, rappelle-lui brièvement. "
            f"Mentionne l'importance de ce sujet pour l'examen BAC. "
            f"Langue: {language}."
            f"{rag_section}"
        )


prompt_builder = PromptBuilder()
