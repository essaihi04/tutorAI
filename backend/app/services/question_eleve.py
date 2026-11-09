"""La question libre de l'élève pendant le cours (user rule, 8 novembre 2026) : écrite, dite au micro, ou une image
(photo d'un exercice, d'un schéma, d'une page du cahier).

Le tuteur classe d'abord la question par rapport au COURS (user rule, 9 novembre 2026) :
  - « diapo »      : la notion de la diapositive (ou déjà vue plus tôt dans ce cours) → il l'explique AU TABLEAU, à
                     la voix, avec la figure ; le texte n'est montré qu'à la demande de l'élève ;
  - « suivante »   : une notion de ce cours traitée dans une diapositive qui vient → il le dit (phrase préenregistrée,
                     titre de la diapositive au tableau) et revient à la diapositive actuelle ;
  - « prerequis »  : une notion des années précédentes ou de base → il efface le tableau à la brosse pendant une
                     phrase préenregistrée (le temps de préparer le script et la voix : `/question-eleve/explication`),
                     puis l'explique sur le tableau propre et la relie à la diapositive ;
  - « hors_cours » : un autre cours, un autre chapitre, une autre matière → il ne répond pas et le dit simplement.

Tout le contexte est donné : le titre, ce qu'il vient d'expliquer, ce que la simulation montre (`ce_qui_se_voit`), ses
instants clés et ses repères (pour montrer en parlant), et le plan du cours (diapositives d'avant et d'après).
"""
from __future__ import annotations

import base64
from typing import Optional

from app.services.reexplication import valider_gestes
from app.services.simulation_reaction import REGLES_VOIX, lire_json, parole_propre

CATEGORIES = ("diapo", "suivante", "prerequis", "hors_cours")


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


def plan_du_cours(deck: Optional[dict], slide_id: str) -> tuple[list[dict], int]:
    """Les diapositives du cours dans l'ordre (id, titre, sous-titre) et la place de la diapositive actuelle (-1 si inconnue)."""
    plan: list[dict] = []
    for a in (deck or {}).get("activities", []) or []:
        for s in a.get("slides", []) or []:
            plan.append({"id": s.get("id", ""), "title": s.get("title", ""),
                         "lead": str((s.get("screen_content") or {}).get("lead") or "")[:140]})
    idx = next((i for i, s in enumerate(plan) if s["id"] == slide_id), -1)
    return plan, idx


def _parties(compris: dict) -> str:
    parties = []
    if compris["texte"]:
        parties.append(f"Question écrite : {compris['texte'][:800]}")
    if compris["transcription"]:
        parties.append(f"Question dite au micro (transcription) : {compris['transcription'][:800]}")
    if compris["image_texte"]:
        parties.append(f"Texte lu sur l'image qu'il a envoyée : {compris['image_texte']}")
    return "\n".join(parties) or "Il n'a rien écrit de lisible : demande-lui de reformuler, en une phrase."


REGLES_TABLEAU = """RÈGLES DU TABLEAU (« tableau ») — ce que tu écris à la craie pendant que tu parles, dans l'ordre de ta parole :
- 2 à 6 lignes courtes en FRANÇAIS (la langue du bac BIOF), 60 caractères au plus chacune ;
- des mots-clés, une définition courte, les relations (τ = SM / v, v = d / Δt), une valeur avec son unité ;
- jamais la phrase que tu dis recopiée : le tableau résume, la voix explique."""

REGLES_EXERCICE = """EXERCICE D'ÉVALUATION (« exercice ») — après ton explication, tu demandes s'il a bien compris et tu le vérifies
par un petit exercice sur CE que tu viens d'expliquer (rien d'autre) ; choisis le type selon le cas :
- "association" : relier des notions à leurs définitions, des grandeurs à leurs unités ou à leurs relations (3 ou 4 paires) ;
- "vrai_faux" : des propriétés, des idées reçues, des conséquences (3 affirmations, au moins une vraie et une fausse) ;
- "qcm" : choisir une relation, un résultat, une interprétation (3 ou 4 choix, une seule bonne réponse) ;
en français écrit, court, niveau bac ; « explication » : la correction écrite en une ou deux phrases ;
« parole_juste » / « parole_faux » : ce que tu dis après sa réponse juste / fausse (règles de la voix ; la fausse
redit l'idée clé en une phrase)."""

FORMAT_EXERCICE = """"exercice": {"type": "qcm|vrai_faux|association", "enonce": "la consigne", "choix": ["…", "…", "…"], "bonne": 0, "affirmations": [{"texte": "…", "vrai": true}], "paires": [{"gauche": "…", "droite": "…"}], "explication": "…", "parole_juste": "…", "parole_faux": "…"}"""


def valider_exercice(e) -> Optional[dict]:
    """L'exercice qui suit l'explication, nettoyé ; None s'il est inutilisable (le tableau s'en passe)."""
    if not isinstance(e, dict):
        return None
    t = str(e.get("type") or "").strip().lower().replace("-", "_").replace(" ", "_")
    court = lambda v, n=160: str(v or "").strip()[:n]  # noqa: E731
    base = {"type": t, "enonce": court(e.get("enonce"), 300), "explication": court(e.get("explication"), 400),
            "parole_juste": parole_propre(e.get("parole_juste")) or "", "parole_faux": parole_propre(e.get("parole_faux")) or ""}
    if t == "qcm":
        choix = [court(c) for c in (e.get("choix") or []) if court(c)][:4]
        try:
            bonne = int(e.get("bonne"))
        except (TypeError, ValueError):
            return None
        return {**base, "choix": choix, "bonne": bonne} if len(choix) >= 2 and 0 <= bonne < len(choix) else None
    if t == "vrai_faux":
        aff = [{"texte": court(a.get("texte")), "vrai": bool(a.get("vrai"))} for a in (e.get("affirmations") or [])
               if isinstance(a, dict) and court(a.get("texte")) and isinstance(a.get("vrai"), bool)][:4]
        return {**base, "affirmations": aff} if len(aff) >= 2 else None
    if t == "association":
        paires = [{"gauche": court(p.get("gauche"), 80), "droite": court(p.get("droite"), 120)} for p in (e.get("paires") or [])
                  if isinstance(p, dict) and court(p.get("gauche")) and court(p.get("droite"))][:4]
        droites = {p["droite"] for p in paires}
        return {**base, "paires": paires} if len(paires) >= 2 and len(droites) == len(paires) else None
    return None


def prompt_question(ctx: dict, compris: dict, plan: Optional[list[dict]] = None, idx: int = -1, cours: str = "") -> str:
    moments = ctx.get("moments") or {}
    reperes = ctx.get("reperes") or {}
    plan = plan or []
    sim = ""
    if moments or reperes:
        sim = f"""La simulation affichée sait se figer sur ces instants (play_until) : {', '.join(f'{k} ({v})' for k, v in moments.items()) or 'aucun'}.
Repères qu'on peut montrer du doigt (highlight) : {', '.join(f'{k} ({v})' for k, v in reperes.items()) or 'aucun'}.
Si ta réponse s'appuie sur la figure, fais 1 à 4 gestes dans l'ordre de ton explication, avec ces noms seulement."""
    if plan and idx >= 0:
        avant = "\n".join(f"  - {s['title']}" for s in plan[:idx]) or "  (aucune)"
        apres = "\n".join(f"  - [{s['id']}] {s['title']} — {s['lead']}" for s in plan[idx + 1:]) or "  (aucune : c'est la dernière)"
        plan_txt = f"""Le cours « {cours} ». Diapositives déjà faites :
{avant}
Diapositive actuelle : {plan[idx]['title']}
Diapositives qui viennent (id entre crochets) :
{apres}"""
    else:
        plan_txt = f"Le cours « {cours or ctx.get('title', '')} » (plan des diapositives inconnu)."
    return f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF au Maroc. Il suit la diapositive « {ctx.get('title', '')} » et lève la main.
{plan_txt}
Ce que tu viens d'expliquer : {str(ctx.get('speech') or '')[:1200]}
Ce que l'élève voit en ce moment : {str(ctx.get('ce_qui_se_voit') or 'la diapositive')[:600]}
{_parties(compris)}

D'ABORD, CLASSE sa question (« categorie ») :
- "diapo" : elle porte sur la diapositive actuelle, ou sur une notion de CE cours déjà vue plus haut → tu l'expliques ;
- "suivante" : elle porte sur une notion de CE cours traitée dans une diapositive qui VIENT → tu ne l'expliques pas
  maintenant ; donne l'id de cette diapositive (« diapo_id ») ;
- "prerequis" : elle porte sur une notion des années précédentes (collège, tronc commun, 1re bac) ou de base, utile
  pour comprendre cette diapositive (vitesse moyenne, période, conversion d'unités, proportionnalité, sinus…) → ne
  l'explique pas ici (tu l'expliqueras après avoir effacé le tableau) ; nomme-la dans « notion » ;
- "hors_cours" : un autre chapitre ou cours, une autre matière (chimie, SVT, maths sans lien), ou sans rapport → tu
  ne réponds pas.
« notion » : la notion demandée, en 2 à 6 mots français.

SEULEMENT si "diapo" : réponds à SA question, précisément, en 3 à 6 phrases dites, en t'appuyant sur la figure quand
c'est possible, puis ramène-le au cours en une phrase. Si c'est un exercice (image), ne donne pas la réponse finale :
nomme le cas, la relation à utiliser et la première étape, et demande-lui de continuer. Pour les autres catégories,
laisse « parole », « tableau », « ecrit » et « gestes » vides.
{sim}

{REGLES_TABLEAU}

{REGLES_EXERCICE} (Seulement si "diapo".)

{REGLES_VOIX}

Réponds UNIQUEMENT par ce JSON :
{{"categorie": "diapo|suivante|prerequis|hors_cours", "notion": "...", "diapo_id": "", "parole": "ta réponse dite (règles de la voix)", "tableau": ["ligne 1", "ligne 2"], "ecrit": "l'essentiel en français écrit, deux phrases au plus, avec les relations", "gestes": [{{"commande": "play_until", "parametres": {{"moment": "..."}}}}, {{"repere": "..."}}], {FORMAT_EXERCICE}}}"""


def prompt_prerequis(ctx: dict, question: str, notion: str) -> str:
    """La notion de base, expliquée sur le tableau effacé, puis reliée à la diapositive."""
    return f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF au Maroc. Pendant la diapositive « {ctx.get('title', '')} »,
il a demandé : « {question[:800]} ». C'est une notion de base des années précédentes : « {notion[:120]} ».
Ce que tu venais d'expliquer : {str(ctx.get('speech') or '')[:900]}

Tu viens d'effacer le tableau. Explique cette notion depuis le début, simplement, avec un exemple de la vie
courante, en 4 à 7 phrases dites ; puis, en une phrase, dis à quoi elle sert dans la diapositive actuelle.

{REGLES_TABLEAU}

{REGLES_EXERCICE}

{REGLES_VOIX}

Réponds UNIQUEMENT par ce JSON :
{{"parole": "ton explication dite (règles de la voix)", "tableau": ["ligne 1", "ligne 2"], "ecrit": "l'essentiel en français écrit, deux phrases au plus", {FORMAT_EXERCICE}}}"""


def _tableau(v) -> list[str]:
    if isinstance(v, str):
        v = [l for l in v.split("\n")]
    if not isinstance(v, list):
        return []
    return [str(l).strip()[:90] for l in v if str(l).strip()][:6]


def reponse_depuis(texte_llm: str, ctx: dict, plan: Optional[list[dict]] = None, idx: int = -1) -> Optional[dict]:
    d = lire_json(texte_llm)
    if not d:
        return None
    cat = str(d.get("categorie") or "diapo").strip().lower().replace("-", "_").replace(" ", "_")
    if cat not in CATEGORIES:
        cat = "diapo"
    notion = str(d.get("notion") or "").strip()[:120]
    base = {"categorie": cat, "notion": notion, "diapo_suivante": None, "parole": "", "ecrit": "", "tableau": [], "gestes": [], "exercice": None}
    if cat == "suivante":
        plan = plan or []
        cible = next((i for i, s in enumerate(plan) if s["id"] == str(d.get("diapo_id") or "").strip()), -1)
        if cible > idx >= 0 or (cible >= 0 and idx < 0):
            base["diapo_suivante"] = {"id": plan[cible]["id"], "title": plan[cible]["title"]}
        elif cible >= 0:
            cat = base["categorie"] = "diapo"    # une diapositive déjà faite : c'est une notion du cours, on l'explique
        return base if cat == "suivante" else _avec_reponse(base, d, ctx)
    if cat in ("prerequis", "hors_cours"):
        return base
    return _avec_reponse(base, d, ctx)


def _avec_reponse(base: dict, d: dict, ctx: dict) -> Optional[dict]:
    parole = parole_propre(d.get("parole"))
    if not parole:
        return None
    return {**base, "parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:500], "tableau": _tableau(d.get("tableau")),
            "gestes": valider_gestes(d.get("gestes"), ctx.get("moments") or {}, ctx.get("reperes") or {})[:4],
            "exercice": valider_exercice(d.get("exercice"))}


def explication_depuis(texte_llm: str) -> Optional[dict]:
    d = lire_json(texte_llm)
    parole = parole_propre((d or {}).get("parole"))
    if not parole:
        return None
    return {"parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:500], "tableau": _tableau(d.get("tableau")),
            "exercice": valider_exercice(d.get("exercice"))}
