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
                                           temperature=0.5, max_tokens=700, student_id=_compte(student),
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
    prompt = qe.prompt_question(ctx, compris)
    for _ in range(2):
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}],
                                           system_prompt="Tu es un professeur de physique bienveillant et exigeant. Tu réponds uniquement en JSON valide.",
                                           temperature=0.5, max_tokens=700, student_id=_compte(student), session_type="course_player")
        except Exception as e:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"LLM indisponible : {e}") from e
        r = qe.reponse_depuis(texte, ctx)
        if r:
            return {**r, "question_comprise": compris["texte"] or compris["transcription"] or compris["image_texte"][:300]}
    raise HTTPException(status_code=502, detail="Réponse du LLM inutilisable")
