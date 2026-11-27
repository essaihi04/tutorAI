"""
Vision Service — Analyze student images (handwritten answers, curves, schemas)
27/11/2026 : Claude lit la photo (texte + blocs [Dessin de l'élève : …]) avec la question et les règles de lecture du
mode classe ; Mistral OCR + DeepSeek, et Pixtral pour les dessins, seulement si Claude n'a pas pu lire.
"""
import logging
import re
from app.config import get_settings
from app.services.ocr_service import extract_text_from_image, describe_diagram_with_vision

logger = logging.getLogger(__name__)
settings = get_settings()


def contexte_lecture(question_content: str, correction_content: str = "", subject: str = "") -> str:
    """Les règles de lecture de l'évaluation du prof en classe (`public_classe.contexte_lecture`), pour une copie d'examen."""
    vus: set[str] = set()
    mots: list[str] = []
    for m in re.split(r"[\s,;:.!?«»\"“”()\[\]$\\{}]+", f"{question_content} {correction_content}"):
        t = m.strip("'’")
        if len(t) < 2 or re.fullmatch(r"\d+([.,]\d+)?", t) or t.lower() in vus:
            continue
        vus.add(t.lower())
        mots.append(t)
    vocabulaire = " ".join(mots)[:1900]
    lignes = [
        "C'est la photo de la feuille d'un élève de 2e Bac PC BIOF (Maroc) : sa réponse à une question d'examen, écrite à la main.",
        f"Matière : {subject}." if subject else "",
        f"Question posée : {question_content[:1500]}" if question_content and question_content != "Réponse de l'élève" else "",
        "Pour un QCM ou un vrai/faux, garde le repère de chaque proposition (a, b, c…) et la lettre ou le mot choisi (A, B, vrai, faux).",
        "Normalise les symboles et les unités (exposants en Unicode : m², 10⁻³ ; flèches →). Jamais de LaTeX ni de signe $.",
        "Garde les mots de l'élève et son raisonnement : ne corrige NI ses erreurs NI ses résultats, ne complète rien, n'ajoute aucune explication.",
        f"Mots, symboles et grandeurs de ce sujet : {vocabulaire}" if vocabulaire else "",
        "Écriture difficile : l'élève écrit avec ces mots-là. Quand des lettres se ressemblent (P/Q/D, B/8/b/6, l/1/I, O/0, "
        "u/v, n/r/h, a/o, S/5, Z/2, g/9, t/+, x/×), choisis la lecture qui a un sens dans ce sujet. "
        "Mais un mot nettement écrit reste tel quel, même faux : tu lis, tu ne corriges pas.",
        "Rends le texte lu et, pour chaque dessin (courbe, histogramme, schéma, tableau…), son bloc [Dessin de l'élève : …].",
    ]
    return "\n".join(x for x in lignes if x)


async def analyze_student_image(
    image_base64: str,
    question_content: str,
    correction_content: str,
    question_type: str = "open",
    mime_type: str = "image/png",
    subject: str = "",
) -> dict:
    """
    Analyze a student's image answer: Claude reads it (text + drawings) with the question as context;
    Mistral OCR + DeepSeek, plus Pixtral for diagrams, only as a fallback.
    Returns: { extracted_text, elements, errors_found, curve_analysis }
    """
    # Strip data URL prefix if present (e.g. "data:image/png;base64,...")
    if image_base64.startswith("data:"):
        header, image_base64 = image_base64.split(",", 1)
        if ";" in header:
            mime_type = header.split(":")[1].split(";")[0]

    logger.info(f"Analyzing image for subject: '{subject}'")
    ocr = await extract_text_from_image(image_base64, mime_type, correct_math=True, subject=subject,
                                        contexte=contexte_lecture(question_content, correction_content, subject))
    extracted_text = re.sub(r"\$+", "", str(ocr.get("text") or "")).strip()
    diagram_desc = ""
    if ocr.get("lecteur") != "claude":
        # Claude décrit déjà les dessins dans son texte : Pixtral seulement en secours
        try:
            d = await describe_diagram_with_vision(image_base64, mime_type, subject=subject)
            diagram_desc = str(d.get("description") or "")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Vision description failed, skipping: {e}")

    if not extracted_text and not diagram_desc:
        logger.warning("No content extracted from image")
        return {
            "extracted_text": "",
            "elements": "",
            "errors_found": [],
            "curve_analysis": None,
            "error": "Aucun contenu détecté dans l'image.",
        }

    # Append diagram description to extracted text if available
    if diagram_desc:
        extracted_text += "\n\n--- Description du schéma/courbe ---\n" + diagram_desc
    
    # Analyze text vs correction
    elements, errors = _analyze_text_vs_correction(extracted_text, correction_content)
    
    return {
        "extracted_text": extracted_text,
        "elements": elements,
        "errors_found": errors,
        "curve_analysis": diagram_desc or None,
        "diagram_description": diagram_desc,
    }


def _analyze_text_vs_correction(extracted_text: str, correction: str) -> tuple[str, list]:
    """
    Simple text-based analysis comparing extracted text with correction.
    """
    if not extracted_text:
        return "", []
    
    elements = "Texte extrait:\n" + extracted_text[:500]
    errors = []
    
    if correction and len(correction) > 50:
        # Basic comparison
        correction_lower = correction.lower()
        extracted_lower = extracted_text.lower()
        
        # Check if key terms from correction are present
        words = correction_lower.split()
        key_terms = [w for w in words if len(w) > 4]
        found_terms = [t for t in key_terms if t in extracted_lower]
        
        if len(found_terms) < len(key_terms) * 0.3:
            errors.append("Certains éléments de la correction semblent manquants.")
        else:
            elements += "\n\nÉléments clés de la correction présents: oui"
    
    return elements, errors
