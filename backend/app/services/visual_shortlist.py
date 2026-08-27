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
    schema_entry,
    schema_title,
)
from app.services.scientific_presets import SCIENTIFIC_PRESETS
from app.services.scientific_visual_skill import MODELES_3D
from app.services.scientific_visual_router import demande_du_mouvement, demande_une_courbe


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


#: Ce qui se trace dans un REPÈRE, et pas à la craie. Le verbe est le même —
#: « trace », « dessine » — mais la demande ne l'est pas : un croquis au crayon
#: est une planche pré-dessinée du programme, il ne peut pas placer les points
#: de la fonction que l'élève vient d'écrire. « Trace la courbe de f » appelle
#: JSXGraph, pas la boîte à craies.
_A_TRACER = re.compile(
    r"(?<!\w)(?:courbe|graphe|graphique|repere)(?!\w)|f\s*\(\s*x\s*\)",
    re.IGNORECASE,
)


def demande_un_croquis(texte: str) -> bool:
    """L'élève demande-t-il un DESSIN au tableau, et non une planche ?"""
    if not texte:
        return False
    plie = plier(texte)
    if _A_TRACER.search(plie):
        return False
    return bool(_CROQUIS.search(plie) or _CROQUIS.search(texte))


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


def _classer(
    catalogue: dict[str, dict[str, Any]],
    contexte: str,
    limite: int,
    seuil: int = 2,
) -> list[tuple[str, int]]:
    contexte_plie = plier(contexte)
    if not contexte_plie.strip():
        return []
    trouves = [
        (identifiant, _score(definition.get("keywords", ()), contexte_plie))
        for identifiant, definition in catalogue.items()
    ]
    trouves = [(identifiant, score) for identifiant, score in trouves if score >= seuil]
    trouves.sort(key=lambda item: item[1], reverse=True)
    return trouves[:limite]


def apparier_presets(contexte: str, limite: int = 2, seuil: int = 2) -> list[tuple[str, int]]:
    """Les scènes animées du catalogue qui couvrent cette notion.

    Le seuil de 2 est le même que celui du registre SVG : un mot-clé
    distinctif seul suffit (« chimiosmose », « myogramme »), un mot de
    chapitre seul ne suffit pas.

    Il descend à 1 quand l'élève demande à voir la chose BOUGER, et c'est le
    seul cas. Le seuil protège d'une animation hors sujet ; mais face à
    « montre-moi l'onde qui bouge », l'alternative n'est pas le silence : c'est
    un dessin FIXE, qui ne répond pas à la question posée. Une scène du bon
    chapitre, même rapprochée sur le seul mot « onde », vaut mieux qu'une image
    immobile envoyée à quelqu'un qui demande du mouvement.
    """
    return _classer(SCIENTIFIC_PRESETS, contexte, limite, seuil)


def apparier_modeles_3d(contexte: str, limite: int = 1) -> list[tuple[str, int]]:
    """Les modèles 3D audités qui couvrent cette notion."""
    return _classer(MODELES_3D, contexte, limite)


def _porte_la_notion(schema_id: str, contexte_plie: str) -> bool:
    """La figure PARLE-t-elle du mot par lequel elle a été touchée ?

    Un mot-clé générique — « énergie », « cycle », « structure » — vaut un
    point parce qu'il traverse le programme. Il ne devient une raison
    d'afficher CETTE figure que lorsqu'il la nomme : il est alors dans son
    titre ou son identifiant, et pas seulement dans sa liste de mots-clés.
    """
    entree = schema_entry(schema_id)
    if not entree:
        return False
    # Les identifiants s'écrivent avec des tirets bas, que `\w` avale : sans
    # cette césure, « onde » ne se trouverait pas dans `phys_ondes_mecaniques`.
    # Seul le tiret bas est coupé : effacer toute la ponctuation perdrait les
    # notions qui en contiennent une, à commencer par « 0/0 ».
    identite = plier(f"{entree['id']} {entree['title']}").replace("_", " ")
    return any(
        mot_cle_present(mot, contexte_plie) and mot_cle_present(mot, identite)
        for mot in entree.get("keywords", ())
        if isinstance(mot, str) and mot.strip()
    )


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
    contexte_plie = plier(contexte)

    def _meilleur(garder_les_croquis: bool) -> tuple[str, int] | None:
        """Le mieux rapproché, et à défaut le moins mal — mais pas n'importe quoi.

        Le seuil de 2 dit « ce rapprochement est sûr ». Il vaut pour DÉCIDER —
        c'est le rôle du routeur. Ici on ne décide rien : on dresse la liste de
        ce qui existe sur la notion. Un mot de chapitre seul (« onde »,
        « cellule ») n'y suffit pas tant qu'une figure mieux rapprochée est
        disponible ; mais quand il n'y en a aucune, taire la planche du
        chapitre revient à laisser le tuteur improviser un dessin alors que
        celui du programme était là.

        Le repêchage exige alors que le mot en question soit CE DONT LA FIGURE
        PARLE — présent dans son titre ou son identifiant. « onde » repêche les
        ondes mécaniques ; « énergie », qui traverse la moitié du programme,
        ne repêche pas les oscillations RLC pour une question de chimie sur
        l'énergie d'activation.
        """
        touches = [
            (sid, score) for sid, score in classement
            if est_croquis(sid) is garder_les_croquis
        ]
        srs = [item for item in touches if item[1] >= 2]
        repeches = [item for item in touches if _porte_la_notion(item[0], contexte_plie)]
        return (srs or repeches or [None])[0]

    veut_mouvement = demande_du_mouvement(demande)
    return {
        "reference": _meilleur(False),
        "croquis": _meilleur(True),
        "presets": apparier_presets(contexte, seuil=1 if veut_mouvement else 2),
        "modeles_3d": apparier_modeles_3d(contexte),
        "simulations": apparier_simulations(contexte, simulations),
        "veut_croquis": demande_un_croquis(demande),
        "veut_mouvement": veut_mouvement,
        "veut_profondeur": demande_de_la_profondeur(demande),
        "veut_courbe": demande_une_courbe(demande),
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
    deja_affiches: Sequence[str] | None = None,
) -> str:
    """L'instruction compacte à injecter avant le prompt du tuteur.

    Rend une chaîne vide quand rien n'est prêt : dire « aucune ressource ne
    couvre cette notion » à chaque tour occuperait le contexte pour ne rien
    apprendre au modèle, qui sait déjà générer une figure quand il n'a rien.

    `deja_affiches` est ce que l'élève a DÉJÀ sous les yeux. Il ne retire rien
    de la liste — une figure revue est parfois exactement ce qu'il faut — mais
    il empêche la seule chose qu'un affichage automatique produit tout seul :
    renvoyer la même image à chaque phrase, ce qui efface le tableau et le
    redessine à l'identique au milieu d'une explication.
    """
    carte = carte_des_visuels(contexte, demande, simulations)
    vus = {identifiant for identifiant in (deja_affiches or []) if identifiant}

    def _marque(identifiant: str) -> str:
        return "  ← DÉJÀ À L'ÉCRAN" if identifiant in vus else ""

    inventaire: list[str] = []
    if carte["reference"]:
        schema_id = carte["reference"][0]
        inventaire.append(
            f"  • SCHÉMA DE RÉFÉRENCE : {schema_id} — {schema_title(schema_id)}"
            f"{_marque(schema_id)}"
        )
    if carte["croquis"]:
        schema_id = carte["croquis"][0]
        inventaire.append(
            f"  • CROQUIS AU CRAYON  : {schema_id} — {schema_title(schema_id)}"
            f"{_marque(schema_id)}"
        )
    for preset_id, _ in carte["presets"]:
        inventaire.append(
            f"  • SCÈNE ANIMÉE       : {_ligne_preset(preset_id)}{_marque(preset_id)}"
        )
    for model_id, _ in carte["modeles_3d"]:
        inventaire.append(
            f"  • MODÈLE 3D          : {_ligne_modele_3d(model_id)}{_marque(model_id)}"
        )
    for ressource in carte["simulations"]:
        titre = str(ressource.get("title") or "").strip() or "simulation du cours"
        inventaire.append(f"  • SIMULATION DU COURS: « {titre} » — ouvre-la avec OUVRIR_SIMULATION")

    if not inventaire:
        return ""

    lignes = [
        "[LA BIBLIOTHÈQUE COUVRE CETTE NOTION — AFFICHE-EN UNE MAINTENANT]",
        "Ces ressources sont déjà tracées, légendées et conformes au BAC. Les",
        "afficher rend mieux et coûte moins cher qu'une figure improvisée.",
        "",
        *inventaire,
        "",
        "TU N'ATTENDS PAS QU'ON TE LE DEMANDE. L'élève ne sait pas que ces",
        "figures existent : c'est à toi de les sortir, comme un professeur qui",
        "va au tableau sans qu'on l'en prie. Par défaut, l'une d'elles part",
        "DANS CETTE RÉPONSE.",
        "",
        "LAQUELLE : une demande EXPLICITE (« dessine », « en 3D », « trace la",
        "courbe ») est toujours servie telle quelle. Sans demande explicite,",
        "l'ordre est celui de ce que l'élève peut FAIRE avec :",
        "  1. la SCÈNE ANIMÉE ou la SIMULATION DU COURS — il la manipule ;",
        "  2. à défaut, le CROQUIS AU CRAYON ou le SCHÉMA de la bibliothèque ;",
        "  3. à défaut de tout, la figure que tu génères toi-même.",
        "Ne descends d'un cran que si le cran du dessus est vide.",
    ]

    # L'ordre des règles suit celui des intentions détectées : la première qui
    # s'applique est celle que l'élève a formulée, pas celle qui reste.
    if carte["veut_courbe"]:
        # Elle passe AVANT tout le reste : l'élève a écrit sa fonction, et
        # aucune des ressources ci-dessus ne la contient. Les lui envoyer
        # reviendrait à répondre à une autre question que la sienne.
        lignes.append(
            "→ Il a ÉCRIT une fonction à tracer : AUCUNE des ressources "
            "ci-dessus ne contient SA courbe. Trace-la toi-même — ligne "
            "`scientific`, moteur `jsxgraph`, un élément `function` avec son "
            "expression. Les ressources listées ne servent alors qu'à la "
            "MÉTHODE, et seulement si tu y viens ensuite."
        )
    elif carte["veut_profondeur"] and carte["modeles_3d"]:
        lignes.append(
            "→ Il demande à TOURNER AUTOUR / à voir en 3D : envoie le MODÈLE 3D "
            "(ligne `scientific`, moteur `three`)."
        )
    elif carte["veut_croquis"] and carte["croquis"]:
        lignes.append(
            "→ Il demande un DESSIN (« dessine », « croquis », « au tableau », "
            "« رسم ليا ») : envoie le CROQUIS AU CRAYON dans un pas `figure` de "
            "`show_live`, pas la planche de référence."
        )
    elif carte["presets"] or carte["simulations"]:
        # LE CAS NORMAL, et le plus important.
        #
        # C'était la planche de référence qui partait par défaut, et la scène
        # animée n'apparaissait que si l'élève avait prononcé « fais bouger ».
        # Un élève ne demande pas ce qu'il ignore : il n'a jamais su qu'une
        # scène existait, et l'a donc rarement vue. Or c'est la SEULE surface
        # qu'il peut manipuler — il change un paramètre, il regarde ce que ça
        # fait, et il comprend avant qu'on lui explique.
        #
        # Une image fixe et une ligne au tableau viennent APRÈS, pour fixer ce
        # qu'il vient de voir bouger. Jamais avant.
        lignes.append(
            "→ UNE SCÈNE QUI BOUGE COUVRE CETTE NOTION : c'est par ELLE que ton "
            "explication COMMENCE — scène animée (ligne `scientific`, moteur "
            "`preset`) ou SIMULATION DU COURS (`OUVRIR_SIMULATION`). N'attends "
            "pas qu'il demande à voir bouger : il ne sait pas que c'est "
            "possible. Une planche fixe et une ligne au tableau viennent "
            "APRÈS, pour fixer ce qu'il aura vu."
        )
    elif carte["reference"]:
        lignes.append(
            "→ AUCUNE SCÈNE MANIPULABLE sur cette notion : on descend d'un cran. "
            "Affiche le SCHÉMA DE RÉFÉRENCE avec `show_schema` pendant que tu "
            "expliques, et commente-le au lieu de le décrire."
        )
    elif carte["croquis"]:
        lignes.append(
            "→ Ni scène, ni planche de référence sur cette notion : trace le "
            "CROQUIS AU CRAYON dans un pas `figure` de `show_live`."
        )
    elif carte["modeles_3d"]:
        lignes.append(
            "→ Rien de plat sur cette notion, mais un MODÈLE 3D la couvre : "
            "envoie-le (ligne `scientific`, moteur `three`). L'élève le tourne "
            "lui-même, ce qu'un dessin ne fera jamais."
        )

    if vus:
        # Le seul défaut que l'affichage automatique produit tout seul. Il
        # n'était pas visible tant que le tuteur attendait qu'on lui demande.
        deja = ", ".join(sorted(vus))
        lignes.append(
            f"→ DÉJÀ À L'ÉCRAN : {deja}. Ne les RENVOIE pas — l'élève les a sous "
            "les yeux, et les rouvrir efface le tableau pour le redessiner à "
            "l'identique. Continue dessus (commente, zoome, change de variante "
            "avec `control`), ou passe à une AUTRE ressource de la liste quand "
            "ton explication avance."
        )

    if carte["presets"] or carte["simulations"]:
        # Montrer la scène ne suffit pas : elle était affichée puis recouverte
        # par le tableau dans la même réponse, avant que l'élève ait eu le
        # temps de toucher un curseur. Une simulation qu'on n'a pas manipulée
        # n'apprend rien de plus qu'une image.
        lignes.extend([
            "",
            "L'ORDRE D'UNE EXPLICATION QUI COMMENCE PAR UNE SCÈNE — quatre temps,",
            "et un seul par réponse :",
            "  1. TU LA LANCES, et ton explication se tient À CÔTÉ : deux ou trois",
            "     phrases dans le chat qui disent QUOI REGARDER (« observe ce qui",
            "     arrive quand la fréquence monte »). Rien ne s'écrit au tableau",
            "     dans cette réponse : la scène occupe l'écran, et ce que tu",
            "     écrirais recouvrirait ce que tu demandes de regarder.",
            "  2. TU LUI LAISSES LA MAIN. Termine par une consigne de",
            "     MANIPULATION — quel curseur bouger, quoi comparer — puis",
            "     ARRÊTE-TOI. Tu ne continues pas dans la même réponse : c'est",
            "     son tour, et c'est le seul moment où il apprend par lui-même.",
            "  3. QUAND IL REVIENT, tu poses LA QUESTION DE COMPRÉHENSION sur ce",
            "     qu'il vient de voir — une seule, courte, sur le lien de cause à",
            "     effet qu'il a manipulé. Tu n'écris toujours rien.",
            "  4. SEULEMENT APRÈS SA RÉPONSE tu passes au TABLEAU : `show_live`",
            "     écrit la définition, la formule, la conclusion — ce qu'il",
            "     recopie dans son cahier. Le tableau CONCLUT ce qu'il a vu ; il",
            "     ne le précède jamais.",
            "→ Ne saute aucun de ces quatre temps, et n'en mets pas deux dans la",
            "  même réponse. Une scène lancée et aussitôt recouverte de texte est",
            "  une scène que l'élève n'a pas manipulée : elle ne lui a rien appris",
            "  de plus qu'une image fixe.",
            "",
        ])
    lignes.append(
        "→ Une seule ressource à la fois : ouvrir la suivante ferme la précédente. "
        "Enchaîne-les dans l'ordre de ton explication plutôt que de tout empiler."
    )
    lignes.append(
        "→ N'INVENTE AUCUN identifiant : ceux ci-dessus existent, les autres non, "
        "et l'élève ne verrait rien."
    )
    lignes.append(
        "→ SEULE EXCEPTION à l'affichage par défaut : le tour où tu POSES une "
        "question et attends la réponse de l'élève. Écrire au tableau y "
        "reviendrait à lui montrer ce que tu lui demandes de trouver. Tu affiches "
        "au tour SUIVANT, quand tu reprends sa réponse."
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
