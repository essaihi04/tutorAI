"""
Vision Service — Analyze student images (handwritten answers, curves, schemas)
Uses Mistral OCR + DeepSeek for text + Pixtral for diagrams/curves.
Pipeline complet pour maths/physique BAC.
"""
import logging
from app.config import get_settings
from app.services.ocr_service import extract_full_document, describe_diagram_with_vision

logger = logging.getLogger(__name__)
settings = get_settings()


async def analyze_student_image(
    image_base64: str,
    question_content: str,
    correction_content: str,
    question_type: str = "open",
    mime_type: str = "image/png",
    subject: str = "",
) -> dict:
    """
    Analyze a student's image answer using:
    - Mistral OCR + DeepSeek for text extraction and LaTeX correction
    - Mistral Pixtral for curve/diagram description
    Returns: { extracted_text, elements, errors_found, curve_analysis }
    """
    # Strip data URL prefix if present (e.g. "data:image/png;base64,...")
    if image_base64.startswith("data:"):
        header, image_base64 = image_base64.split(",", 1)
        if ";" in header:
            mime_type = header.split(":")[1].split(";")[0]

    # Extract text AND describe diagrams (vision enabled, subject-specific)
    logger.info(f"Analyzing image for subject: '{subject}'")
    result = await extract_full_document(image_base64, mime_type, use_vision=True, subject=subject)
    
    extracted_text = result.get("text", "") or result.get("ocr_text", "")
    diagram_desc = result.get("diagram_description", "")
    
    if not extracted_text and not diagram_desc:
        logger.warning(f"No content extracted from image")
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
