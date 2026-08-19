"""Le vocabulaire d'affichage du prof, en un seul endroit.

Le modèle pilote l'écran en glissant des balises dans sa prose :
``<ui>``, ``<board>``, ``<draw>``, ``<schema>``, ``<live>``,
``<exam_exercise>``, ``<suggestions>``. Le mécanisme est bon — mesuré sur le
prompt de production, il place quelque chose au tableau 5 fois sur 5 et n'a
produit aucun JSON illisible. Ce qui coûtait cher, c'est qu'il était décrit
NULLE PART de façon unique :

  - la liste des balises était recopiée à l'identique dans
    ``_sanitize_history_content`` et ``_extract_display_text`` — 14
    substitutions chacune, soit 28 lignes à tenir synchronisées à la main ;
  - les SOUS-TYPES de ``<ui>`` (``show_live`` = tableau vivant,
    ``show_board`` = tableau, ``qcm`` = exercice) n'étaient écrits que dans
    un tableau ASCII au milieu d'un prompt de 82 000 caractères.

Le second point n'est pas théorique : en analysant ce code j'ai conclu que le
tableau ne se déclenchait jamais, parce que je cherchais ``<board>`` alors
que l'explication pas-à-pas passe par ``<ui> show_live``. Le diagnostic était
faux. Quiconque touchera ce code après nous s'y trompera de la même façon
tant que le vocabulaire ne sera pas explicite et testé.

Ce module ne change RIEN au protocole : il le nomme.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Optional


# ── Le vocabulaire ────────────────────────────────────────────────

#: Les balises que le modèle peut émettre. L'ordre n'a pas d'importance,
#: mais la liste est la SEULE source de vérité — plus de copie ailleurs.
BALISES: tuple[str, ...] = (
    "ui",
    "board",
    "draw",
    "schema",
    "live",
    "exam_exercise",
    "suggestions",
    # `mode` ne dessine rien : il dit ce que l'élève est en train de FAIRE
    # (cours, exercice, examen, question). Il est ici parce que la propriété
    # qui compte est la même que pour les autres — une commande adressée au
    # système, qui doit disparaître de la prose lue et entendue par l'élève,
    # et surtout de l'historique, sinon le modèle se met à l'imiter. Ce qu'il
    # signifie appartient à `session_mode`, seul juge des transitions.
    "mode",
)

#: Les commandes écrites EN CLAIR, sans chevrons. Le prompt les demande ainsi
#: exprès : une annonce faite en darija n'est reconnue par aucun détecteur, et
#: `OUVRIR_IMAGE` ne dépend d'aucune langue.
#:
#: Mais elles voyagent dans la prose, et elles n'étaient retirées qu'à UN seul
#: endroit — `_extract_display_text`, c'est-à-dire le chemin NON streamé. Le
#: chat est streamé : l'élève lisait « شوف هاد الصورة. OUVRIR_IMAGE دابا ڭولي
#: ليا… » et la synthèse vocale, qui ne les connaît pas davantage, les
#: prononçait. Elles vivent donc ici, avec les balises, pour la même raison :
#: ce sont des ordres adressés au système, jamais au lycéen.
#:
#: Triées par longueur décroissante : « FERMER_EXERCICE » doit disparaître
#: avant qu'on ne cherche « EXERCICE: ».
MOTS_CLES: tuple[str, ...] = tuple(sorted(
    (
        "OUVRIR_IMAGE", "FERMER_IMAGE", "CACHER_MEDIA",
        "OUVRIR_SIMULATION", "FERMER_SIMULATION",
        "OUVRIR_EXERCICE", "FERMER_EXERCICE",
        "OUVRIR_TABLEAU", "FERMER_TABLEAU", "EFFACER_TABLEAU", "RESET_TABLEAU",
        "TOUT_FERMER", "PHASE_SUIVANTE",
        "DESSINER_SCHEMA:", "EXERCICE:",
    ),
    key=len,
    reverse=True,
))

_MOTIF_COMMANDES = re.compile(
    "|".join(re.escape(mot) for mot in MOTS_CLES)
)
_ESPACES_EN_TROP = re.compile(r"[ \t]{2,}")

#: La plus longue commande : une queue plus courte que ça, retenue en fin de
#: flux, laisserait passer un mot-clé coupé entre deux tokens.
LONGUEUR_MOT_CLE_MAX = max(len(mot) for mot in MOTS_CLES)

#: Sous-types rencontrés dans le JSON d'un ``<ui>``. Ce sont eux qui disent
#: ce que le bloc FAIT réellement — un ``<ui>`` n'est pas forcément un
#: exercice, et c'est le piège de tout ce protocole.
UI_TABLEAU_VIVANT = "show_live"     # le prof écrit/dessine en direct
UI_TABLEAU = "show_board"           # récapitulatif statique
UI_EXERCICE = ("qcm", "vrai_faux", "association")

# Primitives de tracé : leur présence signe un tableau, même sans le
# sous-type explicite (le modèle l'omet parfois).
_PRIMITIVES_TRACE = frozenset(
    {"write", "draw", "math", "arrow", "box", "rect", "text", "zoom", "subtitle"}
)

# Une balise laissée ouverte en fin de réponse (flux coupé, max_tokens
# atteint) doit être retirée JUSQU'À LA FIN : sinon un demi-JSON part dans le
# chat de l'élève. C'est le rôle de la seconde variante de chaque motif.
_MOTIFS_COMPLETS = tuple(
    re.compile(rf"<{b}>[\s\S]*?</{b}>", re.DOTALL) for b in BALISES
)
_MOTIFS_OUVERTS = tuple(
    re.compile(rf"<{b}>[\s\S]*", re.DOTALL) for b in BALISES
)

_MOTIFS_EXTRACTION = {
    b: re.compile(rf"<{b}>([\s\S]*?)</{b}>", re.DOTALL) for b in BALISES
}


@dataclass
class Bloc:
    """Un bloc de balise trouvé dans la réponse."""

    balise: str
    brut: str
    donnees: Optional[Any] = None      # None si le contenu n'est pas du JSON

    @property
    def lisible(self) -> bool:
        return self.donnees is not None


def retirer_balises(texte: str) -> str:
    """Retire TOUS les blocs de balises, y compris ceux restés ouverts.

    Remplace mot pour mot les 14 substitutions qui étaient recopiées dans
    `_sanitize_history_content` et `_extract_display_text`. Le comportement
    est identique : bloc complet d'abord, puis balise ouverte jusqu'à la fin.
    """
    if not texte:
        return ""
    for complet, ouvert in zip(_MOTIFS_COMPLETS, _MOTIFS_OUVERTS):
        texte = complet.sub("", texte)
        texte = ouvert.sub("", texte)
    return texte


def extraire(texte: str) -> list[Bloc]:
    """Tous les blocs présents, dans l'ordre où ils apparaissent.

    Le JSON est décodé quand c'est possible ; sinon `donnees` reste None et
    l'appelant décide. On ne lève jamais : une réponse abîmée doit dégrader
    l'affichage, pas interrompre le cours.
    """
    trouves: list[tuple[int, Bloc]] = []
    for balise, motif in _MOTIFS_EXTRACTION.items():
        for m in motif.finditer(texte or ""):
            brut = m.group(1).strip()
            try:
                donnees = json.loads(brut)
            except (json.JSONDecodeError, ValueError):
                donnees = None
            trouves.append((m.start(), Bloc(balise, brut, donnees)))
    trouves.sort(key=lambda t: t[0])
    return [b for _, b in trouves]


def _sous_types(valeur: Any, vus: Optional[list[str]] = None) -> list[str]:
    """Tous les champs de typage rencontrés dans un JSON imbriqué."""
    vus = [] if vus is None else vus
    if isinstance(valeur, dict):
        for cle, v in valeur.items():
            if cle in ("type", "kind", "action", "mode") and isinstance(v, str):
                vus.append(v.lower())
            _sous_types(v, vus)
    elif isinstance(valeur, list):
        for v in valeur:
            _sous_types(v, vus)
    return vus


def roles_ui(donnees: Any) -> frozenset[str]:
    """Ce qu'un bloc ``<ui>`` fait : 'tableau', 'exercice', ou LES DEUX.

    LE point qui induit en erreur : un ``<ui>`` est aussi bien le tableau
    vivant qu'un QCM. Compter les ``<ui>`` comme des exercices fait conclure
    à tort que le prof n'écrit jamais au tableau.

    Et il ne faut pas non plus trancher dans l'autre sens. Un QCM réellement
    émis en production porte ``show_board`` (où l'afficher) ET ``qcm`` (ce que
    c'est) : ce sont deux dimensions, pas deux valeurs concurrentes. Renvoyer
    un seul mot obligerait à en sacrifier une, et ferait passer des exercices
    pour des tableaux. D'où l'ensemble.
    """
    types = set(_sous_types(donnees))
    roles = set()
    if (UI_TABLEAU_VIVANT in types or UI_TABLEAU in types
            or types & _PRIMITIVES_TRACE):
        roles.add("tableau")
    if types & set(UI_EXERCICE):
        roles.add("exercice")
    return frozenset(roles)


def retirer_commandes(texte: str) -> str:
    """Retire les commandes en clair, sans toucher aux balises.

    Séparée de `retirer_balises` parce que les deux ne s'appliquent pas
    toujours ensemble : l'historique garde les commandes (le modèle doit
    continuer à savoir qu'elles existent), la bulle de chat et la voix, non.
    """
    if not texte:
        return ""
    return _ESPACES_EN_TROP.sub(" ", _MOTIF_COMMANDES.sub("", texte))


def texte_parle(texte: str) -> str:
    """Ce que l'élève doit LIRE et ENTENDRE : la prose, sans les commandes."""
    return retirer_commandes(retirer_balises(texte)).strip()
