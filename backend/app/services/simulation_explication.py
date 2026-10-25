"""Le professeur explique une simulation en la montrant du doigt, et réagit aux vérifications.

Les laboratoires dessinés au tableau (``frontend/public/media/simulations/shared/tableau``)
annoncent dans leur manifeste des **repères** pointables (``capabilities.reperes`` :
identifiant → libellé) et un **script d'explication** (``capabilities.explication`` :
une phrase par repère, par variante). Le tuteur dit chaque phrase en envoyant
``highlight {target}`` : le professeur animé entre dans la simulation, montre le
repère du doigt, et le laboratoire l'entoure à la craie.

Quand l'élève vérifie une réponse dans le laboratoire (action ``check``, état
``correct``), ce module décide de la réaction : rien de plus qu'un geste si c'est
juste ; un indice en pointant le bon repère à la première erreur ; à partir de la
deuxième, le professeur **relance lui-même la simulation** et la ré-explique
autrement, repère par repère. Même chose quand l'élève dit qu'il ne comprend pas.

Fonctions pures, sans accès au réseau : ``session_handler`` les appelle.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Optional

#: Commandes qui montrent un repère au lieu d'appuyer sur un bouton.
COMMANDES_POINTAGE = ("highlight", "point", "montrer", "show")
#: Actions d'un laboratoire qui signifient « l'élève a vérifié sa réponse ».
ACTIONS_VERIFICATION = frozenset({"check", "verify", "check_experiment", "verifier"})
#: Deux réactions du serveur à moins de ce délai (s) seraient du bavardage.
DELAI_MIN_REACTION_S = 8.0
#: Au-delà, le tuteur a déjà tout dit : on laisse la conversation reprendre la main.
REACTIONS_MAX_PAR_VARIANTE = 3

_PAS_COMPRIS = re.compile(
    r"(je (ne )?(comprends?|capte|vois|pige) (pas|rien)|pas compris|j'ai pas compris|"
    r"ما ?فهمت|مافهمتش|فهمت ?والو|ma ?fhemt|mafhemtch|fhemt walo|comprends rien|c'est flou|"
    r"peux[- ]tu (ré|re)expliquer|réexplique|re-?explique|encore une fois|montre[- ]moi encore)",
    re.IGNORECASE,
)


def eleve_ne_comprend_pas(texte: str) -> bool:
    """« Je n'ai pas compris », « ما فهمت », « réexplique » : l'élève demande à revoir."""
    return bool(_PAS_COMPRIS.search(str(texte or "")))


# ──────────────────────────────────────────────────────────── manifeste

def fusionner_manifeste(existant: dict, entrant: dict) -> bool:
    """Enrichit un manifeste déjà reçu avec ce que le doublon apporte de plus.

    Les laboratoires renvoient leur manifeste une fois les repères connus
    (après le premier dessin) : les commandes n'ont pas changé, mais les
    ``reperes`` et l'``explication`` sont là. Rend True si quelque chose a été
    ajouté.
    """
    caps_e = existant.setdefault("capabilities", {}) if isinstance(existant, dict) else {}
    caps_n = entrant.get("capabilities", {}) if isinstance(entrant, dict) else {}
    if not isinstance(caps_n, dict):
        return False
    change = False
    for cle in ("reperes", "explication", "controls", "state_schema"):
        valeur = caps_n.get(cle)
        if valeur and valeur != caps_e.get(cle):
            caps_e[cle] = valeur
            change = True
    for cle in ("commands", "globals"):
        nouvelles = [c for c in (caps_n.get(cle) or []) if c not in (caps_e.get(cle) or [])]
        if nouvelles:
            caps_e[cle] = list(caps_e.get(cle) or []) + nouvelles
            change = True
    schema_e = caps_e.setdefault("command_schema", {})
    for cle, valeur in (caps_n.get("command_schema") or {}).items():
        if cle not in schema_e:
            schema_e[cle] = valeur
            change = True
    if not caps_e.get("config") and caps_n.get("config"):
        caps_e["config"] = caps_n["config"]
        change = True
    texte = str(entrant.get("page_text") or "")
    if len(texte) > len(str(existant.get("page_text") or "")):
        existant["page_text"] = texte
        change = True
    return change


def reperes_du_manifeste(manifest: dict) -> dict[str, str]:
    caps = (manifest or {}).get("capabilities", {}) or {}
    reperes = caps.get("reperes") or {}
    return {str(k): str(v) for k, v in reperes.items()} if isinstance(reperes, dict) else {}


def script_explication(manifest: dict, variante: Optional[str] = None) -> list[dict]:
    """Le script de la variante courante : ``[{"repere": id, "texte": phrase}, …]``.

    L'explication peut être un dictionnaire par variante ou une liste plate
    (chaque pas pouvant porter ``variante``).
    """
    caps = (manifest or {}).get("capabilities", {}) or {}
    brut = caps.get("explication")
    if not brut:
        return []
    if isinstance(brut, dict):
        pas = brut.get(variante) if variante else None
        if pas is None:
            pas = next(iter(brut.values()), []) if len(brut) == 1 else []
        brut = pas or []
    if not isinstance(brut, list):
        return []
    resultat = []
    for pas in brut:
        if not isinstance(pas, dict) or not pas.get("texte"):
            continue
        if variante and pas.get("variante") and pas["variante"] != variante:
            continue
        resultat.append({"repere": str(pas.get("repere") or ""), "texte": str(pas["texte"])})
    return resultat


def commande_relance(manifest: dict) -> str:
    """La commande qui rejoue la simulation : ``fire_pulse`` si le labo l'a, sinon ``start``."""
    commandes = ((manifest or {}).get("capabilities", {}) or {}).get("commands") or []
    for candidate in ("fire_pulse", "run_trial", "run_model", "start"):
        if candidate in commandes:
            return candidate
    return "start"


# ──────────────────────────────────────────────────────────── prompt

def action_pointage(repere: str, phrase: str = "") -> str:
    charge = {"command": "highlight", "parameters": {"target": repere}}
    if phrase:
        charge["guidance_text"] = phrase[:120]
    return ('<ui>{"actions":[{"type":"simulation","action":"control","payload":'
            + json.dumps(charge, ensure_ascii=False) + '}]}</ui>')


def bloc_prompt(manifest: dict, variante: Optional[str] = None) -> str:
    """Le bloc du prompt système : repères pointables, script d'explication et règles du geste."""
    reperes = reperes_du_manifeste(manifest)
    if not reperes:
        return ""
    script = script_explication(manifest, variante)
    lignes = ["[LE PROFESSEUR MONTRE LA SIMULATION DU DOIGT]",
              "Repères pointables (highlight → target) : "
              + " ; ".join(f"{k} = {v}" for k, v in reperes.items()) + "."]
    if script:
        lignes.append("Script d'explication de cette expérience, dans l'ordre (dis chaque phrase avec tes mots, "
                      "en pointant son repère) :")
        for i, pas in enumerate(script, 1):
            lignes.append(f"  {i}. [{pas['repere']}] {pas['texte']}")
    premier = script[0]["repere"] if script else next(iter(reperes))
    lignes += [
        "RÈGLES DU GESTE :",
        "- Pour expliquer la simulation, écris la phrase PUIS l'action de pointage juste après, un repère par "
        "phrase, jusqu'à 4 pointages par réponse : le professeur vole dans la simulation, montre le repère du "
        "doigt pendant que tu parles, et le laboratoire l'entoure à la craie. Exemple : "
        f"« Regarde la source. » {action_pointage(premier)}",
        "- Quand l'état contient correct: true, félicite précisément ce qui est juste (il lève les bras). "
        "correct: false : nomme ce qui est juste, donne UN indice en pointant le repère qui manque, puis laisse "
        "réessayer (il fait non de la tête, sans gronder).",
        "- Si l'élève dit qu'il n'a pas compris, ou échoue une deuxième fois : relance la simulation toi-même "
        f"(commande {commande_relance(manifest)}), puis ré-explique autrement en suivant le script, repère par repère.",
    ]
    return "\n".join(lignes)


def prompt_reexplication(contexte: dict, manifest: dict, variante: Optional[str], etat: dict,
                         echecs: int, demande_eleve: bool = False) -> str:
    """Le prompt d'une réaction du serveur à une vérification ratée (ou à « je n'ai pas compris »)."""
    script = script_explication(manifest, variante)
    reperes = reperes_du_manifeste(manifest)
    etat_json = json.dumps(etat or {}, ensure_ascii=False, default=str)
    if len(etat_json) > 2500:
        etat_json = etat_json[:2500] + "…"
    relance = demande_eleve or echecs >= 2
    lignes = [
        f"Tu es le tuteur en {contexte.get('subject', 'Sciences')} d'un élève de 2e BAC. "
        f"Leçon : {contexte.get('lesson_title', '')}.",
        ("L'élève dit qu'il n'a pas compris la simulation." if demande_eleve else
         f"L'élève vient de vérifier sa réponse dans la simulation et elle est fausse (échec n°{echecs})."),
        f"État réel de la simulation : {etat_json}",
        "Repères pointables : " + " ; ".join(f"{k} = {v}" for k, v in reperes.items()) + ".",
    ]
    if script:
        lignes.append("Script d'explication : " + " | ".join(f"[{p['repere']}] {p['texte']}" for p in script))
    if relance:
        lignes += [
            "CONSIGNE : commence par UNE phrase qui annonce que tu relances l'expérience, suivie de l'action "
            + f'<ui>{{"actions":[{{"type":"simulation","action":"control","payload":{{"command":"{commande_relance(manifest)}"}}}}]}}</ui>',
            "Puis ré-explique AUTREMENT (pas les mêmes mots), 3 phrases au plus, chacune suivie de son action de "
            f"pointage, par exemple {action_pointage(script[0]['repere'] if script else next(iter(reperes), ''))}.",
            "Termine par la question à refaire, sans donner la réponse.",
        ]
    else:
        lignes += [
            "CONSIGNE : en 2 phrases, nomme ce qui est juste dans ce qu'il a fait, puis donne UN indice précis en "
            "pointant le repère concerné (une action de pointage après la phrase, comme "
            f"{action_pointage(script[0]['repere'] if script else next(iter(reperes), ''))}). Ne donne pas la réponse ; "
            "invite à réessayer.",
        ]
    lignes.append("Parle en français simple, chaleureux et exigeant. Aucune balise <eval>.")
    return "\n".join(lignes)


# ──────────────────────────────────────────────────────────── décision

def derniere_action(actions: list) -> str:
    if not actions:
        return ""
    last = actions[-1]
    return str(last.get("action", "") if isinstance(last, dict) else last)


def decider_reaction(orch: dict, etat: dict, actions: list, maintenant: Optional[float] = None) -> Optional[str]:
    """Que fait le serveur après ce nouvel état ? ``None`` (rien), ``"indice"`` ou ``"relance"``.

    Ne réagit qu'à une vérification (action ``check``) portant ``correct``, une
    fois par vérification, pas plus de ``REACTIONS_MAX_PAR_VARIANTE`` fois par
    variante, et jamais deux fois en moins de ``DELAI_MIN_REACTION_S``. Met à
    jour ``orch["verification"]`` (compteurs et horodatage).
    """
    if not isinstance(etat, dict) or derniere_action(actions) not in ACTIONS_VERIFICATION:
        return None
    correct = etat.get("correct")
    if not isinstance(correct, bool):
        return None
    suivi = orch.setdefault("verification", {"cle": None, "echecs": {}, "reactions": {}, "derniere": None})
    variante = str(etat.get("current_variant") or etat.get("variant") or "_")
    cle = f"{variante}:{len(actions)}:{correct}"
    if suivi.get("cle") == cle:
        return None
    suivi["cle"] = cle
    now = time.time() if maintenant is None else maintenant
    if correct:
        suivi["echecs"][variante] = 0
        return None
    suivi["echecs"][variante] = suivi["echecs"].get(variante, 0) + 1
    if suivi["reactions"].get(variante, 0) >= REACTIONS_MAX_PAR_VARIANTE:
        return None
    if suivi.get("derniere") is not None and now - float(suivi["derniere"]) < DELAI_MIN_REACTION_S:
        return None
    suivi["reactions"][variante] = suivi["reactions"].get(variante, 0) + 1
    suivi["derniere"] = now
    return "relance" if suivi["echecs"][variante] >= 2 else "indice"


def nombre_echecs(orch: dict, variante: Optional[str]) -> int:
    suivi = (orch or {}).get("verification") or {}
    return int((suivi.get("echecs") or {}).get(str(variante or "_"), 0))
