import re
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.dependencies import get_current_student
from app.schemas.course_player import (
    CourseIntentResolveRequest,
    CourseProgressUpdate,
    SlideAttemptCreate,
    SlideAttemptFeedback,
)
from app.services.course_player_service import course_player_service
from app.services.subject_access_service import subject_access_service


router = APIRouter(prefix="/course-player", tags=["course-player"])


def _deck_ids(deck: dict) -> tuple[set[str], set[str]]:
    activity_ids: set[str] = set()
    slide_ids: set[str] = set()
    for activity in deck.get("activities") or []:
        activity_ids.add(str(activity.get("id") or ""))
        for slide in activity.get("slides") or []:
            slide_ids.add(str(slide.get("id") or ""))
    return activity_ids, slide_ids


async def _authorised_deck(student: dict, lesson_id: str, deck_id: str) -> dict:
    if not subject_access_service.is_lesson_allowed(student, lesson_id):
        raise HTTPException(status_code=403, detail="Cette leçon n'est pas incluse dans votre accès")
    deck = await course_player_service.get_deck(lesson_id)
    if not deck or str(deck.get("id")) != str(deck_id):
        raise HTTPException(status_code=404, detail="Cours introuvable pour cette leçon")
    return deck


@router.post("/resolve")
async def resolve_course_intent(
    body: CourseIntentResolveRequest,
    student: dict = Depends(get_current_student),
):
    """Transforme une demande explicite de cours en route chapitre/leçon."""
    return await course_player_service.resolve_course_intent(body.text, student)


@router.get("/catalog")
async def get_course_catalog(student: dict = Depends(get_current_student)):
    """Matières accessibles et cours scénarisés ouvrables avec Moalim."""
    return await course_player_service.get_catalog(student)


@router.get("/lessons/{lesson_id}")
async def get_lesson_deck(lesson_id: str, student: dict = Depends(get_current_student)):
    if not subject_access_service.is_lesson_allowed(student, lesson_id):
        raise HTTPException(status_code=403, detail="Cette leçon n'est pas incluse dans votre accès")
    deck = await course_player_service.get_deck(lesson_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Aucun cours publié pour cette leçon")
    progress = await course_player_service.get_progress(student["id"], str(deck.get("id") or ""))
    return {"deck": deck, "progress": progress}


@router.post("/progress")
async def save_course_progress(
    body: CourseProgressUpdate,
    student: dict = Depends(get_current_student),
):
    deck = await _authorised_deck(student, body.lesson_id, body.deck_id)
    activity_ids, slide_ids = _deck_ids(deck)
    if body.activity_id and body.activity_id not in activity_ids:
        raise HTTPException(status_code=400, detail="Activité étrangère à ce cours")
    if body.slide_id and body.slide_id not in slide_ids:
        raise HTTPException(status_code=400, detail="Diapositive étrangère à ce cours")
    persisted = await course_player_service.save_progress(student["id"], body.model_dump())
    if body.status == "completed":
        await course_player_service.mark_lesson_complete(student["id"], body.lesson_id)
    return {"saved": True, "persisted": persisted}


@router.post("/attempts", response_model=SlideAttemptFeedback)
async def save_slide_attempt(
    body: SlideAttemptCreate,
    student: dict = Depends(get_current_student),
):
    payload = body.model_dump()
    deck = await _authorised_deck(student, body.lesson_id, body.deck_id)
    _, slide_ids = _deck_ids(deck)
    if body.slide_id not in slide_ids:
        raise HTTPException(status_code=400, detail="Diapositive étrangère à ce cours")
    is_correct, feedback, should_requeue = await course_player_service.evaluate_attempt(payload)
    await course_player_service.save_attempt(student["id"], payload, is_correct, feedback)
    return SlideAttemptFeedback(
        is_correct=is_correct,
        feedback=feedback,
        should_requeue=should_requeue,
    )


def _compte(student: dict) -> Optional[str]:
    """L'identifiant à donner au suivi des tokens : aucun pour un visiteur de la page publique (pas de compte)."""
    sid = str(student.get("id") or "")
    return None if not sid or sid.startswith("public-") else sid


class SimReactionRequest(BaseModel):
    """L'élève a manipulé lui-même la simulation de la diapositive (mode concentration)."""
    mode: Literal["interpreter", "corriger"] = "interpreter"
    diapo: dict = Field(default_factory=dict)          # {title, speech}
    avant: dict = Field(default_factory=dict)          # état de la simulation avant son geste
    apres: dict = Field(default_factory=dict)          # état après (nouveau résultat)
    historique: list[dict] = Field(default_factory=list)   # [{type, correct}] des questions de cette diapositive
    question: dict = Field(default_factory=dict)       # mode « corriger » : la question directe posée
    reponse: str = Field(default="", max_length=600)


@router.post("/sim-reaction")
async def simulation_reaction(body: SimReactionRequest, student: dict = Depends(get_current_student)):
    """Interprète le nouveau résultat de l'élève et pose une question, ou corrige une réponse directe.

    Le texte dit (`parole`) part ensuite à la voix (`/tts/speak`) : l'élève reste sur la même diapositive.
    """
    from app.services import simulation_reaction as sr
    from app.services.llm_service import llm_service

    systeme = "Tu es un professeur de physique bienveillant et exigeant. Tu réponds uniquement en JSON valide."
    if body.mode == "corriger":
        prompt = sr.prompt_correction(body.diapo, body.question, body.reponse)
        genre = None
    else:
        prompt, genre = sr.prompt_interpretation(body.diapo, body.avant, body.apres, body.historique[-6:])
    for _ in range(2):                                  # une seconde chance si le JSON est inutilisable
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}], system_prompt=systeme,
                                           temperature=0.5, max_tokens=700 if genre is None else 1800, student_id=_compte(student),
                                           session_type="course_player")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"LLM indisponible : {e}") from e
        resultat = sr.correction_depuis(texte) if genre is None else sr.reaction_depuis(texte, genre)
        if resultat:
            return resultat
    raise HTTPException(status_code=502, detail="Réponse du LLM inutilisable")


class AnswerReactionRequest(BaseModel):
    """Une réponse de l'élève à une question ou un exercice de la diapositive (mode concentration)."""
    diapo: dict = Field(default_factory=dict)          # {title, speech}
    question: dict = Field(default_factory=dict)       # {type, enonce, choix?, bonne?, attendu?}
    reponse: str = Field(default="", max_length=800)
    tentative: int = Field(default=1, ge=1, le=5)
    verdict: Optional[bool] = None                     # connu quand la clé est dans l'exercice


@router.post("/answer-reaction")
async def answer_reaction(body: AnswerReactionRequest, student: dict = Depends(get_current_student)):
    """Juge (si la clé n'est pas connue) et réagit à la réponse, comme un prof : indice d'abord, réponse au 2e essai."""
    from app.services import reponse_eleve
    from app.services.llm_service import llm_service

    prompt = reponse_eleve.prompt_reponse(body.diapo, body.question, body.reponse, body.tentative, body.verdict)
    for _ in range(2):
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}],
                                           system_prompt="Tu es un professeur de physique bienveillant et exigeant. Tu réponds uniquement en JSON valide.",
                                           temperature=0.4, max_tokens=500, student_id=_compte(student),
                                           session_type="course_player")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"LLM indisponible : {e}") from e
        resultat = reponse_eleve.reaction_reponse(texte, body.verdict)
        if resultat:
            return resultat
    raise HTTPException(status_code=502, detail="Réponse du LLM inutilisable")


class AcquisEvent(BaseModel):
    """Une réponse de l'élève à une question du cours, avec la méthode d'explication (skill `suivi-des-acquis`)."""
    deck_id: Optional[str] = None
    slide_id: str
    slide_title: str = ""
    cle: str = "q"
    type: str = "qcm"
    enonce: str = Field(default="", max_length=500)
    reponse: str = Field(default="", max_length=500)
    tentative: int = Field(default=1, ge=1, le=5)
    correct: Optional[bool] = None
    reaction_preparee: bool = False
    competence_ids: list[str] = Field(default_factory=list)
    methodes: dict = Field(default_factory=dict)


@router.post("/acquis")
async def enregistrer_acquis(body: AcquisEvent, student: dict = Depends(get_current_student)):
    from app.services import suivi_acquis
    e = body.model_dump()
    if not e["competence_ids"] and e.get("deck_id"):
        deck = suivi_acquis.charger_deck(e["deck_id"])
        if deck:
            e["competence_ids"] = suivi_acquis.competences_du_cours(deck)[1].get(e["slide_id"], [])
    suivi_acquis.enregistrer(str(student["id"]), e)
    return {"ok": True}


@router.get("/acquis/{deck_id}")
async def bilan_acquis(deck_id: str, student: dict = Depends(get_current_student)):
    """Le bilan de l'élève sur ce cours : statut, trajet et méthodes par compétence, lacunes à reprendre."""
    from app.services import suivi_acquis
    deck = suivi_acquis.charger_deck(deck_id) or {}
    b = suivi_acquis.bilan(suivi_acquis.lire(str(student["id"]), deck_id), deck)
    return {**b, "lacunes": suivi_acquis.lacunes(b), "bloc_prompt": suivi_acquis.bloc_prompt(b, deck.get("title", ""))}


class ReexplicationRequest(BaseModel):
    """Une réponse fausse : le tuteur réexplique autrement et pose une question jumelle (cycle 1 à 3)."""
    deck_id: Optional[str] = None
    slide_id: str = ""
    title: str = ""
    speech: str = Field(default="", max_length=3000)
    question: dict = Field(default_factory=dict)
    reponses_fausses: str = Field(default="", max_length=600)
    cycle: int = Field(default=1, ge=1, le=3)
    methodes_essayees: list[str] = Field(default_factory=list)
    moments: dict = Field(default_factory=dict)
    reperes: dict = Field(default_factory=dict)


@router.post("/reexplication")
async def reexplication(body: ReexplicationRequest, student: dict = Depends(get_current_student)):
    from app.services import reexplication as rx, suivi_acquis
    from app.services.llm_service import llm_service

    ctx = body.model_dump()
    try:   # ce qui marche avec cet élève, d'après son suivi
        evs = suivi_acquis.lire(str(student["id"]), body.deck_id) if body.deck_id else []
        deck = suivi_acquis.charger_deck(body.deck_id or "") or {}
        ctx["methodes_qui_marchent"] = [suivi_acquis.NOMS_METHODES.get(m, m) for m in suivi_acquis.bilan(evs, deck)["methodes_qui_marchent"][:4]] if evs else []
    except Exception:  # noqa: BLE001
        ctx["methodes_qui_marchent"] = []
    prompt, n = rx.prompt_reexplication(ctx)
    for _ in range(2):
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}],
                                           system_prompt="Tu es un professeur de physique bienveillant et exigeant. Tu réponds uniquement en JSON valide.",
                                           temperature=0.6, max_tokens=900, student_id=_compte(student), session_type="course_player")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"LLM indisponible : {e}") from e
        r = rx.reexplication_depuis(texte, ctx, n)
        if r:
            return r
    raise HTTPException(status_code=502, detail="Réponse du LLM inutilisable")


class TranscrireRequest(BaseModel):
    """L'élève vient de parler au micro : on lui montre tout de suite ce qui a été compris, avant d'envoyer."""
    audio_b64: str = Field(..., min_length=10, max_length=6_000_000)


@router.post("/transcrire")
async def transcrire(body: TranscrireRequest, student: dict = Depends(get_current_student)):
    """MoulSot v4 (kernel de la voix), Gemini en secours. Le texte revient dans le champ de la question : l'élève
    voit si la transcription est juste, la corrige s'il le faut, puis l'envoie (9 novembre 2026)."""
    from app.services import question_eleve as qe

    compris = await qe.comprendre("", body.audio_b64, None, "image/png")
    if not compris["transcription"]:
        from app.services.kaggle_tts import pilote
        pilote.besoin_de_voix("stt")
        # 409 et pas 503 : main.py remplace le texte de toute réponse 5xx par « Erreur interne du service ».
        raise HTTPException(status_code=409, detail="Le micro se prépare (la reconnaissance vocale démarre, une à trois minutes). Réessaie dans un instant, ou écris ta question.")
    return {"texte": compris["transcription"]}


class OcrReponseRequest(BaseModel):
    """La photo de la feuille de l'élève (sa réponse ou sa question) : lue, puis montrée dans le champ AVANT tout envoi."""
    image_b64: str = Field(..., min_length=10, max_length=8_000_000)
    image_mime: str = "image/jpeg"
    deck_id: Optional[str] = None
    title: str = Field(default="", max_length=300)
    lead: str = Field(default="", max_length=500)
    matiere: str = Field(default="", max_length=60)
    chapitre: str = Field(default="", max_length=300)
    enonce: str = Field(default="", max_length=600)        # la question à laquelle il répond, s'il y en a une


def matiere_du_cours(deck_id: str, deck: Optional[dict]) -> str:
    """physique / chimie / math / svt, d'après le cours (son champ `subject`, sinon le préfixe de son id)."""
    sujet = str((deck or {}).get("subject") or (deck or {}).get("matiere") or "").lower()
    cle = f"{sujet} {deck_id or ''}".lower()
    if "chim" in cle or cle.startswith("chem"):
        return "chimie"
    if "math" in cle:
        return "math"
    if "svt" in cle or "bio" in cle:
        return "svt"
    return "physique"


def contexte_ocr(body: OcrReponseRequest, deck: Optional[dict]) -> tuple[str, str]:
    """(matière, contexte) donnés à la correction de l'OCR : la diapositive, le chapitre, la notation à rendre."""
    matiere = body.matiere.strip() or matiere_du_cours(body.deck_id or "", deck)
    chapitre = body.chapitre.strip() or str((deck or {}).get("title") or "")
    lignes = [
        "C'est la photo de la feuille d'un élève de 2e Bac PC BIOF (Maroc) : sa réponse ou sa question, écrite à la main.",
        f"Matière : {matiere}." + (f" Chapitre : {chapitre}." if chapitre else ""),
        f"Diapositive : « {body.title} »" + (f" — {body.lead}" if body.lead else "") + "." if body.title else "",
        f"Question posée : {body.enonce}" if body.enonce else "",
        "Normalise les symboles, les unités et la notation comme ce chapitre les écrit : lettres grecques en Unicode (λ, τ, θ, ω, Δ, µ),"
        " exposants et indices en Unicode (m·s⁻¹, 10⁻³, x², y_M devient yM), flèches de réaction (→, ⇌), unités du SI (Hz, m, s, Ω, °C).",
        "Jamais de LaTeX ni de signe $. Garde les mots de l'élève, sa langue (français ou darija) et son raisonnement :"
        " ne corrige NI ses erreurs de physique NI ses résultats, ne complète rien, n'ajoute aucune explication.",
        "Rends uniquement le texte lu, prêt à être relu par l'élève.",
    ]
    return matiere, "\n".join(x for x in lignes if x)


@router.post("/ocr-reponse")
async def ocr_reponse(body: OcrReponseRequest, student: dict = Depends(get_current_student)):
    """« 📷 Photo » : Mistral OCR puis DeepSeek (`ocr_service`) avec le contexte de la diapositive. Le texte revient dans
    le champ ; l'élève le corrige à la main avant d'envoyer (10 novembre 2026) — jamais d'envoi automatique."""
    from app.services import suivi_acquis
    from app.services.ocr_service import extract_text_from_image

    deck = suivi_acquis.charger_deck(body.deck_id) if body.deck_id else None
    matiere, contexte = contexte_ocr(body, deck)
    try:
        r = await extract_text_from_image(body.image_b64, body.image_mime or "image/jpeg", correct_math=True,
                                          subject=matiere, contexte=contexte)
    except Exception:  # noqa: BLE001
        r = {}
    texte = str(r.get("text") or r.get("markdown") or "").strip()
    texte = re.sub(r"\$+", "", texte)[:3000]
    if not texte:
        # 422 et pas 5xx : main.py remplace le texte de toute réponse 5xx par « Erreur interne du service ».
        raise HTTPException(status_code=422, detail="Je n’ai pas pu lire la photo : prends-la de plus près, bien éclairée, ou écris ta réponse.")
    return {"texte": texte}


class QuestionEleveRequest(BaseModel):
    """L'élève lève la main pendant le cours : question écrite, dite au micro (audio en base64) ou image (base64)."""
    deck_id: Optional[str] = None
    slide_id: str = ""
    title: str = ""
    speech: str = Field(default="", max_length=3000)
    ce_qui_se_voit: str = Field(default="", max_length=1500)
    texte: str = Field(default="", max_length=1500)
    audio_b64: Optional[str] = Field(default=None, max_length=6_000_000)
    image_b64: Optional[str] = Field(default=None, max_length=8_000_000)
    image_mime: str = "image/png"
    moments: dict = Field(default_factory=dict)
    reperes: dict = Field(default_factory=dict)


@router.post("/question-eleve")
async def question_eleve(body: QuestionEleveRequest, student: dict = Depends(get_current_student)):
    """Comprend la question (texte, micro, image), puis le tuteur répond avec le contexte de la diapositive."""
    from app.services import question_eleve as qe
    from app.services.llm_service import llm_service

    # Le micro passe par MoulSot v4 (dans le kernel de la voix), Gemini seulement en secours (9 novembre 2026).
    compris = await qe.comprendre(body.texte, body.audio_b64, body.image_b64, body.image_mime)
    if body.audio_b64 and not (compris["texte"] or compris["transcription"] or compris["image_texte"]):
        # Rien d'audible ou reconnaissance pas encore prête (le GPU démarre ~3 min) : on le dit, sans faire parler le LLM.
        from app.services.kaggle_tts import pilote
        pilote.besoin_de_voix("stt")
        # 409 et pas 503 : main.py remplace le texte de toute réponse 5xx par « Erreur interne du service ».
        raise HTTPException(status_code=409, detail="Le micro se prépare (la reconnaissance vocale démarre, une à trois minutes). Réessaie dans un instant, ou écris ta question.")
    ctx = body.model_dump(exclude={"audio_b64", "image_b64"})
    # Le plan du cours : pour savoir si la notion vient dans une diapositive suivante (9 novembre 2026).
    from app.services import suivi_acquis
    deck = suivi_acquis.charger_deck(body.deck_id or "") if body.deck_id else None
    plan, idx = qe.plan_du_cours(deck, body.slide_id)
    prompt = qe.prompt_question(ctx, compris, plan, idx, (deck or {}).get("title", ""))
    for _ in range(2):
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}],
                                           system_prompt="Tu es un professeur de physique bienveillant et exigeant. Tu réponds uniquement en JSON valide.",
                                           temperature=0.5, max_tokens=1400, student_id=_compte(student), session_type="course_player")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"LLM indisponible : {e}") from e
        r = qe.reponse_depuis(texte, ctx, plan, idx)
        if r:
            return {**r, "question_comprise": compris["texte"] or compris["transcription"] or compris["image_texte"][:300]}
    raise HTTPException(status_code=502, detail="Réponse du LLM inutilisable")


class ExplicationRequest(BaseModel):
    """Une notion de base demandée : le tableau s'efface à la brosse pendant que cette explication se prépare."""
    deck_id: Optional[str] = None
    slide_id: str = ""
    title: str = ""
    speech: str = Field(default="", max_length=3000)
    question: str = Field(default="", max_length=1500)
    notion: str = Field(default="", max_length=200)


@router.post("/question-eleve/explication")
async def question_eleve_explication(body: ExplicationRequest, student: dict = Depends(get_current_student)):
    from app.services import question_eleve as qe
    from app.services.llm_service import llm_service

    prompt = qe.prompt_prerequis(body.model_dump(), body.question or body.notion, body.notion or body.question)
    for _ in range(2):
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}],
                                           system_prompt="Tu es un professeur de physique bienveillant et exigeant. Tu réponds uniquement en JSON valide.",
                                           temperature=0.5, max_tokens=1400, student_id=_compte(student), session_type="course_player")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"LLM indisponible : {e}") from e
        r = qe.explication_depuis(texte)
        if r:
            return r
    raise HTTPException(status_code=502, detail="Réponse du LLM inutilisable")
