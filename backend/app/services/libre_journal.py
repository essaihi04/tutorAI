"""Ce que le tuteur avait sous la main, et ce qu'il en a fait.

En mode libre, la séance n'a ni leçon ni objectif : le tuteur choisit seul son
support à chaque tour. Quand l'élève dit « ça ne marche toujours pas », il n'y
avait rien à regarder — la conversation n'est stockée nulle part, et les deux
journaux existants (`visual_gaps`, `schema_gaps`) ne disent que ce qui a
MANQUÉ, jamais ce qui a été décidé. Impossible de répondre à la seule question
qui compte : le tuteur a-t-il ignoré une ressource, ou n'y en avait-il aucune ?

Ce journal met les deux moitiés côte à côte, une ligne par tour :

* l'OFFRE — ce que la bibliothèque a rapproché de la phrase de l'élève, et
  quel moteur le routeur imposait ;
* l'ENVOI — ce qui est réellement parti à l'écran.

Les deux moitiés arrivent à deux moments différents du tour : l'offre au
moment de construire le prompt, l'envoi après la réponse du modèle. Elles sont
donc retenues par session le temps de se rejoindre.

Trois défauts se lisent alors directement, sans rejouer la séance :

* ``ressource_ignoree`` — la bibliothèque couvrait la notion et rien n'est
  parti. C'est le défaut qui a motivé tout le câblage de `visual_shortlist`.
* ``promesse_non_tenue`` — la réponse annonce « regarde le tableau » sans
  qu'aucun bloc ne parte. L'élève regarde un écran vide et croit que son
  application est cassée ; c'est la faute la plus coûteuse, parce qu'il ne
  peut pas savoir d'où elle vient.
* ``identifiant_inconnu`` — le modèle a inventé un identifiant. L'élève ne
  voit rien, et le serveur n'en disait rien non plus.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import threading
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)


def _tracer(message: str) -> None:
    """Écrit la ligne SUR LA CONSOLE, là où le développeur regarde.

    Le projet n'appelle `logging.basicConfig` nulle part : sous uvicorn, la
    racine reste à WARNING et un `logger.info` ne s'affiche jamais. C'est la
    raison pour laquelle tout le handler de session trace avec `print` — ce
    journal fait de même, sinon les lignes qu'on vient d'écrire seraient
    invisibles précisément quand on les cherche.

    L'encodage est celui d'une console Windows, qui n'accepte pas toujours
    l'UTF-8 : une trace ne doit jamais faire tomber une séance.
    """
    _log.info(message)
    try:
        print(message)
    except UnicodeEncodeError:
        encodage = sys.stdout.encoding or "utf-8"
        print(message.encode(encodage, errors="replace").decode(encodage, errors="replace"))

#: Même convention que les deux autres journaux : surchargeable pour que la
#: suite de tests n'écrive pas dans le fichier de production.
FICHIER = Path(
    os.environ.get("LIBRE_JOURNAL_PATH")
    or Path(__file__).resolve().parents[2] / "data" / "libre_journal.jsonl"
)

_MAX_LIGNES = 5000

#: L'offre d'un tour, en attente de sa réponse. Bornée : une session qui se
#: ferme sans réponse ne doit pas retenir sa ligne pour toujours.
_offres: dict[str, dict[str, Any]] = {}
_verrou = threading.Lock()
_MAX_OFFRES = 64


#: « Regarde le tableau. » En français, en darija et en arabizi — c'est une
#: PROMESSE, et elle n'a le droit d'exister que dans une réponse qui porte
#: réellement le bloc correspondant.
_ANNONCE = re.compile(
    r"(?:regarde|voici|voila|voilà)\s+(?:le\s+|ce\s+)?(?:tableau|schema|schéma|figure)"
    r"|j(?:e vais|'ai)\s+(?:te\s+)?(?:montrer|dessiner|ecrire|écrire|tracer)"
    r"|(?:شوف|كتبت ليك|غادي نرسم|غادي نكتب|رسمت ليك)",
    re.IGNORECASE,
)


def _resume_offre(carte: dict[str, Any], route: dict[str, Any]) -> dict[str, Any]:
    """Les identifiants nus : c'est sur eux qu'on compare, pas sur la prose."""
    return {
        "reference": (carte.get("reference") or [None])[0],
        "croquis": (carte.get("croquis") or [None])[0],
        "presets": [identifiant for identifiant, _ in carte.get("presets") or []],
        "modeles_3d": [identifiant for identifiant, _ in carte.get("modeles_3d") or []],
        "simulations": [
            str(ressource.get("title") or "")[:60]
            for ressource in carte.get("simulations") or []
        ],
        "veut_croquis": bool(carte.get("veut_croquis")),
        "veut_mouvement": bool(carte.get("veut_mouvement")),
        "veut_profondeur": bool(carte.get("veut_profondeur")),
        "route_source": route.get("source"),
        "route_moteur": route.get("engine"),
    }


def retenir_offre(
    session: str,
    demande: str,
    carte: dict[str, Any],
    route: dict[str, Any],
) -> None:
    """Note ce que la bibliothèque proposait, avant que le modèle ne réponde."""
    offre = _resume_offre(carte or {}, route or {})
    with _verrou:
        if len(_offres) >= _MAX_OFFRES:
            # Les plus vieilles n'auront jamais leur réponse : la session est
            # partie. On les laisse tomber plutôt que de grossir sans fin.
            for vieille in list(_offres)[: _MAX_OFFRES // 2]:
                _offres.pop(vieille, None)
        _offres[session] = {"demande": (demande or "")[:200], "offre": offre}

    propose = [
        identifiant
        for identifiant in (
            [offre["reference"], offre["croquis"]]
            + offre["presets"]
            + offre["modeles_3d"]
        )
        if identifiant
    ]
    _tracer(
        f"[Libre] OFFRE   : {', '.join(propose) or 'rien'}"
        f" | route={offre['route_source']}/{offre['route_moteur'] or '-'}"
        f" | demande={(demande or '')[:70]!r}"
    )


def _lire_envoi(actions: list[dict[str, Any]] | None) -> dict[str, Any]:
    """Ce qui part vraiment à l'écran, lu depuis les actions déjà décodées."""
    schemas: list[str] = []
    presets: list[str] = []
    moteurs: list[str] = []
    gestes: list[str] = []

    for action in actions or []:
        if not isinstance(action, dict):
            continue
        nom = str(action.get("action") or "").strip().lower()
        if nom:
            gestes.append(nom)
        identifiant = action.get("schema_id") or action.get("schemaId")
        if isinstance(identifiant, str) and identifiant.strip():
            schemas.append(identifiant.strip())

        # Une figure de moteur peut voyager dans une ligne de `show_board`,
        # dans un pas de `show_live` ou seule : on regarde partout plutôt que
        # de supposer une forme.
        pile: list[Any] = [action.get("payload"), action.get("scientific")]
        while pile:
            noeud = pile.pop()
            if isinstance(noeud, list):
                pile.extend(noeud)
                continue
            if not isinstance(noeud, dict):
                continue
            pile.extend(noeud.get("lines") or [])
            pile.extend(noeud.get("steps") or [])
            science = noeud.get("scientific")
            if isinstance(science, dict):
                pile.append(science)
            identifiant = noeud.get("schema_id") or noeud.get("schemaId")
            if isinstance(identifiant, str) and identifiant.strip():
                schemas.append(identifiant.strip())
            moteur = noeud.get("engine")
            if isinstance(moteur, str) and moteur.strip():
                moteurs.append(moteur.strip())
            preset = noeud.get("presetId") or noeud.get("preset_id")
            if isinstance(preset, str) and preset.strip():
                presets.append(preset.strip())

    return {
        "schemas": sorted(set(schemas)),
        "presets": sorted(set(presets)),
        "moteurs": sorted(set(moteurs)),
        "gestes": sorted(set(gestes)),
    }


def _identifiants_inconnus(envoi: dict[str, Any]) -> list[str]:
    """Les identifiants que le modèle a inventés — l'élève ne voit rien."""
    from app.services.schema_catalog import schema_entry
    from app.services.scientific_presets import SCIENTIFIC_PRESETS

    inconnus = [i for i in envoi["schemas"] if schema_entry(i) is None]
    inconnus += [i for i in envoi["presets"] if i not in SCIENTIFIC_PRESETS]
    return inconnus


def noter_tour(
    session: str,
    reponse: str,
    actions: list[dict[str, Any]] | None,
    mode: str = "libre",
) -> dict[str, Any] | None:
    """Referme le tour : rapproche l'offre de l'envoi et écrit la ligne.

    N'échoue JAMAIS bruyamment. Perdre une ligne d'observation est sans
    conséquence ; interrompre la séance d'un élève ne l'est pas.
    """
    try:
        with _verrou:
            attendu = _offres.pop(session, None)
        envoi = _lire_envoi(actions)
        offre = (attendu or {}).get("offre") or {}

        avait = bool(
            offre.get("reference")
            or offre.get("croquis")
            or offre.get("presets")
            or offre.get("modeles_3d")
            or offre.get("simulations")
        )
        a_envoye = bool(
            envoi["schemas"] or envoi["presets"] or envoi["moteurs"] or envoi["gestes"]
        )
        inconnus = _identifiants_inconnus(envoi)

        ligne = {
            "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "mode": mode,
            "demande": (attendu or {}).get("demande", ""),
            "offre": offre,
            "envoi": envoi,
            # Les trois défauts, calculés ici pour que le fichier se lise sans
            # avoir à refaire le raisonnement à chaque relecture.
            "ressource_ignoree": avait and not a_envoye,
            "promesse_non_tenue": bool(_ANNONCE.search(reponse or "")) and not a_envoye,
            "identifiants_inconnus": inconnus,
        }

        defauts = [
            nom
            for nom, present in (
                ("RESSOURCE IGNOREE", ligne["ressource_ignoree"]),
                ("PROMESSE NON TENUE", ligne["promesse_non_tenue"]),
                ("IDENTIFIANT INCONNU", bool(inconnus)),
            )
            if present
        ]
        vu = ", ".join(envoi["schemas"] + envoi["presets"] + envoi["moteurs"]) or "rien"
        _tracer(
            f"[Libre] ENVOI   : {vu}"
            f" | gestes={', '.join(envoi['gestes']) or 'aucun'}"
        )
        if defauts:
            # Sur sa propre ligne, en majuscules : c'est ce qu'on cherche des
            # yeux en faisant défiler une console pleine.
            _tracer(f"[Libre] DEFAUT  : {' + '.join(defauts)}")

        _ecrire(ligne)
        return ligne
    except Exception as erreur:  # noqa: BLE001 — l'observation ne casse rien
        _log.warning("[Libre] tour non journalisé : %s", erreur)
        return None


def _ecrire(ligne: dict[str, Any]) -> None:
    try:
        FICHIER.parent.mkdir(parents=True, exist_ok=True)
        if FICHIER.exists() and sum(1 for _ in FICHIER.open(encoding="utf-8")) >= _MAX_LIGNES:
            _log.warning("[Libre] journal plein (%s lignes) — ligne ignorée", _MAX_LIGNES)
            return
        with FICHIER.open("a", encoding="utf-8") as flux:
            flux.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    except OSError as erreur:
        _log.warning("[Libre] impossible d'écrire : %s", erreur)


# ── Relecture ─────────────────────────────────────────────────────────

def tours(limite: int = 50) -> list[dict[str, Any]]:
    """Les derniers tours journalisés, du plus récent au plus ancien."""
    if not FICHIER.exists():
        return []
    lignes = []
    with FICHIER.open(encoding="utf-8") as flux:
        for ligne in flux:
            try:
                lignes.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return lignes[-limite:][::-1]


def bilan(limite: int = 500) -> dict[str, Any]:
    """Combien de tours, et combien portaient chacun des trois défauts.

    C'est la réponse à « est-ce que c'est toujours le même problème ? » :
    un nombre, pas une impression.
    """
    derniers = tours(limite)
    compte: Counter[str] = Counter()
    for ligne in derniers:
        if ligne.get("ressource_ignoree"):
            compte["ressource_ignoree"] += 1
        if ligne.get("promesse_non_tenue"):
            compte["promesse_non_tenue"] += 1
        if ligne.get("identifiants_inconnus"):
            compte["identifiant_inconnu"] += 1
    return {"tours": len(derniers), "defauts": dict(compte)}
