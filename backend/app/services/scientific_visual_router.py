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

# Les verbes du mouvement se conjuguent : l'élève écrit « la bille REBONDIT »,
# « le solide GLISSE », pas l'infinitif du mot-clé. Une terminaison libre
# rattrape ces formes ; sans elle, `\brebond\b` manquait « rebondit » et la
# scène partait en dessin figé — or un rebond dessiné ne rebondit pas.
_DYNAMIC = re.compile(
    r"(?<!\w)(?:simulation|simule\w*|anime\w*|animation|mouvement|tombe\w*|chute"
    r"|oscill\w*|collision|choc|percussion|rebond\w*|roule\w*|glisse\w*"
    r"|trajectoire)(?!\w)",
    re.IGNORECASE,
)

#: Le second verrou de la simulation : un mot de MÉCANIQUE. « Anime la
#: photosynthèse » ne part pas vers Matter.js, qui ne connaît que des corps,
#: des chocs et de la pesanteur. Les mobiles du BAC y figurent nommément —
#: une bille, un chariot, un palet — sans quoi « deux billes qui se
#: percutent » retombait sur le dessin à main levée, immobile.
_MECANIQUE = re.compile(
    r"(?<!\w)(?:chute|collision|choc|percussion|pendule|ressort|projectile"
    r"|plan incline|mecanique|bille|chariot|palet|mobile|rebond\w*"
    r"|glisse\w*)(?!\w)",
    re.IGNORECASE,
)

# La seule scène Three.js validée aujourd'hui est la mitochondrie. Il faut à
# la fois la notion ET un besoin de profondeur/caméra : « schéma de la
# mitochondrie » garde le SVG BAC, tandis que « tourne/zoome la mitochondrie
# en 3D » ouvre le modèle manipulable.
_MITOCHONDRIE_3D = re.compile(
    r"(?=.*(?<!\w)mitochondri\w*(?!\w))"
    r"(?=.*(?<!\w)(?:3d|trois dimensions|profondeur|rotation|tourn\w*|zoom\w*|camera|manipul\w*|simulation)(?!\w))",
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


#: « Fais-moi voir ça BOUGER ». Ce n'est pas une nuance de style : une image
#: fixe ne répond pas à la question, et le tuteur qui en envoie une promet
#: alors un mouvement qu'il n'a pas le droit de produire. L'élève redemande,
#: le tuteur repromet — la boucle observée en séance du 23 août, où « dir lya
#: chi simulation de contraction » a rendu quatre fois le même paragraphe et
#: la même photo de sarcomère.
#:
#: La darija compte autant que le français : c'est la langue dans laquelle la
#: demande a été faite.
#: « mouvement » tout court en est ABSENT, et c'est délibéré : c'est un nom
#: de la physique, pas une demande. Le mouvement circulaire uniforme, le
#: mouvement rectiligne, la quantité de mouvement se DESSINENT — un rayon, un
#: vecteur vitesse, un vecteur accélération. Seul « EN mouvement » demande à
#: voir bouger. Même prudence pour « dynamique », qui nomme un chapitre.
_MOUVEMENT = re.compile(
    r"(?<!\w)(?:simulation|simule\w*|animation|anime\w*|bouge\w*"
    r"|tourn\w*|zoom\w*|en mouvement)(?!\w)"
    # L'arabizi que la reconnaissance vocale produit telle quelle :
    # « kaytharrek », « t7arrak », « ytharek » — « ça bouge ».
    r"|(?<!\w)(?:ka)?[yi]?t[h7]arr?[ae]k\w*(?!\w)"
    r"|(?:محاكاة|كيتحرك|يتحرك|تتحرك|تحريك|كيبان كيتحرك)",
    re.IGNORECASE,
)


def demande_du_mouvement(texte: str) -> bool:
    """L'élève demande-t-il de voir la chose EN MOUVEMENT ?"""
    if not texte:
        return False
    # Le repli sans accents sert le français ; l'arabe est cherché tel quel,
    # `_fold` ne gardant que les lettres latines et grecques.
    return bool(_MOUVEMENT.search(_fold(texte)) or _MOUVEMENT.search(texte))


#: Un échiquier de croisement, un tableau de variations ou un tableau
#: d'avancement ne sont pas des dessins : les faire dessiner produit une
#: figure fausse là où deux colonnes disent tout, et cela contredit le
#: PROTOCOLE GÉNÉTIQUE qui exige déjà `type=table`. Le motif est nommé parce
#: que le routeur le consulte AVANT tout rapprochement (cf.
#: `route_scientific_visual`), et pas seulement au moment de choisir un
#: moteur de dessin.
_TABLEAU = _mots(
    "echiquier", "damier", "tableau de variation", "tableau de signe",
    "tableau d avancement", "tableau descriptif", "table de verite",
)

# L'ordre décide : le premier motif qui répond emporte le moteur. Les cas les
# moins ambigus passent donc en tête.
_ENGINE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("table", _TABLEAU),
    (
        "jsxgraph",
        _mots("courbe", "fonction", "repere", "coordonnee", "vecteur", "force",
              "optique", "rayon", "lentille", "miroir", "foyer", "focale",
              "refraction", "reflexion", "diffraction", "incidence", "image",
              "tangente", "asymptote", "trajectoire", "orbite", "cercle",
              "geometrie", "complexe", "onde periodique", "graphique",
              "bilan des force", "champ", "pendule simple",
              # Un diagramme de prédominance ou de distribution EST un axe
              # gradué en pH, avec des domaines bornés par le pKa. Dessiné à
              # main levée, il perd la seule chose qu'il montre : où se situe
              # la frontière.
              "predominance", "distribution"),
    ),
    (
        "cytoscape",
        # « arbre » tout court est retiré : il attirait l'arbre GÉNÉALOGIQUE,
        # qui se dessine en carrés et ronds rangés par génération et non en
        # réseau. Les arbres qui SONT des graphes restent nommés en entier.
        _mots("chaine", "cycle", "voie", "etape", "processus", "reseau", "bilan",
              "cause", "consequence", "algorithme", "transformation",
              "metabolisme", "reaction en cascade", "arbre phylogenetique",
              "phylogenie", "arbre de decision",
              # Une régulation se lit comme une boucle : capteur → centre →
              # effecteur, et la flèche de retour qui referme le circuit.
              # C'est un graphe orienté, pas une coupe anatomique.
              "regulation", "retroaction", "retrocontrole", "homeostasie",
              "boucle de regulation"),
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
    if _MITOCHONDRIE_3D.search(folded):
        return "three"
    if _DYNAMIC.search(folded) and _MECANIQUE.search(folded):
        return "matter"
    for engine, pattern in _ENGINE_PATTERNS:
        if pattern.search(folded):
            return engine
    return "roughsvg"


def _noms_des_modeles_3d() -> str:
    """Les identifiants 3D réellement audités, nommés dans le prompt.

    La phrase disait « la mitochondrie », et `model` « vaut toujours
    `mitochondrion` ». C'était vrai tant qu'il n'y avait qu'un modèle ; le
    jour où un second est ajouté au registre, cette prose l'interdit au tuteur
    sans que rien ne signale la contradiction.
    """
    from app.services.scientific_visual_skill import MODELES_3D

    return ", ".join(f"`{model_id}`" for model_id in MODELES_3D)


def _fiche_reclame_un_tableau(blueprint: dict[str, Any]) -> bool:
    """La fiche demande-t-elle elle-même un tableau parmi ses obligations ?

    C'est ce qui distingue une fiche qui SAIT placer le tableau dans une
    figure plus large — le monohybridisme, qui l'exige avec les chromosomes
    et les gamètes — d'une fiche qui se trouve simplement là.
    """
    return any(
        _TABLEAU.search(_fold(str(element)))
        for element in blueprint.get("must_show", [])
    )


def route_scientific_visual(context: str, demande: str | None = None) -> dict[str, Any]:
    """Décide entre schéma validé, blueprint BAC et génération générale.

    `context` est tout ce qui décrit la séance — titre, chapitre, objectif et
    les derniers messages de l'élève. `demande`, quand elle est fournie, est
    la SEULE phrase que l'élève vient d'écrire. Les deux ne servent pas à la
    même chose : rapprocher un schéma gagne à voir large, mais décider qu'on
    veut un tableau et non un dessin doit se lire dans la demande elle-même —
    un objectif de leçon qui dit « dresser le tableau d'avancement » ne doit
    pas transformer en tableau toutes les figures de la séance.
    """
    schema_id, schema_score = match_schema(context)
    blueprint, blueprint_score = match_visual_blueprint(context)

    # ── Ce qui n'est pas un dessin ne le devient pas par ressemblance ──
    #
    # La route `table` existait déjà, mais elle vivait dans la BRANCHE de
    # génération : elle n'était atteinte que lorsque rien d'autre ne
    # répondait. Or « dessine le tableau d'avancement de la réaction »
    # contient « réaction », mot-clé de `chem_cinetique`, et repartait donc
    # avec le schéma du CHAPITRE cinétique — une figure juste, mais qui ne
    # répond pas : l'élève voulait le tableau d'avancement de SA réaction, à
    # lui, avec ses quantités de matière. Même chose pour « tableau de
    # variations », que « variation » envoyait vers `math_derivation`.
    #
    # La réserve : une fiche qui RÉCLAME elle-même ce tableau garde la main.
    # Celle du monohybridisme liste « échiquier » parmi ses éléments
    # obligatoires, mais demande AUSSI les chromosomes et les gamètes autour,
    # et elle porte déjà la consigne qui laisse l'échiquier lui-même en
    # `type=table` : la court-circuiter perdrait tout le reste de la figure.
    # Une fiche qui n'en parle pas, elle, n'a rien à dire sur la question —
    # « suivi temporel » ne sait rien d'un tableau d'avancement.
    ou_lire = context if demande is None else demande
    if _TABLEAU.search(_fold(ou_lire)) and not (
        blueprint and blueprint_score >= 3 and _fiche_reclame_un_tableau(blueprint)
    ):
        return {
            "source": "generated",
            "title": "Tableau demandé par l'élève",
            "engine": "table",
            "must_show": [],
            "avoid": [],
            "score": 0,
            "explicit": visual_request_is_explicit(context),
        }

    # ── Une image fixe ne répond pas à « fais-la bouger » ──
    #
    # Le registre SVG passait avant tout. « dir lya chi simulation de
    # contraction » contient « contraction », mot-clé de `svt_muscle_sarcomere` :
    # le tuteur recevait l'ordre « affiche ce schéma, NE LE REDESSINE PAS » et
    # renvoyait une photo de sarcomère. L'élève redemandait, le tuteur
    # repromettait une simulation qu'il n'avait pas le droit de produire —
    # quatre fois le même paragraphe, séance du 23 août 2026.
    #
    # Le schéma validé ne disparaît pas : il devient l'ACCOMPAGNEMENT, pas la
    # réponse. Ce qui bouge reste à trouver, et le prompt dit où le chercher.
    if demande_du_mouvement(ou_lire):
        return {
            "source": "mouvement",
            "schema_id": schema_id if schema_id and schema_score >= 3 else None,
            "title": schema_title(schema_id) if schema_id else "Phénomène en mouvement",
            "engine": recommend_generated_engine(f"{context} {ou_lire}"),
            "must_show": list(blueprint.get("must_show", [])) if blueprint and blueprint_score >= 3 else [],
            "avoid": list(blueprint.get("avoid", [])) if blueprint and blueprint_score >= 3 else [],
            "score": schema_score,
            "explicit": True,
        }

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


def build_visual_route_prompt(context: str, demande: str | None = None) -> str:
    """Instruction compacte injectée avant le prompt général du tuteur."""
    route = route_scientific_visual(context, demande)

    if route["source"] == "mouvement":
        lignes = [
            "[L'ÉLÈVE DEMANDE À VOIR LE PHÉNOMÈNE BOUGER]",
            f"Sujet : {route['title']}.",
            "Une image fixe NE RÉPOND PAS à cette demande. Tu as cinq moyens, "
            "dans cet ordre :",
            "1. `OUVRIR_SIMULATION` si le cours en possède une sur cette notion — "
            "c'est toujours le meilleur choix, elle est faite pour être manipulée.",
            "2. Une ligne `scientific` avec le moteur `preset` si la notion figure "
            "dans le catalogue contrôlable du chapitre. Le preset réutilise "
            "JSXGraph/Cytoscape et accepte `start`, `pause`, `next`, "
            "`set_variant` et `highlight`.",
            "3. Une ligne `scientific` avec le moteur `three` quand la demande "
            "exige rotation, zoom ou profondeur, et que la notion figure parmi "
            f"les modèles 3D audités ({_noms_des_modeles_3d()}). Ils sont "
            "versionnés : reprends l'identifiant tel quel, n'en invente aucun.",
            "4. Une ligne `scientific` avec le moteur `matter` pour une mécanique "
            "2D. Elle exige `measures` (une grandeur lue en direct) ou "
            "`parameters` (un réglage) — sans quoi c'est une animation, pas une "
            "simulation, et un dessin aurait suffi.",
            "5. Si le phénomène ne relève d'aucun des quatre — un repliement sans "
            "preset, par exemple — montre "
            "l'état AVANT et l'état APRÈS côte à côte dans une figure "
            f"`{route['engine']}`, et nomme ce qui a changé entre les deux.",
            "",
            "INTERDIT ABSOLU : annoncer un mouvement, une simulation ou une "
            "animation sans qu'il en parte réellement une dans CETTE réponse. "
            "Une phrase comme « غادي ندير ليك محاكاة » ou « je vais te montrer "
            "l'animation » est une PROMESSE. Si tu ne peux pas la tenir, ne la "
            "fais pas : explique avec ce que tu as, et dis à l'élève ce que tu "
            "lui montres exactement.",
        ]
        if route.get("schema_id"):
            lignes.insert(2, (
                f"Un schéma validé existe — `{route['schema_id']}` — mais il est FIXE : "
                "il accompagne ton explication, il ne remplace pas ce que l'élève "
                "demande."
            ))
        if route.get("must_show"):
            lignes.append("Éléments scientifiques obligatoires : " + "; ".join(route["must_show"]) + ".")
        if route.get("avoid"):
            lignes.append("Erreurs scientifiques interdites : " + "; ".join(route["avoid"]) + ".")
        return "\n".join(lignes)

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

    # Le visuel PART, qu'on l'ait demandé ou non.
    #
    # La règle était « produis-le lorsqu'il sert l'objectif ; ne l'ajoute pas
    # comme décoration ». Prudente, et vraie sur le papier — sauf qu'un modèle
    # à qui on laisse le choix de ne rien dessiner ne dessine pas. La
    # bibliothèque déjà tracée a la même consigne depuis qu'elle est câblée :
    # l'élève ignore ce qui existe, il ne le réclamera jamais, et attendre sa
    # demande revient à ne rien montrer. Une figure GÉNÉRÉE ne se comporte pas
    # autrement.
    #
    # « Explicite » ne décide donc plus s'il faut une figure, mais avec quelle
    # fermeté : une demande formulée ne se négocie pas, une réponse ordinaire
    # se dessine quand même.
    obligation = (
        "L'élève demande explicitement un schéma : tu DOIS produire maintenant une ligne "
        "`scientific` dans `show_board`."
        if route["explicit"]
        else
        "Il n'a rien demandé — c'est le cas NORMAL, et ce n'est pas une raison de "
        "répondre sans figure. Produis cette ligne `scientific` DANS CETTE RÉPONSE : "
        "l'élève ne sait pas ce que tu peux dessiner, il ne le réclamera jamais."
    )
    lines = [
        "[SCHÉMA À GÉNÉRER — AUCUN SVG VALIDÉ ASSEZ PRÉCIS]",
        obligation,
        f"Moteur imposé : `{route['engine']}`. Titre cible : {route['title']}.",
        "Deux réserves, et deux seulement : le tour où tu POSES une question et "
        "attends la réponse reste SANS figure — la dessiner reviendrait à montrer "
        "ce que tu demandes de trouver ; et si la figure que tu viens d'envoyer "
        "est encore à l'écran, commente-la au lieu de la refaire.",
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
