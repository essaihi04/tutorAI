"""Ce que le tuteur a voulu montrer sans que la bibliothèque l'ait.

Le défaut se voyait jusqu'ici de la pire façon : un élève tombait sur un
tableau à la place d'un schéma de cellule végétale, et il fallait qu'on le
remarque par-dessus son épaule. Or le serveur SAIT, à l'instant où il cherche
un schéma, qu'il n'en a trouvé aucun — il ne le disait à personne.

Chaque échec de rapprochement est donc noté ici, avec le sujet de la séance.
Le fichier se lit comme une liste de courses : ce sont les schémas qui
manquent VRAIMENT, classés par ce que les élèves demandent, et non par ce
qu'on imagine qu'il faudrait dessiner.

Le programme du BAC est fini : cette liste doit se vider.
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import unicodedata
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
    os.environ.get("SCHEMA_GAPS_PATH")
    or Path(__file__).resolve().parents[2] / "data" / "schema_gaps.jsonl"
)

# Un même sujet revient à chaque tour d'une séance : on ne le note qu'une fois
# par processus, sinon la liste de courses devient un journal de bord.
_deja_notes: set[str] = set()
_verrou = threading.Lock()

# Au-delà, le fichier n'est plus une liste de courses mais un dépotoir.
_MAX_LIGNES = 2000

_BRUIT = re.compile(
    r"\b(bonjour|salut|merci|ok|oui|non|ça va|ca va|d'accord|au revoir)\b",
    re.IGNORECASE,
)


def _empreinte(sujet: str) -> str:
    plie = unicodedata.normalize("NFKD", sujet.lower())
    plie = "".join(c for c in plie if not unicodedata.combining(c))
    return " ".join(sorted(set(re.findall(r"[a-z0-9]{4,}", plie))))[:200]


def sujet_exploitable(sujet: str) -> bool:
    """Un sujet ne vaut d'être noté que s'il désigne une notion.

    « bonjour ça va » n'appelle aucun schéma : le noter ferait croire à un
    manque là où il n'y a rien à dessiner.
    """
    nettoye = (sujet or "").strip()
    if len(nettoye) < 12:
        return False
    return bool(_empreinte(nettoye)) and not _BRUIT.fullmatch(nettoye.strip())


def noter_manque(sujet: str, meilleur_candidat: str | None = None, score: int = 0) -> bool:
    """Enregistre un schéma qui aurait dû exister. Rend True s'il a été noté.

    N'échoue JAMAIS bruyamment : un défaut d'écriture de cette liste ne doit
    pas interrompre une séance. Le pire qui puisse arriver est de perdre une
    ligne de liste de courses.
    """
    if not sujet_exploitable(sujet):
        return False

    empreinte = _empreinte(sujet)
    with _verrou:
        if empreinte in _deja_notes:
            return False
        _deja_notes.add(empreinte)

    ligne = {
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sujet": sujet.strip()[:300],
        "meilleur_candidat": meilleur_candidat or "",
        "score": score,
    }
    try:
        FICHIER.parent.mkdir(parents=True, exist_ok=True)
        if FICHIER.exists() and sum(1 for _ in FICHIER.open(encoding="utf-8")) >= _MAX_LIGNES:
            _log.warning("[SchemaManquant] liste pleine (%s lignes) — ligne ignorée", _MAX_LIGNES)
            return False
        with FICHIER.open("a", encoding="utf-8") as flux:
            flux.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    except OSError as erreur:
        _log.warning("[SchemaManquant] impossible d'écrire : %s", erreur)
        return False

    _log.info("[SchemaManquant] aucun schéma pour « %s » (meilleur : %s, score=%s)",
              ligne["sujet"], ligne["meilleur_candidat"] or "aucun", score)
    return True


def manques(limite: int = 50) -> list[dict]:
    """Les manques enregistrés, du plus récent au plus ancien."""
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
