"""La question libre de l'élève pendant le cours (user rule, 8 novembre 2026) : écrite, dite au micro, ou une image
(photo d'un exercice, d'un schéma, d'une page du cahier).

Le tuteur répond SANS quitter la diapositive, avec tout le contexte : le titre, ce qu'il vient d'expliquer, ce que
la simulation montre (`ce_qui_se_voit`), ses instants clés et ses repères (pour montrer en parlant), et les acquis
de l'élève. Il répond en JSON : `parole` (règles de la voix), `ecrit` (court, en français), `gestes` (dans la
simulation, seulement des instants et repères existants). Une question hors du chapitre reçoit une réponse courte
et un retour au cours ; une question hors programme est dite hors programme (professeur, règle 8).
"""
from __future__ import annotations

import base64
from typing import Optional

from app.services.reexplication import valider_gestes
from app.services.simulation_reaction import REGLES_VOIX, lire_json, parole_propre


async def comprendre(texte: str, audio_b64: Optional[str], image_b64: Optional[str], image_mime: str, gemini_seul: bool = False) -> dict:
    """Ce que l'élève a demandé, en texte : sa phrase, la transcription du micro, le texte lu sur l'image."""
    out = {"texte": (texte or "").strip(), "transcription": "", "image_texte": ""}
    if audio_b64:
        try:
            from app.services.stt_service import stt_service
            data = base64.b64decode(audio_b64.split(",", 1)[-1])
            out["transcription"] = (await stt_service.transcribe_audio(data, "mixed", gemini_seul=gemini_seul) or "").strip()
        except Exception:  # noqa: BLE001
            out["transcription"] = ""
    if image_b64:
        try:
            from app.services.ocr_service import extract_text_from_image
            r = await extract_text_from_image(image_b64, image_mime or "image/png", correct_math=True, subject="physique")
            out["image_texte"] = (r.get("text") or r.get("markdown") or "").strip()[:2500]
        except Exception:  # noqa: BLE001
            out["image_texte"] = ""
    return out


def prompt_question(ctx: dict, compris: dict) -> str:
    moments = ctx.get("moments") or {}
    reperes = ctx.get("reperes") or {}
    parties = []
    if compris["texte"]:
        parties.append(f"Question écrite : {compris['texte'][:800]}")
    if compris["transcription"]:
        parties.append(f"Question dite au micro (transcription) : {compris['transcription'][:800]}")
    if compris["image_texte"]:
        parties.append(f"Texte lu sur l'image qu'il a envoyée : {compris['image_texte']}")
    sim = ""
    if moments or reperes:
        sim = f"""La simulation affichée sait se figer sur ces instants (play_until) : {', '.join(f'{k} ({v})' for k, v in moments.items()) or 'aucun'}.
Repères qu'on peut montrer du doigt (highlight) : {', '.join(f'{k} ({v})' for k, v in reperes.items()) or 'aucun'}.
Si ta réponse s'appuie sur la figure, fais 1 à 4 gestes dans l'ordre de ton explication, avec ces noms seulement."""
    return f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF au Maroc. Il suit la diapositive « {ctx.get('title', '')} » et lève la main.
Ce que tu viens d'expliquer : {str(ctx.get('speech') or '')[:1200]}
Ce que l'élève voit en ce moment : {str(ctx.get('ce_qui_se_voit') or 'la diapositive')[:600]}
{chr(10).join(parties) or "Il n'a rien écrit de lisible : demande-lui de reformuler, en une phrase."}

Réponds à SA question, précisément, en 3 à 6 phrases, en t'appuyant sur la figure quand c'est possible, puis
ramène-le au cours en une phrase. Si la question porte sur un autre chapitre, réponds en deux phrases et dis que
ça viendra ; si elle est hors programme du bac, dis-le simplement. Si c'est un exercice (image), ne donne pas la
réponse finale : nomme le cas, la relation à utiliser et la première étape, et demande-lui de continuer.
{sim}

{REGLES_VOIX}

Réponds UNIQUEMENT par ce JSON :
{{"parole": "ta réponse dite (règles de la voix)", "ecrit": "l'essentiel en français écrit, deux phrases au plus, avec les relations", "gestes": [{{"commande": "play_until", "parametres": {{"moment": "..."}}}}, {{"repere": "..."}}]}}"""


def reponse_depuis(texte_llm: str, ctx: dict) -> Optional[dict]:
    d = lire_json(texte_llm)
    if not d:
        return None
    parole = parole_propre(d.get("parole"))
    if not parole:
        return None
    return {"parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:500],
            "gestes": valider_gestes(d.get("gestes"), ctx.get("moments") or {}, ctx.get("reperes") or {})[:4]}
