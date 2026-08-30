"""Une étape, une surface, une action.

Le tuteur accumulait les supports. Une même réponse pouvait poser une scène,
puis une image, puis rouvrir une simulation : quatre écrans pour une seule
idée, et un élève qui ne sait plus où regarder. Les scores de
`resource_decision_service` disent quel support convient le mieux ; ils ne
disent rien du NOMBRE de supports, ni de ce que l'élève doit FAIRE devant.

Ce module tranche les deux. Il rend UNE étape — une surface, une action
attendue, un critère de réussite — et rien d'autre. L'ordre est fixe, et
chaque marche n'est franchie que si la précédente ne sert pas l'objectif :

    scène contrôlable → image validée → modèle 3D → simulation → cahier

Deux marches ont une condition propre, et c'est tout l'intérêt de l'ordre.
Le modèle 3D ne se justifie que si la PROFONDEUR compte — sinon il coûte une
rotation pour rien. La simulation ne se justifie que si MANIPULER ou MESURER
change la compréhension : sans paramètre à changer ni mesure à lire, c'est
une scène animée qu'il fallait, pas un laboratoire.

Le modèle explique ; ce module valide le choix et la transition.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

from app.services.visual_shortlist import (
    demande_de_la_profondeur,
    demande_du_mouvement,
    plier,
)


#: L'entrée en matière, avant toute surface. Elle ne s'affiche pas : elle se
#: dit et s'écrit. L'élève qui arrive sur une notion ne sait ni d'où il part
#: ni où on l'emmène ; ouvrir une scène avant de le lui dire, c'est le mettre
#: devant un écran sans lui avoir donné de raison de le regarder.
INTRODUCTION: str = "introduction"


#: Les cinq surfaces, dans l'ordre où le tuteur les essaie.
ORDRE_PAR_DEFAUT: tuple[str, ...] = (
    "scene",
    "image",
    "modele_3d",
    "simulation",
    "cahier",
)


#: Ce que l'élève doit FAIRE devant chaque surface. Un support sans action
#: demandée n'est qu'une illustration : l'élève le regarde et n'en retient
#: rien. C'est la question qui transforme l'écran en travail.
ACTION_ATTENDUE: dict[str, str] = {
    INTRODUCTION: (
        "Ouvre par deux phrases : ce que l'élève sait déjà sur cette notion, et "
        "pourquoi elle compte au BAC. Annonce ensuite le plan en trois ou quatre "
        "étapes courtes, numérotées, et dis par laquelle vous commencez. "
        "N'ouvre AUCUN support ce tour-ci — le plan s'écrit au tableau."
    ),
    "scene": "Pose UNE question d'observation sur la scène, puis attends la réponse.",
    "image": "Focalise UNE seule zone de l'image, puis pose une question dessus.",
    "modele_3d": "Fais tourner le modèle sur UN seul axe, puis demande ce que la profondeur révèle.",
    "simulation": (
        "Fais prédire AVANT de lancer, fais modifier UN paramètre, fais lire UNE mesure, "
        "puis fais expliquer l'écart avec la prédiction."
    ),
    "cahier": (
        "Dicte au cahier pas à pas : définition, pause copie, relation avec ses unités, "
        "pause copie, croquis légendé, pause reproduis, puis rappel sans regarder."
    ),
}


#: Ce qui prouve que l'étape a servi. « J'ai compris » n'en fait pas partie :
#: c'est la règle du checkpoint, et elle vaut ici aussi.
CRITERE_DE_REUSSITE: dict[str, str] = {
    INTRODUCTION: "L'élève sait où on l'emmène et par quoi on commence.",
    "scene": "L'élève décrit ce qui change dans la scène, avec ses mots.",
    "image": "L'élève nomme la zone montrée et dit à quoi elle sert.",
    "modele_3d": "L'élève dit ce que la vue en profondeur ajoute au schéma plat.",
    "simulation": "L'élève relie sa mesure à sa prédiction et explique l'écart.",
    "cahier": "L'élève reproduit le croquis et redit la relation sans regarder.",
}


@dataclass(frozen=True)
class EtapeRoutee:
    """Une étape de séance : une surface, une action, un critère, un repli."""

    rang: int
    surface: str
    action_attendue: str
    critere: str
    repli: str | None
    raison: str

    @property
    def type_de_ressource(self) -> str | None:
        """Le `resource_type` de la bibliothèque, quand la surface en a un."""
        return {
            "image": "image",
            "simulation": "simulation",
        }.get(self.surface)


# ── Ce que le type de concept appelle ─────────────────────────────────
#
# Le bandeau du bas de la planche : chaque famille de notions a une forme
# qui la sert mieux que les autres. Ce n'est pas un style d'apprentissage,
# c'est la nature de l'objet — une force a une direction, un processus a un
# ordre, une définition n'a ni l'une ni l'autre.

_FIGURE_COORDONNEE = re.compile(
    r"\b(vecteur|vecteurs|force|forces|optique|lentille|miroir|rayon|"
    r"coordonn|repere|repère|fonction|derivee|dérivée|integrale|intégrale|"
    r"courbe|graphe|geometrie|géométrie|complexe|complexes)\b"
)
_SCHEMA_CAUSAL = re.compile(
    r"\b(processus|reseau|réseau|chaine|chaîne|cycle|circuit|voie|voies|"
    r"mecanisme|mécanisme|etape|étape|transmission|regulation|régulation|"
    r"boucle|cascade)\b"
)
_MOUVEMENT_MESURE = re.compile(
    r"\b(mouvement|vitesse|acceleration|accélération|chute|oscillation|"
    r"pendule|trajectoire|projectile|frottement|amortissement|resonance|"
    r"résonance|periode|période|onde|ondes|propagation|celerite|célérité|"
    r"amplitude|frequence|fréquence)\b"
)


def forme_attendue(contexte: str) -> str:
    """La forme qui sert cette famille de notions.

    Renvoie l'une des quatre du bandeau : `figure_coordonnee`,
    `schema_causal`, `simulation_mesuree` ou `tableau_ordinaire`. Le tableau
    ordinaire est le défaut assumé — définitions, relations et tableaux n'ont
    besoin d'aucune figure, et leur en imposer une les dessert.
    """
    plie = plier(contexte or "")
    if _MOUVEMENT_MESURE.search(plie):
        return "simulation_mesuree"
    if _FIGURE_COORDONNEE.search(plie):
        return "figure_coordonnee"
    if _SCHEMA_CAUSAL.search(plie):
        return "schema_causal"
    return "tableau_ordinaire"


# ── Manipuler change-t-il la compréhension ? ──────────────────────────

_A_MANIPULER = re.compile(
    r"\b(manipul|mesur|parametre|paramètre|varier|varie|fais varier|"
    r"experience|expérience|experimenter|expérimenter|tester|teste|essaie|"
    r"regler|régler|augmente|diminue|influence|effet de|depend|dépend)\w*"
)


def manipulation_utile(demande: str, contexte: str = "") -> bool:
    """L'élève doit-il vraiment MODIFIER quelque chose pour comprendre ?

    Sans paramètre à changer ni mesure à lire, une simulation complète est un
    décor. La planche est explicite là-dessus : on lui préfère alors une scène
    ou un schéma. Le mouvement seul ne suffit pas — une chute qu'on regarde se
    montre très bien par une scène contrôlable.
    """
    joint = plier(f"{demande or ''} {contexte or ''}")
    if _A_MANIPULER.search(joint):
        return True
    # La mécanique en mouvement APPELLE la mesure : c'est la correspondance du
    # bandeau. Une chute, une oscillation, une onde ne se comprennent pas en
    # les regardant passer — il faut changer la hauteur, la raideur, la
    # fréquence, et lire ce que ça donne.
    return forme_attendue(f"{demande or ''} {contexte or ''}") == "simulation_mesuree"


def router(
    *,
    demande: str = "",
    contexte: str = "",
    scene_disponible: bool = False,
    image_disponible: bool = False,
    modele_3d_disponible: bool = False,
    simulation_disponible: bool = False,
    manipulation_exigee: bool = False,
    plan_annonce: bool = True,
    deja_montre: Sequence[str] = (),
) -> EtapeRoutee:
    """L'étape à tenir maintenant : une surface, une action, un critère.

    `deja_montre` porte les surfaces déjà servies pour ce même micro-objectif.
    Une surface déjà vue ne se reprend pas : c'est ce qui empêche la boucle où
    le tuteur repose la même image à chaque tour faute de mieux. Le cahier,
    lui, reste toujours ouvert — il n'y a rien en dessous.

    `manipulation_exigee` est la porte de sortie de l'élève : quand c'est LUI
    qui réclame la simulation, on ne lui oppose pas notre jugement sur
    l'utilité de manipuler. Le serveur valide le choix du modèle, pas celui de
    l'élève.
    """
    # Rien ne s'ouvre avant que l'élève sache où on l'emmène. L'introduction
    # passe donc devant toutes les surfaces, une seule fois par notion.
    if not plan_annonce:
        return EtapeRoutee(
            rang=0,
            surface=INTRODUCTION,
            action_attendue=ACTION_ATTENDUE[INTRODUCTION],
            critere=CRITERE_DE_REUSSITE[INTRODUCTION],
            repli=ORDRE_PAR_DEFAUT[0],
            raison="plan_non_annonce",
        )

    vues = set(deja_montre or ())
    profondeur = demande_de_la_profondeur(demande or "")
    manipuler = manipulation_exigee or manipulation_utile(demande, contexte)

    # Jamais l'image ET la 3D : la planche l'écrit en toutes lettres. La
    # profondeur est la seule chose qui fasse préférer la seconde — et quand
    # elle compte, l'image plate ne doit pas passer devant sous prétexte
    # qu'elle vient plus tôt dans l'ordre.
    en_trois_d = modele_3d_disponible and profondeur
    disponibilite = {
        "scene": scene_disponible,
        "image": image_disponible and not en_trois_d,
        "modele_3d": en_trois_d,
        "simulation": simulation_disponible and manipuler,
        "cahier": True,
    }
    raisons = {
        "scene": "scene_pertinente",
        "image": "image_bac_validee",
        "modele_3d": "profondeur_utile",
        "simulation": "manipulation_utile",
        "cahier": "aucune_ressource_ne_sert_l_objectif",
    }

    restantes = [s for s in ORDRE_PAR_DEFAUT if s not in vues]
    for rang, surface in enumerate(ORDRE_PAR_DEFAUT, start=1):
        if surface in vues or not disponibilite[surface]:
            continue
        suivantes = [
            s for s in restantes
            if ORDRE_PAR_DEFAUT.index(s) > rang - 1 and disponibilite[s]
        ]
        return EtapeRoutee(
            rang=rang,
            surface=surface,
            action_attendue=ACTION_ATTENDUE[surface],
            critere=CRITERE_DE_REUSSITE[surface],
            repli=suivantes[0] if suivantes else None,
            raison=raisons[surface],
        )

    # Toutes les surfaces ont été servies : on revient au cahier, qui se
    # rouvre autant de fois qu'il le faut.
    return EtapeRoutee(
        rang=len(ORDRE_PAR_DEFAUT),
        surface="cahier",
        action_attendue=ACTION_ATTENDUE["cahier"],
        critere=CRITERE_DE_REUSSITE["cahier"],
        repli=None,
        raison="toutes_les_surfaces_deja_vues",
    )


# ── Le budget d'un écran ──────────────────────────────────────────────

def budget_respecte(surfaces_de_ce_tour: Sequence[str]) -> bool:
    """Un écran porte UNE ressource principale, jamais deux.

    Le cahier ne compte pas comme une ressource : le tableau accompagne la
    surface au lieu de la concurrencer — c'est lui qui porte la question.
    """
    principales = [s for s in surfaces_de_ce_tour if s != "cahier"]
    return len(principales) <= 1


def consigne_d_etape(etape: EtapeRoutee) -> str:
    """Ce que le modèle doit lire pour tenir l'étape, en clair et court."""
    lignes = [
        f"ÉTAPE {etape.rang} — {etape.surface.replace('_', ' ').upper()}.",
        etape.action_attendue,
        f"Réussi quand : {etape.critere}",
        "UNE seule idée nouvelle, UNE seule action demandée, UNE seule question.",
        "N'affiche AUCUN nouvel écran avant la réponse de l'élève.",
    ]
    if etape.repli:
        lignes.append(f"Si ça ne prend pas, passe à : {etape.repli.replace('_', ' ')}.")
    return "\n".join(lignes)
