"""Le tuteur réagit à ce que l'élève a fait LUI-MÊME dans la simulation d'une diapositive.

L'élève déplace un élément (le micro M₂, le point M, le fond de la mer…) et obtient un nouveau résultat.
Le tuteur, sans quitter la diapositive :
  1. interprète ce nouveau résultat en le comparant au précédent (ce qui a changé, pourquoi) ;
  2. pose UNE question sur ce résultat, du type qui convient à ce que l'élève a montré jusque-là :
     vrai/faux s'il s'est trompé à la question précédente, QCM par défaut, question directe s'il a juste ;
  3. corrige la réponse (QCM et vrai/faux sont corrigés dans le navigateur ; une réponse directe est jugée ici).

Le résultat n'est montré qu'à la demande (règle du 10 novembre 2026) : quand l'élève appuie sur « 🔎 Ton résultat »,
TOUT ce qui est écrit dans le panneau est dit par le tuteur — l'interprétation (`parole` ↔ `ecrit`), puis la question
lue à voix haute (`parole_question`). Chaque option a son propre retour, écrit et dit quand l'élève la choisit :
  - QCM : `question.retours = [{ecrit, parole}]`, un par choix, dans l'ordre de `choix` ;
  - vrai/faux : `affirmation.retours = [{ecrit, parole} pour « Vrai », {ecrit, parole} pour « Faux »]`.
`parole_juste` / `parole_faux` restent (anciens écrans, et secours si un retour manque).

Le texte dit suit les règles de la voix (skill `voix-du-cours`) : darija simple, français pour les termes du
programme, les nombres, les unités et les équations, en toutes lettres, sans chiffres ni symboles ni tashkil.
Le LLM (DeepSeek, via `llm_service.chat`) répond en JSON ; tout ce qui sort d'ici est vérifié et borné.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional

TYPES = ("vrai_faux", "qcm", "directe")

REGLES_VOIX = """RÈGLES DU TEXTE DIT (« parole ») — il est lu tel quel par une voix entraînée sur des profs marocains :
- darija simple, phrases courtes, une idée par phrase ; mots courants (يعني، دابا، إذن، شوف، مزيان، يلا) ;
- EN FRANÇAIS : les termes du programme (le retard, la célérité, la distance, la division, la sensibilité…), les
  équations (« tau égale d sur v »), les mots d'examen (calculer, justifier) ;
- les NOMBRES et les UNITÉS en mots français, jamais en chiffres ni en symboles : « six divisions »,
  « trois millisecondes », « un virgule zéro deux mètre », « trois cent quarante mètres par seconde » ;
- aucun chiffre, aucun symbole (= / × τ), aucun markdown, aucun tashkil ;
- une phrase toute en français de plus de dix mots se coupe par des virgules.
Exemple : « شوف، بعدتي M deux. دابا la distance هي un virgule zéro deux mètre، و tau ولا trois millisecondes. »"""


RETOUR = '{"ecrit": "...", "parole": "..."}'


def type_de_question(historique: list[dict]) -> str:
    """Le type de question suit la compréhension montrée sur cette diapositive."""
    if not historique:
        return "qcm"
    dernier = historique[-1]
    if dernier.get("correct") is False:
        return "vrai_faux"
    if dernier.get("correct") is True and dernier.get("type") in ("qcm", "vrai_faux"):
        return "directe"
    return "qcm"


def _etat_court(etat: dict) -> str:
    etat = etat or {}
    garde = {k: etat.get(k) for k in ("ce_qui_se_voit", "parameters", "tau_ms", "divisions", "mesures", "time_s") if k in etat}
    texte = json.dumps(garde, ensure_ascii=False, default=str)
    return texte[:1800]


def prompt_interpretation(diapo: dict, avant: dict, apres: dict, historique: list[dict]) -> tuple[str, str]:
    """(prompt, type de question imposé)."""
    genre = type_de_question(historique)
    consigne_retours = {
        "qcm": "« retours » a exactement un élément par choix, dans l'ordre de « choix ».",
        "vrai_faux": "chaque affirmation porte « retours » = [retour si l'élève répond Vrai, retour s'il répond Faux].",
        "directe": "(question directe : pas de retours, la réponse sera jugée à part).",
    }[genre]
    forme = {
        "vrai_faux": '"question": {"type": "vrai_faux", "enonce": "...", "affirmations": [{"texte": "...", "vrai": true, "retours": [RETOUR_SI_VRAI, RETOUR_SI_FAUX]}, {"texte": "...", "vrai": false, "retours": [RETOUR_SI_VRAI, RETOUR_SI_FAUX]}], "explication": "..."}',
        "qcm": '"question": {"type": "qcm", "enonce": "...", "choix": ["...", "...", "..."], "bonne": 0, "retours": [RETOUR_CHOIX_0, RETOUR_CHOIX_1, RETOUR_CHOIX_2], "explication": "..."}',
        "directe": '"question": {"type": "directe", "enonce": "...", "attendu": "la réponse juste, courte", "explication": "..."}',
    }[genre]
    forme = forme.replace("RETOUR_SI_VRAI", RETOUR).replace("RETOUR_SI_FAUX", RETOUR)
    forme = re.sub(r"RETOUR_CHOIX_\d", RETOUR, forme)
    forme = forme[:-1] + (', "parole_juste": "ce que tu dis s\'il répond juste (une ou deux phrases, règles de la voix)", '
                          '"parole_faux": "ce que tu dis s\'il se trompe : la bonne réponse et pourquoi (deux phrases, règles de la voix)"}')
    prompt = f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF au Maroc. Il suit la diapositive « {diapo.get('title', '')} ».
Ce que tu viens d'expliquer à voix haute : {str(diapo.get('speech') or '')[:1200]}

L'élève a manipulé LUI-MÊME la simulation et obtenu un nouveau résultat.
AVANT sa manipulation : {_etat_court(avant)}
APRÈS sa manipulation : {_etat_court(apres)}

1. Interprète son nouveau résultat : ce qui a changé par rapport à avant, avec les valeurs, et pourquoi (la loi du cours).
   Deux à quatre phrases. Félicite-le d'avoir essayé, sans en faire trop.
2. Pose UNE question de type « {genre} » sur ce résultat précis (une prédiction ou une justification, pas une définition).
   L'énoncé et les choix sont en FRANÇAIS écrit, avec les valeurs et les unités (on peut écrire 3,0 ms, τ, d).
3. TOUT ce qui est écrit est dit : « ecrit » ne contient rien que « parole » ne dise (mêmes idées, mêmes valeurs, dans
   le même ordre) ; « parole_question » lit à voix haute l'énoncé ET chaque choix (ou chaque affirmation), règles de la voix.
4. CHAQUE option a son propre retour {{"ecrit": "...", "parole": "..."}} : {consigne_retours}
   « ecrit » : une ou deux phrases en français écrit ; « parole » : la même chose dite (règles de la voix) — la bonne
   option : bravo et pourquoi c'est juste ; une option fausse : pourquoi elle est fausse, puis la bonne réponse et sa raison.

{REGLES_VOIX}

Réponds UNIQUEMENT par ce JSON :
{{"parole": "ton interprétation dite (règles ci-dessus), qui finit en annonçant la question sans la lire", "ecrit": "la même interprétation en français écrit, courte, avec les valeurs", "parole_question": "la question lue à voix haute, avec ses choix (règles de la voix)", {forme}}}"""
    return prompt, genre


def prompt_correction(diapo: dict, question: dict, reponse: str) -> str:
    return f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF. Diapositive « {diapo.get('title', '')} ».
Question posée : {question.get('enonce', '')}
Réponse attendue : {question.get('attendu', '')}
Réponse de l'élève : {reponse[:500]}

Juge la réponse (le fond compte, pas l'orthographe). Si elle est juste, dis précisément ce qui est juste. Sinon, nomme ce qui
manque et donne la bonne réponse avec sa justification, en deux ou trois phrases.

{REGLES_VOIX}

Réponds UNIQUEMENT par ce JSON : {{"correct": true, "parole": "...", "ecrit": "..."}}"""


def lire_json(texte: str) -> Optional[dict]:
    """Le premier objet JSON du texte du modèle (il l'entoure parfois de ```json)."""
    if not texte:
        return None
    m = re.search(r"\{.*\}", texte, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    return d if isinstance(d, dict) else None




def parole_propre(texte: Any) -> str:
    """Le texte dit, sans markdown ni tashkil. Les chiffres qui resteraient sont lus par la normalisation de la voix."""
    t = str(texte or "")
    t = re.sub(r"[*_#`>]+", "", t)
    t = re.sub(r"[ً-ْ]", "", t)          # jamais de tashkil
    return re.sub(r"\s+", " ", t).strip()[:900]


def valider_retours(retours: Any, n: int) -> Optional[list[dict]]:
    """Les retours d'une question, alignés sur ses options : exactement `n`, chacun écrit ET dit ; sinon aucun."""
    if not isinstance(retours, list) or len(retours) != n:
        return None
    out = []
    for r in retours:
        if not isinstance(r, dict):
            return None
        ecrit, parole = str(r.get("ecrit") or "").strip()[:400], parole_propre(r.get("parole"))[:500]
        if not ecrit or not parole:
            return None
        out.append({"ecrit": ecrit, "parole": parole})
    return out


def valider_question(q: Any, genre: str) -> Optional[dict]:
    if not isinstance(q, dict) or not str(q.get("enonce") or "").strip():
        return None
    out = {"type": genre, "enonce": str(q["enonce"]).strip()[:400], "explication": str(q.get("explication") or "").strip()[:500],
           "parole_juste": parole_propre(q.get("parole_juste")), "parole_faux": parole_propre(q.get("parole_faux"))}
    if genre == "qcm":
        choix = [str(c).strip()[:200] for c in (q.get("choix") or []) if str(c).strip()][:4]
        bonne = q.get("bonne")
        if len(choix) < 2 or not isinstance(bonne, int) or not 0 <= bonne < len(choix):
            return None
        out.update(choix=choix, bonne=bonne)
        retours = valider_retours(q.get("retours"), len(choix))
        if retours:
            out["retours"] = retours
    elif genre == "vrai_faux":
        aff = []
        for a in (q.get("affirmations") or []):
            if not isinstance(a, dict) or not str(a.get("texte") or "").strip():
                continue
            item = {"texte": str(a.get("texte")).strip()[:250], "vrai": bool(a.get("vrai"))}
            retours = valider_retours(a.get("retours"), 2)       # [si l'élève dit Vrai, s'il dit Faux]
            if retours:
                item["retours"] = retours
            aff.append(item)
        aff = aff[:3]
        if not aff:
            return None
        out.update(affirmations=aff)
    else:
        attendu = str(q.get("attendu") or "").strip()
        if not attendu:
            return None
        out.update(attendu=attendu[:300])
    return out


def reaction_depuis(texte_llm: str, genre: str) -> Optional[dict]:
    d = lire_json(texte_llm)
    if not d:
        return None
    parole = parole_propre(d.get("parole"))
    question = valider_question(d.get("question"), genre)
    if not parole or not question:
        return None
    return {"parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:600],
            "parole_question": parole_propre(d.get("parole_question"))[:700], "question": question}


def correction_depuis(texte_llm: str) -> Optional[dict]:
    d = lire_json(texte_llm)
    if not d or not isinstance(d.get("correct"), bool):
        return None
    return {"correct": d["correct"], "parole": parole_propre(d.get("parole")), "ecrit": str(d.get("ecrit") or "").strip()[:600]}
