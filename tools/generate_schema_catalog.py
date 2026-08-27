"""Regenerate the Python view of the SVG schema library.

The schemas themselves live in the browser bundle
(`frontend/src/components/session/schemas/schemas_*.ts`) — that is where they
are drawn and rendered.  The tutor prompt, however, has to name them: the model
can only write `<schema>svt_mitose</schema>` if it knows the id exists.

Until now that list was retyped by hand inside two prompt blocks of
`llm_service.py`.  Every schema added on the front end was invisible to the
model until someone remembered to copy the id over — `svt_adn_structure` was
already missing from one of the two lists.

This script reads the registry and writes `app/services/schema_catalog.py`.
Run it after adding or renaming a schema:

    python tools/generate_schema_catalog.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "frontend" / "src" / "components" / "session" / "schemas"
TARGET = ROOT / "backend" / "app" / "services" / "schema_catalog.py"

SUBJECT_LABELS = {
    "svt": "SVT",
    "physics": "PHYSIQUE",
    "chemistry": "CHIMIE",
    "math": "MATHS",
}
SUBJECT_ORDER = ["svt", "physics", "chemistry", "math"]

# Un schéma déclare toujours ces quatre champs dans cet ordre — mais un
# commentaire peut s'intercaler, et un schéma qui échappe à cette lecture
# disparaît SILENCIEUSEMENT du catalogue : le tuteur cesse de le connaître.
COMMENTAIRE = r"(?:\s*//[^\n]*)*\s*"
ENTRY = re.compile(
    r"id:\s*'(?P<id>[^']+)'," + COMMENTAIRE +
    r"title:\s*'(?P<title>(?:[^'\\]|\\.)*)'," + COMMENTAIRE +
    r"subject:\s*'(?P<subject>[^']+)'," + COMMENTAIRE +
    r"keywords:\s*\[(?P<keywords>[^\]]*)\]",
)
MOT = re.compile(r"'((?:[^'\\]|\\.)*)'")
METADATA_BLOCK = re.compile(
    r"^\s*,\s*metadata:\s*\{(?P<body>.*?)\}\s*,\s*category:",
    re.DOTALL,
)
METADATA_STRING = re.compile(
    r"(?P<name>courseId|chapter|lesson|visualStyle|resourceRole|paletteId|sourceUrl|sourceTeacher|sourceVideoTitle|auditStatus):\s*"
    r"'(?P<value>(?:[^'\\]|\\.)*)'",
)
METADATA_ARRAY = re.compile(
    r"(?P<name>learningObjectives|llmIntents|drawingSteps|sourceTimecodes):\s*"
    r"\[(?P<value>.*?)\]",
    re.DOTALL,
)


def _metadata_after(source: str, offset: int) -> dict:
    """Lit le bloc déclaratif placé juste après les mots-clés d'un schéma.

    Le format est volontairement borné à des chaînes et listes de chaînes :
    ces métadonnées arrivent dans le prompt du tuteur, jamais du JavaScript.
    """
    match = METADATA_BLOCK.match(source[offset:])
    if not match:
        return {}
    body = match.group("body")
    metadata = {
        item.group("name"): item.group("value").replace("\\'", "'")
        for item in METADATA_STRING.finditer(body)
    }
    for item in METADATA_ARRAY.finditer(body):
        metadata[item.group("name")] = [
            value.replace("\\'", "'")
            for value in MOT.findall(item.group("value"))
        ]
    return metadata


def collect() -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(SCHEMAS_DIR.glob("schemas_*.ts")):
        source = path.read_text(encoding="utf-8")
        for match in ENTRY.finditer(source):
            schema_id = match.group("id")
            if schema_id in seen:
                continue
            seen.add(schema_id)
            entry = {
                "id": schema_id,
                "title": match.group("title").replace("\\'", "'"),
                "subject": match.group("subject"),
                # Les mots-clés servent au rapprochement automatique côté
                # serveur. Les recopier à la main dans le handler, c'était la
                # même dérive que pour les identifiants : un schéma ajouté
                # restait introuvable.
                "keywords": [
                    mot.replace("\\'", "'")
                    for mot in MOT.findall(match.group("keywords"))
                ],
            }
            metadata = _metadata_after(source, match.end())
            if metadata:
                entry["metadata"] = metadata
            found.append(entry)
    return found


HELPERS = r'''@lru_cache(maxsize=None)
def _motif(mot: str) -> re.Pattern:
    """Un mot-clé ne compte que s'il est un MOT, pas une suite de lettres.

    Cherché en simple sous-chaîne, `exp` se trouve dans « expansion » et `ln`
    dans une dizaine de mots : un cours sur la dorsale océanique se voyait
    proposer le schéma des fonctions exponentielles. Les bornes règlent le
    problème pour le français comme pour l'arabe, les bornes de mot étant
    unicode.

    Le pluriel reste admis (`s` ou `x` final) : un cours parle des
    « myofibrilles » et des « crêtes », le mot-clé est au singulier, et
    l'exiger à la lettre faisait manquer le bon schéma.
    """
    return re.compile(rf"(?<!\w){re.escape(_sans_accents(mot))}[sx]?(?!\w)", re.UNICODE)


#: Les caracteres que deux claviers ecrivent differemment pour la MEME chose.
#:
#: Un mot-cle recopie depuis un manuel porte l'apostrophe typographique
#: (« energie d’activation ») ; l'eleve, lui, tape celle du clavier
#: (« energie d'activation »). `re.escape` compare des caracteres : les deux
#: ne se rencontraient jamais, et la scene animee de l'energie d'activation
#: restait introuvable pour la question qui la nomme mot pour mot.
_PONCTUATION_EQUIVALENTE = str.maketrans({
    "’": "'", "‘": "'", "ʼ": "'", "`": "'", "´": "'",
    "‑": "-", "–": "-", "—": "-",
})


def _sans_accents(texte: str) -> str:
    """Un eleve tape « accretion » : le mot-cle accentue doit quand meme repondre."""
    plie = unicodedata.normalize("NFKD", (texte or "").lower())
    plie = "".join(c for c in plie if not unicodedata.combining(c))
    return plie.translate(_PONCTUATION_EQUIVALENTE)


#: Les sigles du programme : trop courts pour le seuil de six lettres, et
#: pourtant les mots les plus distinctifs de leur chapitre. « ATP » ne designe
#: rien d'autre que l'ATP. Sans cette liste, « c'est quoi l'ATP ? » ne valait
#: qu'un point : ni le croquis ATP-ADP, ni la scene du cycle ne sortaient, et
#: l'eleve recevait de la prose sur la notion la plus dessinee du chapitre.
_SIGLES = {
    "adn", "arn", "arnm", "arnt", "atp", "adp", "amp", "nad", "nadh", "fad",
    "fadh", "co2", "o2", "h2o", "ph", "pka", "pke", "exao", "rc", "rlc",
    "tvi", "fem", "cog", "svt",
}


_MOTS_GENERIQUES = {
    "reaction", "structure", "cycle", "energie", "bilan", "comparaison", "courbe",
    "fonction", "cellule", "muscle", "mouvement", "mecanique", "onde", "oscillation",
    "force", "tableau", "schema", "equilibre", "complexe", "arithmetique", "division",
    # « variation » est un mot-cle de la DERIVATION, et un mot francais partout
    # ailleurs. Seul, il valait deux points : « la variation de la pression
    # arterielle » — une courbe de SVT — se voyait proposer le schema de
    # derivation. Une vraie lecon de derivation dit « derivee » ou
    # « derivation », et garde donc son schema.
    "variation",
}


def _poids_mot_cle(mot: str) -> int:
    """Une notion distinctive seule doit suffire, un mot de chapitre non.

    « mitose », « électrolyse » ou « sarcomère » désignent sans ambiguïté une
    figure et valent deux points. « structure » ou « énergie » restent à un
    point pour ne jamais imposer un schéma sur une simple coïncidence.
    """
    normalise = _sans_accents(mot.strip())
    if " " in normalise:
        return 3
    if normalise in _SIGLES:
        return 2
    if len(normalise) >= 6 and normalise not in _MOTS_GENERIQUES:
        return 2
    return 1


#: Les terminaisons qui separent deux formes du MEME mot, de la plus longue a
#: la plus courte. Elles ne font pas une analyse morphologique : elles couvrent
#: le seul ecart qu'on observe entre un mot-cle et une question d'eleve — le
#: nom dans le catalogue (« contraction », « glissement », « propagation »), le
#: verbe dans la bouche de l'eleve (« se contracte », « glisse », « se
#: propage »).
_TERMINAISONS = (
    "ations", "ation", "ements", "ement", "ions", "ion", "ees", "ee", "es",
    "er", "ez", "e", "s", "x",
)


def _racine(mot: str) -> str:
    """La racine d'un mot, ou le mot lui-meme quand la couper l'appauvrirait.

    Le plancher de cinq lettres est ce qui empeche la famille de mots de
    devenir un rapprochement au jugé : « onde » se reduirait a « ond », qui
    touche « onduler » et « ondee » ; « force » a « forc », qui touche
    « forcement ». Ces racines-la sont laissees entieres.
    """
    for terminaison in _TERMINAISONS:
        if mot.endswith(terminaison) and len(mot) - len(terminaison) >= 5:
            return mot[: -len(terminaison)]
    return mot


def racines_du_contexte(contexte_plie: str) -> frozenset[str]:
    """Les racines de tous les mots d'un contexte deja plie."""
    return frozenset(_racine(mot) for mot in re.findall(r"[a-z0-9]+", contexte_plie))


def mot_cle_de_la_famille(mot: str, racines: frozenset[str]) -> bool:
    """Ce mot-cle est-il une autre forme d'un mot de la question ?

    Reserve aux mots-cles d'UN SEUL mot. Sur un mot-cle compose, comparer des
    racines sans tenir compte de l'ordre reviendrait a rapprocher « bilan des
    forces » et « bilan energetique » : deux figures sans rapport.
    """
    nu = _sans_accents(mot.strip())
    if not nu or " " in nu:
        return False
    return _racine(nu) in racines


# ── Surface publique du rapprochement ─────────────────────────────
#
# Le catalogue des schémas n'est pas la seule bibliothèque à rapprocher d'une
# phrase d'élève : les scènes animées et les modèles 3D ont eux aussi des
# mots-clés, et il n'y a aucune raison qu'ils soient comparés autrement. Les
# trois fonctions ci-dessous exposent la MÊME mécanique — repli sans accents,
# bornes de mot, pondération — pour que `visual_shortlist` n'en réécrive pas
# une seconde, forcément divergente.


def plier(texte: str) -> str:
    """La forme comparable d'un texte : minuscules, sans accents."""
    return _sans_accents(texte or "")


def mot_cle_present(mot: str, contexte_plie: str) -> bool:
    """Le mot-clé apparaît-il comme MOT dans un contexte déjà plié ?"""
    return bool(_motif(mot).search(contexte_plie))


def poids_mot_cle(mot: str) -> int:
    """Ce que vaut ce mot-clé : 3 s'il est composé, 2 s'il est distinctif, 1 sinon."""
    return _poids_mot_cle(mot)


def _rapprochements(context: str) -> list[tuple[int, int, str]]:
    """Tous les schémas touchés par le contexte, du meilleur au moins bon.

    Le tri est STABLE : à score et précision égaux, l'ordre du catalogue
    tranche, exactement comme le faisait la comparaison stricte d'origine.
    """
    contexte = _sans_accents(context or "")
    if not contexte.strip():
        return []

    racines = racines_du_contexte(contexte)
    trouvailles: list[tuple[int, int, str]] = []
    for entry in SCHEMA_CATALOG:
        trouves = [mot for mot in entry["keywords"] if _motif(mot).search(contexte)]
        # Le mot-clé dit « contraction », l'élève écrit « le muscle se
        # contracte » : c'est le même mot, et le rapprochement le manquait.
        # Une famille de mots vaut UN point, jamais les deux d'une
        # correspondance exacte — elle complète un rapprochement, elle ne le
        # fabrique pas à elle seule quand le mot-clé est générique.
        familles = [
            mot for mot in entry["keywords"]
            if mot not in trouves and mot_cle_de_la_famille(mot, racines)
        ]
        if not trouves and not familles:
            continue
        score = sum(_poids_mot_cle(mot) for mot in trouves) + len(familles)
        # À score égal, le mot-clé le plus long tranche : « fibre musculaire »
        # l'emporte sur « muscle », qui désigne le chapitre et non la figure.
        precision = max(len(mot) for mot in (trouves or familles))
        trouvailles.append((score, precision, entry["id"]))
    trouvailles.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return trouvailles


def match_schema(context: str) -> tuple[str | None, int]:
    """Le schéma de la bibliothèque qui colle le mieux au contexte, et son score.

    Un mot-clé en PLUSIEURS mots pèse double : « fibre musculaire » désigne un
    schéma, « muscle » désigne un chapitre entier. Sans cette pondération, un
    cours sur la fibre musculaire se voyait proposer le sarcomère, les deux
    étant à égalité sur des mots génériques.

    Les appelants décident du seuil : rapprocher n'est pas afficher.
    """
    trouvailles = _rapprochements(context)
    if not trouvailles:
        return None, 0
    score, _, schema_id = trouvailles[0]
    return schema_id, score


def classer_schemas(context: str, limite: int = 8) -> list[tuple[str, int]]:
    """Le classement complet, et pas seulement son vainqueur.

    Un seul identifiant ne suffit plus depuis que la bibliothèque contient DEUX
    versions de la même notion : le schéma de référence, détaillé, et le
    croquis au crayon que le professeur trace au tableau. Choisir entre les
    deux dépend de ce que l'élève demande, pas du score — il faut donc les voir
    tous les deux.
    """
    return [(schema_id, score) for score, _, schema_id in _rapprochements(context)[:limite]]


def schema_entry(schema_id: str) -> dict | None:
    for entry in SCHEMA_CATALOG:
        if entry["id"] == schema_id:
            return entry
    return None


def est_croquis(schema_id: str) -> bool:
    """Ce schéma est-il la version « craie au tableau » de la notion ?"""
    entry = schema_entry(schema_id)
    if not entry:
        return False
    return (entry.get("metadata") or {}).get("resourceRole") == "teacher_sketch"


def schema_title(schema_id: str) -> str:
    entry = schema_entry(schema_id)
    return entry["title"] if entry else ""

'''


def render(entries: list[dict]) -> str:
    by_subject: dict[str, list[dict[str, str]]] = {}
    for entry in entries:
        by_subject.setdefault(entry["subject"], []).append(entry)

    lines: list[str] = []
    for subject in SUBJECT_ORDER + [s for s in by_subject if s not in SUBJECT_ORDER]:
        group = by_subject.get(subject)
        if not group:
            continue
        lines.append(f"  {SUBJECT_LABELS.get(subject, subject.upper())} :")
        for entry in group:
            metadata = entry.get("metadata") or {}
            if metadata.get("resourceRole") == "teacher_sketch":
                intentions = "; ".join((metadata.get("llmIntents") or [])[:2])
                suffix = f" [CROQUIS CRAYON LIVE BOARD — {intentions}]" if intentions else " [CROQUIS CRAYON LIVE BOARD]"
            else:
                suffix = ""
            lines.append(f"    {entry['id']} — {entry['title']}{suffix}")
    catalogue = "\n".join(lines)

    items = "\n".join(
        "    {"
        f"\"id\": {entry['id']!r}, \"title\": {entry['title']!r}, "
        f"\"subject\": {entry['subject']!r}, \"keywords\": {entry['keywords']!r}, "
        f"\"metadata\": {entry.get('metadata', {})!r}"
        "},"
        for entry in entries
    )

    count = len(entries)
    helpers = HELPERS

    return f'''"""Les schémas SVG disponibles, vus depuis le serveur — FICHIER GÉNÉRÉ.

Ne pas éditer à la main : lancer `python tools/generate_schema_catalog.py`
après avoir ajouté un schéma dans
`frontend/src/components/session/schemas/schemas_*.ts`.

Le catalogue sert au prompt : un identifiant absent d'ici n'existe pas pour le
modèle, et un schéma que personne ne nomme ne s'affiche jamais.
"""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

SCHEMA_CATALOG: list[dict] = [
{items}
]

SCHEMA_IDS: frozenset[str] = frozenset(entry["id"] for entry in SCHEMA_CATALOG)


{helpers}
SCHEMA_CATALOG_PROMPT = """[SCHÉMAS SVG DISPONIBLES — {count} identifiants]
Ces schémas sont déjà dessinés, animés et annotés. Les afficher coûte moins
cher et rend mieux qu'un dessin improvisé : si l'un d'eux couvre la notion,
c'est LUI qu'on affiche, dans TOUS les modes (cours, exercice, examen,
question libre).
Les ressources marquées CROQUIS CRAYON LIVE BOARD sont les versions simples
qu'un professeur peut tracer au tableau. Si l'élève dit « dessine »,
« croquis », « schématise » ou « au tableau », préfère la version CROQUIS de
la notion ; pour une consultation détaillée sans demande de dessin, garde le
schéma de référence.
Format : <schema>identifiant</schema> — ou l'action `show_schema`.
N'INVENTE JAMAIS un identifiant : s'il n'est pas dans cette liste, il n'existe
pas, et l'élève ne voit rien.

{catalogue}
"""
'''


def main() -> None:
    entries = collect()
    if not entries:
        raise SystemExit(f"Aucun schéma trouvé dans {SCHEMAS_DIR}")
    TARGET.write_text(render(entries), encoding="utf-8")
    print(f"{len(entries)} schémas -> {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
