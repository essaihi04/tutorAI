"""
Mistral OCR Service — Extract text from student images (handwritten answers, exams, schemas)
Uses Mistral OCR API + DeepSeek for accurate math/physics text extraction.
Pipeline: Mistral OCR (raw extraction) → DeepSeek (correction + LaTeX formatting)
"""
import httpx
import base64
import logging
import re
from typing import Optional
from app.config import get_settings
from app.services.token_tracking_service import token_tracker

logger = logging.getLogger(__name__)
settings = get_settings()

MISTRAL_OCR_URL = "https://api.mistral.ai/v1/ocr"
MISTRAL_OCR_MODEL = "mistral-ocr-latest"
MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_VISION_MODEL = "mistral-small-latest"  # Use chat model with vision capability
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# ============================================================
# SUBJECT-SPECIFIC PROMPTS
# ============================================================

# --- OCR CORRECTION PROMPTS (DeepSeek) per subject ---
# NOTE: Do NOT use .format() - concatenate OCR text separately

_CORRECTION_BASE = (
    "Corrige le texte OCR suivant extrait d'un document manuscrit du BAC marocain.\n\n"
    "RÈGLES GÉNÉRALES:\n"
    "1. Corrige les erreurs de reconnaissance du français manuscrit:\n"
    '   - "Sait" → "Soit", "Manter" → "Montrer", "Endésquer" → "En déduire"\n'
    '   - "crélatif" → "relatif", "ana" → "On a", "d\'au" → "donc"\n'
    '   - "draites" → "droites", "croisé fiqens" → "croissantes"\n\n'
    "2. Écris les formules en TEXTE LISIBLE sans symboles LaTeX:\n"
    "   - JAMAIS de signe $ autour des formules\n"
    "   - Vecteurs: vec(n), vec(AB)  |  Indices: x_A, y_H\n"
    "   - Fractions: a/b ou (a+b)/(c+d)  |  Racines: sqrt(x)\n"
    "   - Puissances: x², x³, x^n  |  Normes: ||v||\n\n"
    "3. Préserve la structure (titres, numérotation, solutions)\n"
    "4. NE PAS inventer de contenu. Corrige UNIQUEMENT ce qui existe.\n"
    "5. Remplace ![img-0.jpeg](...) par [Schéma dans le document original]\n\n"
)

CORRECTION_PROMPTS = {
    "math": (
        "Tu es un expert en MATHÉMATIQUES du BAC marocain (2BAC Sciences Expérimentales).\n"
        + _CORRECTION_BASE +
        "VOCABULAIRE MATHÉMATIQUE À RECONNAÎTRE:\n"
        "- Suites: u_n, u_(n+1), convergente, divergente, arithmétique, géométrique\n"
        "- Fonctions: f(x), f'(x), f''(x), lim, exp, ln, primitives, intégrales\n"
        "- Dérivées: f'(x), dy/dx, tangente en a\n"
        "- Intégrales: integrale de a à b de f(x)dx\n"
        "- Complexes: z = a + bi, |z|, arg(z), conjugué(z)\n"
        "- Géométrie espace: vec(AB), plan(P), droite(D), produit scalaire, produit vectoriel\n"
        "- Probabilités: P(A), P(A|B), loi binomiale B(n,p), E(X), V(X)\n"
        "- Symboles: pour tout, il existe, appartient à, inclus dans, union, intersection\n\n"
        "TEXTE OCR À CORRIGER:\n"
    ),
    "physique": (
        "Tu es un expert en PHYSIQUE du BAC marocain (2BAC Sciences Physiques).\n"
        + _CORRECTION_BASE +
        "VOCABULAIRE PHYSIQUE À RECONNAÎTRE:\n"
        "- Ondes: lambda, T, f, v = lambda/T, theta = lambda/a, diffraction\n"
        "- Nucléaire: A/Z X, N(t) = N0 * exp(-lambda*t), t_1/2, MeV, défaut de masse\n"
        "- Électricité: u_C, u_R, u_L, i(t), q(t), RC, RL, RLC, tau, omega_0\n"
        "- Mécanique: F = m*a, vec(P), vec(N), vec(f), E_c, E_p, E_m\n"
        "- Oscillateurs: omega_0 = sqrt(k/m), T_0 = 2*pi*sqrt(m/k), amortissement\n"
        "- Unités: N, J, W, V, A, Ohm, F, H, Hz, m/s, rad/s\n"
        "- Éq. diff.: dq/dt + q/RC = E/R, di/dt + R*i/L = E/L\n\n"
        "TEXTE OCR À CORRIGER:\n"
    ),
    "chimie": (
        "Tu es un expert en CHIMIE du BAC marocain (2BAC Sciences Physiques).\n"
        + _CORRECTION_BASE +
        "VOCABULAIRE CHIMIE À RECONNAÎTRE:\n"
        "- Cinétique: v = dx/dt, t_1/2, facteurs cinétiques, catalyseur\n"
        "- Acide-base: pH, pOH, Ka, pKa, Ke, couple acide/base\n"
        "- Équilibre: Qr, K, taux d'avancement tau_f, quotient de réaction\n"
        "- Tableau d'avancement: x, x_max, x_eq, avancement\n"
        "- Piles: f.e.m, anode, cathode, oxydation, réduction, Zn/Cu\n"
        "- Électrolyse: i*t = n*F, électrodes\n"
        "- Estérification: acide + alcool -> ester + eau, rendement\n"
        "- Dosage: C_A * V_A = C_B * V_B, point d'équivalence\n\n"
        "TEXTE OCR À CORRIGER:\n"
    ),
    "svt": (
        "Tu es un expert en SVT du BAC marocain (2BAC Sciences Physiques).\n"
        + _CORRECTION_BASE +
        "VOCABULAIRE SVT À RECONNAÎTRE:\n"
        "- Énergie cellulaire: glycolyse, cycle de Krebs, chaîne respiratoire, ATP, ADP\n"
        "- Respiration: mitochondrie, matrice, crêtes, O2, CO2, 36-38 ATP\n"
        "- Fermentation: anaérobie, éthanol, acide lactique, 2 ATP\n"
        "- Muscle: sarcomère, actine, myosine, bande A, bande I, ligne Z\n"
        "- Génétique: ADN, ARNm, ARNt, transcription, traduction, codon, anticodon\n"
        "- Hérédité: allèle, gène, phénotype, génotype, dominance, récessif\n"
        "- Méiose: prophase, métaphase, anaphase, brassage inter/intra-chromosomique\n"
        "- Géologie: subduction, obduction, collision, métamorphisme, granite\n\n"
        "TEXTE OCR À CORRIGER:\n"
    ),
}

# --- VISION/DIAGRAM PROMPTS per subject ---

_VISION_BASE = (
    "Analyse cette image d'un document du BAC marocain.\n"
    "Décris PRÉCISÉMENT tous les schémas, courbes et figures que tu vois.\n"
    "Écris en français. N'utilise PAS de signes $ pour les formules.\n\n"
)

VISION_PROMPTS = {
    "math": (
        "Tu es un expert en MATHÉMATIQUES du BAC marocain.\n" + _VISION_BASE +
        "ÉLÉMENTS À IDENTIFIER:\n"
        "- Courbes de fonctions: type (exp, ln, polynôme), asymptotes, extremums\n"
        "- Repère: (O, vec(i), vec(j)), échelle, graduations\n"
        "- Points remarquables: intersections avec axes, tangentes\n"
        "- Tableaux de variations: sens de variation, signes\n"
        "- Figures géométriques 3D: plans, droites, sphères, vecteurs normaux\n"
        "- Cercle trigonométrique: angles, coordonnées\n"
        "- Arbres de probabilités: branches, valeurs\n"
    ),
    "physique": (
        "Tu es un expert en PHYSIQUE du BAC marocain.\n" + _VISION_BASE +
        "ÉLÉMENTS À IDENTIFIER:\n"
        "- Circuits électriques: composants (R, L, C, générateur), connexions\n"
        "- Oscillogrammes: période, amplitude, fréquence, déphasage\n"
        "- Courbes u_C(t), i(t), q(t): régime transitoire, constante de temps\n"
        "- Trajectoires: projectile, chute libre, mouvement circulaire\n"
        "- Schémas de forces: vec(P), vec(N), vec(f), vec(T)\n"
        "- Ondes: diffraction, interférences, figure de diffraction\n"
        "- Diagramme N-Z: noyaux, désintégrations alpha/beta\n"
        "- Pendules: ressort, torsion, pesant, position d'équilibre\n"
    ),
    "chimie": (
        "Tu es un expert en CHIMIE du BAC marocain.\n" + _VISION_BASE +
        "ÉLÉMENTS À IDENTIFIER:\n"
        "- Courbes de dosage: pH vs Volume, point d'équivalence, zone tampon\n"
        "- Courbes cinétiques: concentration vs temps, vitesse initiale\n"
        "- Tableaux d'avancement: réactifs, produits, avancement x\n"
        "- Schémas de piles: anode, cathode, pont salin, solutions\n"
        "- Montages de dosage: burette, bécher, pH-mètre, agitateur\n"
        "- Diagrammes de prédominance: espèces acide/base vs pH\n"
    ),
    "svt": (
        "Tu es un expert en SVT du BAC marocain.\n" + _VISION_BASE +
        "ÉLÉMENTS À IDENTIFIER:\n"
        "- Schémas cellulaires: mitochondrie, membrane, matrice, crêtes\n"
        "- Glycolyse / Krebs: étapes, molécules, enzymes, bilans\n"
        "- Chaîne respiratoire: complexes I-IV, ATP synthase, gradient H+\n"
        "- Muscle: sarcomère, filaments actine/myosine, bandes A/I/H\n"
        "- ADN / ARN: double hélice, transcription, traduction, ribosome\n"
        "- Méiose / Mitose: phases, chromosomes, chiasmas\n"
        "- Arbres généalogiques: hérédité, allèles, phénotypes\n"
        "- Coupes géologiques: subduction, collision, nappes, métamorphisme\n"
    ),
}


def _get_subject_key(subject: str) -> str:
    """Normalize subject name to key."""
    if not subject:
        return "math"
    s = subject.lower().strip()
    if "math" in s:
        return "math"
    elif "physi" in s or "phys" in s:
        return "physique"
    elif "chimi" in s or "chem" in s:
        return "chimie"
    elif "svt" in s or "vie" in s or "terre" in s or "biolo" in s:
        return "svt"
    return "math"


async def describe_diagram_with_vision(
    image_base64: str,
    mime_type: str = "image/png",
    subject: str = "",
) -> dict:
    """
    Use Mistral Pixtral (vision model) to describe curves, diagrams, and schemas.
    Returns: { description, success, error }
    """
    # Strip data URL prefix if present
    if image_base64.startswith("data:"):
        header, image_base64 = image_base64.split(",", 1)
        if ";" in header:
            mime_type = header.split(":")[1].split(";")[0]

    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": VISION_PROMPTS.get(_get_subject_key(subject), VISION_PROMPTS["math"])},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}
                    }
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 2000,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(MISTRAL_CHAT_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Mistral vision response: {data}")

        choices = data.get("choices", [])
        if choices:
            description = choices[0].get("message", {}).get("content", "")
            if description:
                logger.info(f"Vision described diagram ({len(description)} chars)")
                return {
                    "description": description.strip(),
                    "success": True,
                    "error": None,
                }

        return {
            "description": "",
            "success": False,
            "error": "Aucune description générée.",
        }

    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral Vision API error: {e.response.status_code} - {e.response.text[:300]}")
        return {
            "description": "",
            "success": False,
            "error": f"Erreur API Vision: {e.response.status_code}",
        }
    except Exception as e:
        logger.error(f"Diagram description failed: {e}", exc_info=True)
        return {
            "description": "",
            "success": False,
            "error": f"Erreur: {str(e)}",
        }


async def extract_full_document(
    image_base64: str,
    mime_type: str = "image/png",
    use_vision: bool = False,
    subject: str = "",
) -> dict:
    """
    Extract both text AND diagram descriptions from an image.
    Combines OCR + Vision for complete document understanding.
    Returns: { text, diagrams, success, error }
    """
    # Step 1: Extract text with OCR + DeepSeek correction
    ocr_result = await extract_text_from_image(image_base64, mime_type, correct_math=True, subject=subject)
    
    # Step 2: Describe any diagrams/curves with vision
    diagram_result = {"description": "", "success": False, "error": None}
    if use_vision:
        try:
            logger.info("Calling Mistral Vision for diagram description...")
            diagram_result = await describe_diagram_with_vision(image_base64, mime_type, subject=subject)
            logger.info(f"Vision result: success={diagram_result.get('success')}, desc_len={len(diagram_result.get('description', ''))}, error={diagram_result.get('error')}")
        except Exception as e:
            logger.error(f"Vision description failed, skipping: {e}", exc_info=True)
    
    # Combine results
    combined_text = ocr_result.get("text", "")
    diagram_desc = diagram_result.get("description", "")
    
    # Always include diagram description if available
    if diagram_desc:
        combined_text += f"\n\n--- Description du schéma/courbe ---\n{diagram_desc}"
    
    return {
        "text": combined_text,
        "ocr_text": ocr_result.get("text", ""),
        "diagram_description": diagram_desc,
        "raw_ocr": ocr_result.get("raw_ocr", ""),
        "success": ocr_result.get("success", False) or diagram_result.get("success", False),
        "error": ocr_result.get("error") or diagram_result.get("error"),
    }


async def _correct_math_text_with_deepseek(raw_text: str, subject: str = "", contexte: str = "") -> str:
    """
    Use DeepSeek to correct OCR errors using subject-specific prompt.
    `contexte` (optional): what the text is about (slide, chapter, notation to use). It is placed before the raw
    text, so the correction normalises symbols, units and notation the way that chapter writes them.
    """
    if not raw_text or len(raw_text.strip()) < (3 if contexte else 10):
        return raw_text
    
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": CORRECTION_PROMPTS.get(_get_subject_key(subject), CORRECTION_PROMPTS["math"])
                + (f"CONTEXTE (prioritaire sur les règles ci-dessus) :\n{contexte}\n\nTEXTE OCR :\n" if contexte else "")
                + raw_text + "\n\nTEXTE CORRIGÉ:"
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000,
    }
    
    try:
        logger.info(f"Calling DeepSeek API with key prefix: {settings.deepseek_api_key[:10]}...")
        _start = token_tracker.start_timer()
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            raw_response = response.text
            logger.info(f"DeepSeek raw response: {repr(raw_response[:500])}")
            
            # Try to parse JSON
            try:
                data = response.json()
            except Exception as json_err:
                logger.error(f"DeepSeek JSON parse error: {json_err}, raw: {repr(raw_response[:200])}")
                return raw_text
                
            logger.info(f"DeepSeek parsed type: {type(data)}, content: {repr(str(data)[:200])}")

        # Track DeepSeek correction usage
        usage = data.get("usage", {}) if isinstance(data, dict) else {}
        await token_tracker.record_usage(
            student_id=None, student_email=None,
            provider="deepseek", model="deepseek-chat",
            endpoint="ocr_correction", 
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            request_duration_ms=token_tracker.elapsed_ms(_start),
            session_type="ocr",
        )

        if not isinstance(data, dict):
            logger.error(f"DeepSeek returned non-dict: {type(data)}")
            return raw_text
            
        choices = data.get("choices", [])
        if not choices:
            logger.warning(f"DeepSeek returned no choices")
            return raw_text
            
        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            logger.error(f"First choice is not dict: {type(first_choice)}")
            return raw_text
            
        message = first_choice.get("message", {})
        if not isinstance(message, dict):
            logger.error(f"Message is not dict: {type(message)}")
            return raw_text
            
        corrected = message.get("content", "")
        if corrected and isinstance(corrected, str) and len(corrected.strip()) > (0 if contexte else 10):
            logger.info(f"DeepSeek corrected OCR text ({len(raw_text)} → {len(corrected)} chars)")
            return corrected.strip()
        
        logger.warning(f"DeepSeek returned invalid content: {repr(corrected)[:100]}")
        return raw_text
    
    except httpx.HTTPStatusError as e:
        logger.error(f"DeepSeek HTTP error: {e.response.status_code} - {e.response.text[:200]}")
        return raw_text
    except Exception as e:
        logger.error(f"DeepSeek correction failed: {e}", exc_info=True)
        return raw_text


CONSIGNE_LECTURE_CLAUDE = (
    "Tu lis la photo d'une feuille d'élève marocain (lycée : SVT, physique, chimie ou mathématiques ; en français, parfois "
    "avec un peu d'arabe). Tu la rends en texte pour qu'un professeur la note sans voir la photo.\n"
    "1) LE TEXTE : transcris EXACTEMENT ce que l'élève a écrit, sans rien corriger ni compléter : garde ses erreurs, ses "
    "calculs, ses unités, les numéros des questions (1-1, 2-a…) et les lettres cochées ou entourées (« a) B »). Ignore ce "
    "qui est barré. Un mot illisible : [illisible].\n"
    "2) LES FORMULES : écris-les en notation correcte et lisible, telles que l'élève les a écrites (même fausses) : "
    "fractions avec / et parenthèses, puissances et indices en Unicode (x², 10⁻³, H₃O⁺, Fe²⁺, ²³⁸₉₂U, m·s⁻¹), "
    "λ, θ, Δ, √, ∞, →, ⇌, ≈ ; une équation chimique avec sa flèche et ses coefficients ; jamais de LaTeX ni de symbole $.\n"
    "3) LES DESSINS : pour chaque courbe, graphique, histogramme, diagramme, schéma, croquis, tableau, montage, figure "
    "géométrique ou construction, écris à sa place un bloc « [Dessin de l'élève : <nature>] » qui décrit objectivement, "
    "sans le juger ni le corriger, tout ce qu'un professeur vérifierait sur la copie :\n"
    "- graphique, courbe, histogramme, diagramme : le titre ; chaque axe (sa grandeur, son unité, sa flèche, ses "
    "graduations et si l'échelle est régulière) ; les points ou valeurs placés (lis leurs coordonnées) ; la forme du tracé "
    "(droite passant ou non par l'origine, croissante, décroissante, exponentielle, palier, asymptote, maximum, tangente…) ; "
    "tracé à la règle ou à main levée ; pour un histogramme : chaque classe et la hauteur de sa barre, barres collées ou "
    "séparées, classe vide laissée ou non ; pour un diagramme en secteurs : les secteurs et leurs angles ou pourcentages ;\n"
    "- schéma ou croquis (SVT, montage, dispositif) : ce qui est dessiné, chaque légende et l'élément que pointe sa flèche, "
    "les légendes manquantes, le titre, l'échelle ou le grossissement ;\n"
    "- physique : vecteurs (point d'application, direction, sens, longueur et échelle), rayons lumineux, symboles et "
    "branchement d'un circuit, sens du courant, appareils de mesure, tensions fléchées ;\n"
    "- chimie : formules développées ou semi-développées, schéma de Lewis, montage de titrage ou de chauffage, tableau "
    "d'avancement (chaque case) ;\n"
    "- mathématiques : figure, constructions, codages, tableau de variations ou de signes (chaque case et chaque flèche), "
    "arbre de probabilités ;\n"
    "- tableau : chaque ligne et chaque colonne avec ses valeurs.\n"
    "Dis aussi ce qui manque à l'endroit où on l'attendrait (« pas de titre », « axe des ordonnées sans unité »).\n"
    "Réponds UNIQUEMENT par la transcription et ces blocs, dans l'ordre de la feuille, sans phrase autour. S'il n'y a rien "
    "de lisible, réponds par un texte vide."
)


def _image_pour_claude(image_base64: str, mime_type: str) -> tuple[str, str]:
    """Claude accepte une image d'au plus 5 Mo et la lit au mieux vers 1568 px : une grande photo est réduite."""
    if len(image_base64) * 3 // 4 <= 3_500_000 and mime_type in ("image/jpeg", "image/png", "image/webp", "image/gif"):
        try:
            from PIL import Image
            import io
            with Image.open(io.BytesIO(base64.b64decode(image_base64))) as im:
                if max(im.size) <= 2000:
                    return image_base64, mime_type
        except Exception:  # noqa: BLE001
            return image_base64, mime_type
    from PIL import Image, ImageOps
    import io
    with Image.open(io.BytesIO(base64.b64decode(image_base64))) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((1600, 1600))
        sortie = io.BytesIO()
        im.save(sortie, format="JPEG", quality=85)
    return base64.b64encode(sortie.getvalue()).decode("ascii"), "image/jpeg"


async def _lire_avec_claude(image_base64: str, mime_type: str, subject: str = "", contexte: str = "") -> str:
    """La photo lue par Claude (vision) : le texte de l'élève tel qu'il l'a écrit ; vide si Claude n'est pas joignable."""
    from app.services.llm_service import llm_service
    client = getattr(llm_service, "_claude", None)
    if client is None:
        return ""
    donnees, mime = _image_pour_claude(image_base64, mime_type)
    texte = CONSIGNE_LECTURE_CLAUDE
    if subject or contexte:
        texte += f"\n\nContexte (pour lire les mots du sujet, pas pour corriger) : matière {subject or '?'} ; {contexte[:1500]}"
    debut = token_tracker.start_timer()
    r = await client.beta.messages.create(
        model=settings.anthropic_ocr_model,
        max_tokens=6000,
        output_config={"effort": settings.anthropic_ocr_effort},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": mime, "data": donnees}},
            {"type": "text", "text": texte},
        ]}],
        timeout=60.0,
    )
    try:
        await llm_service._suivre_claude(r, None, None, "ocr", "ocr", debut)
    except Exception:  # noqa: BLE001
        pass
    if getattr(r, "stop_reason", None) == "refusal":
        return ""
    lu = "\n".join(b.text for b in r.content if getattr(b, "type", "") == "text").strip()
    return re.sub(r"\$+", "", lu)


async def extract_text_from_image(
    image_base64: str,
    mime_type: str = "image/png",
    correct_math: bool = True,
    subject: str = "",
    contexte: str = "",
) -> dict:
    """
    Extract text from an image using Mistral OCR + DeepSeek correction.
    Args:
        image_base64: Base64 encoded image
        mime_type: Image MIME type
        correct_math: If True, use DeepSeek to correct math/physics OCR errors
    Returns: { text, markdown, success, error }
    """
    # Strip data URL prefix if present (e.g. "data:image/png;base64,...")
    if image_base64.startswith("data:"):
        header, image_base64 = image_base64.split(",", 1)
        if ";" in header:
            mime_type = header.split(":")[1].split(";")[0]

    # 24/11/2026 : Claude lit la photo d'abord ; Mistral OCR + DeepSeek seulement s'il échoue
    try:
        lu = await _lire_avec_claude(image_base64, mime_type, subject=subject, contexte=contexte)
        if lu:
            return {"text": lu, "markdown": lu, "success": True, "error": None, "lecteur": "claude"}
    except Exception as e:  # noqa: BLE001
        logger.error(f"Lecture Claude impossible, repli sur Mistral OCR : {e}")

    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_OCR_MODEL,
        "document": {
            "type": "image_url",
            "image_url": f"data:{mime_type};base64,{image_base64}",
        },
    }

    try:
        logger.info(f"Calling Mistral OCR API with model: {MISTRAL_OCR_MODEL}")
        _start = token_tracker.start_timer()
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(MISTRAL_OCR_URL, headers=headers, json=payload)
            response.raise_for_status()
            response_text = response.text
            logger.info(f"Mistral OCR raw response length: {len(response_text)}")
            data = response.json()
            logger.info(f"Mistral OCR response type: {type(data)}, keys: {data.keys() if isinstance(data, dict) else 'N/A'}")
        # Track Mistral OCR usage
        await token_tracker.record_usage(
            student_id=None, student_email=None,
            provider="mistral_ocr", model=MISTRAL_OCR_MODEL,
            endpoint="ocr", prompt_tokens=0, completion_tokens=0, total_tokens=1,
            request_duration_ms=token_tracker.elapsed_ms(_start),
            session_type="ocr",
        )

        # Extract text from response
        pages = data.get("pages", [])
        if not pages:
            logger.warning("Mistral OCR returned no pages")
            return {
                "text": "",
                "markdown": "",
                "success": False,
                "error": "Aucun texte détecté dans l'image.",
            }

        # Combine all pages
        markdown_parts = []
        text_parts = []
        for i, page in enumerate(pages):
            if not isinstance(page, dict):
                logger.warning(f"Page {i} is not a dict: {type(page)}")
                continue
            md = page.get("markdown", "")
            if not isinstance(md, str):
                logger.warning(f"Page {i} markdown is not a string: {type(md)}")
                md = str(md)
            if md:
                markdown_parts.append(md)
                try:
                    plain = md.replace("**", "").replace("*", "").replace("`", "")
                    text_parts.append(plain)
                except Exception as e:
                    logger.error(f"Error processing page {i}: {e}")
                    text_parts.append(md)

        raw_text = "\n\n".join(text_parts)
        raw_markdown = "\n\n".join(markdown_parts)
        
        if not raw_text:
            logger.warning("No text extracted after combining pages")
            return {
                "text": "",
                "markdown": "",
                "success": False,
                "error": "Aucun texte détecté dans l'image.",
            }
        
        # Step 2: Use DeepSeek to correct math/physics OCR errors
        if correct_math and raw_text:
            try:
                corrected_text = await _correct_math_text_with_deepseek(raw_text, subject=subject, contexte=contexte)
                return {
                    "text": corrected_text,
                    "markdown": corrected_text,  # Corrected text includes LaTeX
                    "raw_ocr": raw_text,  # Keep original for debugging
                    "success": True,
                    "error": None,
                }
            except Exception as e:
                logger.error(f"DeepSeek correction failed, using raw OCR: {e}")
                return {
                    "text": raw_text,
                    "markdown": raw_markdown,
                    "raw_ocr": raw_text,
                    "success": True,
                    "error": None,
                }

        return {
            "text": raw_text,
            "markdown": raw_markdown,
            "success": True,
            "error": None,
        }

    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral OCR API error: {e.response.status_code} - {e.response.text[:300]}")
        return {
            "text": "",
            "markdown": "",
            "success": False,
            "error": f"Erreur API OCR: {e.response.status_code}",
        }
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}", exc_info=True)
        return {
            "text": "",
            "markdown": "",
            "success": False,
            "error": f"Erreur d'extraction: {str(e)}",
        }


async def extract_text_from_url(document_url: str) -> dict:
    """
    Extract text from a document URL (PDF or image) using Mistral OCR.
    Returns: { text, markdown, success, error }
    """
    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MISTRAL_OCR_MODEL,
        "document": {
            "type": "document_url",
            "document_url": document_url,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(MISTRAL_OCR_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        pages = data.get("pages", [])
        if not pages:
            return {
                "text": "",
                "markdown": "",
                "success": False,
                "error": "Aucun texte détecté dans le document.",
            }

        markdown_parts = []
        text_parts = []
        for page in pages:
            md = page.get("markdown", "")
            if md:
                markdown_parts.append(md)
                plain = md.replace("**", "").replace("*", "").replace("`", "")
                text_parts.append(plain)

        return {
            "text": "\n\n".join(text_parts),
            "markdown": "\n\n".join(markdown_parts),
            "success": True,
            "error": None,
        }

    except httpx.HTTPStatusError as e:
        logger.error(f"Mistral OCR API error: {e.response.status_code} - {e.response.text[:300]}")
        return {
            "text": "",
            "markdown": "",
            "success": False,
            "error": f"Erreur API OCR: {e.response.status_code}",
        }
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return {
            "text": "",
            "markdown": "",
            "success": False,
            "error": f"Erreur d'extraction: {str(e)}",
        }
