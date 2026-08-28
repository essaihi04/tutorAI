"""Ce que le tuteur a voulu dessiner et que le validateur a jeté.

Un élément de figure inconnu ne fait pas échouer la figure : il disparaît, et
les autres s'affichent. C'est le bon choix — mieux vaut une figure amputée que
pas de figure. Mais l'élève, lui, entend « regarde l'angle alpha » et cherche
sur l'écran un angle que personne n'a dessiné. Le tuteur a raison, la figure a
tort, et c'est l'élève qui doute de lui.

Le validateur SAIT, à l'instant où il jette un élément, qu'il vient de créer
ce décalage. Il ne le disait à personne : chaque refus s'écrit maintenant ici,
avec le type demandé et le titre de la figure.

Le fichier se lit comme la liste des primitives qui manquent au contrat,
classée par ce que le modèle essaie VRAIMENT de dessiner. C'est la même
logique que `schema_gaps.py`, un cran plus bas : là il manquait un schéma
entier, ici il manque un trait.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

_log = logging.getLogger(__name__)

#: Où s'écrit le journal. Surchargeable par l'environnement pour UNE
#: raison : la suite de tests appelle le validateur avec des figures
#: volontairement invalides, et chaque exécution ajoutait ses refus au
#: journal de PRODUCTION. Les fixtures ont fini par y être majoritaires —
#: `classement()`, censé dire quelle primitive manque vraiment aux élèves,
#: ne classait plus que du décor de test.
FICHIER = Path(
    os.environ.get("VISUAL_GAPS_PATH")
    or Path(__file__).resolve().parents[2] / "data" / "visual_gaps.jsonl"
)

# Un même refus se répète à chaque tour d'une séance : on ne le note qu'une
# fois par processus, sinon la liste devient un journal de bord.
_deja_notes: set[str] = set()
_verrou = threading.Lock()

# Au-delà, le fichier n'est plus une liste de manques mais un dépotoir.
_MAX_LIGNES = 2000


def noter_element_refuse(moteur: str, types: list[str], titre: str = "") -> bool:
    """Enregistre les types d'éléments jetés d'une figure. Rend True si noté.

    N'échoue JAMAIS bruyamment : perdre une ligne de cette liste est sans
    conséquence, interrompre une séance ne l'est pas.
    """
    propres = sorted({str(t).strip()[:32] for t in types if str(t).strip()})
    if not propres:
        return False

    empreinte = f"{moteur}:{','.join(propres)}"
    with _verrou:
        if empreinte in _deja_notes:
            return False
        _deja_notes.add(empreinte)

    ligne = {
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "moteur": moteur,
        "types": propres,
        "titre": (titre or "")[:120],
    }
    try:
        FICHIER.parent.mkdir(parents=True, exist_ok=True)
        if FICHIER.exists() and sum(1 for _ in FICHIER.open(encoding="utf-8")) >= _MAX_LIGNES:
            _log.warning("[VisuelRefuse] liste pleine (%s lignes) — ligne ignorée", _MAX_LIGNES)
            return False
        with FICHIER.open("a", encoding="utf-8") as flux:
            flux.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    except OSError as erreur:
        _log.warning("[VisuelRefuse] impossible d'écrire : %s", erreur)
        return False

    _log.info("[VisuelRefuse] %s : %s jeté(s) de « %s »",
              moteur, ", ".join(propres), ligne["titre"] or "figure sans titre")
    return True


def refus(limite: int = 50) -> list[dict]:
    """Les refus enregistrés, du plus récent au plus ancien."""
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


def classement() -> list[tuple[str, int]]:
    """Les primitives manquantes, la plus réclamée en tête.

    C'est cette liste qui dit quoi ajouter au contrat ensuite : elle est
    écrite par les demandes réelles, pas par ce qu'on imagine qu'il faudrait
    savoir dessiner.
    """
    compte: Counter[str] = Counter()
    for ligne in refus(limite=_MAX_LIGNES):
        for type_ in ligne.get("types", []):
            compte[f"{ligne.get('moteur', '?')}.{type_}"] += 1
    return compte.most_common()
