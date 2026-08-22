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
            found.append({
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
            })
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


def _sans_accents(texte: str) -> str:
    """Un eleve tape « accretion » : le mot-cle accentue doit quand meme repondre."""
    plie = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in plie if not unicodedata.combining(c))


def match_schema(context: str) -> tuple[str | None, int]:
    """Le schéma de la bibliothèque qui colle le mieux au contexte, et son score.

    Un mot-clé en PLUSIEURS mots pèse double : « fibre musculaire » désigne un
    schéma, « muscle » désigne un chapitre entier. Sans cette pondération, un
    cours sur la fibre musculaire se voyait proposer le sarcomère, les deux
    étant à égalité sur des mots génériques.

    Les appelants décident du seuil : rapprocher n'est pas afficher.
    """
    contexte = _sans_accents(context or "")
    if not contexte.strip():
        return None, 0

    meilleur_id, meilleur_score, meilleur_precision = None, 0, 0
    for entry in SCHEMA_CATALOG:
        trouves = [mot for mot in entry["keywords"] if _motif(mot).search(contexte)]
        if not trouves:
            continue
        score = sum(2 if " " in mot.strip() else 1 for mot in trouves)
        # À score égal, le mot-clé le plus long tranche : « fibre musculaire »
        # l'emporte sur « muscle », qui désigne le chapitre et non la figure.
        precision = max(len(mot) for mot in trouves)
        if (score, precision) > (meilleur_score, meilleur_precision):
            meilleur_id, meilleur_score, meilleur_precision = entry["id"], score, precision
    return (meilleur_id, meilleur_score) if meilleur_score else (None, 0)


def schema_title(schema_id: str) -> str:
    for entry in SCHEMA_CATALOG:
        if entry["id"] == schema_id:
            return entry["title"]
    return ""

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
            lines.append(f"    {entry['id']} — {entry['title']}")
    catalogue = "\n".join(lines)

    items = "\n".join(
        "    {"
        f"\"id\": {entry['id']!r}, \"title\": {entry['title']!r}, "
        f"\"subject\": {entry['subject']!r}, \"keywords\": {entry['keywords']!r}"
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
