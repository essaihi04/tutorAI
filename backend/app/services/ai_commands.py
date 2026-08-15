"""Les commandes d'affichage du prof, en appels d'outils typés.

Aujourd'hui le modèle émet ses commandes en BALISES au milieu de sa prose
(``<board>…</board>``, ``<ui>…</ui>``…), et le serveur les récupère à coups
d'expressions régulières — plus de cent dans le seul `session_handler`. Le
prix se paie deux fois :

  - à la lecture : chaque balise doit être extraite du texte, puis validée à
    la main, puis retirée du flux avant qu'elle n'arrive dans le chat ;
  - à l'écriture : il faut ensuite les EFFACER de l'historique, parce que le
    modèle imite tout ce qu'il y voit — d'où la vingtaine de substitutions de
    `_sanitize_history_content`.

Un appel d'outil n'a aucun de ces deux problèmes : il arrive dans un champ
séparé de la prose, ses arguments sont du JSON validé par le fournisseur, et
il ne pollue jamais le texte que lit l'élève.

Vérifié sur `deepseek-chat` : le modèle émet la prose PUIS l'appel dans le
MÊME flux (« texte -> outil »). Le tool-calling ne coûte donc pas un second
aller-retour, ce qui aurait annulé le travail fait sur la latence.

Ce module ne contient que le contrat et le décodage. Le branchement sur la
session se fait ailleurs, par incréments.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional


# ── Le contrat ────────────────────────────────────────────────────
#
# Un outil par balise existante, avec les MÊMES données : la migration doit
# pouvoir se faire commande par commande, sans rien changer côté navigateur.

OUTILS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "ecrire_au_tableau",
            "description": (
                "Écrit au tableau pendant l'explication : titre puis lignes. "
                "À utiliser dès qu'une notion mérite d'être vue, pas seulement "
                "entendue. Remplace la balise <board>."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "titre": {"type": "string"},
                    "lignes": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["titre", "lignes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ecrire_en_direct",
            "description": (
                "Écrit au tableau ÉTAPE PAR ÉTAPE, synchronisé sur la voix : "
                "chaque étape est dite pendant qu'elle s'écrit. Pour une "
                "démonstration ou un calcul mené. Remplace la balise <live>."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "titre": {"type": "string"},
                    "etapes": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["titre", "etapes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dessiner",
            "description": (
                "Trace un schéma au tableau (axes, courbe, figure, échiquier "
                "de croisement). Remplace la balise <draw>."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "titre": {"type": "string"},
                    "commandes": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Primitives de dessin, comme dans <draw>.",
                    },
                },
                "required": ["commandes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "afficher_schema",
            "description": (
                "Affiche un schéma DÉJÀ EN BIBLIOTHÈQUE par son identifiant, "
                "au lieu de le redessiner. Remplace la balise <schema>."
            ),
            "parameters": {
                "type": "object",
                "properties": {"schema_id": {"type": "string"}},
                "required": ["schema_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "poser_exercice",
            "description": (
                "Pose un exercice interactif : QCM, vrai/faux, association, "
                "test rapide. Remplace la balise <ui>."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "titre": {"type": "string"},
                    "lignes": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Items de l'exercice, comme dans <ui>.",
                    },
                },
                "required": ["lignes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "poser_exercice_bac",
            "description": (
                "Affiche un exercice tiré des examens nationaux. Remplace la "
                "balise <exam_exercise>."
            ),
            "parameters": {
                "type": "object",
                "properties": {"exercice_id": {"type": "string"}},
                "required": ["exercice_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "proposer_suites",
            "description": (
                "Propose 2 à 4 réponses rapides alignées sur ce qui vient "
                "d'être demandé à l'élève. Remplace la balise <suggestions>."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "suggestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 4,
                    },
                },
                "required": ["suggestions"],
            },
        },
    },
]

NOMS_OUTILS: frozenset[str] = frozenset(
    o["function"]["name"] for o in OUTILS
)

# Correspondance avec l'ancien vocabulaire, le temps que les deux chemins
# coexistent. Sert aussi de garde : un outil sans équivalent balise n'aurait
# personne pour l'exécuter côté navigateur.
BALISE_POUR_OUTIL: dict[str, str] = {
    "ecrire_au_tableau": "board",
    "ecrire_en_direct": "live",
    "dessiner": "draw",
    "afficher_schema": "schema",
    "poser_exercice": "ui",
    "poser_exercice_bac": "exam_exercise",
    "proposer_suites": "suggestions",
}


@dataclass
class AppelOutil:
    """Un appel complet, arguments déjà décodés."""

    nom: str
    arguments: dict[str, Any]
    identifiant: str = ""

    @property
    def connu(self) -> bool:
        return self.nom in NOMS_OUTILS

    @property
    def balise(self) -> str:
        """L'ancienne balise équivalente, ou '' si l'outil est inconnu."""
        return BALISE_POUR_OUTIL.get(self.nom, "")


@dataclass
class _Fragment:
    nom: str = ""
    arguments: str = ""
    identifiant: str = ""


class AssembleurAppels:
    """Recolle les appels d'outils arrivant en fragments dans le flux SSE.

    Le fournisseur n'envoie pas un appel d'un bloc : le nom arrive dans le
    premier delta, puis les arguments par tranches de JSON — parfois un
    accolade à la fois — et plusieurs appels s'entrelacent, distingués par
    leur seul `index`. Mesuré sur `deepseek-chat` : **181 fragments** pour un
    unique appel.

    Recoller par concaténation naïve mélangerait deux appels simultanés ;
    d'où l'indexation stricte. Rien n'est décodé avant la fin du flux : un
    JSON tronqué n'est pas une erreur, c'est un appel encore incomplet.
    """

    def __init__(self):
        self._par_index: dict[int, _Fragment] = {}

    def ajouter(self, deltas: Optional[list[dict]]) -> None:
        """Absorbe le champ `tool_calls` d'un delta SSE. Tolère le bruit."""
        if not deltas:
            return
        for i, delta in enumerate(deltas):
            if not isinstance(delta, dict):
                continue
            # `index` est la seule chose qui distingue deux appels en
            # parallèle. Absent, on retombe sur la position dans la liste.
            index = delta.get("index")
            if not isinstance(index, int):
                index = i
            frag = self._par_index.setdefault(index, _Fragment())

            if delta.get("id"):
                frag.identifiant = delta["id"]
            fonction = delta.get("function") or {}
            if fonction.get("name"):
                frag.nom = fonction["name"]
            # Les arguments se CONCATÈNENT : chaque delta n'en porte qu'un
            # bout, et un bout vide est légitime.
            morceau = fonction.get("arguments")
            if isinstance(morceau, str):
                frag.arguments += morceau

    def termines(self) -> list[AppelOutil]:
        """Les appels complets, dans l'ordre d'apparition.

        Un appel dont les arguments ne sont pas du JSON valide est ÉCARTÉ,
        pas propagé : mieux vaut un tableau qui ne s'affiche pas qu'une
        commande à moitié lue envoyée au navigateur.
        """
        appels: list[AppelOutil] = []
        for index in sorted(self._par_index):
            frag = self._par_index[index]
            if not frag.nom:
                continue
            brut = frag.arguments.strip() or "{}"
            try:
                arguments = json.loads(brut)
            except json.JSONDecodeError:
                continue
            if not isinstance(arguments, dict):
                continue
            appels.append(AppelOutil(frag.nom, arguments, frag.identifiant))
        return appels

    def reinitialiser(self) -> None:
        self._par_index.clear()


@dataclass
class EvenementFlux:
    """Ce qu'un flux outillé rend : du texte, ou des appels terminés."""

    texte: str = ""
    appels: list[AppelOutil] = field(default_factory=list)

    @property
    def est_texte(self) -> bool:
        return bool(self.texte)
