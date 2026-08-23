"""Routage des demandes de schémas 2e BAC vers le bon moteur scientifique.

Le registre SVG reste prioritaire. Quand il ne couvre pas une notion, ce
module choisit un moteur déclaratif et fournit au modèle une fiche de qualité
disciplinaire : éléments obligatoires et erreurs à éviter. Une demande
inconnue reste générable grâce au routeur heuristique, sans autoriser de code.
"""

from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.services.schema_catalog import match_schema, schema_title


BLUEPRINTS_PATH = Path(__file__).resolve().parents[2] / "data" / "visual_blueprints_2bac.json"

_EXPLICIT_VISUAL = re.compile(
    r"\b(schema|sch[eé]ma|dessin|dessine|croquis|figure|visualise|montre[- ]moi|representation graphique)\b"
    r"|(?:رسم|خطاطة|تبيان|وريني)",
    re.IGNORECASE,
)

_DYNAMIC = re.compile(
    r"\b(simulation|simule|anime|animation|mouvement|tombe|oscille|collision|rebond|trajectoire)\b",
    re.IGNORECASE,
)

def _mots(*mots: str) -> re.Pattern[str]:
    """Un motif qui admet le pluriel, comme le registre des schémas le fait.

    L'élève écrit « bilan des FORCES ». Le mot-clé, lui, est au singulier :
    `\\bforce\\b` ne le trouvait pas, `bilan` du motif Cytoscape le trouvait,
    et un bilan des forces — trois vecteurs dans un repère — partait vers un
    moteur de RÉSEAUX. Le `s` final valait le mauvais dessin.
    """
    return re.compile(rf"(?<!\w)(?:{'|'.join(mots)})[sx]?(?!\w)", re.IGNORECASE)


# L'ordre décide : le premier motif qui répond emporte le moteur. Les cas les
# moins ambigus passent donc en tête.
_ENGINE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        # Un échiquier de croisement, un tableau de variations ou un tableau
        # d'avancement ne sont pas des dessins : les faire dessiner produit
        # une figure fausse là où deux colonnes disent tout, et cela
        # contredit le PROTOCOLE GÉNÉTIQUE qui exige déjà `type=table`.
        "table",
        _mots("echiquier", "damier", "tableau de variation", "tableau de signe",
              "tableau d avancement", "tableau descriptif", "table de verite"),
    ),
    (
        "jsxgraph",
        _mots("courbe", "fonction", "repere", "coordonnee", "vecteur", "force",
              "optique", "rayon", "lentille", "miroir", "foyer", "focale",
              "refraction", "reflexion", "diffraction", "incidence", "image",
              "tangente", "asymptote", "trajectoire", "orbite", "cercle",
              "geometrie", "complexe", "onde periodique", "graphique",
              "bilan des force", "champ", "pendule simple"),
    ),
    (
        "cytoscape",
        # « arbre » tout court est retiré : il attirait l'arbre GÉNÉALOGIQUE,
        # qui se dessine en carrés et ronds rangés par génération et non en
        # réseau. Les arbres qui SONT des graphes restent nommés en entier.
        _mots("chaine", "cycle", "voie", "etape", "processus", "reseau", "bilan",
              "cause", "consequence", "algorithme", "transformation",
              "metabolisme", "reaction en cascade", "arbre phylogenetique",
              "phylogenie", "arbre de decision"),
    ),
    (
        "roughsvg",
        _mots("cellule", "organe", "organite", "structure", "ultrastructure",
              "chromosome", "appareil", "montage", "circuit", "coupe", "roche",
              "plaque", "membrane", "molecule", "arbre genealogique",
              "genealogie", "experience", "dispositif"),
    ),
)

_STOPWORDS = {
    "avec", "dans", "pour", "sans", "entre", "vers", "schema", "dessin", "figure",
    "cours", "montre", "faire", "les", "des", "une", "sur", "du", "de", "la", "le",
}


def _fold(value: str) -> str:
    folded = unicodedata.normalize("NFKD", (value or "").lower())
    folded = "".join(char for char in folded if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9α-ω]+", folded))


def _tokens(value: str) -> set[str]:
    """Jetons avec une variante singulière légère pour les formulations BAC."""
    result: set[str] = set()
    for token in value.split():
        result.add(token)
        if len(token) > 4 and token.endswith(("s", "x")):
            result.add(token[:-1])
    return result


@lru_cache(maxsize=1)
def visual_blueprints() -> tuple[dict[str, Any], ...]:
    try:
        raw = json.loads(BLUEPRINTS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ()
    if not isinstance(raw, list):
        return ()
    return tuple(item for item in raw if isinstance(item, dict) and item.get("id"))


def visual_request_is_explicit(context: str) -> bool:
    return bool(_EXPLICIT_VISUAL.search(context or ""))


def _blueprint_score(blueprint: dict[str, Any], folded_context: str) -> int:
    score = 0
    context_tokens = _tokens(folded_context) - _STOPWORDS
    for raw_keyword in blueprint.get("keywords", []):
        keyword = _fold(str(raw_keyword))
        if not keyword:
            continue
        if re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", folded_context):
            score += 5 + keyword.count(" ")
            continue
        keyword_tokens = _tokens(keyword) - _STOPWORDS
        common = context_tokens & keyword_tokens
        if keyword_tokens and common:
            score += len(common)
            if keyword_tokens <= context_tokens:
                score += 2
    return score


def match_visual_blueprint(context: str) -> tuple[dict[str, Any] | None, int]:
    folded = _fold(context)
    if not folded:
        return None, 0
    best: dict[str, Any] | None = None
    best_score = 0
    for blueprint in visual_blueprints():
        score = _blueprint_score(blueprint, folded)
        if score > best_score:
            best, best_score = blueprint, score
    return (best, best_score) if best_score >= 3 else (None, best_score)


def recommend_generated_engine(context: str) -> str:
    folded = _fold(context)
    if _DYNAMIC.search(folded) and re.search(
        r"\b(chute|collision|pendule|ressort|projectile|plan incline|mecanique)\b", folded,
    ):
        return "matter"
    for engine, pattern in _ENGINE_PATTERNS:
        if pattern.search(folded):
            return engine
    return "roughsvg"


def route_scientific_visual(context: str) -> dict[str, Any]:
    """Décide entre schéma validé, blueprint BAC et génération générale."""
    schema_id, schema_score = match_schema(context)
    blueprint, blueprint_score = match_visual_blueprint(context)

    # Un rapprochement fort avec un SVG contrôlé reste toujours prioritaire.
    if schema_id and schema_score >= 3:
        return {
            "source": "schema",
            "schema_id": schema_id,
            "title": schema_title(schema_id),
            "score": schema_score,
            "explicit": visual_request_is_explicit(context),
        }

    # Une fiche disciplinaire précise l'emporte sur une coïncidence FAIBLE de
    # vocabulaire du registre (plan COMPLEXE ≠ complexe respiratoire,
    # équilibre lithosphérique ≠ équilibre acide-base).
    if blueprint and blueprint_score >= 3:
        return {
            "source": "blueprint",
            "blueprint_id": blueprint["id"],
            "title": blueprint.get("title", "Schéma scientifique"),
            "engine": blueprint.get("engine", "roughsvg"),
            "must_show": list(blueprint.get("must_show", [])),
            "avoid": list(blueprint.get("avoid", [])),
            "score": blueprint_score,
            "explicit": visual_request_is_explicit(context),
        }

    if schema_id and schema_score >= 2:
        return {
            "source": "schema",
            "schema_id": schema_id,
            "title": schema_title(schema_id),
            "score": schema_score,
            "explicit": visual_request_is_explicit(context),
        }

    if blueprint:
        return {
            "source": "blueprint",
            "blueprint_id": blueprint["id"],
            "title": blueprint.get("title", "Schéma scientifique"),
            "engine": blueprint.get("engine", "roughsvg"),
            "must_show": list(blueprint.get("must_show", [])),
            "avoid": list(blueprint.get("avoid", [])),
            "score": blueprint_score,
            "explicit": visual_request_is_explicit(context),
        }

    return {
        "source": "generated",
        "title": "Schéma scientifique à la demande",
        "engine": recommend_generated_engine(context),
        "must_show": [],
        "avoid": [],
        "score": 0,
        "explicit": visual_request_is_explicit(context),
    }


def build_visual_route_prompt(context: str) -> str:
    """Instruction compacte injectée avant le prompt général du tuteur."""
    route = route_scientific_visual(context)
    if route["source"] == "schema":
        return (
            "[SCHÉMA VALIDÉ DISPONIBLE POUR CETTE SÉANCE]\n"
            f"Utilise `show_schema` avec `{route['schema_id']}` — {route['title']}.\n"
            "Ne le redessine pas : il est déjà contrôlé, légendé et reproductible."
        )

    # Certaines demandes portent le mot « dessine » sans appeler un dessin :
    # un échiquier de croisement, un tableau de variations ou un tableau
    # d'avancement sont des TABLEAUX. Les envoyer vers un moteur graphique
    # produit une figure fausse — et pour la génétique, cela contredit le
    # PROTOCOLE GÉNÉTIQUE, qui impose déjà `type=table` à l'échiquier.
    if route["engine"] == "table":
        return (
            "[CE N'EST PAS UN DESSIN — C'EST UN TABLEAU]\n"
            f"Sujet : {route['title']}.\n"
            "Utilise une ligne `table` dans `show_board`, PAS une ligne `scientific` :\n"
            "un échiquier de croisement, un tableau de variations, de signes ou\n"
            "d'avancement se lisent en lignes et en colonnes. Aucun moteur\n"
            "graphique ne les rend mieux, et tous les rendent faux."
        )

    obligation = (
        "L'élève demande explicitement un schéma : tu DOIS produire maintenant une ligne "
        "`scientific` dans `show_board`."
        if route["explicit"]
        else
        "Produis ce visuel lorsqu'il sert l'objectif de la réponse ; ne l'ajoute pas comme décoration."
    )
    lines = [
        "[SCHÉMA À GÉNÉRER — AUCUN SVG VALIDÉ ASSEZ PRÉCIS]",
        obligation,
        f"Moteur imposé : `{route['engine']}`. Titre cible : {route['title']}.",
    ]
    if route.get("must_show"):
        lines.append("Éléments scientifiques obligatoires : " + "; ".join(route["must_show"]) + ".")
        # Les fiches de génétique demandent l'échiquier PARMI les éléments à
        # montrer, et imposent par ailleurs un moteur graphique. Sans cette
        # réserve, le tuteur reçoit deux ordres contraires : le PROTOCOLE
        # GÉNÉTIQUE exige `type=table` pour l'échiquier, la fiche le fait
        # dessiner. Un échiquier dessiné à main levée perd l'alignement des
        # gamètes, qui est tout ce qu'un échiquier sert à montrer.
        if any("chiquier" in str(item).lower() for item in route["must_show"]):
            lines.append(
                "RÉSERVE : l'échiquier lui-même reste une ligne `table` (cf. PROTOCOLE "
                "GÉNÉTIQUE) — le moteur graphique ne sert qu'au reste (chromosomes, "
                "position des allèles, gamètes)."
            )
    if route.get("avoid"):
        lines.append("Erreurs scientifiques interdites : " + "; ".join(route["avoid"]) + ".")
    lines.extend([
        "Contrôle avant émission : titre court, légendes françaises, flèches non ambiguës, "
        "symboles et unités BAC exacts, aucun texte superposé.",
        "N'émets jamais de JavaScript, HTML, URL, callback ou SVG brut. Le payload doit rester déclaratif.",
    ])
    return "\n".join(lines)
