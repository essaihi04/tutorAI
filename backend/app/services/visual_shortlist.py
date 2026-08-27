"""Ce qui est DÉJÀ prêt à montrer, pour la phrase que l'élève vient d'écrire.

La bibliothèque visuelle a grossi par couches successives, et chaque couche a
apporté son propre chemin d'accès :

* les **schémas SVG** ont un catalogue généré, et le prompt les liste tous ;
* les **croquis au crayon** vivent dans ce même catalogue, marqués
  ``resourceRole: teacher_sketch`` ;
* les **scènes animées** (`scientific_presets`) n'avaient AUCUN rapprochement —
  elles étaient recopiées à la main dans un paragraphe du prompt, et le modèle
  devait se souvenir qu'un identifiant collait à la question ;
* le **modèle 3D** n'était atteignable que par un motif du routeur qui exigeait
  que l'élève prononce lui-même « mitochondrie » ET « 3D » ;
* les **simulations du cours** ne se demandaient qu'à l'aveugle, par
  ``OUVRIR_SIMULATION`` — le serveur cherchait après coup, et ne répondait rien
  quand il ne trouvait pas.

Résultat : en question libre, où la séance n'a ni leçon ni objectif pour
orienter le tuteur, tout ce travail restait invisible. Le tuteur répondait en
prose, ou redessinait à main levée une figure qui existait déjà, animée et
légendée.

Ce module fait le rapprochement UNE fois, sur les cinq surfaces à la fois, et
rend une carte courte : voici les identifiants réels qui couvrent cette
notion, et voici lequel choisir selon ce que l'élève a demandé. Il ne décide
rien à la place du modèle — il lui enlève le besoin de deviner.

Le rapprochement lui-même n'est pas réécrit ici : `schema_catalog` expose sa
mécanique (repli sans accents, bornes de mot, pondération des mots-clés), et
les scènes, les modèles 3D et les ressources de cours sont comparés avec
exactement la même.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Sequence

from app.services.schema_catalog import (
    classer_schemas,
    est_croquis,
    mot_cle_present,
    plier,
    poids_mot_cle,
    schema_title,
)
from app.services.scientific_presets import SCIENTIFIC_PRESETS
from app.services.scientific_visual_skill import MODELES_3D
from app.services.scientific_visual_router import demande_du_mouvement


# ── Ce que l'élève demande, dans les trois langues de la séance ───────

#: « Dessine-moi ça. » La demande de CROQUIS n'est pas une demande de schéma :
#: elle appelle la version au crayon, tracée trait après trait au tableau, et
#: pas la planche de référence détaillée. Les deux existent pour la plupart des
#: notions du chapitre 1 ; les confondre annule tout l'intérêt d'avoir fait les
#: deux.
#:
#: L'arabizi compte autant que le français : « rsem lia », « rassam lia » sont
#: ce que la reconnaissance vocale produit telle quelle.
_CROQUIS = re.compile(
    r"(?<!\w)(?:dessine\w*|dessin|dessiner|croquis|schematise\w*|schematiser"
    r"|trace\w*|esquisse\w*|au tableau|a main levee|main levee)(?!\w)"
    r"|(?<!\w)r[ae]ss?[ae]m\w*(?!\w)"
    r"|(?:ارسم|رسم|خطط|خطاطة)",
    re.IGNORECASE,
)

#: « Fais-la tourner. » La profondeur, la rotation et le zoom sont les trois
#: seules choses qu'un modèle 3D apporte et qu'un schéma n'a pas. Sans l'une
#: d'elles, la planche SVG reste meilleure : elle est légendée, imprimable et
#: conforme au BAC.
_PROFONDEUR = re.compile(
    r"(?<!\w)(?:3d|3 d|trois dimensions|profondeur|volume|relief"
    r"|tourn\w*|pivot\w*|zoom\w*|camera|de tous les cotes)(?!\w)"
    r"|(?:ثلاثي الابعاد|ثلاثية الأبعاد)",
    re.IGNORECASE,
)


def demande_un_croquis(texte: str) -> bool:
    """L'élève demande-t-il un DESSIN au tableau, et non une planche ?"""
    if not texte:
        return False
    return bool(_CROQUIS.search(plier(texte)) or _CROQUIS.search(texte))


def demande_de_la_profondeur(texte: str) -> bool:
    """L'élève demande-t-il à tourner autour de l'objet ?"""
    if not texte:
        return False
    return bool(_PROFONDEUR.search(plier(texte)) or _PROFONDEUR.search(texte))


# ── Le rapprochement, surface par surface ─────────────────────────────

def _score(keywords: Iterable[Any], contexte_plie: str) -> int:
    """Ce que pèse une liste de mots-clés face au contexte."""
    return sum(
        poids_mot_cle(str(mot))
        for mot in keywords
        if isinstance(mot, str) and mot.strip() and mot_cle_present(mot, contexte_plie)
    )


def _classer(catalogue: dict[str, dict[str, Any]], contexte: str, limite: int) -> list[tuple[str, int]]:
    contexte_plie = plier(contexte)
    if not contexte_plie.strip():
        return []
    trouves = [
        (identifiant, _score(definition.get("keywords", ()), contexte_plie))
        for identifiant, definition in catalogue.items()
    ]
    trouves = [(identifiant, score) for identifiant, score in trouves if score >= 2]
    trouves.sort(key=lambda item: item[1], reverse=True)
    return trouves[:limite]


def apparier_presets(contexte: str, limite: int = 2) -> list[tuple[str, int]]:
    """Les scènes animées du catalogue qui couvrent cette notion.

    Le seuil de 2 est le même que celui du registre SVG : un mot-clé
    distinctif seul suffit (« chimiosmose », « myogramme »), un mot de
    chapitre seul ne suffit pas.
    """
    return _classer(SCIENTIFIC_PRESETS, contexte, limite)


def apparier_modeles_3d(contexte: str, limite: int = 1) -> list[tuple[str, int]]:
    """Les modèles 3D audités qui couvrent cette notion."""
    return _classer(MODELES_3D, contexte, limite)


#: Un mot du titre d'une ressource ne devient un mot-clé qu'à partir d'une
#: certaine longueur : « la », « des », « cours » n'identifient rien.
_TITRE_MOT = re.compile(r"[a-z0-9]{5,}")


def apparier_simulations(
    contexte: str,
    ressources: Sequence[dict] | None,
    limite: int = 2,
) -> list[dict]:
    """Les simulations du cours qui parlent de cette notion.

    Elles étaient demandées à l'aveugle : le tuteur écrivait
    ``OUVRIR_SIMULATION`` en espérant que le serveur trouve quelque chose. En
    question libre, où la séance n'a pas de leçon rattachée, il ne trouvait
    généralement rien — et l'élève regardait un écran vide. Les nommer d'avance
    supprime le pari : si la liste est vide, le tuteur SAIT qu'il devra
    produire la scène lui-même.
    """
    contexte_plie = plier(contexte)
    if not contexte_plie.strip() or not ressources:
        return []

    trouves: list[tuple[int, dict]] = []
    for ressource in ressources:
        if not isinstance(ressource, dict):
            continue
        if ressource.get("resource_type") != "simulation":
            continue
        titre = str(ressource.get("title") or "").strip()
        concepts = [c for c in (ressource.get("concepts") or []) if isinstance(c, str)]
        score = _score(concepts, contexte_plie)
        score += _score(_TITRE_MOT.findall(plier(titre)), contexte_plie)
        if score >= 2:
            trouves.append((score, ressource))
    trouves.sort(key=lambda item: item[0], reverse=True)
    return [ressource for _, ressource in trouves[:limite]]


# ── La carte ──────────────────────────────────────────────────────────

def carte_des_visuels(
    contexte: str,
    demande: str = "",
    simulations: Sequence[dict] | None = None,
) -> dict[str, Any]:
    """Tout ce qui est prêt pour cette notion, rangé par surface.

    `contexte` voit large — séance et derniers messages — parce que c'est ce
    qu'il faut pour rapprocher une notion. `demande` est la seule phrase que
    l'élève vient d'écrire : c'est elle, et elle seule, qui dit s'il veut un
    dessin, du mouvement ou de la profondeur.
    """
    classement = classer_schemas(contexte, limite=8)
    croquis = [(sid, score) for sid, score in classement if est_croquis(sid) and score >= 2]
    references = [(sid, score) for sid, score in classement if not est_croquis(sid) and score >= 2]

    return {
        "reference": references[0] if references else None,
        "croquis": croquis[0] if croquis else None,
        "presets": apparier_presets(contexte),
        "modeles_3d": apparier_modeles_3d(contexte),
        "simulations": apparier_simulations(contexte, simulations),
        "veut_croquis": demande_un_croquis(demande),
        "veut_mouvement": demande_du_mouvement(demande),
        "veut_profondeur": demande_de_la_profondeur(demande),
    }


def _ligne_preset(preset_id: str) -> str:
    definition = SCIENTIFIC_PRESETS[preset_id]
    variantes = ", ".join(sorted(definition["variants"]))
    return f"{preset_id} — {definition['title']} (variantes : {variantes})"


def _ligne_modele_3d(model_id: str) -> str:
    definition = MODELES_3D[model_id]
    focus = ", ".join(definition["focus"])
    return f"{model_id} — {definition['title']} (focus : {focus})"


def bloc_visuels_disponibles(
    contexte: str,
    demande: str = "",
    simulations: Sequence[dict] | None = None,
    insister: bool = False,
) -> str:
    """L'instruction compacte à injecter avant le prompt du tuteur.

    Rend une chaîne vide quand rien n'est prêt : dire « aucune ressource ne
    couvre cette notion » à chaque tour occuperait le contexte pour ne rien
    apprendre au modèle, qui sait déjà générer une figure quand il n'a rien.
    """
    carte = carte_des_visuels(contexte, demande, simulations)

    inventaire: list[str] = []
    if carte["reference"]:
        schema_id = carte["reference"][0]
        inventaire.append(
            f"  • SCHÉMA DE RÉFÉRENCE : {schema_id} — {schema_title(schema_id)}"
        )
    if carte["croquis"]:
        schema_id = carte["croquis"][0]
        inventaire.append(
            f"  • CROQUIS AU CRAYON  : {schema_id} — {schema_title(schema_id)}"
        )
    for preset_id, _ in carte["presets"]:
        inventaire.append(f"  • SCÈNE ANIMÉE       : {_ligne_preset(preset_id)}")
    for model_id, _ in carte["modeles_3d"]:
        inventaire.append(f"  • MODÈLE 3D          : {_ligne_modele_3d(model_id)}")
    for ressource in carte["simulations"]:
        titre = str(ressource.get("title") or "").strip() or "simulation du cours"
        inventaire.append(f"  • SIMULATION DU COURS: « {titre} » — ouvre-la avec OUVRIR_SIMULATION")

    if not inventaire:
        return ""

    lignes = [
        "[DÉJÀ PRÊT POUR CETTE DEMANDE — NE REDESSINE PAS CE QUI EXISTE]",
        "Ces ressources sont déjà tracées, légendées et conformes au BAC. Les",
        "afficher rend mieux et coûte moins cher qu'une figure improvisée.",
        "",
        *inventaire,
        "",
        "LAQUELLE : c'est CE QUE L'ÉLÈVE DEMANDE qui tranche, jamais la plus",
        "impressionnante des cinq.",
    ]

    # L'ordre des règles suit celui des intentions détectées : la première qui
    # s'applique est celle que l'élève a formulée, pas celle qui reste.
    if carte["veut_profondeur"] and carte["modeles_3d"]:
        lignes.append(
            "→ Il demande à TOURNER AUTOUR / à voir en 3D : envoie le MODÈLE 3D "
            "(ligne `scientific`, moteur `three`)."
        )
    elif carte["veut_mouvement"] and (carte["presets"] or carte["simulations"]):
        lignes.append(
            "→ Il demande à voir BOUGER : envoie la SCÈNE ANIMÉE (ligne "
            "`scientific`, moteur `preset`) ou ouvre la SIMULATION DU COURS. "
            "Une image fixe ne répond pas à cette demande."
        )
    elif carte["veut_croquis"] and carte["croquis"]:
        lignes.append(
            "→ Il demande un DESSIN (« dessine », « croquis », « au tableau », "
            "« رسم ليا ») : envoie le CROQUIS AU CRAYON dans un pas `figure` de "
            "`show_live`, pas la planche de référence."
        )
    elif carte["reference"]:
        lignes.append(
            "→ Il demande une EXPLICATION : affiche le SCHÉMA DE RÉFÉRENCE avec "
            "`show_schema`, et commente-le au lieu de le décrire."
        )
    elif carte["croquis"]:
        lignes.append(
            "→ Aucune planche de référence sur cette notion : trace le CROQUIS AU "
            "CRAYON dans un pas `figure` de `show_live`."
        )

    lignes.append(
        "→ Une seule ressource à la fois : ouvrir la suivante ferme la précédente. "
        "Enchaîne-les dans l'ordre de ton explication plutôt que de tout empiler."
    )
    lignes.append(
        "→ N'INVENTE AUCUN identifiant : ceux ci-dessus existent, les autres non, "
        "et l'élève ne verrait rien."
    )

    if insister:
        # La question libre est le mode où l'élève travaille seul, et c'était
        # le seul où le tuteur pouvait répondre en prose : toute la
        # bibliothèque restait alors inutilisée. Rappeler qu'elle est là au
        # moment précis où elle correspond à la question coûte deux lignes.
        lignes.append(
            "→ MODE QUESTION LIBRE : cette notion EST couverte. Répondre en texte "
            "seul, ou redessiner une figure listée ci-dessus, est une faute — "
            "l'élève a le support sous les yeux ou il ne l'a pas."
        )

    return "\n".join(lignes)
